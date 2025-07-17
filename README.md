# TW MCP Local Server - Claude 3.7

A comprehensive Python MCP (Model Context Protocol) server implementation with Claude Sonnet 3.7 integration, designed for local and cloud deployment with a focus on empathetic, thoughtful programming assistance.

## 🌟 Features

- **Claude Sonnet 3.7 Integration**: Direct integration with Anthropic's Claude API for powerful AI assistance
- **Vibe Coding**: Empathetic programming companion focusing on understanding, kindness, and deep technical insights
- **Plugin Architecture**: Extensible plugin system for customizable functionality
- **Local & Cloud Deployment**: Run locally on Windows/Linux/Mac or deploy to cloud platforms
- **FastAPI Server**: High-performance async web server with automatic API documentation
- **Configuration Management**: Flexible configuration via environment variables and config files
- **Rate Limiting**: Built-in rate limiting and security features
- **Comprehensive CLI**: Command-line interface for easy management and interaction

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AplUSAndmINUS/tw-mcp-local-server-claude3-7.git
   cd tw-mcp-local-server-claude3-7
   ```

2. **Run the setup script**:
   ```bash
   python scripts/setup.py
   ```

3. **Configure your API key**:
   Edit the `.env` file and set your Anthropic API key:
   ```env
   ANTHROPIC_API_KEY=your-api-key-here
   ```

4. **Start the server**:
   ```bash
   mcp-server run
   ```

5. **Test the connection**:
   ```bash
   mcp-server test
   ```

## 🎯 Vibe Coding Philosophy

This server implements a unique "vibe coding" approach that focuses on:

- **Empathy**: Understanding your needs and frustrations
- **Reassurance**: Providing confidence and encouragement
- **Kindness**: Patient and supportive explanations
- **Understanding**: Grasping broader context and goals
- **Appreciation**: Recognizing the complexity of programming
- **Deep-dive modeling**: Thorough, well-reasoned solutions
- **Strong reasoning**: Clear explanations of the "why" behind recommendations

## 🔧 Usage

### Command Line Interface

```bash
# Start the server
mcp-server run --host localhost --port 8000

# Test API connection
mcp-server test

# Interactive vibe coding session
mcp-server interactive

# Quick vibe coding
mcp-server vibe "Help me optimize this Python function"

# Analyze code files
mcp-server analyze mycode.py --language python --task review

# Check server status
mcp-server status

# List available plugins
mcp-server plugins
```

### API Endpoints

The server provides several REST API endpoints:

- `POST /complete` - Basic text completion
- `POST /vibe-code` - Vibe coding assistance
- `POST /chat` - Multi-turn conversations
- `POST /analyze-code` - Code analysis and improvement
- `GET /health` - Health check
- `GET /plugins` - List available plugins

### Example API Usage

```python
import httpx
import asyncio

async def vibe_code_example():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/vibe-code",
            json={
                "request": "I'm struggling with async/await in Python. Can you help?",
                "context": {
                    "mood": "supportive",
                    "experience_level": "beginner"
                }
            }
        )
        print(response.json())

asyncio.run(vibe_code_example())
```

## 🔌 Plugin System

The server features a flexible plugin architecture. Create custom plugins by extending the `PluginInterface`:

```python
from mcp_server.plugins import PluginInterface, PluginMetadata

class MyPlugin(PluginInterface):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            description="My custom plugin",
            author="Your Name"
        )
    
    async def initialize(self) -> None:
        # Plugin initialization
        pass
    
    async def shutdown(self) -> None:
        # Plugin cleanup
        pass
```

### Built-in Plugins

- **Vibe Coder**: Empathetic programming assistance
- **Code Analyzer**: Code review and improvement suggestions
- **Documentation Generator**: Automatic documentation generation

## ⚙️ Configuration

Configure the server using environment variables or the `.env` file:

```env
# Server Configuration
HOST=localhost
PORT=8000
DEBUG=false

# Claude API Configuration
ANTHROPIC_API_KEY=your-api-key-here
CLAUDE_MODEL=claude-3-sonnet-20240229
MAX_TOKENS=4096
TEMPERATURE=0.7

# Plugin Configuration
ENABLED_PLUGINS=["vibe_coder"]

# Security
SECRET_KEY=your-secret-key
CORS_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 🖥️ Windows Service Installation

For Windows users, the server can be installed as a Windows service:

1. **Install NSSM** (Non-Sucking Service Manager):
   Download from [nssm.cc](https://nssm.cc/download)

2. **Run the service installer**:
   ```bash
   python scripts/windows_service.py
   ```

3. **Or use the batch file**:
   ```cmd
   scripts\install_service.bat
   ```

4. **Manage the service**:
   ```powershell
   .\scripts\manage_service.ps1 start
   .\scripts\manage_service.ps1 stop
   .\scripts\manage_service.ps1 status
   ```

## 🏗️ Architecture

The server follows a multi-layered architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│                    Plugin System                           │
├─────────────────────────────────────────────────────────────┤
│                    Claude Client                           │
├─────────────────────────────────────────────────────────────┤
│                    Configuration Layer                     │
├─────────────────────────────────────────────────────────────┤
│              Local Processing (Optional)                   │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

- **FastAPI Application**: Web server with automatic API documentation
- **Plugin System**: Extensible architecture for custom functionality
- **Claude Client**: Anthropic API integration with retry logic
- **Configuration Layer**: Environment-based configuration management
- **Local Processing**: Optional local CPU/GPU processing capabilities

## 📚 Examples

The `examples/` directory contains:

- `vibe_coding_example.py`: Complete vibe coding demonstration
- `sample_mcp_config.py`: Plugin configuration examples
- `usage_examples.json`: API usage examples
- `custom_plugin_template.py`: Template for creating custom plugins

Run the vibe coding example:
```bash
cd examples
python vibe_coding_example.py
```

## 🧪 Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/
```

### Creating Plugins

1. Create a new Python file in `src/mcp_server/plugins/`
2. Extend `PluginInterface`
3. Implement required methods
4. Add to `ENABLED_PLUGINS` configuration
5. Restart the server

## 🌐 Cloud Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["mcp-server", "run", "--host", "0.0.0.0"]
```

### Environment Variables for Cloud

```env
HOST=0.0.0.0
PORT=8000
ANTHROPIC_API_KEY=your-api-key
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🛡️ Security Features

- **Rate Limiting**: Configurable request rate limiting
- **CORS Protection**: Configurable CORS origins
- **Input Validation**: Pydantic-based request validation
- **Error Handling**: Comprehensive error handling and logging
- **API Key Security**: Secure API key management

## 📝 Logging

The server uses structured logging with configurable levels:

```python
import structlog
logger = structlog.get_logger()

# Logs are automatically structured with context
logger.info("Request processed", user_id=123, duration=0.5)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for the Claude API
- **FastAPI** for the excellent web framework
- **The Python Community** for amazing libraries and tools

## 📞 Support

For support, please:
1. Check the [documentation](docs/)
2. Review [examples](examples/)
3. Open an issue on GitHub
4. Join our community discussions

---

**Happy Vibe Coding! 🚀**
