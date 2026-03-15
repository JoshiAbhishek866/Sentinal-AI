# Design Document: HavoSec Integration into Sentinel AI
## Enhanced Purple Teaming Platform Architecture

**Project Name:** Sentinel AI + HavoSec Integration  
**Version:** 2.0  
**Date:** March 5, 2026

---

## 1. Executive Summary

This document outlines the technical design for integrating HavoSec's advanced multi-agent system, 3D visualization, and workflow automation capabilities into Sentinel AI's AWS serverless purple teaming platform.

### 1.1 Integration Goals
- Enhance agent capabilities with specialized offensive/defensive agents
- Add interactive 3D infrastructure visualization
- Integrate n8n workflow automation
- Implement comprehensive admin dashboard
- Maintain AWS serverless architecture
- Preserve existing functionality

---

## 2. Integrated System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Vue.js 3 Application                                │   │
│  │  ├── Landing Page (HavoSec)                          │   │
│  │  ├── Client Dashboard (HavoSec)                      │   │
│  │  ├── Admin Dashboard (HavoSec)                       │   │
│  │  ├── 3D Architecture Viewer (HavoSec + Three.js)    │   │
│  │  └── Campaign Management (Sentinel AI)              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI Server (AWS App Runner)                     │   │
│  │  ├── Campaign Endpoints (Sentinel AI)               │   │
│  │  ├── Admin Endpoints (HavoSec)                       │   │
│  │  ├── Client Endpoints (HavoSec)                      │   │
│  │  ├── Content Management (HavoSec)                    │   │
│  │  └── WebSocket Server (Real-time updates)           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Agent Orchestration Layer                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Python Orchestrator (Hybrid)                        │   │
│  │  ├── Sentinel AI Agents (LangChain + Bedrock)       │   │
│  │  │   ├── Red Agent (SQL, XSS, Priv Esc)            │   │
│  │  │   └── Blue Agent (WAF, SG, Compliance)          │   │
│  │  ├── HavoSec Offensive Agents                       │   │
│  │  │   ├── Recon Agent                                │   │
│  │  │   ├── Scanner Agent                              │   │
│  │  │   └── Vulnerability Agent                        │   │
│  │  └── HavoSec Defensive Agents                       │   │
│  │      ├── Threat Detection Agent                     │   │
│  │      └── Hardening Agent                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Workflow Automation Layer                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  n8n Workflow Engine                                 │   │
│  │  ├── Security Scan Orchestration                     │   │
│  │  ├── AI Vulnerability Analysis                       │   │
│  │  ├── Automated Patch Recommendations                 │   │
│  │  ├── Incident Response Automation                    │   │
│  │  └── Compliance Report Generation                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     AI Intelligence Layer                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Amazon Bedrock (Claude 3.5 Sonnet)                  │   │
│  │  ├── Agent Reasoning (Sentinel AI)                   │   │
│  │  ├── Vulnerability Analysis                          │   │
│  │  └── Threat Intelligence                             │   │
│  │                                                       │   │
│  │  Knowledge Bases for Amazon Bedrock (RAG)            │   │
│  │  ├── CVE Database                                    │   │
│  │  ├── Attack Patterns                                 │   │
│  │  └── Mitigation Playbooks                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  DynamoDB (Primary - AWS)                            │   │
│  │  ├── CampaignSessions                                │   │
│  │  ├── AuditLogs                                       │   │
│  │  ├── KnowledgeEvolution                              │   │
│  │  ├── Users (Admin/Client)                            │   │
│  │  └── Content (Blog, Pages)                           │   │
│  │                                                       │   │
│  │  S3 (Storage - AWS)                                  │   │
│  │  ├── Compliance Reports                              │   │
│  │  ├── Scan Results                                    │   │
│  │  ├── Architecture Diagrams                           │   │
│  │  └── Media Assets                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Component Integration Design

### 3.1 Agent System Integration

#### 3.1.1 Unified Agent Architecture

```python
# src/agents/base_agent.py (Enhanced)
class BaseAgent:
    """Base class for all agents (Sentinel AI + HavoSec)"""
    def __init__(self, agent_type, llm_client):
        self.agent_type = agent_type  # 'offensive' or 'defensive'
        self.llm_client = llm_client
        self.tools = []
        self.enabled = True
    
    async def execute(self, task):
        """Execute agent task"""
        pass

# Sentinel AI Agents (Bedrock-powered)
class RedAgent(BaseAgent):
    """Offensive agent using Amazon Bedrock"""
    pass

class BlueAgent(BaseAgent):
    """Defensive agent using Amazon Bedrock"""
    pass

# HavoSec Agents (Local/Hybrid)
class ReconAgent(BaseAgent):
    """Network reconnaissance agent"""
    pass

class ScannerAgent(BaseAgent):
    """Port and service scanning agent"""
    pass

class VulnerabilityAgent(BaseAgent):
    """CVE detection agent"""
    pass

class ThreatDetectionAgent(BaseAgent):
    """Real-time threat monitoring agent"""
    pass

class HardeningAgent(BaseAgent):
    """Security hardening agent"""
    pass
```

#### 3.1.2 Agent Orchestrator

```python
# src/core/orchestrator.py (Enhanced)
class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            'offensive': [],
            'defensive': []
        }
        self.n8n_client = N8NClient()
        self.bedrock_client = BedrockClient()
    
    async def execute_campaign(self, campaign_config):
        """Execute multi-agent campaign"""
        # 1. Initialize agents based on config
        # 2. Execute offensive agents
        # 3. Trigger defensive response
        # 4. Coordinate with n8n workflows
        # 5. Generate reports
        pass
```

### 3.2 Frontend Integration

#### 3.2.1 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── sentinel-ai/          # Original Sentinel AI components
│   │   │   └── CampaignDashboard.vue
│   │   ├── havosec/              # HavoSec components
│   │   │   ├── ArchitectureDiagram.vue (3D)
│   │   │   ├── AdminDashboard.vue
│   │   │   ├── ClientDashboard.vue
│   │   │   └── LandingPage.vue
│   │   └── shared/               # Shared components
│   │       ├── Header.vue
│   │       └── Footer.vue
│   ├── views/
│   │   ├── Home.vue              # Landing page
│   │   ├── Dashboard.vue         # Client dashboard
│   │   ├── Admin.vue             # Admin panel
│   │   ├── Architecture.vue      # 3D visualization
│   │   └── Campaigns.vue         # Campaign management
│   ├── router/
│   │   └── index.js              # Unified routing
│   └── stores/
│       ├── campaign.js           # Campaign state
│       ├── agents.js             # Agent state
│       └── auth.js               # Authentication
```

#### 3.2.2 3D Visualization Integration

```vue
<!-- src/views/Architecture.vue -->
<template>
  <div class="architecture-view">
    <ArchitectureDiagram
      :architecture-data="architectureData"
      :real-time-updates="true"
      @node-selected="handleNodeClick"
    />
    <CampaignControls
      @start-campaign="startCampaign"
      @stop-campaign="stopCampaign"
    />
  </div>
</template>

<script setup>
import ArchitectureDiagram from '@/components/havosec/ArchitectureDiagram.vue'
import { useWebSocket } from '@/composables/useWebSocket'

const { architectureData } = useWebSocket('/ws/architecture')
</script>
```

### 3.3 Backend Integration

#### 3.3.1 Unified API Structure

```python
# src/main.py (Enhanced)
from fastapi import FastAPI, WebSocket
from routes import (
    sentinel_campaigns,  # Sentinel AI routes
    havosec_admin,       # HavoSec admin routes
    havosec_clients,     # HavoSec client routes
    havosec_content,     # HavoSec content routes
)

app = FastAPI(title="Sentinel AI + HavoSec Platform")

# Sentinel AI routes
app.include_router(sentinel_campaigns.router, prefix="/api/campaigns")

# HavoSec routes
app.include_router(havosec_admin.router, prefix="/api/admin")
app.include_router(havosec_clients.router, prefix="/api/clients")
app.include_router(havosec_content.router, prefix="/api/content")

# WebSocket for real-time updates
@app.websocket("/ws/architecture")
async def websocket_architecture(websocket: WebSocket):
    await websocket.accept()
    # Stream architecture updates
    pass
```

### 3.4 Workflow Integration

#### 3.4.1 n8n Setup

```yaml
# docker-compose.yml (Enhanced)
version: '3.8'

services:
  sentinel-ai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AWS_REGION=us-east-1
      - BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook
    depends_on:
      - n8n

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
    volumes:
      - ./n8n_workflows:/home/node/.n8n/workflows
```

#### 3.4.2 Workflow Triggers

```python
# src/core/n8n_client.py
class N8NClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    async def trigger_workflow(self, workflow_id, data):
        """Trigger n8n workflow"""
        url = f"{self.base_url}/webhook/{workflow_id}"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            return response.json()
    
    async def trigger_security_scan(self, target):
        """Trigger security scan workflow"""
        return await self.trigger_workflow(
            "security_scan_orchestration",
            {"target": target}
        )
```

---

## 4. Database Schema Integration

### 4.1 DynamoDB Tables (Enhanced)

**Table: CampaignSessions** (Existing + Enhanced)
```
Partition Key: campaign_id (String)
Sort Key: timestamp (Number)
Attributes:
  - status: ACTIVE | COMPLETED | FAILED
  - campaign_type: purple_team | recon | scan | vuln_assessment
  - agents_used: List[String]
  - red_agent_actions: List
  - blue_agent_actions: List
  - havosec_agent_results: Map
  - architecture_snapshot: Map
  - n8n_workflow_ids: List[String]
```

**Table: Users** (New)
```
Partition Key: user_id (String)
Sort Key: user_type (String)  # 'admin' | 'client'
Attributes:
  - email: String
  - name: String
  - company: String
  - role: String
  - permissions: List[String]
  - created_at: Number
```

**Table: ArchitectureScans** (New)
```
Partition Key: scan_id (String)
Sort Key: timestamp (Number)
Attributes:
  - client_id: String
  - nodes: List[Map]
  - connections: List[Map]
  - vulnerabilities: List[Map]
  - scan_type: String
```

---

## 5. Deployment Architecture

### 5.1 AWS Deployment (Primary)

```
AWS Cloud
├── App Runner
│   └── Sentinel AI + HavoSec API
├── Bedrock
│   └── Claude 3.5 Sonnet
├── DynamoDB
│   ├── CampaignSessions
│   ├── Users
│   └── ArchitectureScans
├── S3
│   ├── Reports
│   └── Media
├── CloudWatch
│   └── Logs & Metrics
└── WAF
    └── Security Rules
```

### 5.2 Optional Local Deployment

```
Local Environment
├── Docker Compose
│   ├── Sentinel AI API
│   ├── n8n
│   ├── MongoDB (optional)
│   └── Local LLM (optional)
└── HavoSec Agents
    ├── Recon Agent
    ├── Scanner Agent
    └── Vulnerability Agent
```

---

## 6. Technology Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Vue.js 3, Three.js, GSAP | UI and 3D visualization |
| Backend API | FastAPI, Python 3.11 | REST API and WebSocket |
| AI Engine | Amazon Bedrock (Claude 3.5) | Agent reasoning |
| Agent Framework | LangChain | Tool orchestration |
| Workflow | n8n | Automation |
| Database | DynamoDB | Primary storage |
| Storage | S3 | Files and reports |
| Deployment | AWS App Runner, Docker | Container hosting |
| Monitoring | CloudWatch | Metrics and logs |

---

## 7. Integration Phases

### Phase 1: Backend Integration (Week 1-2)
- Merge agent systems
- Integrate orchestrator
- Update database schema
- Add new API endpoints

### Phase 2: Frontend Integration (Week 3-4)
- Integrate 3D visualization
- Add admin dashboard
- Update landing page
- Implement WebSocket

### Phase 3: Workflow Integration (Week 5)
- Deploy n8n
- Import workflows
- Configure triggers
- Test automation

### Phase 4: Testing & Deployment (Week 6)
- Integration testing
- Performance testing
- Security audit
- AWS deployment

---

**Document Control:**
- **Author:** Kiro AI Assistant
- **Reviewed By:** [Abhishek Joshi]
- **Approved By:** [Abhishek Joshi]
- **Next Review Date:** [15-03-2026]
