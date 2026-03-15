"""
Credential Testing Agent
Ethical brute force simulation and credential testing
"""

import asyncio
from typing import Dict, List, Optional
import hashlib
import time

from src.agents.base_agent import BaseAgent


class CredentialTestingAgent(BaseAgent):
    """
    Credential Testing Agent
    
    Capabilities:
    - Brute force simulation (ethical)
    - Password spraying
    - Default credential checking
    - Common password testing
    - Rate limiting
    - Lockout detection
    - Ethical testing controls
    """
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("credential_testing", config)
        self.default_config = {
            "timeout": 300,
            "max_attempts": 100,
            "rate_limit": 1.0,  # seconds between attempts
            "test_mode": "safe",  # safe, moderate, aggressive
            "check_defaults": True,
            "password_spray": True,
            "lockout_threshold": 5,
            "ethical_mode": True  # Always respect rate limits and stop on lockout
        }
        self.config = {**self.default_config, **(config or {})}
        
        # Common credentials database
        self.default_credentials = self._load_default_credentials()
        self.common_passwords = self._load_common_passwords()
    
    async def execute(self, target: str, options: Optional[Dict] = None) -> Dict:
        """Execute credential testing"""
        
        if not self.config["ethical_mode"]:
            raise ValueError("Ethical mode must be enabled for credential testing")
        
        self.logger.progress("Starting ethical credential testing...")
        
        # Get services from options
        services = options.get("services", []) if options else []
        usernames = options.get("usernames", ["admin", "root", "user"]) if options else ["admin"]
        
        results = {
            "target": target,
            "test_mode": self.config["test_mode"],
            "mode": "simulation",  # Clearly indicates results are simulated
            "services_tested": [],
            "weak_credentials": [],
            "default_credentials": [],
            "password_spray_results": [],
            "lockout_detected": False,
            "recommendations": []
        }
        
        # Test default credentials
        if self.config["check_defaults"]:
            default_results = await self.test_default_credentials(target, services)
            results["default_credentials"] = default_results
        
        # Password spraying
        if self.config["password_spray"]:
            spray_results = await self.password_spray(target, usernames)
            results["password_spray_results"] = spray_results
        
        # Common password testing
        common_results = await self.test_common_passwords(target, usernames[:3])
        results["weak_credentials"] = common_results
        
        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)
        
        # Summary
        results["summary"] = {
            "services_tested": len(results["services_tested"]),
            "weak_found": len(results["weak_credentials"]),
            "defaults_found": len(results["default_credentials"]),
            "lockout_detected": results["lockout_detected"]
        }
        
        self.logger.success(
            f"Credential testing completed: {results['summary']['weak_found']} weak credentials found"
        )
        
        return results
    
    async def test_default_credentials(
        self,
        target: str,
        services: List[Dict]
    ) -> List[Dict]:
        """Test for default credentials"""
        self.logger.progress("Testing default credentials...")
        
        found_defaults = []
        
        for service in services[:5]:  # Limit to 5 services
            service_name = service.get("service", "").lower()
            port = service.get("port")
            
            # Get default credentials for this service
            defaults = self.default_credentials.get(service_name, [])
            
            for cred in defaults:
                username = cred["username"]
                password = cred["password"]
                
                # Simulate credential test (ethical - not actual login)
                result = await self._simulate_credential_test(
                    target,
                    port,
                    username,
                    password
                )
                
                if result["success"]:
                    found_defaults.append({
                        "service": service_name,
                        "port": port,
                        "username": username,
                        "password": password,
                        "severity": "critical",
                        "description": f"Default credentials found for {service_name}"
                    })
                    self.logger.warning(f"Default credentials found: {service_name}")
                
                # Rate limiting
                await asyncio.sleep(self.config["rate_limit"])
        
        return found_defaults
    
    async def password_spray(
        self,
        target: str,
        usernames: List[str]
    ) -> List[Dict]:
        """Password spraying attack simulation"""
        self.logger.progress("Simulating password spray attack...")
        
        spray_results = []
        common_passwords = self.common_passwords[:10]  # Top 10 most common
        
        attempt_count = 0
        
        for password in common_passwords:
            for username in usernames:
                # Check lockout threshold
                if attempt_count >= self.config["lockout_threshold"]:
                    self.logger.warning("Lockout threshold reached, stopping")
                    return spray_results
                
                # Simulate test
                result = await self._simulate_credential_test(
                    target,
                    None,
                    username,
                    password
                )
                
                if result["success"]:
                    spray_results.append({
                        "username": username,
                        "password": password,
                        "method": "password_spray",
                        "severity": "high",
                        "description": f"Weak password found via spray attack"
                    })
                
                attempt_count += 1
                
                # Rate limiting
                await asyncio.sleep(self.config["rate_limit"])
        
        return spray_results
    
    async def test_common_passwords(
        self,
        target: str,
        usernames: List[str]
    ) -> List[Dict]:
        """Test common weak passwords"""
        self.logger.progress("Testing common weak passwords...")
        
        weak_found = []
        passwords_to_test = self.common_passwords[:20]  # Top 20
        
        for username in usernames:
            for password in passwords_to_test:
                # Simulate test
                result = await self._simulate_credential_test(
                    target,
                    None,
                    username,
                    password
                )
                
                if result["success"]:
                    weak_found.append({
                        "username": username,
                        "password": password,
                        "method": "common_password",
                        "severity": "high",
                        "description": f"Common weak password in use"
                    })
                
                # Rate limiting
                await asyncio.sleep(self.config["rate_limit"])
        
        return weak_found
    
    async def _simulate_credential_test(
        self,
        target: str,
        port: Optional[int],
        username: str,
        password: str
    ) -> Dict:
        """
        Simulate credential testing (ethical mode)
        In production, this would attempt actual authentication
        For safety, this is a simulation
        """
        # Simulate network delay
        await asyncio.sleep(0.1)
        
        # Simulate success for demonstration
        # In real implementation, this would use actual authentication
        # For common weak passwords, simulate finding them
        weak_passwords = ["password", "123456", "admin", "default"]
        
        success = password.lower() in weak_passwords
        
        return {
            "success": success,
            "simulated": True,
            "username": username,
            "password": password,
            "target": target,
            "port": port
        }
    
    def _load_default_credentials(self) -> Dict[str, List[Dict]]:
        """Load database of default credentials"""
        return {
            "ssh": [
                {"username": "root", "password": "root"},
                {"username": "admin", "password": "admin"},
            ],
            "ftp": [
                {"username": "ftp", "password": "ftp"},
                {"username": "anonymous", "password": "anonymous"},
            ],
            "mysql": [
                {"username": "root", "password": ""},
                {"username": "root", "password": "root"},
            ],
            "postgresql": [
                {"username": "postgres", "password": "postgres"},
            ],
            "mongodb": [
                {"username": "admin", "password": "admin"},
            ],
            "redis": [
                {"username": "", "password": ""},
            ],
            "http": [
                {"username": "admin", "password": "admin"},
                {"username": "admin", "password": "password"},
            ],
            "telnet": [
                {"username": "admin", "password": "admin"},
            ]
        }
    
    def _load_common_passwords(self) -> List[str]:
        """Load list of common weak passwords"""
        return [
            "password", "123456", "12345678", "qwerty", "abc123",
            "monkey", "1234567", "letmein", "trustno1", "dragon",
            "baseball", "111111", "iloveyou", "master", "sunshine",
            "ashley", "bailey", "passw0rd", "shadow", "123123",
            "654321", "superman", "qazwsx", "michael", "football",
            "welcome", "admin", "default", "root", "toor"
        ]
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if results["default_credentials"]:
            recommendations.append(
                "⚠️ CRITICAL: Change all default credentials immediately"
            )
        
        if results["weak_credentials"]:
            recommendations.append(
                "⚠️ HIGH: Implement strong password policy (min 12 chars, complexity)"
            )
        
        if results["password_spray_results"]:
            recommendations.append(
                "⚠️ HIGH: Enable account lockout after failed login attempts"
            )
        
        recommendations.extend([
            "Enable multi-factor authentication (MFA) for all accounts",
            "Implement password complexity requirements",
            "Use password manager for secure password generation",
            "Regular password rotation policy",
            "Monitor for brute force attempts",
            "Implement CAPTCHA for login forms",
            "Use rate limiting on authentication endpoints",
            "Enable security logging for failed login attempts"
        ])
        
        return recommendations[:10]
