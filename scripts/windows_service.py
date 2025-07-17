#!/usr/bin/env python3
"""
Windows Service Installer for MCP Server
========================================

This script helps install and manage the MCP server as a Windows service.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def create_service_script():
    """Create a service script for Windows."""
    service_script = """
import sys
import os
import time
import threading
import signal
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from mcp_server.server import MCPServer
from mcp_server.config import load_settings

class MCPService:
    def __init__(self):
        self.server = None
        self.running = False
        
    def start(self):
        self.running = True
        settings = load_settings()
        self.server = MCPServer(settings)
        
        # Run in a separate thread
        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Keep the service running
        while self.running:
            time.sleep(1)
    
    def stop(self):
        self.running = False
        if self.server:
            # Server shutdown is handled by FastAPI
            pass

def signal_handler(signum, frame):
    service.stop()
    sys.exit(0)

if __name__ == "__main__":
    service = MCPService()
    
    # Handle stop signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        service.start()
    except KeyboardInterrupt:
        service.stop()
"""
    
    with open("scripts/service.py", "w") as f:
        f.write(service_script)
    
    print("✓ Service script created")

def create_batch_files():
    """Create batch files for Windows service management."""
    
    # Start script
    start_script = '''@echo off
echo Starting MCP Server...
cd /d "%~dp0.."
python scripts/service.py
pause
'''
    
    with open("scripts/start_service.bat", "w") as f:
        f.write(start_script)
    
    # Install script
    install_script = '''@echo off
echo Installing MCP Server Service...
cd /d "%~dp0.."

REM Install as Windows service using NSSM (if available)
where nssm >nul 2>nul
if %errorlevel% == 0 (
    echo Installing with NSSM...
    nssm install MCPServer python "%cd%\\scripts\\service.py"
    nssm set MCPServer AppDirectory "%cd%"
    nssm set MCPServer DisplayName "MCP Server - Claude 3.7"
    nssm set MCPServer Description "Python MCP server with Claude Sonnet 3.7 integration"
    nssm start MCPServer
    echo Service installed and started
) else (
    echo NSSM not found. Please install NSSM for Windows service support.
    echo Starting manually...
    python scripts/service.py
)
pause
'''
    
    with open("scripts/install_service.bat", "w") as f:
        f.write(install_script)
    
    # Uninstall script
    uninstall_script = '''@echo off
echo Uninstalling MCP Server Service...
nssm stop MCPServer
nssm remove MCPServer confirm
echo Service uninstalled
pause
'''
    
    with open("scripts/uninstall_service.bat", "w") as f:
        f.write(uninstall_script)
    
    print("✓ Batch files created")

def create_powershell_script():
    """Create PowerShell script for advanced Windows management."""
    
    ps_script = '''
# MCP Server PowerShell Management Script
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "uninstall", "start", "stop", "restart", "status")]
    [string]$Action
)

$ServiceName = "MCPServer"
$ServiceDisplayName = "MCP Server - Claude 3.7"
$ServiceDescription = "Python MCP server with Claude Sonnet 3.7 integration"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PythonScript = Join-Path $ProjectRoot "scripts\\service.py"

function Install-MCPService {
    Write-Host "Installing MCP Server Service..." -ForegroundColor Green
    
    # Check if NSSM is available
    $nssm = Get-Command nssm -ErrorAction SilentlyContinue
    
    if ($nssm) {
        & nssm install $ServiceName python $PythonScript
        & nssm set $ServiceName AppDirectory $ProjectRoot
        & nssm set $ServiceName DisplayName $ServiceDisplayName
        & nssm set $ServiceName Description $ServiceDescription
        & nssm start $ServiceName
        Write-Host "Service installed and started successfully" -ForegroundColor Green
    } else {
        Write-Host "NSSM not found. Please install NSSM for Windows service support." -ForegroundColor Yellow
        Write-Host "Download from: https://nssm.cc/download" -ForegroundColor Yellow
    }
}

function Uninstall-MCPService {
    Write-Host "Uninstalling MCP Server Service..." -ForegroundColor Yellow
    & nssm stop $ServiceName
    & nssm remove $ServiceName confirm
    Write-Host "Service uninstalled" -ForegroundColor Green
}

function Start-MCPService {
    Write-Host "Starting MCP Server Service..." -ForegroundColor Green
    & nssm start $ServiceName
}

function Stop-MCPService {
    Write-Host "Stopping MCP Server Service..." -ForegroundColor Yellow
    & nssm stop $ServiceName
}

function Restart-MCPService {
    Write-Host "Restarting MCP Server Service..." -ForegroundColor Green
    & nssm restart $ServiceName
}

function Get-MCPServiceStatus {
    Write-Host "MCP Server Service Status:" -ForegroundColor Cyan
    & nssm status $ServiceName
}

switch ($Action) {
    "install" { Install-MCPService }
    "uninstall" { Uninstall-MCPService }
    "start" { Start-MCPService }
    "stop" { Stop-MCPService }
    "restart" { Restart-MCPService }
    "status" { Get-MCPServiceStatus }
}
'''
    
    with open("scripts/manage_service.ps1", "w") as f:
        f.write(ps_script)
    
    print("✓ PowerShell script created")

def main():
    """Main function to create Windows service files."""
    print("🪟 Creating Windows Service Files")
    print("=" * 50)
    
    # Create scripts directory if it doesn't exist
    os.makedirs("scripts", exist_ok=True)
    
    # Create service files
    create_service_script()
    create_batch_files()
    create_powershell_script()
    
    print("\n✅ Windows service files created!")
    print("\nTo install as a Windows service:")
    print("1. Install NSSM from https://nssm.cc/download")
    print("2. Run scripts/install_service.bat as Administrator")
    print("\nAlternatively, use PowerShell:")
    print("   .\\scripts\\manage_service.ps1 install")
    print("\nTo start manually:")
    print("   scripts/start_service.bat")

if __name__ == "__main__":
    main()