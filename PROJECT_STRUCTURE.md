# Sentinel AI - Project Structure

## Directory Layout

```
sentinel-ai/
├── src/                                # Source code (Python backend)
│   ├── __init__.py
│   ├── main.py                        # Unified FastAPI entry point
│   ├── config.py                      # Configuration management
│   ├── agents/                        # All AI agents
│   │   ├── __init__.py               # Exports all agent types
│   │   ├── red_agent.py              # Offensive AI (LangChain + Bedrock)
│   │   ├── blue_agent.py             # Defensive AI (LangChain + Bedrock)
│   │   ├── base_agent.py             # Base agent class for orchestrator agents
│   │   ├── offensive/                # Offensive agent modules
│   │   │   ├── recon_agent.py
│   │   │   ├── scanner_agent.py
│   │   │   ├── vuln_agent.py
│   │   │   ├── credential_testing_agent.py
│   │   │   └── report_generator_agent.py
│   │   ├── defensive/                # Defensive agent modules
│   │   │   ├── threat_detection_agent.py
│   │   │   ├── hardening_agent.py
│   │   │   ├── vuln_prioritization_agent.py
│   │   │   ├── incident_response_agent.py
│   │   │   └── compliance_check_agent.py
│   │   └── core/                     # Core infrastructure agents
│   │       ├── sandbox_manager_agent.py
│   │       └── dashboard_reporter_agent.py
│   ├── core/                          # Core infrastructure
│   │   ├── orchestrator.py           # Multi-agent orchestrator
│   │   ├── database.py               # MongoDB client
│   │   ├── llm_client.py             # LLM integration (Ollama)
│   │   ├── n8n_client.py             # n8n workflow integration
│   │   ├── rag_client.py             # RAG vector database (ChromaDB)
│   │   └── dual_llm_orchestrator.py  # Dual LLM Red/Blue coordination
│   ├── routes/                        # Web platform API routes
│   │   ├── admin_auth.py
│   │   ├── client_auth.py
│   │   ├── content.py
│   │   ├── blog.py
│   │   ├── demo_requests.py
│   │   ├── clients.py
│   │   ├── client_dashboard.py
│   │   ├── uploads.py
│   │   ├── password_reset.py
│   │   ├── notifications.py
│   │   ├── security.py
│   │   ├── architecture.py
│   │   └── seo.py
│   ├── models/                        # Data models
│   │   └── schemas.py
│   └── utils/                         # Utilities
│       ├── helpers.py
│       ├── logger.py
│       └── seed.py
│
├── frontend/                           # Vue.js client dashboard
│   ├── src/
│   │   ├── components/               # UI components
│   │   ├── views/                    # Page views
│   │   ├── stores/                   # State management
│   │   ├── composables/              # Vue composables
│   │   └── router/                   # Client-side routing
│   └── package.json
│
├── admin/                              # Vue.js admin dashboard
│   ├── src/
│   │   ├── views/                    # Admin views
│   │   ├── components/               # Admin components
│   │   ├── stores/                   # State management
│   │   └── router/                   # Admin routing
│   └── package.json
│
├── n8n_workflows/                      # n8n workflow automation
│   ├── 1_security_scan_orchestration.json
│   ├── 2_ai_vulnerability_analysis.json
│   ├── 3_automated_patch_recommendation.json
│   ├── 4_incident_response_automation.json
│   └── 5_compliance_report_generation.json
│
├── content/                            # Static content & documents
│   ├── pdfs/
│   ├── txt/
│   └── xl/
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md
│   └── DEPLOYMENT.md
│
├── .env.example                        # Environment configuration template
├── .gitignore                          # Git ignore rules
├── Dockerfile                          # Container image
├── requirements.txt                    # Python dependencies
├── README.md                           # Project overview
├── design.md                           # System design document
├── requirements.md                     # Requirements specification
└── PROJECT_STRUCTURE.md               # This file
```

## Technology Stack

- **Backend**: Python 3.11, FastAPI, LangChain
- **AI**: Amazon Bedrock (Claude 3.5 Sonnet), Ollama
- **RAG**: ChromaDB, Bedrock Knowledge Bases
- **Data**: DynamoDB (campaigns), MongoDB (platform), S3
- **Compute**: AWS App Runner (Docker)
- **Frontend**: Vue.js 3, Three.js, Vite
- **Admin**: Vue.js 3, CoreUI
- **Workflows**: n8n (5 security automation workflows)
- **Security**: AWS WAF, IAM, KMS
