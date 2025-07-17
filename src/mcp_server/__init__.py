"""
TW MCP Local Server - Claude 3.7 Integration
============================================

A Python MCP (Model Context Protocol) server implementation with Claude Sonnet 3.7 
integration for local and cloud deployment.

Features:
- FastAPI-based server with async/await support
- Claude Sonnet 3.7 API integration via Anthropic SDK
- Plugin system for extensible functionality
- Local and cloud deployment options
- Configuration management
- Comprehensive logging and error handling

Author: AplUSAndmINUS
License: GPL-3.0
"""

__version__ = "0.1.0"
__author__ = "AplUSAndmINUS"
__license__ = "GPL-3.0"

from .server import MCPServer
from .claude_client import ClaudeClient
from .config import Settings

__all__ = ["MCPServer", "ClaudeClient", "Settings"]