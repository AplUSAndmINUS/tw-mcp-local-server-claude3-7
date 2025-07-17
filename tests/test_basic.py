"""
Basic Tests for MCP Server
==========================

These tests validate the core functionality of the MCP server.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
import json

from mcp_server.config import Settings
from mcp_server.claude_client import ClaudeClient, ClaudeResponse
from mcp_server.server import MCPServer
from mcp_server.plugins.vibe_coder import VibeCoderPlugin


class TestSettings:
    """Test configuration management."""
    
    def test_default_settings(self):
        """Test default settings creation."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            settings = Settings()
            assert settings.host == "localhost"
            assert settings.port == 8000
            assert settings.anthropic_api_key == "test-key"
            assert settings.claude_model == "claude-3-sonnet-20240229"
    
    def test_settings_validation(self):
        """Test settings validation."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            settings = Settings()
            
            # Test temperature validation
            with pytest.raises(ValueError):
                settings.temperature = 2.0
            
            # Test max_tokens validation
            with pytest.raises(ValueError):
                settings.max_tokens = 0


class TestClaudeClient:
    """Test Claude API client."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            settings = Settings()
            return ClaudeClient(settings)
    
    @pytest.mark.asyncio
    async def test_complete_mock(self, client):
        """Test completion with mocked API."""
        with patch.object(client.client.messages, 'create') as mock_create:
            # Mock the API response
            mock_response = Mock()
            mock_response.content = [Mock(text="Hello, world!")]
            mock_response.usage = Mock(input_tokens=10, output_tokens=20, total_tokens=30)
            mock_response.model = "claude-3-sonnet-20240229"
            mock_response.stop_reason = "end_turn"
            mock_create.return_value = mock_response
            
            response = await client.complete("Hello")
            
            assert isinstance(response, ClaudeResponse)
            assert response.content == "Hello, world!"
            assert response.model == "claude-3-sonnet-20240229"
    
    @pytest.mark.asyncio
    async def test_vibe_code_mock(self, client):
        """Test vibe coding with mocked API."""
        with patch.object(client.client.messages, 'create') as mock_create:
            # Mock the API response
            mock_response = Mock()
            mock_response.content = [Mock(text="I understand your frustration...")]
            mock_response.usage = Mock(input_tokens=25, output_tokens=100, total_tokens=125)
            mock_response.model = "claude-3-sonnet-20240229"
            mock_response.stop_reason = "end_turn"
            mock_create.return_value = mock_response
            
            response = await client.vibe_code("I'm struggling with Python")
            
            assert isinstance(response, ClaudeResponse)
            assert "understand" in response.content.lower()
    
    def test_format_context(self, client):
        """Test context formatting."""
        context = {
            "language": "python",
            "difficulty": "beginner",
            "nested": {"key": "value"}
        }
        
        formatted = client._format_context(context)
        
        assert "Context:" in formatted
        assert "language: python" in formatted
        assert "difficulty: beginner" in formatted
        assert "nested" in formatted


class TestVibeCoderPlugin:
    """Test the Vibe Coder plugin."""
    
    @pytest.fixture
    def plugin(self):
        """Create a test plugin."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            settings = Settings()
            return VibeCoderPlugin(settings)
    
    def test_plugin_metadata(self, plugin):
        """Test plugin metadata."""
        metadata = plugin.get_metadata()
        
        assert metadata.name == "vibe_coder"
        assert metadata.version == "1.0.0"
        assert metadata.enabled is True
        assert "empathetic" in metadata.description.lower()
    
    def test_system_prompt_generation(self, plugin):
        """Test system prompt generation."""
        prompt = plugin._get_system_prompt(
            mood="supportive",
            focus="learning",
            experience_level="beginner"
        )
        
        assert "empathetic" in prompt.lower()
        assert "supportive" in prompt.lower()
        assert "beginner" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_process_response(self, plugin):
        """Test response processing."""
        mock_response = ClaudeResponse(
            content="Here are some suggestions:\n- Use functions\n- Add comments\n- Test your code",
            usage={"total_tokens": 50},
            model="claude-3-sonnet-20240229"
        )
        
        from mcp_server.plugins.vibe_coder import VibeRequest
        request = VibeRequest(
            request="Help me improve my code",
            experience_level="beginner"
        )
        
        processed = await plugin._process_response(mock_response, request)
        
        assert len(processed.suggestions) > 0
        assert "functions" in processed.suggestions[0].lower()
        assert len(processed.resources) > 0
        assert 0.6 <= processed.confidence <= 0.9


class TestServer:
    """Test the main server."""
    
    @pytest.fixture
    def server(self):
        """Create a test server."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            settings = Settings()
            return MCPServer(settings)
    
    def test_server_creation(self, server):
        """Test server creation."""
        assert server.settings.host == "localhost"
        assert server.settings.port == 8000
        assert server.app is not None
        assert server.claude_client is not None
        assert server.plugin_registry is not None
    
    def test_app_routes(self, server):
        """Test that routes are registered."""
        routes = [route.path for route in server.app.routes]
        
        assert "/health" in routes
        assert "/complete" in routes
        assert "/chat" in routes
        assert "/analyze-code" in routes
        assert "/vibe-code" in routes
        assert "/plugins" in routes
        assert "/settings" in routes


# Integration tests (these would require actual API keys for full testing)
class TestIntegration:
    """Integration tests for the complete system."""
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--integration"),
        reason="Integration tests require --integration flag"
    )
    @pytest.mark.asyncio
    async def test_full_completion_flow(self):
        """Test complete flow with real API (if available)."""
        # This test would run only with --integration flag
        # and would require actual API credentials
        pass
    
    @pytest.mark.skipif(
        not pytest.config.getoption("--integration"),
        reason="Integration tests require --integration flag"
    )
    @pytest.mark.asyncio
    async def test_vibe_coding_flow(self):
        """Test vibe coding flow with real API (if available)."""
        # This test would run only with --integration flag
        # and would require actual API credentials
        pass


def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])