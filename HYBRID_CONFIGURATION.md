# TW MCP Local Server - Hybrid Cloud Configuration

## Overview

This enhanced MCP server provides a hybrid cloud computing solution that prioritizes local execution while seamlessly integrating with Azure cloud resources when needed. The system features empathetic, thoughtful AI assistance through multiple specialized MCP modules.

## 🌟 Key Features

### Hybrid Computing Architecture
- **Local-First Execution**: Prioritizes local resources for maximum efficiency
- **Azure Cloud Integration**: Seamless fallback to Azure Functions for resource-intensive tasks
- **Intelligent Resource Management**: Monitors system resources and makes optimal execution decisions
- **Windows Desktop Optimizations**: Tailored for Windows workstations with specific hardware configurations

### Empathetic AI Assistance
- **Vibe Coding**: Supportive, understanding programming companion
- **Deep Reasoning**: Thorough explanations with clear "why" behind recommendations
- **Emotional Intelligence**: Recognizes and responds to user emotional states
- **Encouraging Guidance**: Builds confidence while providing technical excellence

### Comprehensive MCP Modules

#### 🧠 Ideation & Thoughtcraft
- **Brainstorm**: Unstructured idea generation with mood-based adaptation
- **Mindmap**: Recursive concept branching with visual mapping
- **Perspective Shift**: Reframes questions and challenges defaults
- **Creativity Surge**: Breaks creative gridlock through divergent thinking

#### 🎨 Visual & Image Generation
- **Image Seed**: Thematic visual output generation
- **Palette Gen**: Emotion and brand-driven color schemes
- **Render Style**: Diverse rendering techniques (photo, sketch, surreal)
- **Sketch Flow**: Draft-level visual sequences from minimal input

#### 🎬 Animation & Motion Design
- **Motion Branding**: Logo and tagline animation with brand energy
- **Vibe Fade**: Emotion-driven transitions for ambient visual cues
- **Loop Craft**: Seamless looping animation generation
- **Tempo Sync**: Animation synchronized with ambient inputs

#### 🧪 Model Interaction & Testing
- **LLM Dictation**: Voice-to-model transcription and dictation
- **API Testbed**: Local sandbox for API testing and validation
- **Query Refine**: Prompt language tuning for clarity
- **Agent Weave**: Multi-agent workflow orchestration

#### ✍️ Writing & Composition
- **Writing Muse**: Storylines, brand copy, and essays from seed concepts
- **Composition Sculpt**: Form, tone, and flow control for writing
- **Edit Pass**: Text rewriting and polishing with stylistic presets
- **Persona Writer**: Character-based writing voice emulation

#### 🎧 Music & Audio Development
- **Tone Builder**: Melodic ideas tied to brand emotion
- **Beat Vibe**: Loop creation synced with animations
- **Soundscape**: Multi-layered ambient audio design
- **Voiceflow**: Vocal input/output processing and styling

#### 🗣️ Voice Recognition & Interaction
- **Voice Capture**: Contextual voice capture and labeling
- **Intent Echo**: Tone and emotion analysis in speech
- **Speech Craft**: Natural spoken response generation
- **Command Stream**: Voice-activated MCP task execution

## 🛠️ System Requirements

### Local Windows Desktop Configuration
- **CPU**: AMD Ryzen 5800X or equivalent
- **RAM**: 64GB recommended (minimum 32GB)
- **Storage**: 2TB SSD (split across multiple drives recommended)
- **GPU**: NVIDIA RTX 3070 or better (for visual/animation tasks)
- **Network**: 1Gbps Ethernet + Wi-Fi 6e
- **OS**: Windows 11 Pro for Workstations

### Azure Cloud Resources
- **Azure Functions**: Linux Flex Consumption plan
- **Azure Storage**: Blob, Table, and Queue storage
- **Azure AI Services**: Cognitive Services integration
- **Azure Orchestration**: Durable Functions for complex workflows

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AplUSAndmINUS/tw-mcp-local-server-claude3-7.git
   cd tw-mcp-local-server-claude3-7
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the server**:
   ```bash
   mcp-server run
   ```

### Azure Integration Setup

1. **Azure Prerequisites**:
   - Azure subscription with appropriate permissions
   - Azure CLI installed and authenticated
   - Resource group created for MCP resources

2. **Configure Azure settings**:
   ```env
   AZURE_ENABLED=true
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret
   AZURE_RESOURCE_GROUP=mcp-resources
   ```

3. **Deploy Azure Functions**:
   ```bash
   # Deploy function apps for each MCP module category
   ./scripts/deploy_azure_functions.sh
   ```

## 📊 Hybrid Computing Decision Engine

The system automatically decides between local and Azure execution based on:

### Resource Monitoring
- **CPU Usage**: Monitors real-time CPU utilization
- **Memory Usage**: Tracks available RAM
- **GPU Usage**: Monitors GPU utilization when available
- **Network I/O**: Considers network bandwidth usage

### Decision Criteria
- **Local Execution Preferred When**:
  - CPU usage < 80%
  - Memory usage < 85%
  - GPU usage < 90% (for GPU tasks)
  - Task duration < 5 minutes
  - Network connectivity is limited

- **Azure Execution Chosen When**:
  - Local resources are constrained
  - Task requires specialized Azure AI services
  - Long-running tasks (>5 minutes)
  - High-priority tasks needing guaranteed resources

### Cost Optimization
- **Local Execution**: Zero additional cost
- **Azure Execution**: Consumption-based pricing with cost estimation
- **Hybrid Strategy**: Minimizes cloud costs while maintaining performance

## 🔧 Configuration Options

### Core Server Configuration
```env
# Server settings
HOST=localhost
PORT=8000
DEBUG=false

# Claude API
ANTHROPIC_API_KEY=your-key-here
CLAUDE_MODEL=claude-3-sonnet-20240229
MAX_TOKENS=4096
TEMPERATURE=0.7

# Hybrid computing
HYBRID_COMPUTING_ENABLED=true
PREFER_LOCAL_EXECUTION=true
LOCAL_CPU_THRESHOLD=0.8
LOCAL_MEMORY_THRESHOLD=0.85

# Windows optimizations
WINDOWS_OPTIMIZATIONS=true
WINDOWS_GPU_PRIORITY=true
```

### MCP Module Configuration
```env
# Enable/disable module categories
MCP_IDEATION_ENABLED=true
MCP_VISUAL_ENABLED=true
MCP_ANIMATION_ENABLED=true
MCP_AUDIO_ENABLED=true
MCP_VOICE_ENABLED=true
MCP_WRITING_ENABLED=true
MCP_TESTING_ENABLED=true
```

## 🌐 API Endpoints

### Core Endpoints
- `GET /health` - Health check with system status
- `GET /system/status` - Comprehensive system and resource status
- `POST /system/optimize` - Trigger system optimization
- `GET /plugins` - List available MCP plugins
- `GET /settings` - Server configuration (excluding sensitive data)

### MCP Module Endpoints
- `POST /brainstorm/session` - Start brainstorming session
- `POST /mindmap/create` - Create new mindmap
- `POST /perspective-shift/shift` - Generate perspective shifts
- `POST /creativity-surge/surge` - Create creativity surge session
- `POST /vibe-code` - Empathetic programming assistance

### Hybrid Computing Endpoints
- `GET /system/resources` - Current resource utilization
- `POST /system/execute` - Execute task with hybrid decision
- `GET /azure/status` - Azure integration status

## 🎯 Usage Examples

### Brainstorming Session
```python
import httpx

async def brainstorm_session():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/brainstorm/session",
            json={
                "topic": "Sustainable urban transportation",
                "intent": "problem_solving",
                "mood": "focused",
                "duration_minutes": 15
            }
        )
        return response.json()
```

### Mindmap Creation
```python
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
        return response.json()
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
```python
async def creativity_surge():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/creativity-surge/surge",
            json={
                "challenge": "Design a more engaging user onboarding experience",
                "technique": "random_stimulation",
                "intensity": "high",
                "preferred_style": "playful"
            }
        )
        return response.json()
```

## 📈 Performance Monitoring

### Resource Monitoring
```bash
# Check system status
curl http://localhost:8000/system/status

# Monitor resource usage
curl http://localhost:8000/system/resources
```

### Azure Cost Monitoring
```bash
# Check Azure service status and costs
curl http://localhost:8000/azure/status
```

## 🔒 Security Features

### Local Security
- **Rate Limiting**: Configurable request limits
- **CORS Protection**: Configurable origins
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Secure error responses

### Azure Security
- **OAuth2 Authentication**: Secure Azure service access
- **Key Management**: Secure credential storage
- **Network Security**: VPC and security group configurations
- **Audit Logging**: Complete request/response logging

## 🚀 Deployment

### Local Windows Service
```bash
# Install as Windows service
python scripts/windows_service.py install

# Manage service
python scripts/windows_service.py start
python scripts/windows_service.py stop
python scripts/windows_service.py status
```

### Azure Functions Deployment
```bash
# Deploy all function apps
./scripts/deploy_all_functions.sh

# Deploy specific module
./scripts/deploy_function.sh ideation

# Monitor deployments
./scripts/monitor_functions.sh
```

## 🧪 Testing

### Local Testing
```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/ --integration

# Test specific modules
pytest tests/test_brainstorm.py
pytest tests/test_mindmap.py
```

### Azure Testing
```bash
# Test Azure integration
pytest tests/test_azure_integration.py

# Test hybrid computing
pytest tests/test_hybrid_compute.py
```

## 📚 Advanced Features

### Plugin Development
Create custom MCP plugins by extending the `PluginInterface`:

```python
from mcp_server.plugins import PluginInterface, PluginMetadata

class MyCustomPlugin(PluginInterface):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my_custom_plugin",
            version="1.0.0",
            description="Custom MCP plugin",
            author="Your Name"
        )
    
    async def initialize(self) -> None:
        # Plugin initialization logic
        pass
    
    async def shutdown(self) -> None:
        # Plugin cleanup logic
        pass
```

### Custom Creativity Techniques
Extend the creativity surge module with custom techniques:

```python
async def my_custom_technique(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
    # Custom creativity technique implementation
    pass
```

### Azure Function Development
Create custom Azure Functions for specialized processing:

```python
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Custom Azure Function logic
    pass
```

## 🐛 Troubleshooting

### Common Issues

#### Local Execution Problems
- **High CPU Usage**: Check background processes, adjust thresholds
- **Memory Constraints**: Increase virtual memory, optimize plugins
- **GPU Issues**: Update drivers, check CUDA compatibility

#### Azure Integration Problems
- **Authentication Failures**: Verify credentials and permissions
- **Function Timeouts**: Increase timeout settings, optimize code
- **Cost Overruns**: Monitor usage, adjust execution thresholds

#### Plugin Issues
- **Plugin Load Failures**: Check dependencies, verify syntax
- **Performance Issues**: Profile plugin code, optimize algorithms
- **Memory Leaks**: Monitor memory usage, check cleanup routines

### Debug Mode
Enable debug mode for detailed logging:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

### Log Analysis
```bash
# View server logs
tail -f logs/mcp_server.log

# Search for specific issues
grep "ERROR" logs/mcp_server.log
grep "Azure" logs/mcp_server.log
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `pip install -e ".[dev]"`
4. Make your changes
5. Run tests: `pytest`
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all public functions
- Include unit tests for new features

### Documentation
- Update README for new features
- Add examples for new endpoints
- Document configuration options
- Update API documentation

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for the Claude API
- **Microsoft Azure** for cloud infrastructure
- **FastAPI** for the web framework
- **The Python Community** for excellent libraries

## 📞 Support

For support and questions:
1. Check the [documentation](docs/)
2. Review [examples](examples/)
3. Search [issues](https://github.com/AplUSAndmINUS/tw-mcp-local-server-claude3-7/issues)
4. Open a new issue if needed

---

**Happy Hybrid Computing! 🚀**