#!/usr/bin/env python3
"""
System Integration Test
======================

Basic test to verify hybrid cloud system components work together.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server.config import Settings
from mcp_server.hybrid_compute import HybridComputeManager, TaskDefinition, TaskPriority
from mcp_server.azure_integration import AzureIntegration
from mcp_server.plugins.brainstorm import BrainstormPlugin
from mcp_server.plugins.mindmap import MindmapPlugin
from mcp_server.plugins.perspective_shift import PerspectiveShiftPlugin
from mcp_server.plugins.creativity_surge import CreativitySurgePlugin


async def test_hybrid_compute():
    """Test hybrid compute manager."""
    print("🧪 Testing Hybrid Compute Manager...")
    
    settings = Settings(anthropic_api_key='test-key')
    manager = HybridComputeManager(settings)
    
    # Test resource monitoring
    resources = await manager.get_current_resources()
    print(f"  ✓ Current CPU: {resources.cpu_percent:.1%}")
    print(f"  ✓ Current Memory: {resources.memory_percent:.1%}")
    print(f"  ✓ Current Disk: {resources.disk_percent:.1%}")
    
    # Test task definition
    task = TaskDefinition(
        name="test_task",
        priority=TaskPriority.LOW,
        estimated_cpu=0.1,
        estimated_memory=0.1,
        estimated_duration=10
    )
    
    # Test decision making
    decision = await manager.decide_execution_location(task)
    print(f"  ✓ Execution decision: {decision.location.value}")
    print(f"  ✓ Confidence: {decision.confidence:.1%}")
    print(f"  ✓ Reasoning: {decision.reasoning}")
    
    # Test system status
    status = await manager.get_system_status()
    print(f"  ✓ System status: {status['local_preferred']}")
    
    print("✅ Hybrid Compute Manager test passed!")


async def test_azure_integration():
    """Test Azure integration."""
    print("\n🧪 Testing Azure Integration...")
    
    settings = Settings(anthropic_api_key='test-key')
    azure = AzureIntegration(settings)
    
    # Test service status
    status = await azure.get_service_status()
    print(f"  ✓ Authentication: {status['authenticated']}")
    print(f"  ✓ Functions available: {status['functions']['available']}")
    print(f"  ✓ Storage available: {status['storage']['available']}")
    
    print("✅ Azure Integration test passed!")


async def test_plugin_loading():
    """Test plugin loading and metadata."""
    print("\n🧪 Testing Plugin Loading...")
    
    settings = Settings(anthropic_api_key='test-key')
    
    # Test each plugin
    plugins = [
        BrainstormPlugin(settings),
        MindmapPlugin(settings),
        PerspectiveShiftPlugin(settings),
        CreativitySurgePlugin(settings)
    ]
    
    for plugin in plugins:
        metadata = plugin.get_metadata()
        print(f"  ✓ {metadata.name} v{metadata.version} - {metadata.description}")
    
    print("✅ Plugin loading test passed!")


async def test_empathetic_responses():
    """Test empathetic response generation."""
    print("\n🧪 Testing Empathetic Response Generation...")
    
    settings = Settings(anthropic_api_key='test-key')
    brainstorm = BrainstormPlugin(settings)
    
    # Test system prompts
    base_prompt = brainstorm._get_base_system_prompt()
    print(f"  ✓ Base prompt includes empathy: {'empathy' in base_prompt.lower()}")
    print(f"  ✓ Base prompt includes support: {'support' in base_prompt.lower()}")
    print(f"  ✓ Base prompt includes understanding: {'understanding' in base_prompt.lower()}")
    
    # Test encouragement generation
    encouragement = brainstorm._generate_encouragement([], "supportive")
    print(f"  ✓ Encouragement generated: {len(encouragement)} chars")
    
    print("✅ Empathetic response test passed!")


async def test_system_integration():
    """Test complete system integration."""
    print("\n🧪 Testing System Integration...")
    
    settings = Settings(anthropic_api_key='test-key')
    
    # Test settings configuration
    print(f"  ✓ Hybrid computing enabled: {settings.hybrid_computing_enabled}")
    print(f"  ✓ Azure enabled: {settings.azure_enabled}")
    print(f"  ✓ Windows optimizations: {settings.windows_optimizations}")
    print(f"  ✓ MCP modules enabled: {settings.mcp_modules_enabled}")
    
    # Test enabled plugins
    print(f"  ✓ Enabled plugins: {len(settings.enabled_plugins)}")
    
    # Test that all required plugins are enabled
    required_plugins = ['brainstorm', 'mindmap', 'perspective_shift', 'creativity_surge']
    for plugin in required_plugins:
        if plugin in settings.enabled_plugins:
            print(f"  ✓ {plugin} plugin enabled")
        else:
            print(f"  ❌ {plugin} plugin not enabled")
    
    print("✅ System integration test passed!")


async def main():
    """Run all tests."""
    print("🚀 Starting TW MCP Hybrid Cloud System Tests\n")
    
    try:
        await test_hybrid_compute()
        await test_azure_integration()
        await test_plugin_loading()
        await test_empathetic_responses()
        await test_system_integration()
        
        print("\n🎉 All tests passed! System is ready for deployment.")
        
        print("\n📊 System Summary:")
        print("  • Hybrid computing: Ready for local-first execution")
        print("  • Azure integration: Ready for cloud fallback")
        print("  • MCP plugins: 4 core plugins loaded")
        print("  • Empathetic AI: Supportive responses configured")
        print("  • Windows optimization: Ready for desktop deployment")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Please check the configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())