"""
Vulnerability Detection Agent
Detects vulnerabilities and CVEs in discovered services
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional
import re
from datetime import datetime

from src.agents.base_agent import BaseAgent
from src.utils.helpers import calculate_risk_score


class VulnAgent(BaseAgent):
    """
    Vulnerability Detection Agent
    
    Capabilities:
    - CVE database lookup
    - Vulnerability scoring (CVSS)
    - Exploit availability check
    - Patch information
    - Risk assessment
    """
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("vuln", config)
        self.default_config = {
            "timeout": 60,
            "cve_sources": ["nvd"],  # nvd, exploit-db
            "min_cvss_score": 0.0,
            "include_exploits": True,
            "check_patches": True,
            "nvd_api_key": None  # Set for higher rate limits (50/30s vs 5/30s)
        }
        self.config = {**self.default_config, **(config or {})}
        
        # CVE API endpoints
        self.nvd_api = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.exploit_db_api = "https://www.exploit-db.com/search"
        
        # Rate limiter: max 5 concurrent NVD requests
        self._nvd_semaphore = asyncio.Semaphore(5)
    
    async def execute(self, target: str, options: Optional[Dict] = None) -> Dict:
        """Execute vulnerability detection"""
        
        self.logger.progress("Starting vulnerability detection...")
        
        # Get services from options (from scanner agent)
        services = options.get("services", []) if options else []
        
        if not services:
            self.logger.warning("No services provided for vulnerability detection")
            return {
                "target": target,
                "vulnerabilities": [],
                "risk_score": 0.0,
                "summary": {
                    "total": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }
            }
        
        # Detect vulnerabilities
        all_vulnerabilities = []
        
        for service in services:
            vulns = await self.check_service_vulnerabilities(service)
            all_vulnerabilities.extend(vulns)
        
        # Calculate risk score
        risk_score = calculate_risk_score(all_vulnerabilities)
        
        # Categorize vulnerabilities
        summary = self._categorize_vulnerabilities(all_vulnerabilities)
        
        results = {
            "target": target,
            "services_checked": len(services),
            "vulnerabilities": all_vulnerabilities,
            "risk_score": risk_score,
            "summary": summary,
            "recommendations": self._generate_recommendations(all_vulnerabilities)
        }
        
        self.logger.success(
            f"Found {len(all_vulnerabilities)} vulnerabilities "
            f"(Risk Score: {risk_score:.1f}/10)"
        )
        
        return results
    
    async def check_service_vulnerabilities(self, service: Dict) -> List[Dict]:
        """Check vulnerabilities for a specific service"""
        service_name = service.get("service", "unknown")
        version = service.get("version")
        port = service.get("port")
        
        self.logger.progress(f"Checking {service_name} on port {port}...")
        
        if not version:
            self.logger.warning(f"No version info for {service_name}")
            return []
        
        vulnerabilities = []
        
        # Search CVE database
        if "nvd" in self.config["cve_sources"]:
            nvd_vulns = await self.search_nvd(service_name, version)
            vulnerabilities.extend(nvd_vulns)
        
        # Check for known exploits
        if self.config["include_exploits"]:
            for vuln in vulnerabilities:
                vuln["exploits"] = await self.check_exploits(vuln.get("cve_id"))
        
        return vulnerabilities
    
    async def search_nvd(self, product: str, version: str) -> List[Dict]:
        """Search NVD with rate limiting and backoff"""
        self.logger.progress(f"Searching NVD for {product} {version}...")
        
        vulnerabilities = []
        max_retries = 3
        
        async with self._nvd_semaphore:  # Rate limit concurrent NVD calls
            for attempt in range(max_retries):
                try:
                    headers = {}
                    if self.config.get("nvd_api_key"):
                        headers["apiKey"] = self.config["nvd_api_key"]
                    
                    async with aiohttp.ClientSession() as session:
                        params = {
                            "keywordSearch": f"{product} {version}",
                            "resultsPerPage": 20
                        }
                        
                        async with session.get(
                            self.nvd_api,
                            params=params,
                            headers=headers,
                            timeout=aiohttp.ClientTimeout(total=self.config["timeout"])
                        ) as response:
                            
                            if response.status == 200:
                                data = await response.json()
                                
                                for cve_item in data.get("vulnerabilities", []):
                                    cve = cve_item.get("cve", {})
                                    vuln = self._parse_cve_data(cve, product, version)
                                    
                                    if vuln["cvss_score"] >= self.config["min_cvss_score"]:
                                        vulnerabilities.append(vuln)
                                
                                return vulnerabilities  # Success — exit retry loop
                            
                            elif response.status == 403:
                                wait_time = 2 ** attempt * 6  # 6s, 12s, 24s
                                self.logger.warning(
                                    f"NVD API rate limited (attempt {attempt+1}/{max_retries}), "
                                    f"retrying in {wait_time}s..."
                                )
                                await asyncio.sleep(wait_time)
                            else:
                                self.logger.warning(f"NVD API returned status {response.status}")
                                return vulnerabilities
                
                except asyncio.TimeoutError:
                    self.logger.warning("NVD search timed out")
                    return vulnerabilities
                except Exception as e:
                    self.logger.warning(f"NVD search failed: {e}")
                    return vulnerabilities
        
        return vulnerabilities
    
    def _parse_cve_data(self, cve: Dict, product: str, version: str) -> Dict:
        """Parse CVE data from NVD"""
        cve_id = cve.get("id", "Unknown")
        
        # Get description
        descriptions = cve.get("descriptions", [])
        description = descriptions[0].get("value", "No description") if descriptions else "No description"
        
        # Get CVSS score
        metrics = cve.get("metrics", {})
        cvss_data = metrics.get("cvssMetricV31", [{}])[0] if metrics.get("cvssMetricV31") else {}
        cvss_score = cvss_data.get("cvssData", {}).get("baseScore", 0.0)
        severity = cvss_data.get("cvssData", {}).get("baseSeverity", "UNKNOWN")
        
        # Get published date
        published = cve.get("published", "")
        
        return {
            "cve_id": cve_id,
            "description": description[:500],  # Truncate
            "cvss_score": cvss_score,
            "severity": severity,
            "product": product,
            "version": version,
            "published_date": published,
            "references": [ref.get("url") for ref in cve.get("references", [])[:5]],
            "exploits": []
        }
    
    async def check_exploits(self, cve_id: str) -> List[Dict]:
        """Check for available exploits"""
        if not cve_id or cve_id == "Unknown":
            return []
        
        self.logger.progress(f"Checking exploits for {cve_id}...")
        
        exploits = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Search Exploit-DB
                search_url = f"{self.exploit_db_api}?cve={cve_id}"
                
                async with session.get(
                    search_url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    if response.status == 200:
                        # Parse exploit information
                        # This is simplified - actual implementation would parse HTML/JSON
                        exploits.append({
                            "source": "exploit-db",
                            "available": True,
                            "url": search_url
                        })
        
        except Exception as e:
            self.logger.warning(f"Exploit check failed: {e}")
        
        return exploits
    
    def _categorize_vulnerabilities(self, vulnerabilities: List[Dict]) -> Dict:
        """Categorize vulnerabilities by severity"""
        summary = {
            "total": len(vulnerabilities),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        for vuln in vulnerabilities:
            cvss = vuln.get("cvss_score", 0.0)
            
            if cvss >= 9.0:
                summary["critical"] += 1
            elif cvss >= 7.0:
                summary["high"] += 1
            elif cvss >= 4.0:
                summary["medium"] += 1
            elif cvss > 0.0:
                summary["low"] += 1
            else:
                summary["info"] += 1
        
        return summary
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> List[str]:
        """Generate remediation recommendations"""
        recommendations = []
        
        if not vulnerabilities:
            recommendations.append("No vulnerabilities detected. Continue monitoring.")
            return recommendations
        
        # Count by severity
        critical = sum(1 for v in vulnerabilities if v.get("cvss_score", 0) >= 9.0)
        high = sum(1 for v in vulnerabilities if 7.0 <= v.get("cvss_score", 0) < 9.0)
        
        if critical > 0:
            recommendations.append(
                f"⚠️ URGENT: {critical} critical vulnerabilities found. "
                "Immediate patching required."
            )
        
        if high > 0:
            recommendations.append(
                f"⚠️ HIGH PRIORITY: {high} high-severity vulnerabilities found. "
                "Schedule patching within 48 hours."
            )
        
        # Service-specific recommendations
        services_with_vulns = set(v.get("product") for v in vulnerabilities)
        
        for service in services_with_vulns:
            recommendations.append(
                f"Update {service} to the latest stable version"
            )
        
        # General recommendations
        recommendations.extend([
            "Enable automatic security updates where possible",
            "Implement a vulnerability management program",
            "Regular security scanning and monitoring",
            "Apply defense-in-depth security controls"
        ])
        
        return recommendations[:10]  # Limit to top 10
