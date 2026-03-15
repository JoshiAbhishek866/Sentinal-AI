"""
Base Agent Class
Foundation for all offensive and defensive agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

from src.utils.logger import AgentLogger
from src.utils.helpers import generate_id, format_result


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_type: str, config: Optional[Dict] = None):
        self.agent_type = agent_type
        self.config = config or {}
        self.logger = AgentLogger(agent_type)
        self.status = "idle"
        self.current_execution_id = None
    
    @abstractmethod
    async def execute(self, target: str, options: Optional[Dict] = None) -> Dict:
        """
        Execute the agent
        Must be implemented by subclasses
        
        Args:
            target: Target to scan/analyze
            options: Additional options for execution
        
        Returns:
            Dict containing execution results
        """
        pass
    
    async def run(self, target: str, options: Optional[Dict] = None) -> Dict:
        """
        Run the agent with error handling, timeout, and logging.
        
        Args:
            target: Target to scan/analyze
            options: Additional options
        
        Returns:
            Formatted result dictionary
        """
        self.current_execution_id = generate_id(self.agent_type)
        self.status = "running"
        start_time = datetime.utcnow()
        timeout = self.config.get("timeout", 300)  # default 5 min
        
        self.logger.start(target)
        
        try:
            # Execute the agent with a hard timeout
            result_data = await asyncio.wait_for(
                self.execute(target, options),
                timeout=timeout
            )
            
            # Calculate duration
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.complete(duration)
            
            # Format result
            result = format_result(
                agent_type=self.agent_type,
                target=target,
                data={
                    **result_data,
                    "duration": duration,
                    "execution_id": self.current_execution_id
                },
                status="success"
            )
            
            self.status = "completed"
            return result
        
        except asyncio.TimeoutError:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.error(f"Execution timed out after {timeout}s")
            
            result = format_result(
                agent_type=self.agent_type,
                target=target,
                data={
                    "error": f"Agent timed out after {timeout} seconds",
                    "duration": duration,
                    "execution_id": self.current_execution_id
                },
                status="timeout"
            )
            self.status = "timeout"
            return result
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.error(f"Execution failed: {str(e)}")
            
            # Format error result
            result = format_result(
                agent_type=self.agent_type,
                target=target,
                data={
                    "error": str(e),
                    "duration": duration,
                    "execution_id": self.current_execution_id
                },
                status="failed"
            )
            
            self.status = "failed"
            return result
    
    def get_status(self) -> Dict:
        """Get current agent status"""
        return {
            "agent_type": self.agent_type,
            "status": self.status,
            "execution_id": self.current_execution_id,
            "config": self.config
        }
    
    async def validate_target(self, target: str) -> bool:
        """Validate target before execution"""
        from src.utils.helpers import validate_target
        return validate_target(target)
    
    def update_config(self, config: Dict):
        """Update agent configuration"""
        self.config.update(config)
        self.logger.logger.info(f"Configuration updated: {config}")
