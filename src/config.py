import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
    
    # DynamoDB Tables
    DYNAMODB_TABLE_CAMPAIGNS = os.getenv("DYNAMODB_TABLE_CAMPAIGNS", "CampaignSessions")
    DYNAMODB_TABLE_AUDIT = os.getenv("DYNAMODB_TABLE_AUDIT", "AuditLogs")
    
    # S3
    S3_BUCKET_REPORTS = os.getenv("S3_BUCKET_REPORTS", "sentinel-ai-artifacts")
    
    # Agent Configuration
    RED_AGENT_ROLE_ARN = os.getenv("RED_AGENT_ROLE_ARN")
    BLUE_AGENT_ROLE_ARN = os.getenv("BLUE_AGENT_ROLE_ARN")
    
    # Bedrock Configuration
    BEDROCK_TEMPERATURE = 0.7
    BEDROCK_MAX_TOKENS = 4096
    BEDROCK_TOP_P = 0.9
