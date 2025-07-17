# TW MCP Local Server - Claude 3.7 with Hybrid Cloud Computing

A comprehensive Python MCP (Model Context Protocol) server implementation with Claude Sonnet 3.7 integration, featuring **hybrid cloud computing** that prioritizes local execution while seamlessly integrating with Azure cloud resources for resource-intensive tasks.

## 🌟 Key Features

### 🔥 Hybrid Cloud Architecture
- **Local-First Computing**: Intelligent resource management prioritizing local execution
- **Azure Cloud Integration**: Seamless fallback to Azure Functions for demanding tasks
- **Windows Desktop Optimization**: Tailored for high-performance Windows workstations
- **Resource-Aware Decisions**: Real-time monitoring and intelligent task placement

### 🧠 Empathetic AI Assistance
- **Vibe Coding**: Thoughtful, empathetic programming companion
- **Deep Reasoning**: Comprehensive explanations with clear "why" behind recommendations
- **Supportive Guidance**: Encouraging, patient assistance that builds confidence
- **Emotional Intelligence**: Recognizes and responds to user emotional states

### 🎯 Comprehensive MCP Modules

#### 🧠 Ideation & Thoughtcraft
- **Brainstorm**: Empathetic idea generation triggered by intent or mood
- **Mindmap**: Recursive concept branching with visual mapping and clarity
- **Perspective Shift**: Reframes questions and challenges defaults with support
- **Creativity Surge**: Breaks creative gridlock through divergent thinking

#### 🎨 Visual & Image Generation
- **Image Seed**: Thematic visual output generation
- **Palette Gen**: Emotion and brand-driven color schemes
- **Render Style**: Diverse rendering techniques (photo, sketch, surreal)
- **Sketch Flow**: Draft-level visual sequences from minimal input

#### 🎬 Animation & Motion Design
- **Motion Branding**: Logo and tagline animation synchronized with brand energy
- **Vibe Fade**: Emotion-driven transitions for ambient visual experiences
- **Loop Craft**: Seamless looping animation generation
- **Tempo Sync**: Animation synchronized with ambient inputs (music, voice)

#### 🧪 Model Interaction & Testing
- **LLM Dictation**: Voice-to-model transcription and dictation workflows
- **API Testbed**: Local sandbox for testing and validating API behavior
- **Query Refine**: Prompt language tuning for optimal clarity and results
- **Agent Weave**: Multi-agent workflow orchestration with coordinated logic

#### ✍️ Writing & Composition
- **Writing Muse**: Storylines, brand copy, and essays from seed concepts
- **Composition Sculpt**: Form, tone, and flow control for writing tasks
- **Edit Pass**: Text rewriting and polishing with stylistic presets
- **Persona Writer**: Character-based writing voice emulation

#### 🎧 Music & Audio Development
- **Tone Builder**: Melodic ideas tied to brand emotion and scene context
- **Beat Vibe**: Loop creation synchronized with animations and triggers
- **Soundscape**: Multi-layered ambient audio design generation
- **Voiceflow**: Vocal input/output processing and styling

#### 🗣️ Voice Recognition & Interaction
- **Voice Capture**: Contextual voice capture with intelligent labeling
- **Intent Echo**: Tone and emotion analysis embedded in speech
- **Speech Craft**: Natural spoken response generation
- **Command Stream**: Voice-activated MCP task execution

## 🏗️ Architecture

### Hybrid Computing Decision Engine
```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                     │
├─────────────────────────────────────────────────────────────┤
│               Hybrid Compute Manager                       │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   Local Execution   │    │    Azure Cloud Functions   │ │
│  │  - CPU Monitoring   │    │   - Flex Consumption Plan  │ │
│  │  - Memory Tracking  │    │   - Serverless Compute     │ │
│  │  - GPU Utilization  │    │   - Auto-scaling           │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    MCP Plugin System                       │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │  Ideation    │ │   Visual     │ │    Voice & Audio     │ │
│  │  Modules     │ │  Generation  │ │     Modules          │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Claude Client                           │
├─────────────────────────────────────────────────────────────┤
│                 Configuration Layer                        │
├─────────────────────────────────────────────────────────────┤
│           Azure Integration & Local Processing             │
└─────────────────────────────────────────────────────────────┘
```

### Resource Management Strategy
- **Local Execution Criteria**: CPU < 80%, Memory < 85%, Task duration < 5 min
- **Azure Fallback Triggers**: Resource constraints, long-running tasks, specialized AI services
- **Cost Optimization**: Minimize cloud costs while maintaining performance guarantees
- **Windows-Specific**: GPU prioritization, service integration, desktop optimization

## 🚀 Quick Start

### System Requirements

#### Recommended Windows Desktop Configuration
- **CPU**: AMD Ryzen 5800X or equivalent
- **RAM**: 64GB (32GB minimum)
- **Storage**: 2TB SSD (multiple drives recommended)
- **GPU**: NVIDIA RTX 3070 or better
- **Network**: 1Gbps Ethernet + Wi-Fi 6e
- **OS**: Windows 11 Pro for Workstations

#### Azure Cloud Resources (Optional)
- Azure Functions (Linux Flex Consumption)
- Azure Storage (Blob, Table, Queue)
- Azure AI Services
- Azure Orchestration (Durable Functions)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AplUSAndmINUS/tw-mcp-local-server-claude3-7.git
   cd tw-mcp-local-server-claude3-7
   ```

2. **Run the automated setup**:
   ```bash
   python scripts/setup.py
   ```

3. **Configure your environment**:
   ```bash
   # Copy and edit the configuration file
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Essential Configuration**:
   ```env
   # Claude API
   ANTHROPIC_API_KEY=your-api-key-here
   
   # Hybrid Computing
   HYBRID_COMPUTING_ENABLED=true
   PREFER_LOCAL_EXECUTION=true
   
   # Azure Integration (Optional)
   AZURE_ENABLED=false
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   
   # Windows Optimizations
   WINDOWS_OPTIMIZATIONS=true
   WINDOWS_GPU_PRIORITY=true
   ```

5. **Start the server**:
   ```bash
   mcp-server run
   ```

6. **Verify installation**:
   ```bash
   python tests/test_integration.py
   ```

## 🎯 Usage Examples

### Empathetic Brainstorming
```bash
# CLI brainstorming session
mcp-server vibe "I need creative ideas for improving team collaboration"

# API request
curl -X POST "http://localhost:8000/brainstorm/session" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Sustainable urban transportation",
    "intent": "problem_solving",
    "mood": "focused",
    "duration_minutes": 15
  }'
```

### Mindmap Creation
```python
import httpx
import asyncio

async def create_mindmap():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/mindmap/create",
            json={
                "central_concept": "Machine Learning Applications",
                "depth": 3,
                "breadth": 5,
                "thinking_style": "analytical"
            }
        )
        mindmap = response.json()
        print(f"Created mindmap with {len(mindmap['nodes'])} nodes")
        return mindmap

asyncio.run(create_mindmap())
```

### Perspective Shifting
```python
async def shift_perspective():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/perspective-shift/shift",
            json={
                "original_question": "How can we increase team productivity?",
                "shift_type": "stakeholder",
                "intensity": "moderate"
            }
        )
        return response.json()
```

### Creativity Surge
```bash
# Break creative gridlock
curl -X POST "http://localhost:8000/creativity-surge/surge" \
  -H "Content-Type: application/json" \
  -d '{
    "challenge": "Design a more engaging user onboarding",
    "technique": "random_stimulation",
    "intensity": "high",
    "preferred_style": "playful"
  }'
```

### System Monitoring
```bash
# Check hybrid computing status
curl http://localhost:8000/system/status

# Monitor resource usage
curl http://localhost:8000/system/resources

# Trigger system optimization
curl -X POST http://localhost:8000/system/optimize
```

## 🎯 Vibe Coding Philosophy

This server implements a unique "vibe coding" approach that prioritizes:

- **Empathy**: Understanding your needs, frustrations, and emotional context
- **Reassurance**: Providing confidence and encouragement, especially during challenges
- **Kindness**: Patient, supportive explanations that never condescend
- **Understanding**: Grasping broader context, goals, and long-term objectives
- **Appreciation**: Recognizing the complexity and creativity in programming
- **Deep-dive reasoning**: Thorough, well-reasoned solutions with clear explanations
- **Strong logical reasoning**: Clear explanations of the "why" behind recommendations

## 🔧 Hybrid Computing Features

### Intelligent Resource Management
- **Real-time Monitoring**: CPU, memory, disk, and GPU utilization tracking
- **Adaptive Thresholds**: Windows-optimized performance thresholds
- **Predictive Analytics**: Task duration and resource requirement estimation
- **Cost Optimization**: Minimize cloud costs while maintaining performance

### Local-First Execution
- **Prioritized Local Processing**: Maximum efficiency with your hardware
- **GPU Acceleration**: Leverage NVIDIA RTX capabilities for visual tasks
- **Windows Service Integration**: Seamless Windows desktop integration
- **Resource-Aware Scheduling**: Intelligent task queuing and prioritization

### Azure Cloud Integration
- **Serverless Functions**: Linux Flex Consumption for cost-effective scaling
- **Storage Integration**: Blob, table, and queue operations
- **AI Services**: Cognitive Services for specialized processing
- **Orchestration**: Durable Functions for complex workflows

### Empathetic MCP Modules
Each module is designed with empathy and support at its core:

#### 🧠 Ideation & Thoughtcraft
- **Brainstorm**: Mood-aware idea generation with encouraging feedback
- **Mindmap**: Visual concept mapping with supportive guidance
- **Perspective Shift**: Gentle reframing with empathetic reasoning
- **Creativity Surge**: Breakthrough techniques with motivational support

#### 🎨 Visual & Creative Modules
- **Image Seed**: Emotion-driven visual concepts
- **Palette Gen**: Brand-aligned color psychology
- **Motion Branding**: Dynamic brand expression
- **Vibe Fade**: Ambient emotional transitions

#### 🗣️ Voice & Communication
- **Voice Capture**: Contextual speech recognition
- **Intent Echo**: Emotional tone analysis
- **Speech Craft**: Natural response generation
- **Command Stream**: Voice-controlled workflows

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

## 🏗️ Deployment Options

### Local Windows Desktop
```bash
# Install as Windows service
python scripts/windows_service.py install
python scripts/windows_service.py start

# Or run directly
mcp-server run --host localhost --port 8000
```

### Hybrid Cloud Deployment
```bash
# Deploy Azure Functions
./scripts/deploy_azure_functions.sh

# Configure hybrid settings
export AZURE_ENABLED=true
export AZURE_SUBSCRIPTION_ID=your-subscription-id

# Start with hybrid computing
mcp-server run --hybrid-enabled
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["mcp-server", "run", "--host", "0.0.0.0"]
```

## 📊 Performance & Monitoring

### Resource Monitoring
- **Real-time Metrics**: CPU, memory, disk, GPU utilization
- **Historical Analysis**: Performance trends and patterns
- **Threshold Alerts**: Proactive resource management
- **Cost Tracking**: Azure usage and cost optimization

### System Health
- **Health Endpoints**: `/health`, `/system/status`
- **Plugin Status**: Individual module health checks
- **Azure Integration**: Service availability and latency
- **Performance Metrics**: Response times and throughput

## 🔐 Security & Privacy

### Local Security
- **Rate Limiting**: Configurable request throttling
- **CORS Protection**: Cross-origin request management
- **Input Validation**: Comprehensive request sanitization
- **Secure Defaults**: Production-ready security configuration

### Azure Security
- **OAuth2 Integration**: Secure cloud authentication
- **Managed Identity**: Passwordless Azure access
- **Network Security**: VPC and firewall configuration
- **Audit Logging**: Comprehensive security monitoring

## 📚 Documentation

- **[Hybrid Configuration Guide](HYBRID_CONFIGURATION.md)**: Complete setup and configuration
- **[API Documentation](docs/api.md)**: Comprehensive API reference
- **[Plugin Development](docs/plugins.md)**: Creating custom MCP modules
- **[Azure Integration](docs/azure.md)**: Cloud deployment guide
- **[Windows Service](docs/windows.md)**: Desktop service setup

## 🧪 Testing & Validation

### Automated Testing
```bash
# Run all tests
pytest tests/

# Test hybrid computing
python tests/test_integration.py

# Test individual modules
pytest tests/test_brainstorm.py
pytest tests/test_mindmap.py
```

### Manual Testing
```bash
# Test brainstorming
mcp-server vibe "Help me brainstorm ideas for..."

# Test mindmapping
curl -X POST localhost:8000/mindmap/create -d '{"central_concept": "AI"}'

# Test system status
curl localhost:8000/system/status
```

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup
git clone https://github.com/AplUSAndmINUS/tw-mcp-local-server-claude3-7.git
cd tw-mcp-local-server-claude3-7
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/
```

### Plugin Development
Create custom MCP plugins:
```python
from mcp_server.plugins import PluginInterface, PluginMetadata

class MyPlugin(PluginInterface):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_plugin",
            version="1.0.0",
            description="Custom empathetic plugin",
            author="Your Name"
        )
    
    async def initialize(self) -> None:
        # Initialize with empathy and support
        pass
```

## 🛡️ Security Features

- **Rate Limiting**: Configurable request rate limiting
- **CORS Protection**: Configurable CORS origins
- **Input Validation**: Pydantic-based request validation
- **Error Handling**: Comprehensive error handling and logging
- **API Key Security**: Secure API key management
- **Azure Security**: OAuth2 and managed identity integration

## 📝 Logging & Monitoring

The server uses structured logging with empathetic context:

```python
import structlog
logger = structlog.get_logger()

# Empathetic logging with user context
logger.info("Supporting user through creative challenge", 
           user_mood="frustrated", 
           assistance_type="brainstorming")
```

## 🌐 Cloud Integration

### Azure Functions
- **Ideation Functions**: Brainstorming and mindmapping
- **Visual Functions**: Image and animation generation
- **Audio Functions**: Music and voice processing
- **Orchestration**: Complex workflow management

### Cost Optimization
- **Local-First**: Zero cloud costs for local execution
- **Intelligent Routing**: Cost-aware task placement
- **Usage Monitoring**: Real-time cost tracking
- **Budget Controls**: Configurable spending limits

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
