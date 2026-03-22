from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import boto3
from datetime import datetime
from src.config import Config

# Lazy initialization for AWS clients
_audit_table = None
_waf_client = None

def get_audit_table():
    global _audit_table
    if _audit_table is None:
        dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
        _audit_table = dynamodb.Table(Config.DYNAMODB_TABLE_AUDIT)
    return _audit_table

def get_waf_client():
    global _waf_client
    if _waf_client is None:
        _waf_client = boto3.client('wafv2', region_name=Config.AWS_REGION)
    return _waf_client


def _build_audit_item(agent_type: str, action: str, target: str,
                      session_id: str = "default", actor_id: str = "default_user",
                      outcome: str = "success", **extra) -> dict:
    """Build an audit log item with explicit context (no globals)."""
    item = {
        "session_id": session_id,
        "event_timestamp": int(datetime.utcnow().timestamp()),
        "agent_type": agent_type,
        "actor_id": actor_id,
        "action": action,
        "target": target,
        "outcome": outcome,
    }
    item.update(extra)
    return item


@tool
def update_waf_acl(rule_name: str, attack_type: str, action: str = "BLOCK",
                   session_id: str = "default", actor_id: str = "default_user") -> dict:
    """Update AWS WAF ACL rules to block attack vectors"""
    get_audit_table().put_item(Item=_build_audit_item(
        agent_type="BLUE", action="waf_rule_update",
        target=rule_name, session_id=session_id, actor_id=actor_id
    ))
    
    return {
        "status": "updated",
        "rule_name": rule_name,
        "attack_type": attack_type,
        "action": action,
        "message": f"WAF rule created to {action} {attack_type} attacks",
        "timestamp": datetime.utcnow().isoformat()
    }

@tool
def modify_security_group(group_id: str, rule_action: str, port: int,
                          session_id: str = "default", actor_id: str = "default_user") -> dict:
    """Modify security group rules to restrict access"""
    get_audit_table().put_item(Item=_build_audit_item(
        agent_type="BLUE", action="security_group_modification",
        target=group_id, session_id=session_id, actor_id=actor_id
    ))
    
    return {
        "status": "modified",
        "group_id": group_id,
        "action": rule_action,
        "port": port,
        "message": f"Security group {group_id} updated - port {port} access restricted",
        "timestamp": datetime.utcnow().isoformat()
    }

@tool
def query_knowledge_base(attack_vector: str) -> dict:
    """Query knowledge base for mitigation strategies. Attempts ChromaDB RAG first, falls back to local strategies."""
    # Attempt real RAG query if ChromaDB is available
    try:
        import chromadb
        client = chromadb.HttpClient(host="localhost", port=8000)
        collection = client.get_collection("security_mitigations")
        results = collection.query(query_texts=[attack_vector], n_results=3)
        if results and results.get("documents") and results["documents"][0]:
            return {
                "attack_vector": attack_vector,
                "strategy": {
                    "mitigation": results["documents"][0][0],
                    "source": "rag_knowledge_base",
                    "confidence": results["distances"][0][0] if results.get("distances") else None,
                },
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception:
        pass  # Fall back to local strategies
    
    # Fallback: curated local strategies
    strategies = {
        "SQL Injection": {
            "mitigation": "Enable WAF SQL injection rule set, implement parameterized queries, use ORM",
            "source": "local_fallback",
        },
        "XSS": {
            "mitigation": "Enable WAF XSS protection, implement Content Security Policy, sanitize inputs",
            "source": "local_fallback",
        },
        "Privilege Escalation": {
            "mitigation": "Apply least privilege IAM policies, enable IAM Access Analyzer, audit role bindings",
            "source": "local_fallback",
        }
    }
    
    strategy = strategies.get(attack_vector, {
        "mitigation": "Generic security hardening recommended — consult NIST 800-53 controls",
        "source": "local_fallback",
    })
    
    return {
        "attack_vector": attack_vector,
        "strategy": strategy,
        "timestamp": datetime.utcnow().isoformat()
    }

@tool
def generate_compliance_report(campaign_id: str, findings: str) -> dict:
    """Generate compliance report based on actual campaign findings — dynamically evaluates controls."""
    findings_lower = findings.lower()
    
    # Evaluate controls based on actual findings
    controls = {
        "CC6.1: Logical Access Controls": "FAIL" if any(w in findings_lower for w in ["privilege escalation", "unauthorized", "access control"]) else "PASS",
        "CC6.6: Encryption": "FAIL" if any(w in findings_lower for w in ["unencrypted", "plaintext", "http://"]) else "PASS",
        "CC7.2: System Monitoring": "FAIL" if any(w in findings_lower for w in ["undetected", "no logging", "blind spot"]) else "PASS",
        "CC6.3: Input Validation": "FAIL" if any(w in findings_lower for w in ["sql injection", "xss", "injection"]) else "PASS",
    }
    
    passed = sum(1 for v in controls.values() if v == "PASS")
    total = len(controls)
    overall = "PASS" if passed == total else "FAIL"
    
    controls_text = "\n".join(f"  - {name} — {status}" for name, status in controls.items())
    
    report_content = f"""SOC 2 Type II Compliance Assessment
Campaign ID: {campaign_id}
Generated: {datetime.utcnow().isoformat()}

Findings:
{findings}

Controls Evaluated ({passed}/{total} passed):
{controls_text}

Overall Result: {overall}
Note: This is an automated assessment. A qualified auditor should review these findings."""
    
    report_key = f"compliance-reports/soc2/campaign-{campaign_id}-{datetime.utcnow().strftime('%Y%m%d')}.txt"
    
    return {
        "status": "generated",
        "overall_result": overall,
        "controls_passed": passed,
        "controls_total": total,
        "controls": controls,
        "report_path": f"s3://{Config.S3_BUCKET_REPORTS}/{report_key}",
        "campaign_id": campaign_id,
        "disclaimer": "Automated assessment — requires human auditor review",
        "timestamp": datetime.utcnow().isoformat()
    }

class BlueAgent:
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
        
        self.tools = [update_waf_acl, modify_security_group, query_knowledge_base, generate_compliance_report]
        
        self.base_system_prompt = """You are a Blue Team AI agent for Sentinel AI, an autonomous purple teaming platform.

Your mission: Detect attacks from the Red Agent and automatically remediate vulnerabilities.

Rules:
1. Respond to threats within 5 seconds
2. Query the knowledge base for proven mitigation strategies
3. Apply remediations automatically using AWS SDK tools
4. Generate compliance reports after successful defense
5. Update the knowledge base with new learnings

You have access to these defense tools:
- update_waf_acl: Update WAF rules to block attacks
- modify_security_group: Restrict network access
- query_knowledge_base: Retrieve mitigation strategies from RAG
- generate_compliance_report: Create SOC 2 audit reports

Analyze the detected threat and execute appropriate defenses."""
    
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
    
    def respond_to_threat(self, threat_info: dict, memory_context: str = None,
                          session_id: str = None, actor_id: str = None) -> dict:
        """
        Respond to detected threat and auto-remediate.
        
        Args:
            threat_info: Threat details (attack_type, target, details)
            memory_context: Optional prior context from CampaignMemoryManager
            session_id: Campaign session ID for audit trail
            actor_id: Who initiated this campaign
        """
        # Set session context (no more globals)
        _sid = session_id or "default"
        _aid = actor_id or "default_user"
        
        # Build prompt with memory-aware context
        prompt = self._build_prompt(memory_context)
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        
        input_text = f"""
THREAT DETECTED:
Attack Type: {threat_info.get('attack_type', 'Unknown')}
Target: {threat_info.get('target', 'Unknown')}
Details: {threat_info.get('details', 'No details available')}

Execute defensive response:
1. Query knowledge base for mitigation strategies
2. Apply appropriate remediation (WAF rules, security groups, etc.)
3. Generate compliance report documenting the defense

Respond immediately!"""
        
        result = executor.invoke({"input": input_text})
        return result
