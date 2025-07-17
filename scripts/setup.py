#!/usr/bin/env python3
"""
Quick Start Script for MCP Server
=================================

This script provides a simple way to get started with the MCP server.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def create_config():
    """Create configuration file if it doesn't exist."""
    config_path = Path(".env")
    
    if not config_path.exists():
        print("Creating configuration file...")
        from src.mcp_server.config import create_default_config_file
        create_default_config_file(".env")
        print("✓ Configuration file created")
        print("Please edit .env and set your ANTHROPIC_API_KEY")
        return False
    else:
        print("✓ Configuration file already exists")
        return True

def check_api_key():
    """Check if API key is configured."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Warning: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set your API key in the .env file")
        return False
    return True

def main():
    """Main setup function."""
    print("🚀 MCP Server Quick Start")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create config
    config_exists = create_config()
    
    if config_exists:
        # Check API key
        api_key_set = check_api_key()
        
        if api_key_set:
            print("\n✅ Setup complete!")
            print("\nTo start the server, run:")
            print("  mcp-server run")
            print("\nTo test the connection:")
            print("  mcp-server test")
            print("\nTo start vibe coding:")
            print("  mcp-server vibe 'help me write a function'")
        else:
            print("\n⚠️  Setup incomplete!")
            print("Please set your ANTHROPIC_API_KEY in the .env file")
    else:
        print("\n⚠️  Setup incomplete!")
        print("Please edit the .env file and set your ANTHROPIC_API_KEY")

if __name__ == "__main__":
    main()