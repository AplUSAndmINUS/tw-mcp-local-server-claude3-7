"""
Plugin System for MCP Server
============================

Provides a flexible plugin architecture for extending server functionality.
"""

import importlib
import inspect
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Callable

from pydantic import BaseModel

from ..config import Settings

logger = logging.getLogger(__name__)


class PluginMetadata(BaseModel):
    """Metadata for a plugin."""
    name: str
    version: str
    description: str
    author: str
    requires: List[str] = []
    enabled: bool = True


class PluginInterface(ABC):
    """Base interface for all plugins."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.metadata = self.get_metadata()
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        pass
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        pass
    
    def is_enabled(self) -> bool:
        """Check if the plugin is enabled."""
        return self.metadata.enabled and self.settings.is_plugin_enabled(self.metadata.name)


class PluginRegistry:
    """Registry for managing plugins."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_routes: Dict[str, List[Callable]] = {}
        self.plugin_hooks: Dict[str, List[Callable]] = {}
    
    async def load_plugins(self) -> None:
        """Load all plugins from the plugins directory."""
        plugins_path = self.settings.get_plugins_path()
        
        if not plugins_path.exists():
            logger.warning(f"Plugins directory not found: {plugins_path}")
            return
        
        logger.info(f"Loading plugins from: {plugins_path}")
        
        for plugin_file in plugins_path.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            try:
                await self._load_plugin_file(plugin_file)
            except Exception as e:
                logger.error(f"Error loading plugin {plugin_file}: {str(e)}")
    
    async def _load_plugin_file(self, plugin_file: Path) -> None:
        """Load a single plugin file."""
        module_name = plugin_file.stem
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        
        if spec is None or spec.loader is None:
            logger.error(f"Could not load plugin spec for {plugin_file}")
            return
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find plugin classes
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, PluginInterface) and 
                obj is not PluginInterface):
                
                try:
                    plugin_instance = obj(self.settings)
                    
                    if plugin_instance.is_enabled():
                        await plugin_instance.initialize()
                        self.plugins[plugin_instance.metadata.name] = plugin_instance
                        logger.info(f"Loaded plugin: {plugin_instance.metadata.name}")
                    else:
                        logger.info(f"Plugin disabled: {plugin_instance.metadata.name}")
                        
                except Exception as e:
                    logger.error(f"Error initializing plugin {name}: {str(e)}")
    
    def register_route(self, plugin_name: str, route_function: Callable) -> None:
        """Register a route for a plugin."""
        if plugin_name not in self.plugin_routes:
            self.plugin_routes[plugin_name] = []
        self.plugin_routes[plugin_name].append(route_function)
    
    def register_hook(self, hook_name: str, hook_function: Callable) -> None:
        """Register a hook function."""
        if hook_name not in self.plugin_hooks:
            self.plugin_hooks[hook_name] = []
        self.plugin_hooks[hook_name].append(hook_function)
    
    async def execute_hooks(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute all hooks for a given hook name."""
        results = []
        
        if hook_name in self.plugin_hooks:
            for hook_function in self.plugin_hooks[hook_name]:
                try:
                    if inspect.iscoroutinefunction(hook_function):
                        result = await hook_function(*args, **kwargs)
                    else:
                        result = hook_function(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error executing hook {hook_name}: {str(e)}")
        
        return results
    
    def get_plugin(self, name: str) -> Optional[PluginInterface]:
        """Get a plugin by name."""
        return self.plugins.get(name)
    
    def get_all_plugins(self) -> Dict[str, PluginInterface]:
        """Get all loaded plugins."""
        return self.plugins.copy()
    
    def get_plugin_routes(self, plugin_name: str) -> List[Callable]:
        """Get routes for a specific plugin."""
        return self.plugin_routes.get(plugin_name, [])
    
    async def shutdown_plugins(self) -> None:
        """Shutdown all plugins."""
        for plugin_name, plugin in self.plugins.items():
            try:
                await plugin.shutdown()
                logger.info(f"Shutdown plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error shutting down plugin {plugin_name}: {str(e)}")


# Decorators for plugin development
def plugin_route(path: str, methods: List[str] = None, **kwargs):
    """Decorator for registering plugin routes."""
    if methods is None:
        methods = ["GET"]
    
    def decorator(func):
        func._plugin_route = {
            "path": path,
            "methods": methods,
            "kwargs": kwargs
        }
        return func
    return decorator


def plugin_hook(hook_name: str):
    """Decorator for registering plugin hooks."""
    def decorator(func):
        func._plugin_hook = hook_name
        return func
    return decorator


def plugin_command(command_name: str, description: str = ""):
    """Decorator for registering plugin CLI commands."""
    def decorator(func):
        func._plugin_command = {
            "name": command_name,
            "description": description
        }
        return func
    return decorator