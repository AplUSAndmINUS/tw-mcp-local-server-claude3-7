"""
Hybrid Computing Manager
=======================

Manages the decision-making process between local and Azure cloud computing
resources, prioritizing local execution when possible.
"""

import asyncio
import logging
import psutil
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Awaitable
from pathlib import Path

import structlog
from pydantic import BaseModel

from .config import Settings

logger = structlog.get_logger(__name__)


class ComputeLocation(Enum):
    """Available compute locations."""
    LOCAL = "local"
    AZURE = "azure"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ResourceType(Enum):
    """Types of resources that can be monitored."""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    GPU = "gpu"
    NETWORK = "network"


@dataclass
class SystemResources:
    """System resource utilization data."""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    gpu_percent: float = 0.0
    network_io: float = 0.0
    timestamp: float = 0.0


@dataclass
class TaskDefinition:
    """Definition of a computational task."""
    name: str
    priority: TaskPriority
    estimated_cpu: float  # 0.0 to 1.0
    estimated_memory: float  # 0.0 to 1.0
    estimated_duration: float  # seconds
    requires_gpu: bool = False
    requires_network: bool = False
    can_run_on_azure: bool = True
    azure_function_name: Optional[str] = None


class ComputeDecision(BaseModel):
    """Decision about where to execute a task."""
    location: ComputeLocation
    reasoning: str
    confidence: float  # 0.0 to 1.0
    estimated_cost: float
    estimated_duration: float
    alternative_location: Optional[ComputeLocation] = None


class HybridComputeManager:
    """
    Manages hybrid computing decisions between local and Azure resources.
    
    This class monitors system resources and makes intelligent decisions about
    where to execute tasks based on:
    - Current system utilization
    - Task requirements
    - Azure availability and cost
    - User preferences
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.resource_history: List[SystemResources] = []
        self.running_tasks: Dict[str, TaskDefinition] = {}
        self.azure_available = False
        self.azure_client = None
        
        # Thresholds for local execution
        self.local_thresholds = {
            "cpu_max": 0.8,  # 80% CPU usage
            "memory_max": 0.85,  # 85% memory usage
            "disk_max": 0.9,  # 90% disk usage
            "gpu_max": 0.9,  # 90% GPU usage
        }
        
        # Initialize Azure client if enabled
        if self._should_enable_azure():
            self._initialize_azure_client()
    
    def _should_enable_azure(self) -> bool:
        """Check if Azure integration should be enabled."""
        return (
            hasattr(self.settings, 'azure_enabled') and 
            self.settings.azure_enabled and
            hasattr(self.settings, 'azure_subscription_id') and
            self.settings.azure_subscription_id
        )
    
    def _initialize_azure_client(self) -> None:
        """Initialize Azure client for cloud computing."""
        try:
            # This would be implemented with actual Azure SDK
            # For now, we'll simulate Azure availability
            self.azure_available = True
            logger.info("Azure integration enabled")
        except Exception as e:
            logger.error(f"Failed to initialize Azure client: {e}")
            self.azure_available = False
    
    async def get_current_resources(self) -> SystemResources:
        """Get current system resource utilization."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent / 100.0
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent / 100.0
            
            # GPU usage (if available)
            gpu_percent = 0.0
            if self.settings.gpu_enabled:
                gpu_percent = await self._get_gpu_usage()
            
            # Network I/O
            network_io = 0.0
            if hasattr(psutil, 'net_io_counters'):
                net_io = psutil.net_io_counters()
                network_io = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024  # MB
            
            resources = SystemResources(
                cpu_percent=cpu_percent / 100.0,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                gpu_percent=gpu_percent,
                network_io=network_io,
                timestamp=time.time()
            )
            
            # Keep history for trend analysis
            self.resource_history.append(resources)
            if len(self.resource_history) > 100:  # Keep last 100 readings
                self.resource_history.pop(0)
            
            return resources
            
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            # Return safe defaults
            return SystemResources(
                cpu_percent=0.5,
                memory_percent=0.5,
                disk_percent=0.5,
                timestamp=time.time()
            )
    
    async def _get_gpu_usage(self) -> float:
        """Get GPU utilization if available."""
        try:
            # This would use nvidia-ml-py or similar
            # For now, simulate GPU usage
            return 0.0
        except Exception:
            return 0.0
    
    async def decide_execution_location(self, task: TaskDefinition) -> ComputeDecision:
        """
        Decide where to execute a task based on current resources and requirements.
        
        Args:
            task: The task to be executed
            
        Returns:
            ComputeDecision with location and reasoning
        """
        current_resources = await self.get_current_resources()
        
        # Check if task can run locally
        local_feasible = self._can_run_locally(task, current_resources)
        
        # Check if Azure is available and can run the task
        azure_feasible = self.azure_available and task.can_run_on_azure
        
        # Make decision based on feasibility and preferences
        if local_feasible and not self._should_prefer_azure(task, current_resources):
            return ComputeDecision(
                location=ComputeLocation.LOCAL,
                reasoning=f"Local execution preferred - sufficient resources available (CPU: {current_resources.cpu_percent:.1%}, Memory: {current_resources.memory_percent:.1%})",
                confidence=self._calculate_local_confidence(current_resources),
                estimated_cost=0.0,
                estimated_duration=task.estimated_duration,
                alternative_location=ComputeLocation.AZURE if azure_feasible else None
            )
        
        elif azure_feasible:
            return ComputeDecision(
                location=ComputeLocation.AZURE,
                reasoning=f"Azure execution chosen - {'local resources insufficient' if not local_feasible else 'better suited for task requirements'}",
                confidence=0.8,
                estimated_cost=self._estimate_azure_cost(task),
                estimated_duration=task.estimated_duration * 1.2,  # Account for network overhead
                alternative_location=ComputeLocation.LOCAL if local_feasible else None
            )
        
        else:
            # Fallback to local even if resources are constrained
            return ComputeDecision(
                location=ComputeLocation.LOCAL,
                reasoning="Local execution as fallback - Azure not available",
                confidence=0.4,
                estimated_cost=0.0,
                estimated_duration=task.estimated_duration * 1.5,  # May be slower
                alternative_location=None
            )
    
    def _can_run_locally(self, task: TaskDefinition, resources: SystemResources) -> bool:
        """Check if task can run locally given current resources."""
        # Check CPU availability
        if resources.cpu_percent + task.estimated_cpu > self.local_thresholds["cpu_max"]:
            return False
        
        # Check memory availability
        if resources.memory_percent + task.estimated_memory > self.local_thresholds["memory_max"]:
            return False
        
        # Check GPU requirements
        if task.requires_gpu and not self.settings.gpu_enabled:
            return False
        
        if task.requires_gpu and resources.gpu_percent > self.local_thresholds["gpu_max"]:
            return False
        
        return True
    
    def _should_prefer_azure(self, task: TaskDefinition, resources: SystemResources) -> bool:
        """Determine if Azure should be preferred over local execution."""
        # High priority tasks with high resource requirements
        if task.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]:
            if task.estimated_cpu > 0.6 or task.estimated_memory > 0.6:
                return True
        
        # Long-running tasks might benefit from Azure
        if task.estimated_duration > 300:  # 5 minutes
            return True
        
        # System under heavy load
        if resources.cpu_percent > 0.7 or resources.memory_percent > 0.7:
            return True
        
        return False
    
    def _calculate_local_confidence(self, resources: SystemResources) -> float:
        """Calculate confidence level for local execution."""
        # Higher confidence when resources are more available
        cpu_confidence = 1.0 - resources.cpu_percent
        memory_confidence = 1.0 - resources.memory_percent
        
        # Average confidence with some weighting
        confidence = (cpu_confidence * 0.4 + memory_confidence * 0.4 + 0.2)
        
        return min(0.95, max(0.1, confidence))
    
    def _estimate_azure_cost(self, task: TaskDefinition) -> float:
        """Estimate cost of running task on Azure."""
        # Simple cost estimation based on task complexity
        base_cost = 0.01  # Base cost per execution
        
        # Factor in CPU and memory requirements
        resource_cost = (task.estimated_cpu + task.estimated_memory) * 0.005
        
        # Factor in duration
        duration_cost = task.estimated_duration * 0.001
        
        return base_cost + resource_cost + duration_cost
    
    async def execute_task(self, task: TaskDefinition, task_function: Callable, **kwargs) -> Any:
        """
        Execute a task based on the decided location.
        
        Args:
            task: Task definition
            task_function: Function to execute
            **kwargs: Additional arguments for the task function
            
        Returns:
            Result of the task execution
        """
        decision = await self.decide_execution_location(task)
        
        logger.info(
            f"Executing task '{task.name}' on {decision.location.value}",
            task_name=task.name,
            location=decision.location.value,
            reasoning=decision.reasoning,
            confidence=decision.confidence
        )
        
        # Track running task
        task_id = f"{task.name}_{int(time.time())}"
        self.running_tasks[task_id] = task
        
        try:
            if decision.location == ComputeLocation.LOCAL:
                result = await self._execute_local(task_function, **kwargs)
            else:
                result = await self._execute_azure(task, task_function, **kwargs)
            
            logger.info(f"Task '{task.name}' completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Task '{task.name}' failed: {e}")
            
            # Try alternative location if available
            if decision.alternative_location:
                logger.info(f"Retrying task '{task.name}' on {decision.alternative_location.value}")
                if decision.alternative_location == ComputeLocation.LOCAL:
                    result = await self._execute_local(task_function, **kwargs)
                else:
                    result = await self._execute_azure(task, task_function, **kwargs)
                return result
            
            raise
            
        finally:
            # Remove from running tasks
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
    
    async def _execute_local(self, task_function: Callable, **kwargs) -> Any:
        """Execute task locally."""
        if asyncio.iscoroutinefunction(task_function):
            return await task_function(**kwargs)
        else:
            return task_function(**kwargs)
    
    async def _execute_azure(self, task: TaskDefinition, task_function: Callable, **kwargs) -> Any:
        """Execute task on Azure."""
        # This would implement actual Azure Functions execution
        # For now, simulate Azure execution with local fallback
        logger.info(f"Simulating Azure execution for task '{task.name}'")
        
        # Add some delay to simulate network overhead
        await asyncio.sleep(0.1)
        
        # Execute locally as fallback
        return await self._execute_local(task_function, **kwargs)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and resource utilization."""
        current_resources = await self.get_current_resources()
        
        return {
            "resources": {
                "cpu_percent": current_resources.cpu_percent,
                "memory_percent": current_resources.memory_percent,
                "disk_percent": current_resources.disk_percent,
                "gpu_percent": current_resources.gpu_percent,
                "network_io": current_resources.network_io,
            },
            "thresholds": self.local_thresholds,
            "azure_available": self.azure_available,
            "running_tasks": len(self.running_tasks),
            "task_history": len(self.resource_history),
            "local_preferred": current_resources.cpu_percent < 0.7 and current_resources.memory_percent < 0.7,
        }
    
    async def optimize_for_windows(self) -> None:
        """Apply Windows-specific optimizations."""
        try:
            # Windows-specific resource monitoring
            if hasattr(psutil, 'win_service_iter'):
                # Monitor Windows services that might affect performance
                pass
            
            # Adjust thresholds for Windows
            self.local_thresholds["memory_max"] = 0.8  # Windows typically uses more memory
            
            logger.info("Applied Windows-specific optimizations")
            
        except Exception as e:
            logger.error(f"Error applying Windows optimizations: {e}")


def create_hybrid_compute_manager(settings: Settings) -> HybridComputeManager:
    """Create a hybrid compute manager instance."""
    return HybridComputeManager(settings)