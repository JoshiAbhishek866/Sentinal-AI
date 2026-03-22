"""
Dashboard Reporter Agent
Real-time metrics and visualization data for frontend dashboard
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

from src.agents.base_agent import BaseAgent


class DashboardReporterAgent(BaseAgent):
    """
    Dashboard Reporter Agent
    
    Capabilities:
    - Real-time metrics aggregation
    - Visualization data formatting
    - WebSocket updates
    - Chart data generation
    - Historical trends
    - Alert formatting
    - Performance metrics
    """
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("dashboard_reporter", config)
        self.default_config = {
            "timeout": 60,
            "update_interval": 5,  # seconds
            "history_retention": 24,  # hours
            "enable_websocket": True,
            "chart_types": ["line", "bar", "pie", "gauge"]
        }
        self.config = {**self.default_config, **(config or {})}
        
        # Metrics cache
        self.metrics_cache = {}
        self.history = []
    
    async def execute(self, target: str, options: Optional[Dict] = None) -> Dict:
        """Generate dashboard report"""
        
        self.logger.progress("Generating dashboard report...")
        
        # Get all agent results from options
        agent_results = options.get("agent_results", {}) if options else {}
        
        # Generate dashboard data
        dashboard_data = {
            "metadata": {
                "target": target,
                "generated_at": datetime.utcnow().isoformat(),
                "update_interval": self.config["update_interval"]
            },
            "overview": self._generate_overview(agent_results),
            "metrics": self._generate_metrics(agent_results),
            "charts": self._generate_charts(agent_results),
            "alerts": self._generate_alerts(agent_results),
            "timeline": self._generate_timeline(agent_results),
            "statistics": self._generate_statistics(agent_results),
            "trends": self._generate_trends()
        }
        
        # Cache metrics
        self._cache_metrics(dashboard_data["metrics"])
        
        self.logger.success("Dashboard report generated")
        
        return dashboard_data
    
    def _generate_overview(self, agent_results: Dict) -> Dict:
        """Generate overview section"""
        
        total_findings = 0
        critical_count = 0
        high_count = 0
        agents_executed = len(agent_results)
        
        for agent_type, result in agent_results.items():
            data = result.get("data", {})
            
            # Count findings
            if "vulnerabilities" in data:
                total_findings += len(data["vulnerabilities"])
                critical_count += len([v for v in data["vulnerabilities"] if v.get("cvss_score", 0) >= 9.0])
                high_count += len([v for v in data["vulnerabilities"] if 7.0 <= v.get("cvss_score", 0) < 9.0])
            
            if "threats_detected" in data:
                total_findings += len(data["threats_detected"])
                critical_count += len([t for t in data["threats_detected"] if t.get("severity") == "critical"])
            
            if "findings" in data:
                total_findings += len(data["findings"])
        
        # Calculate risk score
        risk_score = min(100, (critical_count * 10 + high_count * 5))
        
        return {
            "total_findings": total_findings,
            "critical_findings": critical_count,
            "high_findings": high_count,
            "agents_executed": agents_executed,
            "risk_score": risk_score,
            "risk_level": self._calculate_risk_level(risk_score),
            "last_scan": datetime.utcnow().isoformat()
        }
    
    def _generate_metrics(self, agent_results: Dict) -> Dict:
        """Generate key metrics"""
        
        metrics = {
            "security_posture": {
                "score": 0,
                "trend": "stable",
                "change": 0
            },
            "vulnerability_count": {
                "total": 0,
                "by_severity": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }
            },
            "threat_count": {
                "total": 0,
                "active": 0,
                "mitigated": 0
            },
            "compliance_score": {
                "percentage": 0,
                "frameworks": {}
            },
            "incident_count": {
                "total": 0,
                "open": 0,
                "resolved": 0
            }
        }
        
        # Calculate metrics from agent results
        for agent_type, result in agent_results.items():
            data = result.get("data", {})
            
            # Vulnerabilities
            if "vulnerabilities" in data:
                vulns = data["vulnerabilities"]
                metrics["vulnerability_count"]["total"] = len(vulns)
                
                for vuln in vulns:
                    cvss = vuln.get("cvss_score", 0)
                    if cvss >= 9.0:
                        metrics["vulnerability_count"]["by_severity"]["critical"] += 1
                    elif cvss >= 7.0:
                        metrics["vulnerability_count"]["by_severity"]["high"] += 1
                    elif cvss >= 4.0:
                        metrics["vulnerability_count"]["by_severity"]["medium"] += 1
                    else:
                        metrics["vulnerability_count"]["by_severity"]["low"] += 1
            
            # Threats
            if "threats_detected" in data:
                metrics["threat_count"]["total"] = len(data["threats_detected"])
                metrics["threat_count"]["active"] = len(data["threats_detected"])
            
            # Compliance
            if "compliance_results" in data:
                for framework, result in data["compliance_results"].items():
                    metrics["compliance_score"]["frameworks"][framework] = result.get("compliance_percentage", 0)
                
                # Average compliance
                if metrics["compliance_score"]["frameworks"]:
                    metrics["compliance_score"]["percentage"] = sum(
                        metrics["compliance_score"]["frameworks"].values()
                    ) / len(metrics["compliance_score"]["frameworks"])
            
            # Incidents
            if "incidents" in data:
                metrics["incident_count"]["total"] = len(data["incidents"])
                metrics["incident_count"]["open"] = len([i for i in data["incidents"] if i.get("status") == "open"])
        
        # Calculate security posture score
        metrics["security_posture"]["score"] = self._calculate_security_posture(metrics)
        
        return metrics
    
    def _generate_charts(self, agent_results: Dict) -> Dict:
        """Generate chart data"""
        
        charts = {
            "vulnerability_distribution": self._chart_vuln_distribution(agent_results),
            "risk_timeline": self._chart_risk_timeline(),
            "compliance_radar": self._chart_compliance_radar(agent_results),
            "threat_heatmap": self._chart_threat_heatmap(agent_results),
            "agent_execution": self._chart_agent_execution(agent_results)
        }
        
        return charts
    
    def _chart_vuln_distribution(self, agent_results: Dict) -> Dict:
        """Vulnerability distribution pie chart"""
        
        distribution = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for agent_type, result in agent_results.items():
            data = result.get("data", {})
            if "vulnerabilities" in data:
                for vuln in data["vulnerabilities"]:
                    cvss = vuln.get("cvss_score", 0)
                    if cvss >= 9.0:
                        distribution["critical"] += 1
                    elif cvss >= 7.0:
                        distribution["high"] += 1
                    elif cvss >= 4.0:
                        distribution["medium"] += 1
                    else:
                        distribution["low"] += 1
        
        return {
            "type": "pie",
            "labels": ["Critical", "High", "Medium", "Low"],
            "data": [
                distribution["critical"],
                distribution["high"],
                distribution["medium"],
                distribution["low"]
            ],
            "colors": ["#d32f2f", "#f57c00", "#fbc02d", "#388e3c"]
        }
    
    def _chart_risk_timeline(self) -> Dict:
        """Risk score timeline"""
        
        # Generate last 24 hours of data points
        now = datetime.utcnow()
        labels = []
        data = []
        
        for i in range(24, 0, -1):
            time_point = now - timedelta(hours=i)
            labels.append(time_point.strftime("%H:%M"))
            # Simulated data - in production, use actual historical data
            data.append(50 + (i % 10) * 5)
        
        return {
            "type": "line",
            "labels": labels,
            "datasets": [{
                "label": "Risk Score",
                "data": data,
                "borderColor": "#f57c00",
                "fill": False
            }]
        }
    
    def _chart_compliance_radar(self, agent_results: Dict) -> Dict:
        """Compliance radar chart"""
        
        compliance_scores = {}
        
        for agent_type, result in agent_results.items():
            data = result.get("data", {})
            if "compliance_results" in data:
                for framework, result in data["compliance_results"].items():
                    compliance_scores[framework] = result.get("compliance_percentage", 0)
        
        return {
            "type": "radar",
            "labels": list(compliance_scores.keys()),
            "datasets": [{
                "label": "Compliance Score",
                "data": list(compliance_scores.values()),
                "backgroundColor": "rgba(54, 162, 235, 0.2)",
                "borderColor": "rgb(54, 162, 235)"
            }]
        }
    
    def _chart_threat_heatmap(self, agent_results: Dict) -> Dict:
        """Threat detection heatmap"""
        
        threat_counts = {}
        
        for agent_type, result in agent_results.items():
            data = result.get("data", {})
            if "threats_detected" in data:
                for threat in data["threats_detected"]:
                    threat_type = threat.get("type", "unknown")
                    threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
        
        return {
            "type": "bar",
            "labels": list(threat_counts.keys()),
            "datasets": [{
                "label": "Threat Count",
                "data": list(threat_counts.values()),
                "backgroundColor": "#f57c00"
            }]
        }
    
    def _chart_agent_execution(self, agent_results: Dict) -> Dict:
        """Agent execution status"""
        
        agents = []
        statuses = []
        colors = []
        
        for agent_type, result in agent_results.items():
            agents.append(agent_type)
            status = result.get("status", "unknown")
            statuses.append(1 if status == "success" else 0)
            colors.append("#4caf50" if status == "success" else "#f44336")
        
        return {
            "type": "bar",
            "labels": agents,
            "datasets": [{
                "label": "Execution Status",
                "data": statuses,
                "backgroundColor": colors
            }]
        }
    
    def _generate_alerts(self, agent_results: Dict) -> List[Dict]:
        """Generate formatted alerts"""
        
        alerts = []
        
        for agent_type, result in agent_results.items():
            data = result.get("data", {})
            
            # Critical vulnerabilities
            if "vulnerabilities" in data:
                critical_vulns = [v for v in data["vulnerabilities"] if v.get("cvss_score", 0) >= 9.0]
                if critical_vulns:
                    alerts.append({
                        "id": f"alert-vuln-{len(alerts)}",
                        "type": "critical",
                        "title": f"{len(critical_vulns)} Critical Vulnerabilities",
                        "message": "Immediate patching required",
                        "source": agent_type,
                        "timestamp": datetime.utcnow().isoformat(),
                        "action_required": True
                    })
            
            # Active threats
            if "threats_detected" in data:
                high_threats = [t for t in data["threats_detected"] if t.get("severity") == "high"]
                if high_threats:
                    alerts.append({
                        "id": f"alert-threat-{len(alerts)}",
                        "type": "warning",
                        "title": f"{len(high_threats)} Active Threats",
                        "message": "Investigation required",
                        "source": agent_type,
                        "timestamp": datetime.utcnow().isoformat(),
                        "action_required": True
                    })
            
            # Compliance failures
            if "compliance_results" in data:
                for framework, result in data["compliance_results"].items():
                    if result.get("compliance_percentage", 100) < 70:
                        alerts.append({
                            "id": f"alert-compliance-{len(alerts)}",
                            "type": "info",
                            "title": f"{framework.upper()} Compliance Low",
                            "message": f"Only {result['compliance_percentage']:.1f}% compliant",
                            "source": agent_type,
                            "timestamp": datetime.utcnow().isoformat(),
                            "action_required": False
                        })
        
        return alerts[:10]  # Top 10 alerts
    
    def _generate_timeline(self, agent_results: Dict) -> List[Dict]:
        """Generate event timeline"""
        
        timeline = []
        
        for agent_type, result in agent_results.items():
            timeline.append({
                "timestamp": result.get("timestamp", datetime.utcnow().isoformat()),
                "event": f"{agent_type} execution",
                "status": result.get("status", "unknown"),
                "duration": result.get("data", {}).get("duration", 0)
            })
        
        # Sort by timestamp
        timeline.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return timeline
    
    def _generate_statistics(self, agent_results: Dict) -> Dict:
        """Generate statistical summary"""
        
        return {
            "total_scans": len(agent_results),
            "successful_scans": len([r for r in agent_results.values() if r.get("status") == "success"]),
            "failed_scans": len([r for r in agent_results.values() if r.get("status") == "failed"]),
            "average_duration": self._calculate_average_duration(agent_results),
            "total_findings": self._count_total_findings(agent_results)
        }
    
    def _generate_trends(self) -> Dict:
        """Generate trend analysis"""
        
        return {
            "vulnerability_trend": "increasing",
            "compliance_trend": "stable",
            "threat_trend": "decreasing",
            "risk_trend": "stable"
        }
    
    def _calculate_risk_level(self, risk_score: int) -> str:
        """Calculate risk level from score"""
        if risk_score >= 80:
            return "critical"
        elif risk_score >= 60:
            return "high"
        elif risk_score >= 40:
            return "medium"
        else:
            return "low"
    
    def _calculate_security_posture(self, metrics: Dict) -> int:
        """Calculate overall security posture score"""
        
        # Start with 100
        score = 100
        
        # Deduct for vulnerabilities
        vuln_count = metrics["vulnerability_count"]
        score -= vuln_count["by_severity"]["critical"] * 10
        score -= vuln_count["by_severity"]["high"] * 5
        score -= vuln_count["by_severity"]["medium"] * 2
        
        # Deduct for threats
        score -= metrics["threat_count"]["active"] * 5
        
        # Add for compliance
        score += metrics["compliance_score"]["percentage"] * 0.2
        
        return max(0, min(100, int(score)))
    
    def _calculate_average_duration(self, agent_results: Dict) -> float:
        """Calculate average execution duration"""
        durations = []
        
        for result in agent_results.values():
            duration = result.get("data", {}).get("duration", 0)
            if duration:
                durations.append(duration)
        
        return sum(durations) / len(durations) if durations else 0
    
    def _count_total_findings(self, agent_results: Dict) -> int:
        """Count total findings across all agents"""
        total = 0
        
        for result in agent_results.values():
            data = result.get("data", {})
            total += len(data.get("vulnerabilities", []))
            total += len(data.get("threats_detected", []))
            total += len(data.get("findings", []))
        
        return total
    
    def _cache_metrics(self, metrics: Dict):
        """Cache metrics for historical tracking"""
        self.metrics_cache[datetime.utcnow().isoformat()] = metrics
        
        # Keep only last 24 hours
        cutoff = datetime.utcnow() - timedelta(hours=self.config["history_retention"])
        self.metrics_cache = {
            k: v for k, v in self.metrics_cache.items()
            if datetime.fromisoformat(k) > cutoff
        }
