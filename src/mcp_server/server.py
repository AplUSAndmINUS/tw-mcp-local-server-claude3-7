"""
Main MCP Server Implementation
=============================

FastAPI-based server with Claude Sonnet 3.7 integration and plugin support.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any

import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from .config import Settings, load_settings
from .claude_client import ClaudeClient, ClaudeResponse
from .plugins import PluginRegistry
from .hybrid_compute import HybridComputeManager
from .azure_integration import AzureIntegration

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


# Request/Response Models
class CompletionRequest(BaseModel):
    """Request model for completions."""
    prompt: str
    system_prompt: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: bool = False


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Request model for chat."""
    messages: List[ChatMessage]
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class CodeAnalysisRequest(BaseModel):
    """Request model for code analysis."""
    code: str
    language: str = "python"
    task: str = "analyze"
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class VibeCodeRequest(BaseModel):
    """Request model for vibe coding."""
    request: str
    context: Optional[Dict[str, Any]] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: float
    version: str
    claude_status: bool
    plugins_loaded: int


class MCPServer:
    """Main MCP Server class."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or load_settings()
        self.claude_client = ClaudeClient(self.settings)
        self.plugin_registry = PluginRegistry(self.settings)
        self.hybrid_compute = HybridComputeManager(self.settings)
        self.azure_integration = AzureIntegration(self.settings) if self.settings.azure_enabled else None
        self.app = self._create_app()
        
        # Rate limiting storage (in production, use Redis or similar)
        self.rate_limit_storage: Dict[str, List[float]] = {}
    
    def _create_app(self) -> FastAPI:
        """Create and configure the FastAPI application."""
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            """Application lifespan manager."""
            # Startup
            logger.info("Starting MCP Server...")
            await self.plugin_registry.load_plugins()
            
            # Initialize hybrid computing
            if self.settings.hybrid_computing_enabled:
                await self.hybrid_compute.get_current_resources()
                logger.info("Hybrid computing initialized")
            
            # Initialize Azure integration
            if self.azure_integration:
                await self.azure_integration.authenticate()
                logger.info("Azure integration initialized")
            
            # Apply Windows optimizations if enabled
            if self.settings.windows_optimizations:
                await self.hybrid_compute.optimize_for_windows()
                logger.info("Windows optimizations applied")
            
            logger.info("MCP Server started successfully")
            
            yield
            
            # Shutdown
            logger.info("Shutting down MCP Server...")
            await self.plugin_registry.shutdown_plugins()
            
            # Cleanup Azure integration
            if self.azure_integration:
                await self.azure_integration.cleanup_resources()
                logger.info("Azure integration cleaned up")
            
            logger.info("MCP Server shutdown complete")
        
        app = FastAPI(
            title="TW MCP Local Server - Claude 3.7",
            description="Python MCP server with Claude Sonnet 3.7 integration",
            version="0.1.0",
            docs_url="/docs" if self.settings.debug else None,
            redoc_url="/redoc" if self.settings.debug else None,
            lifespan=lifespan
        )
        
        # Add middleware
        app.add_middleware(
            CORSMiddleware,
            **self.settings.get_cors_config()
        )
        
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"] if self.settings.debug else [self.settings.host]
        )
        
        # Add custom middleware
        app.middleware("http")(self._rate_limit_middleware)
        app.middleware("http")(self._logging_middleware)
        
        # Register routes
        self._register_routes(app)
        
        return app
    
    def _register_routes(self, app: FastAPI) -> None:
        """Register all routes."""
        
        @app.get("/health", response_model=HealthResponse)
        async def health_check():
            """Health check endpoint."""
            claude_status = await self.claude_client.health_check()
            
            return HealthResponse(
                status="healthy" if claude_status else "degraded",
                timestamp=time.time(),
                version="0.1.0",
                claude_status=claude_status,
                plugins_loaded=len(self.plugin_registry.get_all_plugins())
            )
        
        @app.post("/complete", response_model=ClaudeResponse)
        async def complete(request: CompletionRequest):
            """Complete a prompt using Claude."""
            try:
                response = await self.claude_client.complete(
                    prompt=request.prompt,
                    system_prompt=request.system_prompt,
                    context=request.context,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    stream=request.stream
                )
                
                if request.stream:
                    return StreamingResponse(
                        response,
                        media_type="text/plain"
                    )
                
                return response
                
            except Exception as e:
                logger.error(f"Error in completion: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/chat", response_model=ClaudeResponse)
        async def chat(request: ChatRequest):
            """Chat with Claude using conversation history."""
            try:
                messages = [
                    {"role": msg.role, "content": msg.content}
                    for msg in request.messages
                ]
                
                response = await self.claude_client.chat(
                    messages=messages,
                    system_prompt=request.system_prompt,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error in chat: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/analyze-code", response_model=ClaudeResponse)
        async def analyze_code(request: CodeAnalysisRequest):
            """Analyze code using Claude."""
            try:
                response = await self.claude_client.analyze_code(
                    code=request.code,
                    language=request.language,
                    task=request.task,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error in code analysis: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/vibe-code", response_model=ClaudeResponse)
        async def vibe_code(request: VibeCodeRequest):
            """Generate code with vibe coding approach."""
            try:
                response = await self.claude_client.vibe_code(
                    request=request.request,
                    context=request.context,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error in vibe coding: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/plugins")
        async def list_plugins():
            """List all loaded plugins."""
            plugins = self.plugin_registry.get_all_plugins()
            return {
                "plugins": [
                    {
                        "name": plugin.metadata.name,
                        "version": plugin.metadata.version,
                        "description": plugin.metadata.description,
                        "author": plugin.metadata.author,
                        "enabled": plugin.is_enabled()
                    }
                    for plugin in plugins.values()
                ]
            }
        
        @app.get("/settings")
        async def get_settings():
            """Get server settings (excluding sensitive data)."""
            return {
                "host": self.settings.host,
                "port": self.settings.port,
                "debug": self.settings.debug,
                "claude_model": self.settings.claude_model,
                "max_tokens": self.settings.max_tokens,
                "temperature": self.settings.temperature,
                "enabled_plugins": self.settings.enabled_plugins,
                "log_level": self.settings.log_level,
                "hybrid_computing_enabled": self.settings.hybrid_computing_enabled,
                "azure_enabled": self.settings.azure_enabled,
                "windows_optimizations": self.settings.windows_optimizations,
                "mcp_modules_enabled": self.settings.mcp_modules_enabled,
            }
        
        @app.get("/system/status")
        async def get_system_status():
            """Get comprehensive system status."""
            try:
                # Get hybrid computing status
                hybrid_status = await self.hybrid_compute.get_system_status()
                
                # Get Azure status if enabled
                azure_status = {}
                if self.azure_integration:
                    azure_status = await self.azure_integration.get_service_status()
                
                # Get plugin status
                plugin_status = {
                    "loaded_plugins": len(self.plugin_registry.get_all_plugins()),
                    "active_plugins": [
                        plugin.metadata.name for plugin in self.plugin_registry.get_all_plugins().values()
                        if plugin.is_enabled()
                    ]
                }
                
                return {
                    "server_status": "running",
                    "hybrid_computing": hybrid_status,
                    "azure_integration": azure_status,
                    "plugins": plugin_status,
                    "timestamp": time.time()
                }
                
            except Exception as e:
                logger.error(f"Error getting system status: {e}")
                return {
                    "server_status": "error",
                    "error": str(e),
                    "timestamp": time.time()
                }
        
        @app.post("/system/optimize")
        async def optimize_system():
            """Trigger system optimization."""
            try:
                # Apply Windows optimizations
                if self.settings.windows_optimizations:
                    await self.hybrid_compute.optimize_for_windows()
                
                # Update resource thresholds based on current usage
                current_resources = await self.hybrid_compute.get_current_resources()
                
                return {
                    "message": "System optimization completed",
                    "current_resources": {
                        "cpu_percent": current_resources.cpu_percent,
                        "memory_percent": current_resources.memory_percent,
                        "gpu_percent": current_resources.gpu_percent,
                    },
                    "timestamp": time.time()
                }
                
            except Exception as e:
                logger.error(f"Error optimizing system: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def _rate_limit_middleware(self, request: Request, call_next) -> Response:
        """Rate limiting middleware."""
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old entries
        if client_ip in self.rate_limit_storage:
            self.rate_limit_storage[client_ip] = [
                timestamp for timestamp in self.rate_limit_storage[client_ip]
                if current_time - timestamp < self.settings.rate_limit_window
            ]
        else:
            self.rate_limit_storage[client_ip] = []
        
        # Check rate limit
        if len(self.rate_limit_storage[client_ip]) >= self.settings.rate_limit_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )
        
        # Add current request
        self.rate_limit_storage[client_ip].append(current_time)
        
        response = await call_next(request)
        return response
    
    async def _logging_middleware(self, request: Request, call_next) -> Response:
        """Logging middleware."""
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host
        )
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            process_time=process_time
        )
        
        return response
    
    def run(self) -> None:
        """Run the server."""
        uvicorn.run(
            self.app,
            host=self.settings.host,
            port=self.settings.port,
            reload=self.settings.reload,
            log_level=self.settings.log_level.lower()
        )
    
    async def start(self) -> None:
        """Start the server programmatically."""
        config = uvicorn.Config(
            self.app,
            host=self.settings.host,
            port=self.settings.port,
            log_level=self.settings.log_level.lower()
        )
        server = uvicorn.Server(config)
        await server.serve()


def create_server(settings: Optional[Settings] = None) -> MCPServer:
    """Create a new MCP server instance."""
    return MCPServer(settings)


if __name__ == "__main__":
    server = create_server()
    server.run()