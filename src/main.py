from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.red_agent import RedAgent
from src.agents.blue_agent import BlueAgent
import boto3
from datetime import datetime
from src.config import Config
import uuid

app = FastAPI(title="Sentinel AI - Autonomous Purple Teaming Platform")

# Initialize agents
red_agent = RedAgent()
blue_agent = BlueAgent()

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION)
campaigns_table = dynamodb.Table(Config.DYNAMODB_TABLE_CAMPAIGNS)

class CampaignRequest(BaseModel):
    target_url: str
    target_description: str
    iam_role: str = "test-role"

class CampaignResponse(BaseModel):
    campaign_id: str
    status: str
    red_agent_result: dict
    blue_agent_result: dict
    timestamp: str

@app.get("/")
def root():
    return {
        "service": "Sentinel AI",
        "tagline": "Attack to Defend. Autonomously.",
        "version": "1.0",
        "status": "operational"
    }

@app.post("/campaigns/start", response_model=CampaignResponse)
def start_campaign(request: CampaignRequest):
    """Initiate a purple teaming validation campaign"""
    campaign_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    try:
        # Initialize campaign in DynamoDB
        campaigns_table.put_item(Item={
            "campaign_id": campaign_id,
            "timestamp": int(datetime.utcnow().timestamp()),
            "status": "ACTIVE",
            "target_url": request.target_url,
            "target_description": request.target_description
        })
        
        # Execute Red Agent attack
        target_info = {
            "url": request.target_url,
            "description": request.target_description,
            "iam_role": request.iam_role
        }
        red_result = red_agent.execute_campaign(target_info)
        
        # Simulate threat detection and trigger Blue Agent
        threat_info = {
            "attack_type": "Multiple vulnerabilities detected",
            "target": request.target_url,
            "details": str(red_result.get("output", "Attack executed"))
        }
        blue_result = blue_agent.respond_to_threat(threat_info)
        
        # Update campaign status
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

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
