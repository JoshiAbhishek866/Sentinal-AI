# Sentinel AI - Autonomous Purple Teaming Platform

**Tagline:** "Attack to Defend. Autonomously."

## Overview

Sentinel AI deploys dual-model AI agents (Red Team + Blue Team) to validate vulnerabilities through active exploitation and auto-remediation on AWS serverless infrastructure.

## Architecture

- **Red Agent**: Offensive AI that executes controlled attacks (SQL injection, XSS, privilege escalation)
- **Blue Agent**: Defensive AI that detects and auto-remediates vulnerabilities
- **Knowledge Base**: RAG-powered learning system that evolves with each attack-defense cycle

## Quick Start

### Prerequisites

- Python 3.11+
- AWS Account with Bedrock access
- AWS credentials configured

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your AWS credentials and configuration

# Run locally
python main.py
```

### Docker Deployment

```bash
# Build image
docker build -t sentinel-ai .

# Run container
docker run -p 8000:8000 --env-file .env sentinel-ai
```

## API Endpoints

### Start Campaign
```bash
POST /campaigns/start
{
  "target_url": "http://test-target.example.com",
  "target_description": "Test web application",
  "iam_role": "test-role"
}
```

### Get Campaign Status
```bash
GET /campaigns/{campaign_id}
```

### Health Check
```bash
GET /health
```

## AWS Deployment

### App Runner Deployment

1. Push Docker image to ECR
2. Create App Runner service
3. Configure environment variables
4. Enable auto-scaling

### Required AWS Resources

- Amazon Bedrock (Claude 3.5 Sonnet)
- Knowledge Bases for Amazon Bedrock
- DynamoDB tables: CampaignSessions, AuditLogs
- S3 bucket for compliance reports
- AWS WAF for attack detection
- IAM roles for Red/Blue agents

## Cost Estimate

- MVP: ~$18/month (single customer)
- Production: ~$28/customer/month (5 customers)

## Security

- Red Agent: Read-only access, no production data
- Blue Agent: Write access to security controls only
- All actions logged to immutable audit trail
- KMS encryption for data at rest

## Compliance

- SOC 2 Type II aligned
- ISO 27001 aligned
- Auto-generated compliance reports

## License

MIT
