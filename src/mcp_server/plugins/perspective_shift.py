"""
Perspective Shift MCP Plugin
===========================

Prompts that reframe questions or challenge defaults with empathy and insight.
Helps users see problems from new angles with supportive reasoning.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..plugins import PluginInterface, PluginMetadata
from ..claude_client import ClaudeClient
from ..hybrid_compute import HybridComputeManager, TaskDefinition, TaskPriority
from ..config import Settings

logger = logging.getLogger(__name__)


class PerspectiveType(Enum):
    """Types of perspective shifts."""
    REFRAME = "reframe"
    CHALLENGE = "challenge"
    ALTERNATIVE = "alternative"
    OPPOSITE = "opposite"
    STAKEHOLDER = "stakeholder"
    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"


class PerspectiveShiftRequest(BaseModel):
    """Request model for perspective shifting."""
    original_question: str
    shift_type: PerspectiveType
    context: Optional[Dict[str, Any]] = None
    intensity: Optional[str] = "moderate"  # gentle, moderate, strong
    focus_area: Optional[str] = None
    target_audience: Optional[str] = None
    desired_outcome: Optional[str] = "insight"  # insight, solution, creativity, clarity


class PerspectiveShiftResponse(BaseModel):
    """Response model for perspective shifting."""
    original_question: str
    shifted_perspectives: List[str]
    reframed_questions: List[str]
    insights: List[str]
    reasoning: str
    empathetic_guidance: str
    next_steps: List[str]
    confidence_level: float


class PerspectiveShiftPlugin(PluginInterface):
    """
    Perspective Shift MCP Plugin for empathetic reframing.
    
    Helps users examine problems, questions, and challenges from new angles
    with supportive guidance and thoughtful reasoning.
    """
    
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.claude_client = ClaudeClient(settings)
        self.hybrid_compute = HybridComputeManager(settings)
        self.router = APIRouter(prefix="/perspective-shift", tags=["ideation"])
        
        # Perspective shift techniques
        self.shift_techniques = {
            PerspectiveType.REFRAME: self._reframe_perspective,
            PerspectiveType.CHALLENGE: self._challenge_perspective,
            PerspectiveType.ALTERNATIVE: self._alternative_perspective,
            PerspectiveType.OPPOSITE: self._opposite_perspective,
            PerspectiveType.STAKEHOLDER: self._stakeholder_perspective,
            PerspectiveType.TEMPORAL: self._temporal_perspective,
            PerspectiveType.CONTEXTUAL: self._contextual_perspective,
        }
        
        self._setup_routes()
    
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return PluginMetadata(
            name="perspective_shift",
            version="1.0.0",
            description="Empathetic perspective shifting and reframing with supportive reasoning",
            author="AplUSAndmINUS",
            requires=["anthropic", "fastapi", "hybrid_compute"],
            enabled=True
        )
    
    async def initialize(self) -> None:
        """Initialize the plugin."""
        logger.info("Initializing Perspective Shift plugin...")
        
        try:
            # Test Claude connection
            await self.claude_client.complete(
                prompt="Ready to explore new perspectives?",
                system_prompt=self._get_base_system_prompt(),
                max_tokens=10
            )
            logger.info("Perspective Shift plugin initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Perspective Shift plugin: {e}")
            raise
    
    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        logger.info("Shutting down Perspective Shift plugin...")
    
    def _setup_routes(self) -> None:
        """Setup plugin routes."""
        
        @self.router.post("/shift", response_model=PerspectiveShiftResponse)
        async def shift_perspective(request: PerspectiveShiftRequest):
            """Generate perspective shifts for a question or problem."""
            try:
                task = TaskDefinition(
                    name=f"perspective_shift_{request.shift_type.value}",
                    priority=TaskPriority.MEDIUM,
                    estimated_cpu=0.3,
                    estimated_memory=0.2,
                    estimated_duration=240,
                    requires_gpu=False,
                    requires_network=True,
                    can_run_on_azure=True,
                    azure_function_name="perspective_shift"
                )
                
                result = await self.hybrid_compute.execute_task(
                    task=task,
                    task_function=self._generate_perspective_shifts,
                    request=request
                )
                
                return result
                
            except Exception as e:
                logger.error(f"Error in perspective shift: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/multi-shift", response_model=List[PerspectiveShiftResponse])
        async def multi_perspective_shift(request: PerspectiveShiftRequest):
            """Generate multiple types of perspective shifts."""
            try:
                # Generate shifts for all types
                shift_types = [
                    PerspectiveType.REFRAME,
                    PerspectiveType.CHALLENGE,
                    PerspectiveType.ALTERNATIVE,
                    PerspectiveType.STAKEHOLDER
                ]
                
                results = []
                for shift_type in shift_types:
                    shift_request = PerspectiveShiftRequest(
                        original_question=request.original_question,
                        shift_type=shift_type,
                        context=request.context,
                        intensity=request.intensity,
                        focus_area=request.focus_area,
                        target_audience=request.target_audience,
                        desired_outcome=request.desired_outcome
                    )
                    
                    result = await self._generate_perspective_shifts(shift_request)
                    results.append(result)
                
                return results
                
            except Exception as e:
                logger.error(f"Error in multi-perspective shift: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/shift-types")
        async def get_shift_types():
            """Get available perspective shift types."""
            return {
                "shift_types": [
                    {
                        "type": shift_type.value,
                        "description": self._get_shift_type_description(shift_type)
                    }
                    for shift_type in PerspectiveType
                ]
            }
    
    async def _generate_perspective_shifts(self, request: PerspectiveShiftRequest) -> PerspectiveShiftResponse:
        """Generate perspective shifts for the given request."""
        
        # Get the appropriate technique
        technique = self.shift_techniques.get(request.shift_type)
        if not technique:
            raise ValueError(f"Unknown shift type: {request.shift_type}")
        
        # Generate shifts using the technique
        shifts = await technique(request)
        
        # Generate reframed questions
        reframed_questions = await self._generate_reframed_questions(request, shifts)
        
        # Generate insights
        insights = await self._generate_insights(request, shifts)
        
        # Generate reasoning
        reasoning = await self._generate_reasoning(request, shifts)
        
        # Generate empathetic guidance
        empathetic_guidance = self._generate_empathetic_guidance(request, shifts)
        
        # Generate next steps
        next_steps = await self._generate_next_steps(request, shifts)
        
        # Calculate confidence level
        confidence_level = self._calculate_confidence_level(request, shifts)
        
        return PerspectiveShiftResponse(
            original_question=request.original_question,
            shifted_perspectives=shifts,
            reframed_questions=reframed_questions,
            insights=insights,
            reasoning=reasoning,
            empathetic_guidance=empathetic_guidance,
            next_steps=next_steps,
            confidence_level=confidence_level
        )
    
    async def _reframe_perspective(self, request: PerspectiveShiftRequest) -> List[str]:
        """Reframe the question or problem."""
        
        system_prompt = self._get_reframe_system_prompt(request.intensity)
        
        prompt = f"""Reframe this question to reveal new insights: "{request.original_question}"

Context: {request.context if request.context else 'General exploration'}
Intensity: {request.intensity}
Focus: {request.focus_area if request.focus_area else 'General reframing'}
Desired outcome: {request.desired_outcome}

Provide 3-4 thoughtful reframes that:
1. Maintain the core intent while changing perspective
2. Open new avenues for thinking
3. Challenge assumptions gently
4. Provide fresh angles for exploration

Be empathetic and supportive in your reframes."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.7
        )
        
        return self._parse_perspectives(response.content)
    
    async def _challenge_perspective(self, request: PerspectiveShiftRequest) -> List[str]:
        """Challenge assumptions in the question."""
        
        system_prompt = self._get_challenge_system_prompt(request.intensity)
        
        prompt = f"""Gently challenge the assumptions in this question: "{request.original_question}"

Context: {request.context if request.context else 'General exploration'}
Intensity: {request.intensity}
Desired outcome: {request.desired_outcome}

Identify 3-4 assumptions and challenge them constructively:
1. What assumptions are embedded in this question?
2. How might these assumptions limit thinking?
3. What would happen if we questioned these assumptions?
4. What new possibilities emerge when we challenge them?

Be supportive and encouraging while challenging - the goal is growth, not criticism."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.6
        )
        
        return self._parse_perspectives(response.content)
    
    async def _alternative_perspective(self, request: PerspectiveShiftRequest) -> List[str]:
        """Generate alternative viewpoints."""
        
        system_prompt = self._get_alternative_system_prompt(request.intensity)
        
        prompt = f"""Generate alternative perspectives for: "{request.original_question}"

Context: {request.context if request.context else 'General exploration'}
Target audience: {request.target_audience if request.target_audience else 'General'}
Desired outcome: {request.desired_outcome}

Create 3-4 alternative viewpoints:
1. How might different people approach this?
2. What are completely different ways to view this?
3. What alternative frameworks could apply?
4. What would change if we started from different assumptions?

Focus on expanding possibilities rather than finding the "right" answer."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.8
        )
        
        return self._parse_perspectives(response.content)
    
    async def _opposite_perspective(self, request: PerspectiveShiftRequest) -> List[str]:
        """Generate opposite or contrarian perspectives."""
        
        system_prompt = self._get_opposite_system_prompt(request.intensity)
        
        prompt = f"""Explore the opposite perspective for: "{request.original_question}"

Context: {request.context if request.context else 'General exploration'}
Intensity: {request.intensity}
Desired outcome: {request.desired_outcome}

Generate 3-4 opposite or contrarian perspectives:
1. What's the opposite way to think about this?
2. What if the problem is actually the solution?
3. What if we're asking the wrong question entirely?
4. What would someone who disagrees completely say?

Be respectful and thoughtful - the goal is insight, not argument."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.7
        )
        
        return self._parse_perspectives(response.content)
    
    async def _stakeholder_perspective(self, request: PerspectiveShiftRequest) -> List[str]:
        """Generate perspectives from different stakeholders."""
        
        system_prompt = self._get_stakeholder_system_prompt(request.intensity)
        
        prompt = f"""Consider this question from different stakeholder perspectives: "{request.original_question}"

Context: {request.context if request.context else 'General exploration'}
Focus: {request.focus_area if request.focus_area else 'Key stakeholders'}
Desired outcome: {request.desired_outcome}

Explore 3-4 different stakeholder viewpoints:
1. Who are the key people affected by this question?
2. How would each stakeholder view this differently?
3. What would each stakeholder prioritize?
4. What concerns would each stakeholder have?

Be empathetic to all perspectives - everyone has valid concerns and viewpoints."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.7
        )
        
        return self._parse_perspectives(response.content)
    
    async def _temporal_perspective(self, request: PerspectiveShiftRequest) -> List[str]:
        """Generate time-based perspectives."""
        
        system_prompt = self._get_temporal_system_prompt(request.intensity)
        
        prompt = f"""Consider this question across different time perspectives: "{request.original_question}"

Context: {request.context if request.context else 'General exploration'}
Desired outcome: {request.desired_outcome}

Explore 3-4 temporal perspectives:
1. How does this look from a short-term vs. long-term view?
2. What would someone from the past think about this?
3. How might this question evolve in the future?
4. What's the historical context that shapes this question?

Consider how time changes the meaning and importance of questions."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.7
        )
        
        return self._parse_perspectives(response.content)
    
    async def _contextual_perspective(self, request: PerspectiveShiftRequest) -> List[str]:
        """Generate perspectives from different contexts."""
        
        system_prompt = self._get_contextual_system_prompt(request.intensity)
        
        prompt = f"""Consider this question in different contexts: "{request.original_question}"

Current context: {request.context if request.context else 'General exploration'}
Focus: {request.focus_area if request.focus_area else 'Different contexts'}
Desired outcome: {request.desired_outcome}

Explore 3-4 different contextual perspectives:
1. How would this question change in different industries/fields?
2. What if this were in a different cultural context?
3. How would scale (personal vs. organizational vs. societal) change this?
4. What if resources, constraints, or priorities were different?

Show how context shapes the meaning and solutions of questions."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.7
        )
        
        return self._parse_perspectives(response.content)
    
    def _parse_perspectives(self, content: str) -> List[str]:
        """Parse perspectives from Claude response."""
        perspectives = []
        
        lines = content.split('\n')
        current_perspective = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for numbered or bulleted items
            if any(line.startswith(marker) for marker in ['1.', '2.', '3.', '4.', '5.', '- ', '• ', '* ']):
                if current_perspective:
                    perspectives.append(current_perspective.strip())
                current_perspective = line
            else:
                current_perspective += " " + line
        
        # Don't forget the last perspective
        if current_perspective:
            perspectives.append(current_perspective.strip())
        
        return perspectives[:4]  # Limit to 4 perspectives
    
    async def _generate_reframed_questions(self, request: PerspectiveShiftRequest, shifts: List[str]) -> List[str]:
        """Generate reframed questions based on the shifts."""
        
        system_prompt = self._get_base_system_prompt()
        
        prompt = f"""Based on these perspective shifts, generate 3-4 reframed questions:

Original question: "{request.original_question}"

Perspective shifts:
{chr(10).join(f"- {shift}" for shift in shifts)}

Create questions that:
1. Incorporate insights from the shifts
2. Are actionable and specific
3. Open new paths for exploration
4. Maintain empathetic tone

Format as clear, direct questions."""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=600,
            temperature=0.6
        )
        
        return self._parse_questions(response.content)
    
    def _parse_questions(self, content: str) -> List[str]:
        """Parse questions from Claude response."""
        questions = []
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and '?' in line:
                # Clean up question
                question = line.lstrip('- •*123456789. ')
                if question:
                    questions.append(question)
        
        return questions[:4]  # Limit to 4 questions
    
    async def _generate_insights(self, request: PerspectiveShiftRequest, shifts: List[str]) -> List[str]:
        """Generate insights from the perspective shifts."""
        
        insights = []
        
        # Add insights based on shift type
        if request.shift_type == PerspectiveType.REFRAME:
            insights.append("Reframing reveals hidden assumptions and opens new solution paths")
        elif request.shift_type == PerspectiveType.CHALLENGE:
            insights.append("Challenging assumptions uncovers limiting beliefs and expands possibilities")
        elif request.shift_type == PerspectiveType.STAKEHOLDER:
            insights.append("Different stakeholders bring valuable perspectives that enrich understanding")
        elif request.shift_type == PerspectiveType.TEMPORAL:
            insights.append("Time perspective reveals how urgency and importance shift over time")
        
        # Add general insights
        insights.append("Multiple perspectives create a richer understanding of complex issues")
        insights.append("Shifting perspective is a skill that improves with practice and openness")
        
        return insights[:3]  # Limit to 3 insights
    
    async def _generate_reasoning(self, request: PerspectiveShiftRequest, shifts: List[str]) -> str:
        """Generate reasoning for the perspective shifts."""
        
        reasoning_parts = []
        
        reasoning_parts.append(f"The {request.shift_type.value} approach was chosen to help you see '{request.original_question}' from a different angle.")
        
        if request.intensity == "gentle":
            reasoning_parts.append("The gentle approach maintains your comfort zone while introducing new viewpoints.")
        elif request.intensity == "strong":
            reasoning_parts.append("The strong approach challenges assumptions more directly to breakthrough limiting thinking.")
        else:
            reasoning_parts.append("The moderate approach balances challenge with support to encourage growth.")
        
        reasoning_parts.append("Each perspective shift is designed to expand your thinking while maintaining empathy and support.")
        
        return " ".join(reasoning_parts)
    
    def _generate_empathetic_guidance(self, request: PerspectiveShiftRequest, shifts: List[str]) -> str:
        """Generate empathetic guidance for the user."""
        
        guidance_parts = []
        
        if request.intensity == "gentle":
            guidance_parts.append("🤗 You're exploring new perspectives with openness and curiosity.")
        elif request.intensity == "strong":
            guidance_parts.append("💪 You're courageously challenging your assumptions - that takes strength!")
        else:
            guidance_parts.append("🌟 You're thoughtfully expanding your perspective - wonderful work!")
        
        guidance_parts.append("Remember, there's no single 'right' perspective.")
        guidance_parts.append("Each viewpoint offers valuable insights that can inform your thinking.")
        guidance_parts.append("Trust your intuition about which perspectives resonate and deserve deeper exploration.")
        
        return " ".join(guidance_parts)
    
    async def _generate_next_steps(self, request: PerspectiveShiftRequest, shifts: List[str]) -> List[str]:
        """Generate next steps based on the perspective shifts."""
        
        next_steps = []
        
        # Common next steps
        next_steps.append("Choose 1-2 perspectives that resonate most strongly with you")
        next_steps.append("Explore the implications of your chosen perspectives more deeply")
        next_steps.append("Consider how these new viewpoints might change your approach")
        
        # Specific next steps based on shift type
        if request.shift_type == PerspectiveType.STAKEHOLDER:
            next_steps.append("Reach out to actual stakeholders to validate these perspectives")
        elif request.shift_type == PerspectiveType.CHALLENGE:
            next_steps.append("Test your assumptions by seeking disconfirming evidence")
        elif request.shift_type == PerspectiveType.TEMPORAL:
            next_steps.append("Create timeline-based action plans with different time horizons")
        
        return next_steps[:3]  # Limit to 3 next steps
    
    def _calculate_confidence_level(self, request: PerspectiveShiftRequest, shifts: List[str]) -> float:
        """Calculate confidence level for the perspective shifts."""
        
        base_confidence = 0.7
        
        # Adjust based on number of shifts
        if len(shifts) >= 3:
            base_confidence += 0.1
        
        # Adjust based on intensity
        if request.intensity == "gentle":
            base_confidence += 0.05
        elif request.intensity == "strong":
            base_confidence += 0.1
        
        # Adjust based on context
        if request.context:
            base_confidence += 0.05
        
        return min(0.95, base_confidence)
    
    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt for perspective shifting."""
        return """You are a compassionate perspective-shifting companion who helps people see 
        questions and problems from new angles. Your approach is:
        
        - **Empathetic**: Understanding the user's current perspective and emotional state
        - **Supportive**: Encouraging growth while maintaining psychological safety
        - **Insightful**: Revealing hidden assumptions and opening new possibilities
        - **Respectful**: Honoring all perspectives while gently challenging limitations
        - **Practical**: Providing actionable insights that lead to meaningful change
        
        Your goal is to expand thinking while maintaining kindness and understanding."""
    
    def _get_reframe_system_prompt(self, intensity: str) -> str:
        """Get system prompt for reframing."""
        base_prompt = self._get_base_system_prompt()
        
        if intensity == "gentle":
            return base_prompt + "\n\nUse gentle reframing that feels safe and comfortable."
        elif intensity == "strong":
            return base_prompt + "\n\nUse bold reframing that challenges assumptions directly."
        else:
            return base_prompt + "\n\nUse balanced reframing that challenges while supporting."
    
    def _get_challenge_system_prompt(self, intensity: str) -> str:
        """Get system prompt for challenging."""
        base_prompt = self._get_base_system_prompt()
        
        if intensity == "gentle":
            return base_prompt + "\n\nChallenge assumptions gently with lots of support and encouragement."
        elif intensity == "strong":
            return base_prompt + "\n\nChallenge assumptions directly but maintain empathy and respect."
        else:
            return base_prompt + "\n\nChallenge assumptions thoughtfully with balanced support."
    
    def _get_alternative_system_prompt(self, intensity: str) -> str:
        """Get system prompt for alternatives."""
        return self._get_base_system_prompt() + "\n\nFocus on creative alternatives and diverse viewpoints."
    
    def _get_opposite_system_prompt(self, intensity: str) -> str:
        """Get system prompt for opposite perspectives."""
        return self._get_base_system_prompt() + "\n\nExplore opposite viewpoints respectfully and constructively."
    
    def _get_stakeholder_system_prompt(self, intensity: str) -> str:
        """Get system prompt for stakeholder perspectives."""
        return self._get_base_system_prompt() + "\n\nConsider all stakeholders with empathy and fairness."
    
    def _get_temporal_system_prompt(self, intensity: str) -> str:
        """Get system prompt for temporal perspectives."""
        return self._get_base_system_prompt() + "\n\nConsider how time changes the meaning and importance of questions."
    
    def _get_contextual_system_prompt(self, intensity: str) -> str:
        """Get system prompt for contextual perspectives."""
        return self._get_base_system_prompt() + "\n\nExplore how different contexts shape questions and solutions."
    
    def _get_shift_type_description(self, shift_type: PerspectiveType) -> str:
        """Get description for a shift type."""
        descriptions = {
            PerspectiveType.REFRAME: "Reframe questions to reveal new insights and possibilities",
            PerspectiveType.CHALLENGE: "Gently challenge assumptions to expand thinking",
            PerspectiveType.ALTERNATIVE: "Generate alternative viewpoints and approaches",
            PerspectiveType.OPPOSITE: "Explore opposite or contrarian perspectives",
            PerspectiveType.STAKEHOLDER: "Consider different stakeholder perspectives",
            PerspectiveType.TEMPORAL: "Examine questions across different time perspectives",
            PerspectiveType.CONTEXTUAL: "Explore questions in different contexts"
        }
        return descriptions.get(shift_type, "Unknown perspective shift type")