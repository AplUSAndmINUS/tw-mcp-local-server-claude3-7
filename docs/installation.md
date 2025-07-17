# Installation Guide

This guide provides detailed instructions for installing and configuring the TW MCP Local Server.

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 1GB free space
- **Network**: Internet connection for Claude API access

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Download the repository**:
   ```bash
   git clone https://github.com/AplUSAndmINUS/tw-mcp-local-server-claude3-7.git
   cd tw-mcp-local-server-claude3-7
   ```

2. **Run the setup script**:
   ```bash
   python scripts/setup.py
   ```

3. **Configure your API key**:
   The setup script will create a `.env` file. Edit it to add your Anthropic API key:
   ```env
   ANTHROPIC_API_KEY=your-api-key-here
   ```

### Method 2: Manual Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Create configuration file**:
   ```bash
   mcp-server init
   ```

4. **Edit configuration**:
   Update the `.env` file with your settings.

### Method 3: Docker Installation

1. **Build the Docker image**:
   ```bash
   docker build -t mcp-server .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your-key mcp-server
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Server Settings
HOST=localhost
PORT=8000
DEBUG=false
LOG_LEVEL=INFO

# Claude Settings
CLAUDE_MODEL=claude-3-sonnet-20240229
MAX_TOKENS=4096
TEMPERATURE=0.7

# Plugin Settings
ENABLED_PLUGINS=["vibe_coder"]

# Security
SECRET_KEY=your-secret-key-change-this
CORS_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Advanced Configuration

For advanced users, you can create a `config.yaml` file:

```yaml
server:
  host: localhost
  port: 8000
  debug: false
  workers: 1

claude:
  api_key: ${ANTHROPIC_API_KEY}
  model: claude-3-sonnet-20240229
  max_tokens: 4096
  temperature: 0.7
  timeout: 30

plugins:
  enabled:
    - vibe_coder
  settings:
    vibe_coder:
      default_mood: supportive
      max_history: 10

security:
  secret_key: ${SECRET_KEY}
  cors_origins:
    - http://localhost:3000
    - http://localhost:8080
  rate_limit:
    requests: 100
    window: 60

logging:
  level: INFO
  format: json
  file: logs/mcp-server.log
```

## Windows Service Installation

For Windows users who want to run the server as a service:

1. **Install NSSM**:
   - Download from [nssm.cc](https://nssm.cc/download)
   - Extract to a folder in your PATH

2. **Run the service installer**:
   ```bash
   python scripts/windows_service.py
   ```

3. **Alternative: Use PowerShell**:
   ```powershell
   .\scripts\manage_service.ps1 install
   ```

4. **Manage the service**:
   ```powershell
   # Start service
   .\scripts\manage_service.ps1 start
   
   # Stop service
   .\scripts\manage_service.ps1 stop
   
   # Check status
   .\scripts\manage_service.ps1 status
   
   # Restart service
   .\scripts\manage_service.ps1 restart
   ```

## Verification

After installation, verify everything is working:

1. **Test API connection**:
   ```bash
   mcp-server test
   ```

2. **Start the server**:
   ```bash
   mcp-server run
   ```

3. **Access the API documentation**:
   Open your browser to `http://localhost:8000/docs`

4. **Try vibe coding**:
   ```bash
   mcp-server vibe "Hello, help me with Python!"
   ```

## Troubleshooting

### Common Issues

**1. API Key Error**:
```
Error: Anthropic API key must be provided
```
Solution: Set your API key in the `.env` file.

**2. Port Already in Use**:
```
Error: Port 8000 is already in use
```
Solution: Use a different port or stop the process using port 8000.

**3. Module Not Found**:
```
ModuleNotFoundError: No module named 'mcp_server'
```
Solution: Install the package with `pip install -e .`

**4. Permission Denied (Windows Service)**:
```
Access is denied
```
Solution: Run the command prompt as Administrator.

### Log Files

Check log files for detailed error information:
- **Development**: Console output
- **Production**: `logs/mcp-server.log`
- **Windows Service**: Windows Event Viewer

### Getting Help

If you encounter issues:

1. Check the [README](../README.md) for common solutions
2. Review the [examples](../examples/) directory
3. Open an issue on GitHub with:
   - Error message
   - Python version
   - Operating system
   - Configuration (without API keys)

## Next Steps

After installation:

1. Read the [API Documentation](api.md)
2. Explore [Plugin Development](plugins.md)
3. Try the [Examples](../examples/)
4. Set up [Monitoring](monitoring.md)

## Updating

To update to a newer version:

1. **Stop the server**:
   ```bash
   # If running as service
   .\scripts\manage_service.ps1 stop
   
   # If running manually
   Ctrl+C
   ```

2. **Pull updates**:
   ```bash
   git pull origin main
   ```

3. **Update dependencies**:
   ```bash
   pip install -e . --upgrade
   ```

4. **Restart the server**:
   ```bash
   mcp-server run
   ```

## Uninstallation

To completely remove the server:

1. **Stop the service** (if installed):
   ```bash
   .\scripts\manage_service.ps1 uninstall
   ```

2. **Remove the virtual environment**:
   ```bash
   deactivate
   rm -rf venv  # On Windows: rmdir /s venv
   ```

3. **Remove the project directory**:
   ```bash
   cd ..
   rm -rf tw-mcp-local-server-claude3-7
   ```