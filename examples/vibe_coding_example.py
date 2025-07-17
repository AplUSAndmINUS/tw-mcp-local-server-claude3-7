"""
Example Vibe Coding MCP Plugin
==============================

This example demonstrates the vibe coding approach with Claude Sonnet 3.7,
focusing on empathy, understanding, and thoughtful programming assistance.
"""

import asyncio
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from mcp_server.claude_client import ClaudeClient
from mcp_server.config import load_settings

class VibeCodeExample:
    """Example vibe coding session."""
    
    def __init__(self):
        self.settings = load_settings()
        self.client = ClaudeClient(self.settings)
        
    async def demonstrate_empathy(self):
        """Demonstrate empathetic programming help."""
        print("🤗 Demonstrating Empathetic Programming Help")
        print("=" * 50)
        
        frustrated_request = """
        I'm really struggling with this Python code. I've been trying to sort a list of dictionaries 
        by multiple keys, but I keep getting errors. I feel like I'm missing something basic and it's 
        really frustrating. Can you help me understand what I'm doing wrong?
        
        My code:
        data = [{'name': 'Alice', 'age': 30, 'score': 85}, 
                {'name': 'Bob', 'age': 25, 'score': 90}, 
                {'name': 'Charlie', 'age': 35, 'score': 85}]
        
        sorted_data = sorted(data, key=lambda x: x['score'], x['age'])
        """
        
        response = await self.client.vibe_code(
            request=frustrated_request,
            context={"emotional_state": "frustrated", "experience_level": "intermediate"}
        )
        
        print(response.content)
        print("\n" + "=" * 50 + "\n")
    
    async def demonstrate_reassurance(self):
        """Demonstrate reassuring guidance."""
        print("🌟 Demonstrating Reassuring Guidance")
        print("=" * 50)
        
        uncertain_request = """
        I'm working on a web scraping project and I'm not sure if I'm doing it right. 
        I'm worried about getting blocked or causing problems. Is this approach okay?
        
        import requests
        from bs4 import BeautifulSoup
        
        for i in range(1000):
            url = f"https://example.com/page/{i}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # process data
        """
        
        response = await self.client.vibe_code(
            request=uncertain_request,
            context={"concern": "ethical_scraping", "experience_level": "beginner"}
        )
        
        print(response.content)
        print("\n" + "=" * 50 + "\n")
    
    async def demonstrate_deep_analysis(self):
        """Demonstrate deep technical analysis."""
        print("🔬 Demonstrating Deep Technical Analysis")
        print("=" * 50)
        
        complex_request = """
        I need to optimize this function for performance. It's part of a data processing pipeline 
        that handles millions of records. Can you help me understand the bottlenecks and suggest 
        improvements?
        
        def process_data(records):
            result = []
            for record in records:
                if record['status'] == 'active':
                    processed = {
                        'id': record['id'],
                        'value': record['value'] * 1.1,
                        'category': record['category'].upper(),
                        'timestamp': record['timestamp']
                    }
                    result.append(processed)
            return result
        """
        
        response = await self.client.vibe_code(
            request=complex_request,
            context={"focus": "performance", "scale": "millions_of_records"}
        )
        
        print(response.content)
        print("\n" + "=" * 50 + "\n")
    
    async def demonstrate_creative_problem_solving(self):
        """Demonstrate creative problem-solving approach."""
        print("🎨 Demonstrating Creative Problem Solving")
        print("=" * 50)
        
        creative_request = """
        I want to create a unique way to visualize my file system as a tree structure in the terminal, 
        but I want it to be more interesting than just printing folder names. Maybe something with 
        colors, sizes, or even ASCII art? I'm open to creative ideas!
        """
        
        response = await self.client.vibe_code(
            request=creative_request,
            context={"approach": "creative", "domain": "visualization"}
        )
        
        print(response.content)
        print("\n" + "=" * 50 + "\n")
    
    async def demonstrate_learning_support(self):
        """Demonstrate learning-focused support."""
        print("📚 Demonstrating Learning Support")
        print("=" * 50)
        
        learning_request = """
        I'm trying to understand decorators in Python. I've read about them but I'm still confused 
        about when and how to use them. Can you explain them in a way that really helps me 
        understand, maybe with some practical examples?
        """
        
        response = await self.client.vibe_code(
            request=learning_request,
            context={"learning_goal": "decorators", "explanation_style": "practical"}
        )
        
        print(response.content)
        print("\n" + "=" * 50 + "\n")
    
    async def run_full_demo(self):
        """Run the complete vibe coding demonstration."""
        print("🚀 Vibe Coding with Claude Sonnet 3.7")
        print("Demonstrating empathy, reassurance, kindness, understanding,")
        print("appreciation, deep-dive modeling, and strong reasoning")
        print("=" * 70)
        
        await self.demonstrate_empathy()
        await self.demonstrate_reassurance()
        await self.demonstrate_deep_analysis()
        await self.demonstrate_creative_problem_solving()
        await self.demonstrate_learning_support()
        
        print("✨ Demo complete! This is the power of vibe coding:")
        print("- Empathetic understanding of developer needs")
        print("- Reassuring guidance that builds confidence")
        print("- Deep technical analysis with clear reasoning")
        print("- Creative problem-solving approaches")
        print("- Learning-focused explanations")
        print("- Appreciation for the complexity of programming")

async def main():
    """Main function to run the example."""
    try:
        example = VibeCodeExample()
        await example.run_full_demo()
    except Exception as e:
        print(f"Error running example: {e}")
        print("Make sure you have set your ANTHROPIC_API_KEY in the .env file")

if __name__ == "__main__":
    asyncio.run(main())