"""
Sample MCP Plugin Configuration
===============================

This file demonstrates how to configure and extend the MCP server with custom plugins.
"""

import json
from pathlib import Path

# Plugin configuration example
plugin_config = {
    "plugins": {
        "vibe_coder": {
            "enabled": True,
            "settings": {
                "default_mood": "supportive",
                "default_focus": "general",
                "default_experience_level": "intermediate",
                "enable_context_awareness": True,
                "max_conversation_history": 10,
                "response_style": "detailed"
            }
        },
        "code_reviewer": {
            "enabled": False,
            "settings": {
                "review_depth": "comprehensive",
                "include_security_checks": True,
                "suggest_improvements": True,
                "languages": ["python", "javascript", "typescript", "java", "go"]
            }
        },
        "documentation_generator": {
            "enabled": False,
            "settings": {
                "style": "google",
                "include_examples": True,
                "generate_types": True,
                "format": "markdown"
            }
        }
    },
    "server": {
        "host": "localhost",
        "port": 8000,
        "debug": False,
        "cors_origins": ["http://localhost:3000", "http://localhost:8080"],
        "rate_limiting": {
            "requests_per_minute": 100,
            "burst_size": 10
        }
    },
    "claude": {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 4096,
        "temperature": 0.7,
        "system_prompts": {
            "vibe_coding": """You are a thoughtful, empathetic programming companion with deep technical expertise. 
            You understand that coding is both an art and a science, and you approach each request with empathy, 
            reassurance, kindness, understanding, appreciation, deep-dive modeling, and strong reasoning.""",
            "code_review": """You are an expert code reviewer with extensive experience in software development. 
            You provide constructive feedback focusing on code quality, security, performance, and maintainability.""",
            "documentation": """You are a technical writer who creates clear, comprehensive documentation. 
            You explain complex concepts in accessible language while maintaining technical accuracy."""
        }
    }
}

# Save the configuration
def save_sample_config():
    """Save sample configuration to file."""
    config_path = Path("examples/sample_config.json")
    with open(config_path, "w") as f:
        json.dump(plugin_config, f, indent=2)
    print(f"Sample configuration saved to {config_path}")

# Custom plugin template
custom_plugin_template = '''"""
Custom Plugin Template
=====================

This template shows how to create a custom plugin for the MCP server.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel

from mcp_server.plugins import PluginInterface, PluginMetadata, plugin_route, plugin_hook
from mcp_server.claude_client import ClaudeClient
from mcp_server.config import Settings


class CustomRequest(BaseModel):
    """Request model for custom plugin."""
    input: str
    options: Optional[Dict[str, Any]] = None


class CustomPlugin(PluginInterface):
    """Custom plugin implementation."""
    
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.claude_client = ClaudeClient(settings)
    
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return PluginMetadata(
            name="custom_plugin",
            version="1.0.0",
            description="A custom plugin for specialized tasks",
            author="Your Name",
            requires=["anthropic"],
            enabled=True
        )
    
    async def initialize(self) -> None:
        """Initialize the plugin."""
        # Perform any setup tasks here
        pass
    
    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        # Perform any cleanup tasks here
        pass
    
    @plugin_route("/custom/process", methods=["POST"])
    async def process_request(self, request: CustomRequest):
        """Process a custom request."""
        # Your custom logic here
        system_prompt = "You are a helpful assistant specialized in custom tasks."
        
        response = await self.claude_client.complete(
            prompt=request.input,
            system_prompt=system_prompt,
            context=request.options
        )
        
        return {"result": response.content}
    
    @plugin_hook("pre_request")
    async def pre_request_hook(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before processing requests."""
        # Add custom preprocessing here
        return request_data
    
    @plugin_hook("post_response")
    async def post_response_hook(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called after processing responses."""
        # Add custom postprocessing here
        return response_data
'''

def save_plugin_template():
    """Save the custom plugin template."""
    template_path = Path("examples/custom_plugin_template.py")
    with open(template_path, "w") as f:
        f.write(custom_plugin_template)
    print(f"Custom plugin template saved to {template_path}")

# Example usage scenarios
usage_examples = {
    "basic_completion": {
        "description": "Basic text completion",
        "request": {
            "method": "POST",
            "url": "http://localhost:8000/complete",
            "body": {
                "prompt": "Help me write a Python function to calculate fibonacci numbers",
                "max_tokens": 1000
            }
        }
    },
    "vibe_coding": {
        "description": "Vibe coding with empathetic assistance",
        "request": {
            "method": "POST",
            "url": "http://localhost:8000/vibe-code",
            "body": {
                "request": "I'm struggling with async/await in Python. Can you help me understand?",
                "context": {
                    "mood": "supportive",
                    "experience_level": "beginner"
                }
            }
        }
    },
    "code_analysis": {
        "description": "Analyze and improve code",
        "request": {
            "method": "POST",
            "url": "http://localhost:8000/analyze-code",
            "body": {
                "code": "def process_data(data):\\n    result = []\\n    for item in data:\\n        if item > 0:\\n            result.append(item * 2)\\n    return result",
                "language": "python",
                "task": "improve"
            }
        }
    },
    "chat_conversation": {
        "description": "Multi-turn conversation",
        "request": {
            "method": "POST",
            "url": "http://localhost:8000/chat",
            "body": {
                "messages": [
                    {"role": "user", "content": "What's the best way to handle errors in Python?"},
                    {"role": "assistant", "content": "There are several approaches to error handling in Python..."},
                    {"role": "user", "content": "Can you show me an example with try/except?"}
                ]
            }
        }
    }
}

def save_usage_examples():
    """Save usage examples to file."""
    examples_path = Path("examples/usage_examples.json")
    with open(examples_path, "w") as f:
        json.dump(usage_examples, f, indent=2)
    print(f"Usage examples saved to {examples_path}")

def main():
    """Generate all example files."""
    print("Generating MCP Server Examples...")
    save_sample_config()
    save_plugin_template()
    save_usage_examples()
    print("All example files generated successfully!")

if __name__ == "__main__":
    main()