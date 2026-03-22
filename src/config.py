import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AWS Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
    
    # DynamoDB Tables
    DYNAMODB_TABLE_CAMPAIGNS = os.getenv("DYNAMODB_TABLE_CAMPAIGNS", "CampaignSessions")
    DYNAMODB_TABLE_AUDIT = os.getenv("DYNAMODB_TABLE_AUDIT", "AuditLogs")
    DYNAMODB_TABLE_MEMORY = os.getenv("DYNAMODB_TABLE_MEMORY", "SentinelAI_CampaignMemory")
    
    # S3
    S3_BUCKET_REPORTS = os.getenv("S3_BUCKET_REPORTS", "sentinel-ai-artifacts")
    
    # Agent Configuration (AWS Bedrock)
    RED_AGENT_ROLE_ARN = os.getenv("RED_AGENT_ROLE_ARN")
    BLUE_AGENT_ROLE_ARN = os.getenv("BLUE_AGENT_ROLE_ARN")
    
    # Bedrock Configuration
    BEDROCK_TEMPERATURE = 0.7
    BEDROCK_MAX_TOKENS = 4096
    BEDROCK_TOP_P = 0.9
    
    # MongoDB Configuration
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "sentinel_ai")
    
    # n8n Configuration
    N8N_URL = os.getenv("N8N_URL", "http://localhost:5678")
    N8N_API_KEY = os.getenv("N8N_API_KEY")
    
    # Local LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama2")
    LLM_URL = os.getenv("LLM_URL", "http://localhost:11434")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")
    ADMIN_JWT_SECRET = os.getenv("ADMIN_JWT_SECRET")

    # ChromaDB (Knowledge Store / Data Flywheel)
    CHROMADB_PATH = os.getenv("CHROMADB_PATH", "./data/chromadb")
    CHROMADB_COLLECTION = os.getenv("CHROMADB_COLLECTION", "security_findings")

    # OpenAI (Optional — Multi-LLM support)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

    # Azure OpenAI (Optional — Multi-LLM support)
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

    # Threat Intelligence
    THREAT_INTEL_CACHE_TTL_HOURS = int(os.getenv("THREAT_INTEL_CACHE_TTL_HOURS", "24"))
    NVD_API_KEY = os.getenv("NVD_API_KEY")  # Optional — higher rate limits

    # Agent Enhancements
    AGENT_MODE = os.getenv("AGENT_MODE", "default")  # 'default' or 'langgraph'
    AGENT_KILL_SWITCH = os.getenv("AGENT_KILL_SWITCH", "false")

# Validate critical secrets
if not Config.JWT_SECRET or not Config.ADMIN_JWT_SECRET:
    raise ValueError("CRITICAL: JWT_SECRET or ADMIN_JWT_SECRET environment variables are missing! "
                     "These must be set in production to prevent token forgery.")

