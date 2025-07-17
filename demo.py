#!/usr/bin/env python3
"""
Demo Script for MCP Server
==========================

This script demonstrates the basic functionality of the MCP server.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Set environment variable for testing
os.environ['ANTHROPIC_API_KEY'] = 'test-key-for-demo'

def test_configuration():
    """Test configuration loading."""
    print("🔧 Testing Configuration")
    print("-" * 30)
    
    from mcp_server.config import Settings
    
    settings = Settings()
    print(f"✓ Host: {settings.host}")
    print(f"✓ Port: {settings.port}")
    print(f"✓ Model: {settings.claude_model}")
    print(f"✓ Max Tokens: {settings.max_tokens}")
    print(f"✓ Temperature: {settings.temperature}")
    print(f"✓ Enabled Plugins: {settings.enabled_plugins}")
    print()

def test_server_creation():
    """Test server creation."""
    print("🚀 Testing Server Creation")
    print("-" * 30)
    
    from mcp_server.server import MCPServer
    from mcp_server.config import Settings
    
    settings = Settings()
    server = MCPServer(settings)
    
    print(f"✓ FastAPI app created: {type(server.app).__name__}")
    print(f"✓ Claude client created: {type(server.claude_client).__name__}")
    print(f"✓ Plugin registry created: {type(server.plugin_registry).__name__}")
    print()

def test_plugin_system():
    """Test plugin system."""
    print("🔌 Testing Plugin System")
    print("-" * 30)
    
    from mcp_server.plugins.vibe_coder import VibeCoderPlugin
    from mcp_server.config import Settings
    
    settings = Settings()
    plugin = VibeCoderPlugin(settings)
    
    metadata = plugin.get_metadata()
    print(f"✓ Plugin Name: {metadata.name}")
    print(f"✓ Plugin Version: {metadata.version}")
    print(f"✓ Plugin Description: {metadata.description}")
    print(f"✓ Plugin Author: {metadata.author}")
    print(f"✓ Plugin Enabled: {metadata.enabled}")
    print()

def test_claude_client():
    """Test Claude client creation."""
    print("🤖 Testing Claude Client")
    print("-" * 30)
    
    from mcp_server.claude_client import ClaudeClient
    from mcp_server.config import Settings
    
    settings = Settings()
    client = ClaudeClient(settings)
    
    print(f"✓ Model: {client.model}")
    print(f"✓ Max Tokens: {client.max_tokens}")
    print(f"✓ Temperature: {client.temperature}")
    print(f"✓ Client Type: {type(client.client).__name__}")
    print()

def show_project_structure():
    """Show the project structure."""
    print("📁 Project Structure")
    print("-" * 30)
    
    project_files = [
        "src/mcp_server/",
        "src/mcp_server/__init__.py",
        "src/mcp_server/config.py",
        "src/mcp_server/server.py", 
        "src/mcp_server/claude_client.py",
        "src/mcp_server/cli.py",
        "src/mcp_server/plugins/",
        "src/mcp_server/plugins/__init__.py",
        "src/mcp_server/plugins/vibe_coder.py",
        "examples/",
        "examples/vibe_coding_example.py",
        "examples/sample_mcp_config.py",
        "docs/",
        "docs/installation.md",
        "docs/api.md",
        "scripts/",
        "scripts/setup.py",
        "scripts/windows_service.py",
        "tests/",
        "tests/test_basic.py",
        "requirements.txt",
        "pyproject.toml",
        "README.md"
    ]
    
    for file_path in project_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (missing)")
    print()

def show_next_steps():
    """Show next steps for using the server."""
    print("📝 Next Steps")
    print("-" * 30)
    print("1. Set your actual Anthropic API key:")
    print("   - Create a .env file")
    print("   - Add: ANTHROPIC_API_KEY=your-actual-key")
    print()
    print("2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("3. Test the server:")
    print("   python -m mcp_server.server")
    print()
    print("4. Use the CLI:")
    print("   python -m mcp_server.cli run")
    print()
    print("5. Try vibe coding:")
    print("   python examples/vibe_coding_example.py")
    print()
    print("6. Read the documentation:")
    print("   - README.md")
    print("   - docs/installation.md")
    print("   - docs/api.md")

def main():
    """Main demonstration function."""
    print("🎉 TW MCP Local Server - Claude 3.7 Demo")
    print("=" * 50)
    print()
    
    try:
        test_configuration()
        test_server_creation()
        test_plugin_system()
        test_claude_client()
        show_project_structure()
        show_next_steps()
        
        print("✅ All tests passed! The MCP server is ready to use.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()