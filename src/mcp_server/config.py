"""
Configuration Management for MCP Server
=======================================

Handles configuration loading from environment variables and config files.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the MCP server."""
    
    # Server Configuration
    host: str = Field(default="localhost", description="Server host address")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Enable debug mode")
    reload: bool = Field(default=False, description="Enable auto-reload")
    
    # Claude API Configuration
    anthropic_api_key: str = Field(description="Anthropic API key for Claude")
    claude_model: str = Field(default="claude-3-sonnet-20240229", description="Claude model to use")
    max_tokens: int = Field(default=4096, description="Maximum tokens for Claude responses")
    temperature: float = Field(default=0.7, description="Temperature for Claude responses")
    
    # Local Processing Configuration
    enable_local_processing: bool = Field(default=True, description="Enable local CPU/GPU processing")
    local_model_path: Optional[str] = Field(default=None, description="Path to local model files")
    gpu_enabled: bool = Field(default=False, description="Enable GPU processing")
    max_local_memory: int = Field(default=8192, description="Maximum memory for local processing (MB)")
    
    # Plugin Configuration
    plugins_directory: str = Field(default="plugins", description="Directory containing plugins")
    enabled_plugins: List[str] = Field(
        default_factory=lambda: [
            "vibe_coder", "brainstorm", "mindmap", "perspective_shift", "creativity_surge",
            "image_seed", "palette_gen", "render_style", "sketch_flow",
            "motion_branding", "vibe_fade", "loop_craft", "tempo_sync",
            "llm_dictation", "api_testbed", "query_refine", "agent_weave",
            "writing_muse", "composition_sculpt", "edit_pass", "persona_writer",
            "tone_builder", "beat_vibe", "soundscape", "voiceflow",
            "voice_capture", "intent_echo", "speech_craft", "command_stream"
        ], 
        description="List of enabled plugins"
    )
    
    # Security Configuration
    secret_key: str = Field(default="your-secret-key-change-this", description="Secret key for JWT tokens")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration time")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")
    
    # CORS Configuration
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8080"],
        description="CORS allowed origins"
    )
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per minute")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")
    
    # Hybrid Computing Configuration
    hybrid_computing_enabled: bool = Field(default=True, description="Enable hybrid local/cloud computing")
    prefer_local_execution: bool = Field(default=True, description="Prefer local execution when possible")
    local_cpu_threshold: float = Field(default=0.8, description="CPU threshold for local execution")
    local_memory_threshold: float = Field(default=0.85, description="Memory threshold for local execution")
    
    # Azure Cloud Configuration
    azure_enabled: bool = Field(default=False, description="Enable Azure cloud integration")
    azure_subscription_id: Optional[str] = Field(default=None, description="Azure subscription ID")
    azure_tenant_id: Optional[str] = Field(default=None, description="Azure tenant ID")
    azure_client_id: Optional[str] = Field(default=None, description="Azure client ID")
    azure_client_secret: Optional[str] = Field(default=None, description="Azure client secret")
    azure_resource_group: str = Field(default="mcp-resources", description="Azure resource group")
    azure_functions_key: Optional[str] = Field(default=None, description="Azure Functions key")
    
    # Windows-specific Configuration
    windows_optimizations: bool = Field(default=True, description="Enable Windows-specific optimizations")
    windows_service_mode: bool = Field(default=False, description="Run as Windows service")
    windows_gpu_priority: bool = Field(default=True, description="Prioritize GPU usage on Windows")
    
    # MCP Module Configuration
    mcp_modules_enabled: bool = Field(default=True, description="Enable MCP modules")
    mcp_ideation_enabled: bool = Field(default=True, description="Enable ideation modules")
    mcp_visual_enabled: bool = Field(default=True, description="Enable visual generation modules")
    mcp_animation_enabled: bool = Field(default=True, description="Enable animation modules")
    mcp_audio_enabled: bool = Field(default=True, description="Enable audio modules")
    mcp_voice_enabled: bool = Field(default=True, description="Enable voice modules")
    mcp_writing_enabled: bool = Field(default=True, description="Enable writing modules")
    mcp_testing_enabled: bool = Field(default=True, description="Enable testing modules")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    @field_validator("anthropic_api_key")
    @classmethod
    def validate_api_key(cls, v):
        if not v or v == "your-anthropic-api-key":
            raise ValueError("Anthropic API key must be provided")
        return v
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0")
        return v
    
    @field_validator("max_tokens")
    @classmethod
    def validate_max_tokens(cls, v):
        if v < 1 or v > 200000:
            raise ValueError("Max tokens must be between 1 and 200000")
        return v
    
    def get_plugins_path(self) -> Path:
        """Get the full path to the plugins directory."""
        return Path(self.plugins_directory).resolve()
    
    def is_plugin_enabled(self, plugin_name: str) -> bool:
        """Check if a plugin is enabled."""
        return plugin_name in self.enabled_plugins
    
    def get_cors_config(self) -> Dict[str, Any]:
        """Get CORS configuration for FastAPI."""
        return {
            "allow_origins": self.cors_origins,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }


def load_settings() -> Settings:
    """Load settings from environment variables and config files."""
    return Settings()


def create_default_config_file(path: str = ".env") -> None:
    """Create a default configuration file."""
    config_template = """# MCP Server Configuration
# Copy this file to .env and update the values

# Server Configuration
HOST=localhost
PORT=8000
DEBUG=false
RELOAD=false

# Claude API Configuration
ANTHROPIC_API_KEY=your-anthropic-api-key-here
CLAUDE_MODEL=claude-3-sonnet-20240229
MAX_TOKENS=4096
TEMPERATURE=0.7

# Local Processing Configuration
ENABLE_LOCAL_PROCESSING=true
GPU_ENABLED=false
MAX_LOCAL_MEMORY=8192

# Plugin Configuration
PLUGINS_DIRECTORY=plugins
ENABLED_PLUGINS=["vibe_coder"]

# Security Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging Configuration
LOG_LEVEL=INFO
# LOG_FILE=mcp_server.log

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
"""
    
    with open(path, "w") as f:
        f.write(config_template)
    
    print(f"Default configuration file created at {path}")
    print("Please update the ANTHROPIC_API_KEY and other settings as needed.")