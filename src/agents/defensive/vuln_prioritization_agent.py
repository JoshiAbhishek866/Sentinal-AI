"""
Vulnerability Prioritization Agent
AI-powered vulnerability risk assessment and prioritization
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime

from src.agents.base_agent import BaseAgent


class VulnPrioritizationAgent(BaseAgent):
    """
    Vulnerability Prioritization Agent
    
    Capabilities:
    - AI-powered risk assessment
    - CVSS + contextual analysis
    - Business impact evaluation
    - Exploit availability weighting
    - Patch priority calculation
    - Resource allocation guidance
    """
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("vuln_prioritization", config)
        self.default_config = {
            "timeout": 120,
            "use_ai": True,
            "consider_exploits": True,
            "consider_business_impact": True,
            "max_priority_vulns": 20
        }
        self.config = {**self.default_config, **(config or {})}
    
    async def execute(self, target: str, options: Optional[Dict] = None) -> Dict:
        """Execute vulnerability prioritization"""
        
        self.logger.progress("Starting AI-powered vulnerability prioritization...")
        
        # Get vulnerabilities from options
        vulnerabilities = options.get("vulnerabilities", []) if options else []
        
        if not vulnerabilities:
            self.logger.warning("No vulnerabilities provided for prioritization")
            return {
                "target": target,
                "prioritized_vulnerabilities": [],
                "summary": {"total": 0}
            }
        
        # Prioritize vulnerabilities
        prioritized = []
        
        for vuln in vulnerabilities:
            priority_score = await self._calculate_priority_score(vuln)
            
            prioritized_vuln = {
                **vuln,
                "priority_score": priority_score["score"],
                "priority_level": priority_score["level"],
                "factors": priority_score["factors"],
                "recommended_timeline": priority_score["timeline"],
                "business_impact": priority_score["business_impact"]
            }
            
            prioritized.append(prioritized_vuln)
        
        # Sort by priority score
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Generate summary
        summary = self._generate_summary(prioritized)
        
        # Create remediation plan
        remediation_plan = self._create_remediation_plan(prioritized)
        
        results = {
            "target": target,
            "total_vulnerabilities": len(vulnerabilities),
            "prioritized_vulnerabilities": prioritized[:self.config["max_priority_vulns"]],
            "summary": summary,
            "remediation_plan": remediation_plan,
            "resource_allocation": self._suggest_resource_allocation(prioritized)
        }
        
        self.logger.success(
            f"Prioritized {len(prioritized)} vulnerabilities"
        )
        
        return results
    
    async def _calculate_priority_score(self, vuln: Dict) -> Dict:
        """Calculate comprehensive priority score"""
        
        # Base CVSS score (0-10)
        cvss_score = vuln.get("cvss_score", 0.0)
        
        # Initialize factors
        factors = {
            "cvss_base": cvss_score,
            "exploit_available": 0,
            "public_exploit": 0,
            "ease_of_exploitation": 0,
            "asset_criticality": 0,
            "data_exposure": 0,
            "patch_available": 0
        }
        
        # Exploit availability (+3 points)
        if self.config["consider_exploits"]:
            exploits = vuln.get("exploits", [])
            if exploits:
                factors["exploit_available"] = 3
                if any("public" in str(e).lower() for e in exploits):
                    factors["public_exploit"] = 2
        
        # Ease of exploitation
        if cvss_score >= 9.0:
            factors["ease_of_exploitation"] = 3
        elif cvss_score >= 7.0:
            factors["ease_of_exploitation"] = 2
        elif cvss_score >= 4.0:
            factors["ease_of_exploitation"] = 1
        
        # Asset criticality (from context)
        service = vuln.get("product", "").lower()
        if any(critical in service for critical in ["database", "auth", "admin"]):
            factors["asset_criticality"] = 3
        
        # Data exposure risk
        if "data" in vuln.get("description", "").lower():
            factors["data_exposure"] = 2
        
        # Patch availability (-1 if available)
        if vuln.get("patch_available"):
            factors["patch_available"] = -1
        
        # Calculate total score
        total_score = sum(factors.values())
        
        # Determine priority level
        if total_score >= 15:
            level = "critical"
            timeline = "Immediate (0-24 hours)"
            business_impact = "Severe - Potential data breach or system compromise"
        elif total_score >= 10:
            level = "high"
            timeline = "Urgent (1-7 days)"
            business_impact = "High - Significant security risk"
        elif total_score >= 5:
            level = "medium"
            timeline = "Scheduled (7-30 days)"
            business_impact = "Moderate - Should be addressed soon"
        else:
            level = "low"
            timeline = "Planned (30-90 days)"
            business_impact = "Low - Monitor and patch during maintenance"
        
        return {
            "score": total_score,
            "level": level,
            "timeline": timeline,
            "business_impact": business_impact,
            "factors": factors
        }
    
    def _generate_summary(self, prioritized: List[Dict]) -> Dict:
        """Generate prioritization summary"""
        summary = {
            "total": len(prioritized),
            "by_priority": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "average_score": 0,
            "highest_score": 0,
            "with_exploits": 0,
            "requiring_immediate_action": 0
        }
        
        scores = []
        
        for vuln in prioritized:
            level = vuln.get("priority_level", "low")
            summary["by_priority"][level] += 1
            
            score = vuln.get("priority_score", 0)
            scores.append(score)
            
            if vuln.get("exploits"):
                summary["with_exploits"] += 1
            
            if level in ["critical", "high"]:
                summary["requiring_immediate_action"] += 1
        
        if scores:
            summary["average_score"] = sum(scores) / len(scores)
            summary["highest_score"] = max(scores)
        
        return summary
    
    def _create_remediation_plan(self, prioritized: List[Dict]) -> Dict:
        """Create phased remediation plan"""
        plan = {
            "phase_1_immediate": [],
            "phase_2_urgent": [],
            "phase_3_scheduled": [],
            "phase_4_planned": []
        }
        
        for vuln in prioritized:
            level = vuln.get("priority_level", "low")
            
            item = {
                "cve_id": vuln.get("cve_id", "N/A"),
                "product": vuln.get("product", "Unknown"),
                "cvss_score": vuln.get("cvss_score", 0),
                "priority_score": vuln.get("priority_score", 0),
                "timeline": vuln.get("recommended_timeline", "")
            }
            
            if level == "critical":
                plan["phase_1_immediate"].append(item)
            elif level == "high":
                plan["phase_2_urgent"].append(item)
            elif level == "medium":
                plan["phase_3_scheduled"].append(item)
            else:
                plan["phase_4_planned"].append(item)
        
        return plan
    
    def _suggest_resource_allocation(self, prioritized: List[Dict]) -> Dict:
        """Suggest resource allocation"""
        critical_count = len([v for v in prioritized if v.get("priority_level") == "critical"])
        high_count = len([v for v in prioritized if v.get("priority_level") == "high"])
        
        allocation = {
            "immediate_team_size": 0,
            "estimated_hours": 0,
            "recommended_approach": "",
            "external_help_needed": False
        }
        
        # Calculate team size needed
        if critical_count > 10:
            allocation["immediate_team_size"] = 5
            allocation["external_help_needed"] = True
        elif critical_count > 5:
            allocation["immediate_team_size"] = 3
        elif critical_count > 0:
            allocation["immediate_team_size"] = 2
        else:
            allocation["immediate_team_size"] = 1
        
        # Estimate hours
        allocation["estimated_hours"] = (
            critical_count * 8 +  # 8 hours per critical
            high_count * 4 +      # 4 hours per high
            len(prioritized) * 1  # 1 hour per other
        )
        
        # Recommend approach
        if critical_count > 5:
            allocation["recommended_approach"] = "Emergency response - Form dedicated team, pause non-critical work"
        elif critical_count > 0:
            allocation["recommended_approach"] = "Priority patching - Allocate senior resources immediately"
        else:
            allocation["recommended_approach"] = "Standard remediation - Include in regular maintenance cycle"
        
        return allocation
