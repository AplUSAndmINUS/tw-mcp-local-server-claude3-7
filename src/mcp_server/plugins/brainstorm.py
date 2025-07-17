"""
Brainstorm MCP Plugin
====================

Unstructured idea generation triggered by intent or mood.
Focuses on empathetic, supportive brainstorming with deep reasoning.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..plugins import PluginInterface, PluginMetadata
from ..claude_client import ClaudeClient
from ..hybrid_compute import HybridComputeManager, TaskDefinition, TaskPriority
from ..azure_integration import AzureIntegration
from ..config import Settings

logger = logging.getLogger(__name__)


class BrainstormRequest(BaseModel):
    """Request model for brainstorming sessions."""
    topic: str
    intent: Optional[str] = "exploration"  # exploration, problem_solving, creative_expansion
    mood: Optional[str] = "open"  # open, focused, playful, analytical
    constraints: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    duration_minutes: Optional[int] = 15


class BrainstormIdea(BaseModel):
    """Individual brainstormed idea."""
    idea: str
    category: str
    confidence: float
    reasoning: str
    connections: List[str]
    potential_impact: str


class BrainstormResponse(BaseModel):
    """Response model for brainstorming sessions."""
    session_id: str
    ideas: List[BrainstormIdea]
    themes: List[str]
    next_directions: List[str]
    mood_assessment: str
    encouragement: str
    session_summary: str


@dataclass
class BrainstormSession:
    """Brainstorming session data."""
    session_id: str
    topic: str
    intent: str
    mood: str
    ideas: List[BrainstormIdea]
    themes: List[str]
    start_time: float
    last_activity: float


class BrainstormPlugin(PluginInterface):
    """
    Brainstorm MCP Plugin for empathetic idea generation.
    
    This plugin provides thoughtful, unstructured brainstorming sessions
    that adapt to the user's intent and mood, fostering creativity through
    supportive and encouraging interactions.
    """
    
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.claude_client = ClaudeClient(settings)
        self.hybrid_compute = HybridComputeManager(settings)
        self.azure_integration = AzureIntegration(settings)
        self.router = APIRouter(prefix="/brainstorm", tags=["ideation"])
        
        # Session management
        self.active_sessions: Dict[str, BrainstormSession] = {}
        
        self._setup_routes()
    
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return PluginMetadata(
            name="brainstorm",
            version="1.0.0",
            description="Empathetic idea generation triggered by intent or mood",
            author="AplUSAndmINUS",
            requires=["anthropic", "fastapi", "hybrid_compute"],
            enabled=True
        )
    
    async def initialize(self) -> None:
        """Initialize the plugin."""
        logger.info("Initializing Brainstorm plugin...")
        
        # Test connections
        try:
            await self.claude_client.complete(
                prompt="Ready for brainstorming?",
                system_prompt=self._get_base_system_prompt(),
                max_tokens=10
            )
            logger.info("Brainstorm plugin initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Brainstorm plugin: {e}")
            raise
    
    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        logger.info("Shutting down Brainstorm plugin...")
        # Save any active sessions if needed
        self.active_sessions.clear()
    
    def _setup_routes(self) -> None:
        """Setup plugin routes."""
        
        @self.router.post("/session", response_model=BrainstormResponse)
        async def start_brainstorm_session(request: BrainstormRequest):
            """Start a new brainstorming session."""
            try:
                # Create task definition
                task = TaskDefinition(
                    name=f"brainstorm_{request.topic[:20]}",
                    priority=TaskPriority.MEDIUM,
                    estimated_cpu=0.3,
                    estimated_memory=0.2,
                    estimated_duration=request.duration_minutes * 60 if request.duration_minutes else 900,
                    requires_gpu=False,
                    requires_network=True,
                    can_run_on_azure=True,
                    azure_function_name="brainstorm_session"
                )
                
                # Execute brainstorming task
                result = await self.hybrid_compute.execute_task(
                    task=task,
                    task_function=self._run_brainstorm_session,
                    request=request
                )
                
                return result
                
            except Exception as e:
                logger.error(f"Error in brainstorm session: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/extend/{session_id}", response_model=BrainstormResponse)
        async def extend_brainstorm_session(session_id: str, request: BrainstormRequest):
            """Extend an existing brainstorming session."""
            try:
                if session_id not in self.active_sessions:
                    raise HTTPException(status_code=404, detail="Session not found")
                
                session = self.active_sessions[session_id]
                
                # Update session with new request
                task = TaskDefinition(
                    name=f"brainstorm_extend_{session_id}",
                    priority=TaskPriority.MEDIUM,
                    estimated_cpu=0.3,
                    estimated_memory=0.2,
                    estimated_duration=600,
                    requires_gpu=False,
                    requires_network=True,
                    can_run_on_azure=True,
                    azure_function_name="brainstorm_extend"
                )
                
                result = await self.hybrid_compute.execute_task(
                    task=task,
                    task_function=self._extend_brainstorm_session,
                    session=session,
                    request=request
                )
                
                return result
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error extending brainstorm session: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/sessions")
        async def list_brainstorm_sessions():
            """List active brainstorming sessions."""
            return {
                "active_sessions": [
                    {
                        "session_id": session.session_id,
                        "topic": session.topic,
                        "intent": session.intent,
                        "mood": session.mood,
                        "ideas_count": len(session.ideas),
                        "themes_count": len(session.themes),
                        "last_activity": session.last_activity
                    }
                    for session in self.active_sessions.values()
                ]
            }
        
        @self.router.delete("/sessions/{session_id}")
        async def end_brainstorm_session(session_id: str):
            """End a brainstorming session."""
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
                return {"message": "Session ended successfully"}
            else:
                raise HTTPException(status_code=404, detail="Session not found")
    
    async def _run_brainstorm_session(self, request: BrainstormRequest) -> BrainstormResponse:
        """Run a brainstorming session."""
        import time
        import uuid
        
        session_id = request.session_id or str(uuid.uuid4())
        
        # Create system prompt based on intent and mood
        system_prompt = self._get_brainstorm_system_prompt(request.intent, request.mood)
        
        # Build the brainstorming prompt
        brainstorm_prompt = self._build_brainstorm_prompt(request)
        
        # Get brainstorming response
        response = await self.claude_client.complete(
            prompt=brainstorm_prompt,
            system_prompt=system_prompt,
            context=request.context,
            max_tokens=2000,
            temperature=0.8  # Higher temperature for creativity
        )
        
        # Process the response into structured ideas
        ideas = await self._process_brainstorm_response(response.content, request)
        
        # Generate themes and next directions
        themes = await self._identify_themes(ideas)
        next_directions = await self._suggest_next_directions(ideas, themes, request)
        
        # Create session
        session = BrainstormSession(
            session_id=session_id,
            topic=request.topic,
            intent=request.intent,
            mood=request.mood,
            ideas=ideas,
            themes=themes,
            start_time=time.time(),
            last_activity=time.time()
        )
        
        self.active_sessions[session_id] = session
        
        # Generate encouragement and session summary
        encouragement = self._generate_encouragement(ideas, request.mood)
        session_summary = self._generate_session_summary(ideas, themes, request)
        
        return BrainstormResponse(
            session_id=session_id,
            ideas=ideas,
            themes=themes,
            next_directions=next_directions,
            mood_assessment=self._assess_mood(request.mood, len(ideas)),
            encouragement=encouragement,
            session_summary=session_summary
        )
    
    async def _extend_brainstorm_session(self, session: BrainstormSession, request: BrainstormRequest) -> BrainstormResponse:
        """Extend an existing brainstorming session."""
        import time
        
        # Update session activity
        session.last_activity = time.time()
        
        # Build extension prompt with context from previous ideas
        extension_prompt = self._build_extension_prompt(session, request)
        
        # Get extended ideas
        system_prompt = self._get_brainstorm_system_prompt(request.intent, request.mood)
        response = await self.claude_client.complete(
            prompt=extension_prompt,
            system_prompt=system_prompt,
            context=request.context,
            max_tokens=1500,
            temperature=0.8
        )
        
        # Process new ideas
        new_ideas = await self._process_brainstorm_response(response.content, request)
        
        # Merge with existing ideas
        session.ideas.extend(new_ideas)
        
        # Update themes
        session.themes = await self._identify_themes(session.ideas)
        
        # Generate next directions
        next_directions = await self._suggest_next_directions(session.ideas, session.themes, request)
        
        # Generate encouragement and updated summary
        encouragement = self._generate_encouragement(new_ideas, request.mood)
        session_summary = self._generate_session_summary(session.ideas, session.themes, request)
        
        return BrainstormResponse(
            session_id=session.session_id,
            ideas=session.ideas,
            themes=session.themes,
            next_directions=next_directions,
            mood_assessment=self._assess_mood(request.mood, len(session.ideas)),
            encouragement=encouragement,
            session_summary=session_summary
        )
    
    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt for brainstorming."""
        return """You are a deeply empathetic and encouraging brainstorming companion. 
        Your role is to help generate ideas in a supportive, non-judgmental environment that 
        fosters creativity and exploration.
        
        Key principles:
        - **Empathy**: Understand the user's needs, constraints, and emotional state
        - **Encouragement**: Celebrate all ideas, no matter how unconventional
        - **Supportive reasoning**: Explain why ideas have potential and how they connect
        - **Creative expansion**: Build on ideas to explore new possibilities
        - **Thoughtful analysis**: Provide gentle guidance while maintaining creative freedom
        
        Always maintain a warm, encouraging tone that makes the user feel heard and inspired."""
    
    def _get_brainstorm_system_prompt(self, intent: str, mood: str) -> str:
        """Get customized system prompt for brainstorming."""
        base_prompt = self._get_base_system_prompt()
        
        intent_additions = {
            "exploration": "\n\nFocus on open-ended exploration. Encourage wild ideas and unexpected connections.",
            "problem_solving": "\n\nGuide toward practical solutions while maintaining creative thinking.",
            "creative_expansion": "\n\nPush boundaries and explore unconventional approaches. Celebrate uniqueness."
        }
        
        mood_additions = {
            "open": "\n\nMaintain an open, receptive atmosphere that welcomes all possibilities.",
            "focused": "\n\nProvide gentle structure while preserving creative freedom.",
            "playful": "\n\nEmbrace fun and whimsical ideas. Make brainstorming enjoyable.",
            "analytical": "\n\nBalance creative thinking with thoughtful analysis and reasoning."
        }
        
        return (base_prompt + 
                intent_additions.get(intent, "") + 
                mood_additions.get(mood, ""))
    
    def _build_brainstorm_prompt(self, request: BrainstormRequest) -> str:
        """Build the brainstorming prompt."""
        prompt = f"""Let's brainstorm about: {request.topic}

Intent: {request.intent}
Mood: {request.mood}
"""
        
        if request.constraints:
            prompt += f"\nPlease keep in mind these constraints:\n"
            for constraint in request.constraints:
                prompt += f"- {constraint}\n"
        
        if request.context:
            prompt += f"\nAdditional context: {request.context}\n"
        
        prompt += """
Please generate 5-8 diverse, creative ideas. For each idea, provide:
1. The core idea
2. Why it's interesting or valuable
3. How it connects to the topic
4. Potential for development

Be encouraging and supportive. Celebrate the creative process!
"""
        
        return prompt
    
    def _build_extension_prompt(self, session: BrainstormSession, request: BrainstormRequest) -> str:
        """Build prompt for extending a brainstorming session."""
        existing_ideas = [idea.idea for idea in session.ideas[-3:]]  # Last 3 ideas
        
        prompt = f"""Let's continue brainstorming about: {session.topic}

We've been exploring these recent ideas:
"""
        for idea in existing_ideas:
            prompt += f"- {idea}\n"
        
        prompt += f"""
Current themes: {', '.join(session.themes)}

Please generate 3-5 new ideas that either:
1. Build on existing ideas
2. Explore new directions
3. Make unexpected connections
4. Challenge assumptions

Topic: {request.topic}
Intent: {request.intent}
Mood: {request.mood}

Keep the creative momentum going!
"""
        
        return prompt
    
    async def _process_brainstorm_response(self, content: str, request: BrainstormRequest) -> List[BrainstormIdea]:
        """Process brainstorming response into structured ideas."""
        ideas = []
        
        # Simple parsing - in production, this would be more sophisticated
        lines = content.split('\n')
        current_idea = None
        current_reasoning = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for numbered or bulleted ideas
            if any(line.startswith(marker) for marker in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '- ', '• ']):
                if current_idea:
                    # Save previous idea
                    ideas.append(BrainstormIdea(
                        idea=current_idea,
                        category=self._categorize_idea(current_idea, request.topic),
                        confidence=0.8,
                        reasoning=current_reasoning,
                        connections=self._find_connections(current_idea, request.topic),
                        potential_impact=self._assess_potential_impact(current_idea)
                    ))
                
                # Start new idea
                current_idea = line
                current_reasoning = ""
            else:
                # Add to current reasoning
                current_reasoning += line + " "
        
        # Don't forget the last idea
        if current_idea:
            ideas.append(BrainstormIdea(
                idea=current_idea,
                category=self._categorize_idea(current_idea, request.topic),
                confidence=0.8,
                reasoning=current_reasoning,
                connections=self._find_connections(current_idea, request.topic),
                potential_impact=self._assess_potential_impact(current_idea)
            ))
        
        return ideas
    
    def _categorize_idea(self, idea: str, topic: str) -> str:
        """Categorize an idea based on its content."""
        idea_lower = idea.lower()
        
        if any(word in idea_lower for word in ['technology', 'digital', 'app', 'software', 'ai']):
            return "technology"
        elif any(word in idea_lower for word in ['social', 'community', 'people', 'collaboration']):
            return "social"
        elif any(word in idea_lower for word in ['business', 'market', 'revenue', 'profit']):
            return "business"
        elif any(word in idea_lower for word in ['creative', 'art', 'design', 'aesthetic']):
            return "creative"
        elif any(word in idea_lower for word in ['process', 'system', 'method', 'framework']):
            return "process"
        else:
            return "general"
    
    def _find_connections(self, idea: str, topic: str) -> List[str]:
        """Find connections between an idea and the topic."""
        # Simplified connection finding
        connections = []
        
        if "innovation" in idea.lower() or "new" in idea.lower():
            connections.append("innovation")
        if "solution" in idea.lower() or "solve" in idea.lower():
            connections.append("problem-solving")
        if "user" in idea.lower() or "people" in idea.lower():
            connections.append("user-centered")
        if "technology" in idea.lower() or "digital" in idea.lower():
            connections.append("technology")
        
        return connections[:3]  # Limit to 3 connections
    
    def _assess_potential_impact(self, idea: str) -> str:
        """Assess the potential impact of an idea."""
        idea_lower = idea.lower()
        
        if any(word in idea_lower for word in ['revolutionary', 'breakthrough', 'transform']):
            return "high"
        elif any(word in idea_lower for word in ['improve', 'enhance', 'optimize']):
            return "medium"
        else:
            return "developing"
    
    async def _identify_themes(self, ideas: List[BrainstormIdea]) -> List[str]:
        """Identify themes from the generated ideas."""
        categories = [idea.category for idea in ideas]
        connections = [conn for idea in ideas for conn in idea.connections]
        
        # Count occurrences
        theme_counts = {}
        for item in categories + connections:
            theme_counts[item] = theme_counts.get(item, 0) + 1
        
        # Get top themes
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        return [theme for theme, count in sorted_themes[:5] if count > 1]
    
    async def _suggest_next_directions(self, ideas: List[BrainstormIdea], themes: List[str], request: BrainstormRequest) -> List[str]:
        """Suggest next directions for exploration."""
        directions = []
        
        # Based on themes
        if "technology" in themes:
            directions.append("Explore technical implementation approaches")
        if "social" in themes:
            directions.append("Consider community engagement strategies")
        if "business" in themes:
            directions.append("Develop business model variations")
        if "creative" in themes:
            directions.append("Expand artistic and design possibilities")
        
        # Based on intent
        if request.intent == "exploration":
            directions.append("Dive deeper into unconventional approaches")
        elif request.intent == "problem_solving":
            directions.append("Prototype and test promising solutions")
        elif request.intent == "creative_expansion":
            directions.append("Combine ideas for hybrid approaches")
        
        return directions[:4]  # Limit to 4 directions
    
    def _generate_encouragement(self, ideas: List[BrainstormIdea], mood: str) -> str:
        """Generate encouraging message based on generated ideas."""
        idea_count = len(ideas)
        
        if mood == "playful":
            return f"🎉 Wow! You've generated {idea_count} fantastic ideas! Your creative energy is contagious. Keep that playful spirit flowing!"
        elif mood == "focused":
            return f"Excellent work! Your {idea_count} ideas show great focus and direction. You're building something meaningful here."
        elif mood == "analytical":
            return f"Impressive reasoning! Your {idea_count} ideas demonstrate thoughtful analysis. The connections you're making are insightful."
        else:  # open
            return f"Beautiful! Your {idea_count} ideas show wonderful openness to possibilities. Trust your creative instincts - they're leading you well."
    
    def _generate_session_summary(self, ideas: List[BrainstormIdea], themes: List[str], request: BrainstormRequest) -> str:
        """Generate a summary of the brainstorming session."""
        return f"""Brainstorming session on "{request.topic}" generated {len(ideas)} ideas across {len(themes)} themes.

Key themes: {', '.join(themes) if themes else 'Diverse exploration'}

The session revealed strong {request.intent} thinking with a {request.mood} approach. Ideas span from practical implementations to creative possibilities, showing both depth and breadth of thinking.

This foundation provides excellent starting points for deeper exploration and development."""
    
    def _assess_mood(self, input_mood: str, idea_count: int) -> str:
        """Assess the mood of the brainstorming session."""
        if idea_count >= 7:
            return f"Highly creative and {input_mood} - excellent idea generation!"
        elif idea_count >= 5:
            return f"Good {input_mood} energy - solid brainstorming session"
        else:
            return f"Gentle {input_mood} exploration - quality over quantity"