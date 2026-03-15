from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.agents.red_agent import RedAgent
from src.agents.blue_agent import BlueAgent
import boto3
from datetime import datetime
from src.config import Config
import uuid
import os
from dotenv import load_dotenv

from src.core.orchestrator import AgentOrchestrator
from src.core.database import Database
from src.core.n8n_client import N8NClient
from src.core.llm_client import LLMClient
from src.core.memory import CampaignMemoryManager
from src.core.hooks import SecurityHookProvider, AttackDefenseFeedbackHook
from src.utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger(__name__)

app = FastAPI(
    title="Sentinel AI - Autonomous Purple Teaming Platform",
    description="Multi-agent security orchestration with offensive and defensive AI agents",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LangChain agents (AWS Bedrock)
red_agent = RedAgent()
blue_agent = BlueAgent()

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
campaigns_table = dynamodb.Table(Config.DYNAMODB_TABLE_CAMPAIGNS)

# Global instances for orchestrator subsystem
orchestrator = None
database = None
n8n_client = None
llm_client = None
memory_manager = None
hook_provider = None
feedback_hook = None


# ==================== Models ====================

class CampaignRequest(BaseModel):
    target_url: str
    target_description: str
    iam_role: str = "test-role"
    actor_id: str = "default_user"

class CampaignResponse(BaseModel):
    campaign_id: str
    status: str
    red_agent_result: dict
    blue_agent_result: dict
    timestamp: str


# ==================== Lifecycle ====================

@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup"""
    global orchestrator, database, n8n_client, llm_client
    global memory_manager, hook_provider, feedback_hook
    
    logger.info("🚀 Starting Sentinel AI Platform...")
    
    # Initialize Campaign Memory (DynamoDB — cross-session intelligence)
    try:
        CampaignMemoryManager.ensure_table_exists()
        memory_manager = CampaignMemoryManager()
        feedback_hook = AttackDefenseFeedbackHook(memory_manager=memory_manager)
        logger.info("✅ Campaign memory initialized (DynamoDB)")
    except Exception as e:
        logger.warning(f"⚠️ Campaign memory not available: {e}")
        memory_manager = None
        feedback_hook = None
    
    # Initialize MongoDB database (for orchestrator subsystem)
    try:
        database = Database(
            url=os.getenv("MONGO_URL", "mongodb://localhost:27017"),
            db_name=os.getenv("MONGO_DB", "sentinel_ai")
        )
        await database.connect()
        logger.info("✅ MongoDB database connected")
    except Exception as e:
        logger.warning(f"⚠️ MongoDB not available: {e} — orchestrator features disabled")
        database = None
    
    # Initialize n8n client
    try:
        n8n_client = N8NClient(
            url=os.getenv("N8N_URL", "http://localhost:5678"),
            api_key=os.getenv("N8N_API_KEY")
        )
        logger.info("✅ n8n client initialized")
    except Exception as e:
        logger.warning(f"⚠️ n8n not available: {e}")
        n8n_client = None
    
    # Initialize LLM client
    try:
        llm_client = LLMClient(
            provider=os.getenv("LLM_PROVIDER", "ollama"),
            model=os.getenv("LLM_MODEL", "llama2"),
            url=os.getenv("LLM_URL", "http://localhost:11434")
        )
        logger.info("✅ LLM client initialized")
    except Exception as e:
        logger.warning(f"⚠️ LLM not available: {e}")
        llm_client = None
    
    # Initialize lifecycle hooks (auto-persist, auto-enrich)
    hook_provider = SecurityHookProvider(
        memory_manager=memory_manager,
        n8n_client=n8n_client,
        llm_client=llm_client,
        database=database,
    )
    
    # Initialize orchestrator (requires all subsystems)
    if database and n8n_client and llm_client:
        try:
            orchestrator = AgentOrchestrator(
                database=database,
                n8n_client=n8n_client,
                llm_client=llm_client
            )
            await orchestrator.initialize()
            logger.info("✅ Agent orchestrator initialized with 12 agents")
        except Exception as e:
            logger.warning(f"⚠️ Orchestrator initialization failed: {e}")
            orchestrator = None
    
    # Import and seed database for web platform routes
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB", "sentinel_ai")
        db_client = AsyncIOMotorClient(mongo_url)
        app.state.db = db_client[db_name]
        logger.info("✅ Web platform database connected")
    except Exception as e:
        logger.warning(f"⚠️ Web platform database not available: {e}")
    
    logger.info("🎉 Sentinel AI Platform is ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down Sentinel AI Platform...")
    
    if orchestrator:
        await orchestrator.shutdown()
    
    if database:
        await database.disconnect()
    
    logger.info("👋 Shutdown complete")


# ==================== Root & Health ====================

@app.get("/")
def root():
    return {
        "service": "Sentinel AI",
        "tagline": "Attack to Defend. Autonomously.",
        "version": "2.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if database and database.is_connected else "disconnected",
        "n8n": "connected" if n8n_client else "not initialized",
        "llm": "connected" if llm_client else "not initialized",
        "agents": orchestrator.get_agent_status() if orchestrator else {}
    }


# ==================== Campaign Endpoints (AWS Bedrock) ====================

@app.post("/campaigns/start", response_model=CampaignResponse)
async def start_campaign(request: CampaignRequest):
    """
    Initiate a purple teaming validation campaign.
    
    The attack-defense feedback loop:
    1. Load prior Red/Blue history for this target
    2. Inject Blue's past patches into Red's prompt (probe new vectors)
    3. Red Agent attacks
    4. Inject Red's findings + history into Blue's prompt
    5. Blue Agent defends
    6. Persist both results for next session's feedback loop
    """
    campaign_id = str(uuid.uuid4())
    session_id = campaign_id  # one session per campaign
    actor_id = request.actor_id
    timestamp = datetime.utcnow().isoformat()
    
    try:
        # Initialize campaign in DynamoDB
        campaigns_table.put_item(Item={
            "campaign_id": campaign_id,
            "timestamp": int(datetime.utcnow().timestamp()),
            "status": "ACTIVE",
            "target_url": request.target_url,
            "target_description": request.target_description,
            "actor_id": actor_id
        })
        
        # ── Step 1: Load prior context for Red Agent ──
        red_context = None
        if feedback_hook:
            red_context = await feedback_hook.get_red_context(request.target_url)
        
        # ── Step 2: Execute Red Agent with historical awareness ──
        target_info = {
            "url": request.target_url,
            "description": request.target_description,
            "iam_role": request.iam_role
        }
        red_result = red_agent.execute_campaign(
            target_info,
            memory_context=red_context,
            session_id=session_id,
            actor_id=actor_id
        )
        
        # ── Step 3: Persist Red findings to campaign memory ──
        if memory_manager:
            await memory_manager.store_finding(
                target=request.target_url,
                agent_type="red",
                finding=red_result,
                campaign_id=campaign_id,
                actor_id=actor_id,
                session_id=session_id,
            )
        
        # ── Step 4: Load context for Blue Agent (includes Red's findings) ──
        blue_context = None
        if feedback_hook:
            blue_context = await feedback_hook.get_blue_context(
                request.target_url, red_result=red_result
            )
        
        # ── Step 5: Execute Blue Agent with attack-aware context ──
        threat_info = {
            "attack_type": "Multiple vulnerabilities detected",
            "target": request.target_url,
            "details": str(red_result.get("output", "Attack executed"))
        }
        blue_result = blue_agent.respond_to_threat(
            threat_info,
            memory_context=blue_context,
            session_id=session_id,
            actor_id=actor_id
        )
        
        # ── Step 6: Persist Blue defense to campaign memory ──
        if memory_manager:
            await memory_manager.store_finding(
                target=request.target_url,
                agent_type="blue",
                finding=blue_result,
                campaign_id=campaign_id,
                actor_id=actor_id,
                session_id=session_id,
            )
        
        # ── Finalize campaign ──
        campaigns_table.update_item(
            Key={"campaign_id": campaign_id, "timestamp": int(datetime.utcnow().timestamp())},
            UpdateExpression="SET #status = :status, red_agent_actions = :red, blue_agent_actions = :blue",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": "COMPLETED",
                ":red": str(red_result),
                ":blue": str(blue_result)
            }
        )
        
        return CampaignResponse(
            campaign_id=campaign_id,
            status="COMPLETED",
            red_agent_result=red_result,
            blue_agent_result=blue_result,
            timestamp=timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Campaign failed: {str(e)}")

@app.get("/campaigns/{campaign_id}")
def get_campaign(campaign_id: str):
    """Retrieve campaign details"""
    try:
        response = campaigns_table.get_item(Key={"campaign_id": campaign_id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return response["Item"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Orchestrator Endpoints ====================

@app.post("/agents/execute/{agent_type}")
async def execute_agent(agent_type: str, target: dict):
    """Execute a specific agent from the multi-agent system"""
    if not orchestrator:
        return {"error": "Orchestrator not initialized — check MongoDB, n8n, and LLM connections"}
    
    result = await orchestrator.execute_agent(agent_type, target)
    return result

@app.get("/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    if not orchestrator:
        return {"error": "Orchestrator not initialized"}
    
    return orchestrator.get_agent_status()

@app.get("/results/{result_id}")
async def get_result(result_id: str):
    """Get agent execution result"""
    if not database:
        return {"error": "Database not initialized"}
    
    result = await database.get_result(result_id)
    return result

@app.get("/workflows")
async def list_workflows():
    """List all n8n workflows"""
    if not n8n_client:
        return {"error": "n8n client not initialized"}
    
    workflows = await n8n_client.list_workflows()
    return workflows


# ==================== Web Platform Routes ====================

try:
    from src.routes.admin_auth import router as admin_auth_router
    from src.routes.client_auth import router as client_auth_router
    from src.routes.content import router as content_router
    from src.routes.blog import router as blog_router
    from src.routes.demo_requests import router as demo_router
    from src.routes.clients import router as clients_router
    from src.routes.client_dashboard import router as client_dashboard_router
    from src.routes.uploads import router as uploads_router
    from src.routes.password_reset import router as password_reset_router
    from src.routes.notifications import router as notifications_router
    from src.routes.security import router as security_router
    from src.routes.architecture import router as architecture_router
    from src.routes.seo import router as seo_router

    app.include_router(admin_auth_router, prefix="/api/admin/auth", tags=["Admin Auth"])
    app.include_router(content_router, prefix="/api/admin/content", tags=["Admin Content"])
    app.include_router(content_router, prefix="/api/content", tags=["Public Content"])
    app.include_router(blog_router, prefix="/api/admin/blog", tags=["Admin Blog"])
    app.include_router(blog_router, prefix="/api/blog", tags=["Public Blog"])
    app.include_router(demo_router, prefix="/api/admin/demo-requests", tags=["Admin Demo"])
    app.include_router(demo_router, prefix="/api/demo", tags=["Public Demo"])
    app.include_router(demo_router, prefix="/api/book-demo", tags=["Book Demo"])
    app.include_router(clients_router, prefix="/api/admin/clients", tags=["Admin Clients"])
    app.include_router(client_auth_router, prefix="/api/auth", tags=["Client Auth"])
    app.include_router(client_dashboard_router, prefix="/api/dashboard", tags=["Client Dashboard"])
    app.include_router(uploads_router, prefix="/api/uploads", tags=["File Uploads"])
    app.include_router(password_reset_router, prefix="/api/auth", tags=["Password Reset & Verification"])
    app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"])
    app.include_router(security_router, prefix="/api/security", tags=["Security Scanning"])
    app.include_router(architecture_router, tags=["Architecture Maps"])
    app.include_router(seo_router, prefix="/api/seo", tags=["SEO Management"])
    app.include_router(seo_router, prefix="/api/admin/seo", tags=["Admin SEO Management"])
except ImportError as e:
    logger.warning(f"⚠️ Some web platform routes could not be loaded: {e}")


@app.get("/api/health")
async def api_health_check():
    return {"status": "OK", "service": "Sentinel AI API"}

@app.get("/api/admin/dashboard")
async def admin_dashboard():
    try:
        from src.routes.blog import get_blog_stats
        from src.routes.demo_requests import get_demo_stats
        from src.routes.clients import get_client_stats
        
        blog_stats = await get_blog_stats(app.state.db)
        demo_stats = await get_demo_stats(app.state.db)
        client_stats = await get_client_stats(app.state.db)
        
        return {
            "overview": {
                "blog": blog_stats,
                "demoRequests": demo_stats,
                "clients": client_stats
            }
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
