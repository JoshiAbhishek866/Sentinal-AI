"""
Sentinel AI Agents Package
Offensive, Defensive, and Core security agents
"""

# Existing LangChain-based agents
from src.agents.red_agent import RedAgent
from src.agents.blue_agent import BlueAgent

# Base agent class
from src.agents.base_agent import BaseAgent

# Offensive agents
from src.agents.offensive import (
    ReconAgent,
    ScannerAgent,
    VulnAgent,
    CredentialTestingAgent,
    ReportGeneratorAgent
)

# Defensive agents
from src.agents.defensive import (
    ThreatDetectionAgent,
    HardeningAgent,
    VulnPrioritizationAgent,
    IncidentResponseAgent,
    ComplianceCheckAgent
)

# Core infrastructure agents
from src.agents.core import (
    SandboxManagerAgent,
    DashboardReporterAgent
)
