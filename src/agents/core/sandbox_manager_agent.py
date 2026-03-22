"""
Sandbox Manager Agent
Docker-based isolated environment management
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

from src.agents.base_agent import BaseAgent


class SandboxManagerAgent(BaseAgent):
    """
    Sandbox Manager Agent
    
    Capabilities:
    - Docker container management
    - Isolated environment creation
    - Resource allocation
    - Network isolation
    - Automatic cleanup
    - Security controls
    - Multi-sandbox orchestration
    """
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__("sandbox_manager", config)
        self.default_config = {
            "timeout": 300,
            "max_sandboxes": 10,
            "default_memory_limit": "512m",
            "default_cpu_limit": 1.0,
            "network_isolation": True,
            "auto_cleanup": True,
            "cleanup_timeout": 3600,  # 1 hour
            "use_docker": True
        }
        self.config = {**self.default_config, **(config or {})}
        
        # Track active sandboxes
        self.active_sandboxes = {}
    
    async def execute(self, target: str, options: Optional[Dict] = None) -> Dict:
        """Execute sandbox management operation"""
        
        operation = options.get("operation", "create") if options else "create"
        
        self.logger.progress(f"Sandbox operation: {operation}")
        
        if operation == "create":
            return await self.create_sandbox(target, options)
        elif operation == "destroy":
            sandbox_id = options.get("sandbox_id") if options else None
            return await self.destroy_sandbox(sandbox_id)
        elif operation == "list":
            return await self.list_sandboxes()
        elif operation == "cleanup":
            return await self.cleanup_old_sandboxes()
        else:
            return {"error": f"Unknown operation: {operation}"}
    
    async def create_sandbox(self, target: str, options: Optional[Dict] = None) -> Dict:
        """Create isolated sandbox environment"""
        
        self.logger.progress(f"Creating sandbox for {target}...")
        
        # Check sandbox limit
        if len(self.active_sandboxes) >= self.config["max_sandboxes"]:
            return {
                "error": "Maximum sandbox limit reached",
                "max_sandboxes": self.config["max_sandboxes"]
            }
        
        # Generate sandbox ID
        sandbox_id = self._generate_sandbox_id(target)
        
        # Configure sandbox
        sandbox_config = {
            "sandbox_id": sandbox_id,
            "target": target,
            "created_at": datetime.utcnow().isoformat(),
            "status": "creating",
            "resources": {
                "memory_limit": options.get("memory_limit", self.config["default_memory_limit"]) if options else self.config["default_memory_limit"],
                "cpu_limit": options.get("cpu_limit", self.config["default_cpu_limit"]) if options else self.config["default_cpu_limit"]
            },
            "network": {
                "isolated": self.config["network_isolation"],
                "internal_ip": None,
                "exposed_ports": []
            },
            "security": {
                "read_only_root": True,
                "no_new_privileges": True,
                "drop_capabilities": ["ALL"]
            }
        }
        
        # Create Docker container (simulated)
        container_info = await self._create_docker_container(sandbox_config)
        
        sandbox_config["container_id"] = container_info["container_id"]
        sandbox_config["status"] = "running"
        sandbox_config["network"]["internal_ip"] = container_info["ip_address"]
        
        # Store sandbox info
        self.active_sandboxes[sandbox_id] = sandbox_config
        
        self.logger.success(f"Sandbox created: {sandbox_id}")
        
        return {
            "sandbox_id": sandbox_id,
            "status": "running",
            "container_id": container_info["container_id"],
            "ip_address": container_info["ip_address"],
            "resources": sandbox_config["resources"],
            "created_at": sandbox_config["created_at"]
        }
    
    async def destroy_sandbox(self, sandbox_id: str) -> Dict:
        """Destroy sandbox environment"""
        
        if not sandbox_id:
            return {"error": "Sandbox ID required"}
        
        if sandbox_id not in self.active_sandboxes:
            return {"error": f"Sandbox not found: {sandbox_id}"}
        
        self.logger.progress(f"Destroying sandbox: {sandbox_id}")
        
        sandbox = self.active_sandboxes[sandbox_id]
        
        # Stop and remove container
        await self._destroy_docker_container(sandbox["container_id"])
        
        # Remove from active sandboxes
        del self.active_sandboxes[sandbox_id]
        
        self.logger.success(f"Sandbox destroyed: {sandbox_id}")
        
        return {
            "sandbox_id": sandbox_id,
            "status": "destroyed",
            "destroyed_at": datetime.utcnow().isoformat()
        }
    
    async def list_sandboxes(self) -> Dict:
        """List all active sandboxes"""
        
        sandboxes = []
        
        for sandbox_id, sandbox in self.active_sandboxes.items():
            sandboxes.append({
                "sandbox_id": sandbox_id,
                "target": sandbox["target"],
                "status": sandbox["status"],
                "created_at": sandbox["created_at"],
                "container_id": sandbox.get("container_id"),
                "ip_address": sandbox.get("network", {}).get("internal_ip")
            })
        
        return {
            "total_sandboxes": len(sandboxes),
            "sandboxes": sandboxes
        }
    
    async def cleanup_old_sandboxes(self) -> Dict:
        """Cleanup old/stale sandboxes"""
        
        self.logger.progress("Cleaning up old sandboxes...")
        
        cleaned = []
        current_time = datetime.utcnow()
        
        for sandbox_id, sandbox in list(self.active_sandboxes.items()):
            created_at = datetime.fromisoformat(sandbox["created_at"])
            age_seconds = (current_time - created_at).total_seconds()
            
            if age_seconds > self.config["cleanup_timeout"]:
                await self.destroy_sandbox(sandbox_id)
                cleaned.append(sandbox_id)
        
        self.logger.success(f"Cleaned up {len(cleaned)} sandboxes")
        
        return {
            "cleaned_count": len(cleaned),
            "cleaned_sandboxes": cleaned
        }
    
    def _generate_sandbox_id(self, target: str) -> str:
        """Generate unique sandbox ID"""
        data = f"{target}{datetime.utcnow()}"
        hash_id = hashlib.md5(data.encode()).hexdigest()[:8]
        return f"sandbox-{hash_id}"
    
    async def _create_docker_container(self, config: Dict) -> Dict:
        """Create Docker container (simulated)"""
        
        # In production, this would use Docker SDK
        # docker.from_env().containers.run(...)
        
        self.logger.progress("Creating Docker container...")
        
        # Simulate container creation
        await asyncio.sleep(0.5)
        
        container_id = f"container-{config['sandbox_id']}"
        ip_address = f"172.17.0.{len(self.active_sandboxes) + 2}"
        
        return {
            "container_id": container_id,
            "ip_address": ip_address,
            "status": "running"
        }
    
    async def _destroy_docker_container(self, container_id: str):
        """Destroy Docker container (simulated)"""
        
        # In production, this would use Docker SDK
        # container.stop()
        # container.remove()
        
        self.logger.progress(f"Destroying container: {container_id}")
        
        # Simulate container destruction
        await asyncio.sleep(0.3)
    
    async def execute_in_sandbox(
        self,
        sandbox_id: str,
        command: str
    ) -> Dict:
        """Execute command in sandbox"""
        
        if sandbox_id not in self.active_sandboxes:
            return {"error": f"Sandbox not found: {sandbox_id}"}
        
        self.logger.progress(f"Executing in sandbox {sandbox_id}: {command}")
        
        # In production, this would use Docker SDK
        # container.exec_run(command)
        
        # Simulate command execution
        await asyncio.sleep(0.2)
        
        return {
            "sandbox_id": sandbox_id,
            "command": command,
            "exit_code": 0,
            "output": "Command executed successfully (simulated)"
        }
    
    async def get_sandbox_logs(self, sandbox_id: str) -> Dict:
        """Get sandbox logs"""
        
        if sandbox_id not in self.active_sandboxes:
            return {"error": f"Sandbox not found: {sandbox_id}"}
        
        # In production, this would fetch actual container logs
        
        return {
            "sandbox_id": sandbox_id,
            "logs": [
                "Sandbox initialized",
                "Security controls applied",
                "Network isolation enabled",
                "Ready for operations"
            ]
        }
    
    async def get_sandbox_stats(self, sandbox_id: str) -> Dict:
        """Get sandbox resource usage stats"""
        
        if sandbox_id not in self.active_sandboxes:
            return {"error": f"Sandbox not found: {sandbox_id}"}
        
        # In production, this would fetch actual container stats
        
        return {
            "sandbox_id": sandbox_id,
            "cpu_usage": "15%",
            "memory_usage": "128MB / 512MB",
            "network_io": {
                "rx_bytes": 1024,
                "tx_bytes": 2048
            },
            "disk_io": {
                "read_bytes": 4096,
                "write_bytes": 8192
            }
        }
