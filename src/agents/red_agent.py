from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
import boto3
from datetime import datetime
from src.config import Config

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
audit_table = dynamodb.Table(Config.DYNAMODB_TABLE_AUDIT)

# Module-level session context — updated by campaign caller
_session_context = {"session_id": "default", "actor_id": "default_user"}


def set_session_context(session_id: str, actor_id: str):
    """Set the session context for audit logging."""
    _session_context["session_id"] = session_id
    _session_context["actor_id"] = actor_id


@tool
def execute_sql_injection(target_url: str, payload: str) -> dict:
    """Execute SQL injection attack against target URL with safety checks"""
    # Safety check: reject production targets
    if "prod" in target_url.lower() or "production" in target_url.lower():
        return {
            "status": "rejected",
            "reason": "Production target detected - attack blocked",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Log attack attempt
    audit_table.put_item(Item={
        "session_id": _session_context["session_id"],
        "event_timestamp": int(datetime.utcnow().timestamp()),
        "agent_type": "RED",
        "actor_id": _session_context["actor_id"],
        "action": "sql_injection_attempt",
        "target": target_url,
        "payload": payload,
        "outcome": "simulated"
    })
    
    return {
        "status": "executed",
        "attack_type": "SQL Injection",
        "target": target_url,
        "payload": payload,
        "simulated_result": "Vulnerability detected - SQL error returned",
        "timestamp": datetime.utcnow().isoformat()
    }

@tool
def test_xss_vulnerability(target_url: str, payload: str) -> dict:
    """Test XSS vulnerability on target endpoint"""
    audit_table.put_item(Item={
        "session_id": _session_context["session_id"],
        "event_timestamp": int(datetime.utcnow().timestamp()),
        "agent_type": "RED",
        "actor_id": _session_context["actor_id"],
        "action": "xss_test",
        "target": target_url,
        "payload": payload,
        "outcome": "simulated"
    })
    
    return {
        "status": "executed",
        "attack_type": "XSS",
        "target": target_url,
        "payload": payload,
        "simulated_result": "XSS payload reflected in response",
        "timestamp": datetime.utcnow().isoformat()
    }

@tool
def test_privilege_escalation(iam_role: str) -> dict:
    """Test IAM privilege escalation vectors"""
    audit_table.put_item(Item={
        "session_id": _session_context["session_id"],
        "event_timestamp": int(datetime.utcnow().timestamp()),
        "agent_type": "RED",
        "actor_id": _session_context["actor_id"],
        "action": "privilege_escalation_test",
        "target": iam_role,
        "outcome": "simulated"
    })
    
    return {
        "status": "executed",
        "attack_type": "Privilege Escalation",
        "target_role": iam_role,
        "simulated_result": "Overly permissive IAM policy detected",
        "timestamp": datetime.utcnow().isoformat()
    }

class RedAgent:
    def __init__(self):
        self.llm = ChatBedrock(
            model_id=Config.BEDROCK_MODEL_ID,
            region_name=Config.AWS_REGION,
            model_kwargs={
                "temperature": Config.BEDROCK_TEMPERATURE,
                "max_tokens": Config.BEDROCK_MAX_TOKENS,
                "top_p": Config.BEDROCK_TOP_P
            }
        )
        
        self.tools = [execute_sql_injection, test_xss_vulnerability, test_privilege_escalation]
        
        self.base_system_prompt = """You are a Red Team AI agent for Sentinel AI, an autonomous purple teaming platform.
            
Your mission: Identify and validate security vulnerabilities through controlled exploitation.

Rules:
1. NEVER target production systems or customer data
2. Always log your actions to the audit trail
3. Use the provided tools to execute attacks
4. Focus on: SQL injection, XSS, privilege escalation, API abuse
5. Provide detailed attack reports for the Blue Agent to learn from

You have access to these attack tools:
- execute_sql_injection: Test SQL injection vulnerabilities
- test_xss_vulnerability: Test cross-site scripting vulnerabilities  
- test_privilege_escalation: Test IAM privilege escalation

Analyze the target infrastructure and execute appropriate attacks."""
    
    def _build_prompt(self, memory_context: str = None) -> ChatPromptTemplate:
        """Build prompt with optional memory context injected."""
        system = self.base_system_prompt
        if memory_context:
            system += f"\n\n{memory_context}"
        
        return ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
    
    def execute_campaign(self, target_info: dict, memory_context: str = None,
                         session_id: str = None, actor_id: str = None) -> dict:
        """
        Execute offensive campaign against target infrastructure.
        
        Args:
            target_info: Target details (url, description, iam_role)
            memory_context: Optional prior findings context from CampaignMemoryManager
            session_id: Campaign session ID for audit trail
            actor_id: Who initiated this campaign
        """
        # Set session context for audit logging
        if session_id or actor_id:
            set_session_context(
                session_id=session_id or "default",
                actor_id=actor_id or "default_user"
            )
        
        # Build prompt with memory-aware context
        prompt = self._build_prompt(memory_context)
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        
        input_text = f"""
Target Infrastructure: {target_info.get('description', 'Unknown')}
Target URL: {target_info.get('url', 'http://test-target.example.com')}
Target IAM Role: {target_info.get('iam_role', 'test-role')}

Execute a comprehensive security validation campaign. Test for:
1. SQL injection vulnerabilities
2. XSS vulnerabilities
3. Privilege escalation opportunities

Report your findings."""
        
        result = executor.invoke({"input": input_text})
        return result
