# Sentinel AI — Autonomous Purple Teaming Platform

**"Attack to Defend. Autonomously."**

## Overview

Sentinel AI is a comprehensive autonomous purple teaming platform that deploys dual-model AI agents (Red Team + Blue Team) backed by a 12-agent orchestration system to validate vulnerabilities through active exploitation and auto-remediation. Built on AWS serverless architecture with lifecycle hooks, persistent campaign memory, and an attack-defense feedback loop.

## Architecture

### Dual AI Agent System (LangChain + Bedrock)
- **Red Agent** — Offensive AI executing controlled attacks (SQL injection, XSS, privilege escalation) with memory-enriched context from prior campaigns.
- **Blue Agent** — Defensive AI detecting and auto-remediating vulnerabilities, learning from the Red Agent's findings.
- **Attack-Defense Feedback Loop** — Red Agent probes gaps in Blue's past defenses; Blue Agent responds to Red's latest findings, creating a continuously evolving security posture.
- **Campaign Memory** — DynamoDB-backed persistent storage with 90-day TTL, storing per-target findings across sessions for contextual awareness.
- **Lifecycle Hooks** — `SecurityHookProvider` auto-loads prior findings before each agent runs and persists results after, removing manual glue from the orchestrator.

### Multi-Agent Orchestrator (12 Specialized Agents)

**Offensive Agents:**
| Agent | Purpose |
|-------|---------|
| Recon Agent | Network reconnaissance, DNS enumeration, subdomain discovery (async, concurrent) |
| Scanner Agent | Port/service scanning with Nmap or async socket fallback (50-concurrent) |
| Vulnerability Agent | CVE detection via NVD API with rate limiting + exponential backoff |
| Credential Testing Agent | Authentication testing (simulation mode, clearly labeled) |
| Report Generator Agent | Automated reports in JSON, HTML (XSS-safe), and Markdown |

**Defensive Agents:**
| Agent | Purpose |
|-------|---------|
| Threat Detection Agent | Log analysis, anomaly detection, IOC matching |
| Hardening Agent | CIS/NIST compliance checking, remediation scripts |
| Vulnerability Prioritization Agent | Risk-based CVSS prioritization |
| Incident Response Agent | Automated incident classification + playbook execution |
| Compliance Check Agent | CIS, NIST, PCI-DSS framework assessment |

**Core Agents:**
| Agent | Purpose |
|-------|---------|
| Sandbox Manager Agent | Isolated testing environments via Docker |
| Dashboard Reporter Agent | Real-time dashboard aggregation |

### Core Infrastructure

| Module | Purpose |
|--------|---------|
| `orchestrator.py` | Coordinates all 12 agents with lifecycle hook integration |
| `hooks.py` | `SecurityHookProvider` + `AttackDefenseFeedbackHook` |
| `memory.py` | `CampaignMemoryManager` — DynamoDB persistent memory with TTL |
| `dual_llm_orchestrator.py` | Dual-model LLM support (Bedrock + Ollama) |
| `database.py` | DynamoDB client for campaigns and executions |
| `llm_client.py` | Unified LLM client (Bedrock Claude, Ollama fallback) |
| `n8n_client.py` | n8n workflow automation (5 security workflows) |
| `rag_client.py` | ChromaDB + Bedrock Knowledge Bases RAG |

### Web Platform
- **Frontend:** Vue.js 3 dashboard with 3D architecture visualization
- **Admin Panel:** Full administration dashboard
- **Backend API:** 14 route modules (auth, clients, blog, security, SEO, notifications, uploads, etc.)
- **Real-time:** WebSocket notifications via `ConnectionManager`
- **Workflow Automation:** 5 n8n security workflows

## Quick Start

### Prerequisites
- Python 3.11+
- AWS Account with Bedrock access
- MongoDB (for web platform)
- Node.js 18+ (for frontend/admin)

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the platform
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Deployment

```bash
docker build -t sentinel-ai .
docker run -p 8000:8000 --env-file .env sentinel-ai
```

### Frontend Development

```bash
cd frontend && npm install && npm run dev    # Client dashboard (port 3000)
cd admin && npm install && npm run dev       # Admin panel (port 3001)
```

## API Endpoints

### Campaign Management (Red/Blue Agents)
- `POST /campaigns/start` — Start purple teaming campaign with attack-defense feedback loop
- `GET /campaigns/{id}` — Get campaign status and results

### Multi-Agent Orchestrator
- `POST /agents/execute/{type}` — Execute specific agent (with lifecycle hooks)
- `GET /agents/status` — All agent statuses
- `GET /workflows` — List n8n security workflows
- `GET /results/{id}` — Get execution results

### Security Scanning
- `POST /api/security/scan` — Run full security scan pipeline
- `POST /api/security/targeted` — Run targeted agent

### Web Platform
- `/api/admin/*` — Admin management & authentication
- `/api/auth/*` — Client authentication (JWT + bcrypt)
- `/api/security/*` — Security scanning interface
- `/api/blog/*` — Blog CMS
- `/api/clients/*` — Client management
- `/api/dashboard/*` — Client dashboard
- `/api/notifications/*` — WebSocket + REST notifications
- `/api/seo/*` — SEO management
- `/api/uploads/*` — File upload management
- `/api/content/*` — Content management
- `/api/demo/*` — Demo request handling
- `/api/password-reset/*` — Password reset flow

### Health
- `GET /health` — Detailed system health (agents, DB, n8n)
- `GET /api/health` — API health check

## Production Hardening

The platform includes the following production-grade improvements:

- **Async-safe agents** — All socket/DNS calls run via `run_in_executor()` to prevent event loop blocking
- **Execution timeouts** — Configurable per-agent timeout via `asyncio.wait_for()` (default: 300s)
- **Concurrent scanning** — Recon (10×), Scanner (50×) concurrent operations via semaphores
- **NVD rate limiting** — Semaphore(5) + exponential backoff on 403 + API key support
- **XSS-safe reports** — All HTML output escaped via `html.escape()`
- **Simulation labeling** — Credential testing results clearly marked as `mode: simulation`
- **Lifecycle hooks** — Automatic context loading and result persistence across all agents
- **Campaign memory** — 90-day TTL per-target DynamoDB memory for cross-session learning

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, LangChain |
| AI Engine | Amazon Bedrock (Claude 3.5 Sonnet), Ollama (local fallback) |
| Agent Framework | LangChain + Custom 12-Agent Orchestrator + Lifecycle Hooks |
| RAG | ChromaDB, Bedrock Knowledge Bases |
| Campaign Memory | DynamoDB (90-day TTL per-target memory) |
| Database | DynamoDB (campaigns/executions), MongoDB (web platform) |
| Frontend | Vue.js 3, Three.js, Vite |
| Workflows | n8n (5 security workflows) |
| Compute | AWS App Runner, Docker |
| Security | AWS WAF, IAM, KMS |
| Auth | JWT (python-jose), bcrypt, Passlib |

## Cost Estimate

- MVP: ~$18/month (single customer)
- Production: ~$28/customer/month (5 customers)

## License

MIT
