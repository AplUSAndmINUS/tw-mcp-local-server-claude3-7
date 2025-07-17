"""
Vibe Coder Plugin
================

A specialized plugin for empathetic, thoughtful programming assistance.
Focuses on understanding, kindness, and deep technical insights.
"""

import logging
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import PluginInterface, PluginMetadata, plugin_route, plugin_hook
from ..claude_client import ClaudeClient, ClaudeResponse
from ..config import Settings

logger = logging.getLogger(__name__)


class VibeRequest(BaseModel):
    """Request model for vibe coding."""
    request: str
    context: Optional[Dict[str, Any]] = None
    mood: Optional[str] = "supportive"  # supportive, encouraging, analytical, creative
    focus: Optional[str] = "general"  # general, performance, readability, architecture
    experience_level: Optional[str] = "intermediate"  # beginner, intermediate, advanced


class VibeResponse(BaseModel):
    """Response model for vibe coding."""
    response: str
    suggestions: list[str]
    resources: list[str]
    confidence: float
    reasoning: str


class VibeCoderPlugin(PluginInterface):
    """
    Vibe Coder Plugin for empathetic programming assistance.
    
    This plugin provides thoughtful, understanding, and encouraging
    programming help with a focus on the developer's emotional and
    technical needs.
    """
    
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.claude_client = ClaudeClient(settings)
        self.router = APIRouter(prefix="/vibe", tags=["vibe-coding"])
        self._setup_routes()
    
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return PluginMetadata(
            name="vibe_coder",
            version="1.0.0",
            description="Empathetic programming companion with deep technical insights",
            author="AplUSAndmINUS",
            requires=["anthropic", "fastapi"],
            enabled=True
        )
    
    async def initialize(self) -> None:
        """Initialize the plugin."""
        logger.info("Initializing Vibe Coder plugin...")
        
        # Test Claude connection
        try:
            test_response = await self.claude_client.complete(
                prompt="Hello, can you help me with programming?",
                system_prompt=self._get_base_system_prompt(),
                max_tokens=50
            )
            logger.info("Vibe Coder plugin initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Vibe Coder: {str(e)}")
            raise
    
    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        logger.info("Shutting down Vibe Coder plugin...")
    
    def _setup_routes(self) -> None:
        """Setup plugin routes."""
        
        @self.router.post("/code", response_model=VibeResponse)
        async def vibe_code(request: VibeRequest):
            """Generate code with vibe coding approach."""
            try:
                system_prompt = self._get_system_prompt(
                    mood=request.mood,
                    focus=request.focus,
                    experience_level=request.experience_level
                )
                
                response = await self.claude_client.complete(
                    prompt=request.request,
                    system_prompt=system_prompt,
                    context=request.context
                )
                
                return await self._process_response(response, request)
                
            except Exception as e:
                logger.error(f"Error in vibe coding: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/review")
        async def vibe_review(request: VibeRequest):
            """Review code with empathetic feedback."""
            try:
                system_prompt = self._get_review_system_prompt(
                    mood=request.mood,
                    experience_level=request.experience_level
                )
                
                response = await self.claude_client.complete(
                    prompt=f"Please review this code:\n{request.request}",
                    system_prompt=system_prompt,
                    context=request.context
                )
                
                return await self._process_response(response, request)
                
            except Exception as e:
                logger.error(f"Error in vibe review: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/explain")
        async def vibe_explain(request: VibeRequest):
            """Explain code concepts with patience and clarity."""
            try:
                system_prompt = self._get_explanation_system_prompt(
                    experience_level=request.experience_level
                )
                
                response = await self.claude_client.complete(
                    prompt=f"Please explain this code or concept:\n{request.request}",
                    system_prompt=system_prompt,
                    context=request.context
                )
                
                return await self._process_response(response, request)
                
            except Exception as e:
                logger.error(f"Error in vibe explanation: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
    
    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt for vibe coding."""
        return """You are a thoughtful, empathetic programming companion with deep technical expertise. 
        You understand that coding is both an art and a science, and you approach each request with:
        
        - **Empathy**: Understanding the developer's needs, frustrations, and goals
        - **Reassurance**: Providing confidence and encouragement, especially when things get challenging
        - **Kindness**: Being patient and supportive in your explanations, never condescending
        - **Understanding**: Grasping the broader context and long-term objectives
        - **Appreciation**: Recognizing the complexity and creativity inherent in programming
        - **Deep-dive modeling**: Providing thorough, well-reasoned solutions with clear explanations
        - **Strong reasoning**: Explaining the "why" behind every recommendation and decision
        
        You create code that is not just functional, but elegant, maintainable, and thoughtfully designed.
        You explain your reasoning clearly, offer alternatives when appropriate, and always consider the
        human behind the code."""
    
    def _get_system_prompt(self, mood: str, focus: str, experience_level: str) -> str:
        """Get a customized system prompt based on parameters."""
        base_prompt = self._get_base_system_prompt()
        
        mood_additions = {
            "supportive": "\n\nBe especially supportive and encouraging. Acknowledge challenges and provide reassurance.",
            "encouraging": "\n\nFocus on building confidence and motivation. Celebrate progress and potential.",
            "analytical": "\n\nProvide deep technical analysis while maintaining warmth and understanding.",
            "creative": "\n\nEncourage creative thinking and innovative solutions. Explore alternative approaches."
        }
        
        focus_additions = {
            "performance": "\n\nFocus on performance optimization while explaining the trade-offs clearly.",
            "readability": "\n\nEmphasize code clarity and maintainability. Make suggestions for better documentation.",
            "architecture": "\n\nConsider system design and architectural patterns. Think about scalability and maintainability.",
            "general": "\n\nProvide well-rounded advice covering multiple aspects of good programming."
        }
        
        experience_additions = {
            "beginner": "\n\nExplain concepts clearly with examples. Avoid jargon and provide step-by-step guidance.",
            "intermediate": "\n\nProvide balanced explanations with some technical depth. Include best practices.",
            "advanced": "\n\nEngage in deeper technical discussions. Assume familiarity with core concepts."
        }
        
        return (base_prompt + 
                mood_additions.get(mood, "") + 
                focus_additions.get(focus, "") + 
                experience_additions.get(experience_level, ""))
    
    def _get_review_system_prompt(self, mood: str, experience_level: str) -> str:
        """Get system prompt for code review."""
        base = self._get_base_system_prompt()
        
        review_addition = """
        
        When reviewing code, focus on:
        1. **Positive aspects**: Start by acknowledging what's working well
        2. **Constructive feedback**: Provide specific, actionable suggestions
        3. **Learning opportunities**: Explain the reasoning behind suggestions
        4. **Encouragement**: Maintain a supportive tone throughout
        5. **Practical impact**: Consider real-world implications of changes
        
        Structure your review to be helpful rather than critical, focusing on growth and improvement."""
        
        return self._get_system_prompt(mood, "general", experience_level) + review_addition
    
    def _get_explanation_system_prompt(self, experience_level: str) -> str:
        """Get system prompt for explanations."""
        base = self._get_base_system_prompt()
        
        explanation_addition = """
        
        When explaining concepts:
        1. **Start with the big picture**: Provide context and motivation
        2. **Break down complexity**: Use analogies and examples
        3. **Show progression**: Build understanding step by step
        4. **Encourage questions**: Make it clear that confusion is normal
        5. **Provide resources**: Suggest further learning opportunities
        
        Remember that understanding takes time, and everyone learns differently."""
        
        return self._get_system_prompt("supportive", "general", experience_level) + explanation_addition
    
    async def _process_response(self, claude_response: ClaudeResponse, request: VibeRequest) -> VibeResponse:
        """Process Claude response into structured vibe response."""
        content = claude_response.content
        
        # Extract suggestions (look for bullet points or numbered lists)
        suggestions = []
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith(('- ', '• ', '* ', '1. ', '2. ', '3. ')):
                suggestions.append(line.strip())
        
        # Generate resources based on the request
        resources = await self._generate_resources(request)
        
        # Calculate confidence based on response length and structure
        confidence = min(0.9, max(0.6, len(content) / 1000))
        
        # Extract reasoning (look for explanations)
        reasoning = "Based on best practices and the specific context provided."
        if "because" in content.lower() or "reason" in content.lower():
            reasoning = "Detailed reasoning provided in the response above."
        
        return VibeResponse(
            response=content,
            suggestions=suggestions[:5],  # Limit to top 5 suggestions
            resources=resources,
            confidence=confidence,
            reasoning=reasoning
        )
    
    async def _generate_resources(self, request: VibeRequest) -> list[str]:
        """Generate relevant learning resources."""
        resources = []
        
        # Basic programming resources
        if request.experience_level == "beginner":
            resources.extend([
                "Python Official Documentation",
                "Real Python Tutorials",
                "Automate the Boring Stuff with Python"
            ])
        elif request.experience_level == "intermediate":
            resources.extend([
                "Clean Code by Robert Martin",
                "Effective Python by Brett Slatkin",
                "Python Tricks by Dan Bader"
            ])
        else:  # advanced
            resources.extend([
                "Architecture Patterns with Python",
                "Fluent Python by Luciano Ramalho",
                "High Performance Python"
            ])
        
        # Focus-specific resources
        if request.focus == "performance":
            resources.append("Python Performance Tuning Guide")
        elif request.focus == "architecture":
            resources.append("System Design Primer")
        elif request.focus == "readability":
            resources.append("PEP 8 Style Guide")
        
        return resources[:3]  # Limit to 3 resources
    
    @plugin_hook("pre_request")
    async def pre_request_hook(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process requests before they're sent to Claude."""
        # Add vibe coding context
        if "vibe" in request_data.get("path", ""):
            request_data["context"] = request_data.get("context", {})
            request_data["context"]["vibe_mode"] = True
        
        return request_data
    
    @plugin_hook("post_response")
    async def post_response_hook(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process responses after they're received from Claude."""
        # Add encouragement to vibe responses
        if response_data.get("context", {}).get("vibe_mode"):
            response_data["encouragement"] = "You're doing great! Keep coding with confidence. 🚀"
        
        return response_data


# CLI command for standalone vibe coding
def main():
    """Main CLI entry point for vibe coding."""
    import asyncio
    import typer
    from rich.console import Console
    from rich.panel import Panel
    
    app = typer.Typer(help="Vibe Coder - Empathetic Programming Assistant")
    console = Console()
    
    @app.command()
    def code(
        request: str = typer.Argument(..., help="Your coding request"),
        mood: str = typer.Option("supportive", help="Mood: supportive, encouraging, analytical, creative"),
        focus: str = typer.Option("general", help="Focus: general, performance, readability, architecture"),
        experience: str = typer.Option("intermediate", help="Experience level: beginner, intermediate, advanced")
    ):
        """Generate code with vibe coding approach."""
        async def run_vibe_code():
            settings = Settings()
            plugin = VibeCoderPlugin(settings)
            await plugin.initialize()
            
            vibe_request = VibeRequest(
                request=request,
                mood=mood,
                focus=focus,
                experience_level=experience
            )
            
            response = await plugin.claude_client.vibe_code(
                request=vibe_request.request,
                context={"mood": mood, "focus": focus, "experience": experience}
            )
            
            console.print(Panel(response.content, title="Vibe Coder Response", border_style="green"))
        
        asyncio.run(run_vibe_code())
    
    app()


if __name__ == "__main__":
    main()