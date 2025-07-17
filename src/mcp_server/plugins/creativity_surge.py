"""
Creativity Surge MCP Plugin
===========================

Divergent thinking module to break creative gridlock with empathy and encouragement.
Helps users unleash their creative potential through supportive, structured exercises.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import random

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..plugins import PluginInterface, PluginMetadata
from ..claude_client import ClaudeClient
from ..hybrid_compute import HybridComputeManager, TaskDefinition, TaskPriority
from ..config import Settings

logger = logging.getLogger(__name__)


class CreativityTechnique(Enum):
    """Types of creativity techniques."""
    DIVERGENT_THINKING = "divergent_thinking"
    RANDOM_STIMULATION = "random_stimulation"
    CONSTRAINT_REMOVAL = "constraint_removal"
    METAPHOR_THINKING = "metaphor_thinking"
    WHAT_IF_SCENARIOS = "what_if_scenarios"
    ASSUMPTION_REVERSAL = "assumption_reversal"
    CREATIVE_COMBINATIONS = "creative_combinations"
    EMOTIONAL_CATALYST = "emotional_catalyst"


class CreativitySurgeRequest(BaseModel):
    """Request model for creativity surge sessions."""
    challenge: str
    technique: CreativityTechnique
    intensity: Optional[str] = "medium"  # low, medium, high, extreme
    duration_minutes: Optional[int] = 10
    context: Optional[Dict[str, Any]] = None
    current_mood: Optional[str] = "neutral"
    energy_level: Optional[str] = "medium"
    preferred_style: Optional[str] = "balanced"  # playful, analytical, intuitive, balanced


class CreativeIdea(BaseModel):
    """Individual creative idea."""
    idea: str
    technique_used: str
    creativity_score: float
    originality_score: float
    feasibility_score: float
    reasoning: str
    development_potential: str
    emotional_appeal: str


class CreativitySurgeResponse(BaseModel):
    """Response model for creativity surge sessions."""
    challenge: str
    technique: CreativityTechnique
    ideas: List[CreativeIdea]
    breakthrough_moments: List[str]
    patterns_identified: List[str]
    energy_boost: str
    encouragement: str
    next_techniques: List[str]
    creative_momentum: float


class CreativeBlock(BaseModel):
    """Creative block analysis."""
    block_type: str
    symptoms: List[str]
    root_causes: List[str]
    breakthrough_strategies: List[str]
    empathetic_support: str


class CreativitySurgePlugin(PluginInterface):
    """
    Creativity Surge MCP Plugin for breaking creative gridlock.
    
    Provides structured, empathetic support to help users overcome creative blocks
    and unleash their creative potential through various proven techniques.
    """
    
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.claude_client = ClaudeClient(settings)
        self.hybrid_compute = HybridComputeManager(settings)
        self.router = APIRouter(prefix="/creativity-surge", tags=["ideation"])
        
        # Creativity techniques mapping
        self.techniques = {
            CreativityTechnique.DIVERGENT_THINKING: self._divergent_thinking,
            CreativityTechnique.RANDOM_STIMULATION: self._random_stimulation,
            CreativityTechnique.CONSTRAINT_REMOVAL: self._constraint_removal,
            CreativityTechnique.METAPHOR_THINKING: self._metaphor_thinking,
            CreativityTechnique.WHAT_IF_SCENARIOS: self._what_if_scenarios,
            CreativityTechnique.ASSUMPTION_REVERSAL: self._assumption_reversal,
            CreativityTechnique.CREATIVE_COMBINATIONS: self._creative_combinations,
            CreativityTechnique.EMOTIONAL_CATALYST: self._emotional_catalyst,
        }
        
        # Random stimulation word lists
        self.random_words = [
            "butterfly", "thunderstorm", "telescope", "whisper", "fountain",
            "rainbow", "magnet", "puzzle", "journey", "crystal", "harmony",
            "adventure", "mystery", "growth", "transformation", "innovation",
            "connection", "discovery", "rhythm", "balance", "flow", "spark",
            "bridge", "key", "doorway", "light", "shadow", "dance", "song"
        ]
        
        self.random_objects = [
            "paperclip", "rubber duck", "mirror", "feather", "compass",
            "prism", "magnet", "spring", "lens", "thread", "stone", "leaf",
            "shell", "bottle", "candle", "clock", "rope", "box", "umbrella"
        ]
        
        self._setup_routes()
    
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return PluginMetadata(
            name="creativity_surge",
            version="1.0.0",
            description="Divergent thinking module to break creative gridlock with empathy",
            author="AplUSAndmINUS",
            requires=["anthropic", "fastapi", "hybrid_compute"],
            enabled=True
        )
    
    async def initialize(self) -> None:
        """Initialize the plugin."""
        logger.info("Initializing Creativity Surge plugin...")
        
        try:
            # Test Claude connection
            await self.claude_client.complete(
                prompt="Ready to unleash creativity?",
                system_prompt=self._get_base_system_prompt(),
                max_tokens=10
            )
            logger.info("Creativity Surge plugin initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Creativity Surge plugin: {e}")
            raise
    
    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        logger.info("Shutting down Creativity Surge plugin...")
    
    def _setup_routes(self) -> None:
        """Setup plugin routes."""
        
        @self.router.post("/surge", response_model=CreativitySurgeResponse)
        async def create_surge(request: CreativitySurgeRequest):
            """Create a creativity surge session."""
            try:
                task = TaskDefinition(
                    name=f"creativity_surge_{request.technique.value}",
                    priority=TaskPriority.MEDIUM,
                    estimated_cpu=0.4,
                    estimated_memory=0.3,
                    estimated_duration=request.duration_minutes * 60 if request.duration_minutes else 600,
                    requires_gpu=False,
                    requires_network=True,
                    can_run_on_azure=True,
                    azure_function_name="creativity_surge"
                )
                
                result = await self.hybrid_compute.execute_task(
                    task=task,
                    task_function=self._generate_creativity_surge,
                    request=request
                )
                
                return result
                
            except Exception as e:
                logger.error(f"Error in creativity surge: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/break-block", response_model=CreativeBlock)
        async def break_creative_block(challenge: str, current_state: str):
            """Analyze and provide strategies for breaking creative blocks."""
            try:
                task = TaskDefinition(
                    name="break_creative_block",
                    priority=TaskPriority.HIGH,
                    estimated_cpu=0.3,
                    estimated_memory=0.2,
                    estimated_duration=180,
                    requires_gpu=False,
                    requires_network=True,
                    can_run_on_azure=True,
                    azure_function_name="break_creative_block"
                )
                
                result = await self.hybrid_compute.execute_task(
                    task=task,
                    task_function=self._analyze_creative_block,
                    challenge=challenge,
                    current_state=current_state
                )
                
                return result
                
            except Exception as e:
                logger.error(f"Error breaking creative block: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.post("/rapid-fire", response_model=CreativitySurgeResponse)
        async def rapid_fire_ideas(challenge: str, count: int = 20):
            """Generate rapid-fire ideas using multiple techniques."""
            try:
                # Use divergent thinking for rapid generation
                request = CreativitySurgeRequest(
                    challenge=challenge,
                    technique=CreativityTechnique.DIVERGENT_THINKING,
                    intensity="high",
                    duration_minutes=5,
                    preferred_style="playful"
                )
                
                result = await self._generate_creativity_surge(request)
                
                # Generate additional ideas with random stimulation
                random_request = CreativitySurgeRequest(
                    challenge=challenge,
                    technique=CreativityTechnique.RANDOM_STIMULATION,
                    intensity="high",
                    duration_minutes=5,
                    preferred_style="playful"
                )
                
                random_result = await self._generate_creativity_surge(random_request)
                
                # Combine results
                combined_ideas = result.ideas + random_result.ideas
                
                return CreativitySurgeResponse(
                    challenge=challenge,
                    technique=CreativityTechnique.DIVERGENT_THINKING,
                    ideas=combined_ideas[:count],
                    breakthrough_moments=result.breakthrough_moments + random_result.breakthrough_moments,
                    patterns_identified=result.patterns_identified,
                    energy_boost="🚀 Rapid-fire session complete! Your creative energy is surging!",
                    encouragement="Amazing rapid-fire creativity! You've generated a wealth of ideas in record time.",
                    next_techniques=["constraint_removal", "metaphor_thinking"],
                    creative_momentum=0.95
                )
                
            except Exception as e:
                logger.error(f"Error in rapid-fire ideas: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/techniques")
        async def get_techniques():
            """Get available creativity techniques."""
            return {
                "techniques": [
                    {
                        "name": technique.value,
                        "description": self._get_technique_description(technique),
                        "best_for": self._get_technique_best_for(technique),
                        "intensity_levels": ["low", "medium", "high", "extreme"]
                    }
                    for technique in CreativityTechnique
                ]
            }
        
        @self.router.get("/inspiration")
        async def get_inspiration():
            """Get creative inspiration and warm-up exercises."""
            return {
                "random_words": random.sample(self.random_words, 5),
                "random_objects": random.sample(self.random_objects, 5),
                "warm_up_exercises": [
                    "List 10 unusual uses for a paperclip",
                    "Describe your challenge as if you were explaining it to a 5-year-old",
                    "What would your challenge look like if it were a color, sound, or texture?",
                    "If your challenge were a person, what would they be like?",
                    "What's the most ridiculous solution you can think of? Now make it practical."
                ],
                "creative_mantras": [
                    "There are no bad ideas, only stepping stones to great ones",
                    "Creativity flows through courage and curiosity",
                    "Every expert was once a beginner who didn't give up",
                    "Your unique perspective is your creative superpower",
                    "Innovation happens when you combine the impossible with the inevitable"
                ]
            }
    
    async def _generate_creativity_surge(self, request: CreativitySurgeRequest) -> CreativitySurgeResponse:
        """Generate a creativity surge session."""
        
        # Get the appropriate technique
        technique = self.techniques.get(request.technique)
        if not technique:
            raise ValueError(f"Unknown creativity technique: {request.technique}")
        
        # Generate ideas using the technique
        ideas = await technique(request)
        
        # Identify breakthrough moments
        breakthrough_moments = await self._identify_breakthrough_moments(ideas, request)
        
        # Identify patterns
        patterns_identified = await self._identify_patterns(ideas, request)
        
        # Generate energy boost message
        energy_boost = self._generate_energy_boost(request, len(ideas))
        
        # Generate encouragement
        encouragement = self._generate_encouragement(request, ideas)
        
        # Suggest next techniques
        next_techniques = self._suggest_next_techniques(request.technique, ideas)
        
        # Calculate creative momentum
        creative_momentum = self._calculate_creative_momentum(ideas, request)
        
        return CreativitySurgeResponse(
            challenge=request.challenge,
            technique=request.technique,
            ideas=ideas,
            breakthrough_moments=breakthrough_moments,
            patterns_identified=patterns_identified,
            energy_boost=energy_boost,
            encouragement=encouragement,
            next_techniques=next_techniques,
            creative_momentum=creative_momentum
        )
    
    async def _divergent_thinking(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas using divergent thinking."""
        
        system_prompt = self._get_divergent_thinking_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Generate creative ideas for this challenge: "{request.challenge}"

Style: {request.preferred_style}
Intensity: {request.intensity}
Duration: {request.duration_minutes} minutes
Current mood: {request.current_mood}
Energy level: {request.energy_level}

Use divergent thinking to generate 8-10 diverse, creative ideas:
1. Quantity over quality - generate as many ideas as possible
2. Build on each idea to create variations
3. Combine unrelated concepts
4. Think outside conventional boundaries
5. Embrace wild and unusual ideas

For each idea, provide:
- The core idea
- Why it could work
- How original it is
- Development potential

Be encouraging and celebrate creative thinking!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1500,
            temperature=0.9  # High temperature for maximum creativity
        )
        
        return await self._parse_creative_ideas(response.content, "divergent_thinking")
    
    async def _random_stimulation(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas using random stimulation."""
        
        # Select random stimuli
        random_word = random.choice(self.random_words)
        random_object = random.choice(self.random_objects)
        
        system_prompt = self._get_random_stimulation_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Use these random stimuli to generate creative ideas for: "{request.challenge}"

Random word: {random_word}
Random object: {random_object}

Style: {request.preferred_style}
Intensity: {request.intensity}

Generate 6-8 ideas by connecting these random elements to your challenge:
1. How does the random word relate to your challenge?
2. What properties of the random object could inspire solutions?
3. What metaphors or analogies emerge?
4. How can you combine these stimuli with your challenge?
5. What unexpected connections can you make?

For each idea, explain:
- The creative connection
- How it addresses the challenge
- Why it's innovative
- Potential for development

Embrace the unexpected and celebrate unusual connections!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.9
        )
        
        return await self._parse_creative_ideas(response.content, "random_stimulation")
    
    async def _constraint_removal(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas by removing constraints."""
        
        system_prompt = self._get_constraint_removal_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Generate ideas by removing constraints for: "{request.challenge}"

Style: {request.preferred_style}
Intensity: {request.intensity}

First, identify constraints that might be limiting thinking:
- What assumptions are you making?
- What resources do you assume you don't have?
- What rules or limitations might not be real?
- What would you do if time, money, or resources were unlimited?

Then generate 6-8 ideas by removing these constraints:
1. What if you had unlimited resources?
2. What if there were no rules or regulations?
3. What if you could start from scratch?
4. What if you could change the fundamental nature of the challenge?
5. What if you could use any technology, even fictional ones?

For each idea, explain:
- Which constraint you removed
- How the idea addresses the challenge
- Why it's liberating
- How it might be adapted to reality

Celebrate the freedom of unconstrained thinking!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.8
        )
        
        return await self._parse_creative_ideas(response.content, "constraint_removal")
    
    async def _metaphor_thinking(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas using metaphor thinking."""
        
        system_prompt = self._get_metaphor_thinking_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Use metaphor thinking to generate ideas for: "{request.challenge}"

Style: {request.preferred_style}
Intensity: {request.intensity}

Create metaphors and analogies to explore your challenge:
1. If your challenge were a living organism, what would it be?
2. If it were a natural phenomenon, what would it be?
3. If it were a machine or tool, what would it be?
4. If it were a story or journey, what would it be?
5. If it were a game or sport, what would it be?

For each metaphor, generate 1-2 ideas by asking:
- How does this metaphor illuminate the challenge?
- What solutions does the metaphor suggest?
- What new perspectives does it offer?
- How can you apply lessons from the metaphor?

Generate 6-8 ideas total, explaining:
- The metaphor used
- The insight it provides
- How it leads to a solution
- Why it's creatively valuable

Embrace the power of metaphorical thinking!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.8
        )
        
        return await self._parse_creative_ideas(response.content, "metaphor_thinking")
    
    async def _what_if_scenarios(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas using what-if scenarios."""
        
        system_prompt = self._get_what_if_scenarios_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Generate ideas using "what if" scenarios for: "{request.challenge}"

Style: {request.preferred_style}
Intensity: {request.intensity}

Create 6-8 "what if" scenarios and explore their implications:
1. What if this challenge existed in a different time period?
2. What if it affected a completely different type of person?
3. What if the scale were 100x larger or smaller?
4. What if you had to solve it with medieval technology?
5. What if you had to solve it with future technology?
6. What if the challenge were the opposite of what it is now?
7. What if everyone in the world faced this challenge?
8. What if solving it were a matter of life and death?

For each scenario, generate an idea that:
- Explores the implications of the "what if"
- Addresses the challenge in this new context
- Can be adapted back to the original challenge
- Offers a fresh perspective

Celebrate the power of imagination and possibility!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.8
        )
        
        return await self._parse_creative_ideas(response.content, "what_if_scenarios")
    
    async def _assumption_reversal(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas by reversing assumptions."""
        
        system_prompt = self._get_assumption_reversal_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Generate ideas by reversing assumptions for: "{request.challenge}"

Style: {request.preferred_style}
Intensity: {request.intensity}

First, identify key assumptions about your challenge:
- What do you assume is true about this challenge?
- What do you assume about the people involved?
- What do you assume about the context or environment?
- What do you assume about available resources?
- What do you assume about the desired outcome?

Then reverse each assumption and generate ideas:
1. What if the opposite were true?
2. What solutions emerge from this reversal?
3. How does this change your perspective?
4. What new possibilities does this create?

Generate 6-8 ideas by reversing different assumptions:
- State the original assumption
- Describe the reversal
- Explain the idea that emerges
- Show how it addresses the challenge
- Highlight why it's innovative

Embrace the power of turning assumptions upside down!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.8
        )
        
        return await self._parse_creative_ideas(response.content, "assumption_reversal")
    
    async def _creative_combinations(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas by combining unrelated concepts."""
        
        # Generate some unrelated concepts
        concepts = [
            "ecosystem", "algorithm", "storytelling", "architecture", "music",
            "cooking", "sports", "art", "engineering", "psychology", "nature",
            "technology", "philosophy", "mathematics", "dance", "chemistry"
        ]
        
        selected_concepts = random.sample(concepts, 4)
        
        system_prompt = self._get_creative_combinations_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Generate ideas by combining these concepts with your challenge: "{request.challenge}"

Concepts to combine: {', '.join(selected_concepts)}

Style: {request.preferred_style}
Intensity: {request.intensity}

Create 6-8 ideas by combining these concepts with your challenge:
1. How does each concept relate to your challenge?
2. What happens when you combine two concepts?
3. How can principles from one field apply to another?
4. What hybrid solutions emerge from these combinations?
5. What unexpected synergies can you create?

For each combination, generate an idea that:
- Explains the combination
- Shows how it addresses the challenge
- Highlights the creative synthesis
- Demonstrates innovative potential

Celebrate the magic of creative combination!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.9
        )
        
        return await self._parse_creative_ideas(response.content, "creative_combinations")
    
    async def _emotional_catalyst(self, request: CreativitySurgeRequest) -> List[CreativeIdea]:
        """Generate ideas using emotional catalysts."""
        
        system_prompt = self._get_emotional_catalyst_prompt(request.intensity, request.preferred_style)
        
        prompt = f"""Use emotional catalysts to generate ideas for: "{request.challenge}"

Style: {request.preferred_style}
Intensity: {request.intensity}
Current mood: {request.current_mood}

Explore different emotional perspectives on your challenge:
1. How would you approach this if you felt passionate excitement?
2. What would you do if you felt deep compassion?
3. How would curiosity change your approach?
4. What would courage inspire you to try?
5. How would joy and playfulness shape your solutions?
6. What would wisdom and patience suggest?

Generate 6-8 ideas by channeling different emotions:
- State the emotion you're channeling
- Explain how it changes your perspective
- Describe the idea that emerges
- Show how emotion enhances creativity
- Highlight the human element

Remember: Emotions are powerful creative fuel!
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1200,
            temperature=0.8
        )
        
        return await self._parse_creative_ideas(response.content, "emotional_catalyst")
    
    async def _parse_creative_ideas(self, content: str, technique: str) -> List[CreativeIdea]:
        """Parse creative ideas from Claude response."""
        ideas = []
        
        lines = content.split('\n')
        current_idea = ""
        current_reasoning = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for numbered or bulleted ideas
            if any(line.startswith(marker) for marker in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '- ', '• ']):
                if current_idea:
                    # Process previous idea
                    ideas.append(self._create_creative_idea(current_idea, current_reasoning, technique))
                
                # Start new idea
                current_idea = line
                current_reasoning = ""
            else:
                # Add to current reasoning
                current_reasoning += line + " "
        
        # Don't forget the last idea
        if current_idea:
            ideas.append(self._create_creative_idea(current_idea, current_reasoning, technique))
        
        return ideas[:8]  # Limit to 8 ideas
    
    def _create_creative_idea(self, idea: str, reasoning: str, technique: str) -> CreativeIdea:
        """Create a CreativeIdea object."""
        # Calculate scores based on content analysis
        creativity_score = self._calculate_creativity_score(idea, reasoning)
        originality_score = self._calculate_originality_score(idea)
        feasibility_score = self._calculate_feasibility_score(idea, reasoning)
        
        # Generate additional fields
        development_potential = self._assess_development_potential(idea, reasoning)
        emotional_appeal = self._assess_emotional_appeal(idea)
        
        return CreativeIdea(
            idea=idea.strip(),
            technique_used=technique,
            creativity_score=creativity_score,
            originality_score=originality_score,
            feasibility_score=feasibility_score,
            reasoning=reasoning.strip(),
            development_potential=development_potential,
            emotional_appeal=emotional_appeal
        )
    
    def _calculate_creativity_score(self, idea: str, reasoning: str) -> float:
        """Calculate creativity score based on content."""
        score = 0.6  # Base score
        
        creative_indicators = [
            'unique', 'innovative', 'novel', 'creative', 'original',
            'unexpected', 'surprising', 'breakthrough', 'revolutionary'
        ]
        
        content = (idea + " " + reasoning).lower()
        for indicator in creative_indicators:
            if indicator in content:
                score += 0.05
        
        return min(1.0, score)
    
    def _calculate_originality_score(self, idea: str) -> float:
        """Calculate originality score."""
        score = 0.7  # Base score
        
        # Check for common phrases that might indicate less originality
        common_phrases = ['the usual', 'traditional', 'standard', 'conventional']
        idea_lower = idea.lower()
        
        for phrase in common_phrases:
            if phrase in idea_lower:
                score -= 0.1
        
        # Check for originality indicators
        originality_indicators = ['never before', 'first time', 'unprecedented', 'groundbreaking']
        
        for indicator in originality_indicators:
            if indicator in idea_lower:
                score += 0.1
        
        return min(1.0, max(0.1, score))
    
    def _calculate_feasibility_score(self, idea: str, reasoning: str) -> float:
        """Calculate feasibility score."""
        score = 0.5  # Base score
        
        # Check for feasibility indicators
        feasible_indicators = ['practical', 'doable', 'achievable', 'realistic', 'implementable']
        challenging_indicators = ['impossible', 'unrealistic', 'fantasy', 'dream']
        
        content = (idea + " " + reasoning).lower()
        
        for indicator in feasible_indicators:
            if indicator in content:
                score += 0.1
        
        for indicator in challenging_indicators:
            if indicator in content:
                score -= 0.1
        
        return min(1.0, max(0.1, score))
    
    def _assess_development_potential(self, idea: str, reasoning: str) -> str:
        """Assess development potential."""
        content = (idea + " " + reasoning).lower()
        
        if any(word in content for word in ['scalable', 'expandable', 'adaptable', 'flexible']):
            return "high"
        elif any(word in content for word in ['limited', 'specific', 'narrow']):
            return "focused"
        else:
            return "moderate"
    
    def _assess_emotional_appeal(self, idea: str) -> str:
        """Assess emotional appeal."""
        idea_lower = idea.lower()
        
        if any(word in idea_lower for word in ['joy', 'excitement', 'love', 'passion', 'delight']):
            return "inspiring"
        elif any(word in idea_lower for word in ['help', 'support', 'care', 'comfort']):
            return "nurturing"
        elif any(word in idea_lower for word in ['challenge', 'adventure', 'bold', 'daring']):
            return "exciting"
        else:
            return "thoughtful"
    
    async def _identify_breakthrough_moments(self, ideas: List[CreativeIdea], request: CreativitySurgeRequest) -> List[str]:
        """Identify breakthrough moments in the ideas."""
        breakthroughs = []
        
        # Find high-creativity ideas
        high_creativity_ideas = [idea for idea in ideas if idea.creativity_score > 0.8]
        
        if high_creativity_ideas:
            breakthroughs.append(f"🚀 {len(high_creativity_ideas)} high-creativity ideas generated!")
        
        # Find high-originality ideas
        high_originality_ideas = [idea for idea in ideas if idea.originality_score > 0.8]
        
        if high_originality_ideas:
            breakthroughs.append(f"💡 {len(high_originality_ideas)} highly original concepts discovered!")
        
        # Technique-specific breakthroughs
        if request.technique == CreativityTechnique.RANDOM_STIMULATION:
            breakthroughs.append("🎯 Unexpected connections formed through random stimulation!")
        elif request.technique == CreativityTechnique.CONSTRAINT_REMOVAL:
            breakthroughs.append("🔓 Mental constraints broken - new possibilities unlocked!")
        elif request.technique == CreativityTechnique.ASSUMPTION_REVERSAL:
            breakthroughs.append("🔄 Assumptions challenged - fresh perspectives gained!")
        
        return breakthroughs[:3]  # Limit to 3 breakthroughs
    
    async def _identify_patterns(self, ideas: List[CreativeIdea], request: CreativitySurgeRequest) -> List[str]:
        """Identify patterns in the generated ideas."""
        patterns = []
        
        # Analyze development potential
        high_potential = [idea for idea in ideas if idea.development_potential == "high"]
        if len(high_potential) > 2:
            patterns.append("Multiple ideas show high development potential")
        
        # Analyze emotional appeal
        emotional_themes = {}
        for idea in ideas:
            theme = idea.emotional_appeal
            emotional_themes[theme] = emotional_themes.get(theme, 0) + 1
        
        dominant_theme = max(emotional_themes, key=emotional_themes.get)
        patterns.append(f"Ideas trend toward {dominant_theme} emotional appeal")
        
        # Analyze feasibility
        avg_feasibility = sum(idea.feasibility_score for idea in ideas) / len(ideas)
        if avg_feasibility > 0.7:
            patterns.append("Ideas show strong practical feasibility")
        elif avg_feasibility < 0.4:
            patterns.append("Ideas explore highly innovative, experimental territory")
        
        return patterns[:3]  # Limit to 3 patterns
    
    def _generate_energy_boost(self, request: CreativitySurgeRequest, idea_count: int) -> str:
        """Generate energy boost message."""
        energy_messages = {
            "low": f"🌱 Gentle creative energy flowing - {idea_count} ideas sprouting!",
            "medium": f"⚡ Creative energy building - {idea_count} ideas generated!",
            "high": f"🔥 High creative energy unleashed - {idea_count} ideas blazing!",
            "extreme": f"💥 Explosive creative energy - {idea_count} ideas erupting!"
        }
        
        return energy_messages.get(request.intensity, f"✨ Creative energy active - {idea_count} ideas generated!")
    
    def _generate_encouragement(self, request: CreativitySurgeRequest, ideas: List[CreativeIdea]) -> str:
        """Generate encouragement based on the results."""
        avg_creativity = sum(idea.creativity_score for idea in ideas) / len(ideas)
        
        if avg_creativity > 0.8:
            return "🌟 Exceptional creative breakthrough! Your ideas are innovative and inspiring. You're in a powerful creative flow!"
        elif avg_creativity > 0.6:
            return "🎨 Strong creative session! Your ideas show real innovation and potential. Keep this creative momentum going!"
        else:
            return "🌈 Good creative exploration! You're building creative confidence and generating valuable ideas. Every idea is a step forward!"
    
    def _suggest_next_techniques(self, current_technique: CreativityTechnique, ideas: List[CreativeIdea]) -> List[str]:
        """Suggest next techniques based on current results."""
        suggestions = []
        
        # Analyze what worked well
        avg_creativity = sum(idea.creativity_score for idea in ideas) / len(ideas)
        avg_feasibility = sum(idea.feasibility_score for idea in ideas) / len(ideas)
        
        if current_technique == CreativityTechnique.DIVERGENT_THINKING:
            suggestions.extend(["random_stimulation", "constraint_removal"])
        elif current_technique == CreativityTechnique.RANDOM_STIMULATION:
            suggestions.extend(["creative_combinations", "metaphor_thinking"])
        elif current_technique == CreativityTechnique.CONSTRAINT_REMOVAL:
            suggestions.extend(["assumption_reversal", "what_if_scenarios"])
        else:
            suggestions.extend(["divergent_thinking", "emotional_catalyst"])
        
        # Adjust based on results
        if avg_creativity < 0.6:
            suggestions.append("random_stimulation")  # Boost creativity
        
        if avg_feasibility < 0.5:
            suggestions.append("constraint_removal")  # Make ideas more practical
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def _calculate_creative_momentum(self, ideas: List[CreativeIdea], request: CreativitySurgeRequest) -> float:
        """Calculate creative momentum score."""
        base_momentum = 0.5
        
        # Factor in idea count
        idea_count_factor = min(1.0, len(ideas) / 8.0)
        
        # Factor in average creativity
        avg_creativity = sum(idea.creativity_score for idea in ideas) / len(ideas)
        
        # Factor in intensity
        intensity_factor = {
            "low": 0.6,
            "medium": 0.8,
            "high": 1.0,
            "extreme": 1.2
        }.get(request.intensity, 0.8)
        
        momentum = base_momentum + (idea_count_factor * 0.3) + (avg_creativity * 0.2)
        momentum *= intensity_factor
        
        return min(1.0, momentum)
    
    async def _analyze_creative_block(self, challenge: str, current_state: str) -> CreativeBlock:
        """Analyze a creative block and provide strategies."""
        
        system_prompt = self._get_creative_block_analysis_prompt()
        
        prompt = f"""Analyze this creative block with empathy and provide breakthrough strategies:

Challenge: {challenge}
Current state: {current_state}

Please analyze:
1. What type of creative block is this?
2. What symptoms are present?
3. What might be the root causes?
4. What breakthrough strategies would help?
5. What empathetic support is needed?

Provide compassionate, actionable guidance to help overcome this block.
"""
        
        response = await self.claude_client.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.7
        )
        
        content = response.content
        
        # Parse the response (simplified)
        return CreativeBlock(
            block_type=self._extract_block_type(content),
            symptoms=self._extract_symptoms(content),
            root_causes=self._extract_root_causes(content),
            breakthrough_strategies=self._extract_breakthrough_strategies(content),
            empathetic_support=self._extract_empathetic_support(content)
        )
    
    def _extract_block_type(self, content: str) -> str:
        """Extract block type from analysis."""
        content_lower = content.lower()
        
        if "perfectionism" in content_lower:
            return "perfectionism"
        elif "fear" in content_lower:
            return "fear-based"
        elif "overwhelm" in content_lower:
            return "overwhelm"
        elif "comparison" in content_lower:
            return "comparison"
        else:
            return "general"
    
    def _extract_symptoms(self, content: str) -> List[str]:
        """Extract symptoms from analysis."""
        # Simplified extraction
        symptoms = []
        lines = content.split('\n')
        
        for line in lines:
            if 'symptom' in line.lower() and ':' in line:
                symptoms.append(line.split(':')[1].strip())
        
        if not symptoms:
            symptoms = ["Difficulty generating ideas", "Feeling stuck", "Self-doubt about creativity"]
        
        return symptoms[:3]
    
    def _extract_root_causes(self, content: str) -> List[str]:
        """Extract root causes from analysis."""
        # Simplified extraction
        causes = []
        lines = content.split('\n')
        
        for line in lines:
            if 'cause' in line.lower() and ':' in line:
                causes.append(line.split(':')[1].strip())
        
        if not causes:
            causes = ["Fear of judgment", "Perfectionism", "Lack of creative confidence"]
        
        return causes[:3]
    
    def _extract_breakthrough_strategies(self, content: str) -> List[str]:
        """Extract breakthrough strategies from analysis."""
        # Simplified extraction
        strategies = []
        lines = content.split('\n')
        
        for line in lines:
            if 'strategy' in line.lower() and ':' in line:
                strategies.append(line.split(':')[1].strip())
        
        if not strategies:
            strategies = [
                "Start with small, low-pressure creative exercises",
                "Use random stimulation to bypass mental blocks",
                "Focus on quantity over quality initially"
            ]
        
        return strategies[:4]
    
    def _extract_empathetic_support(self, content: str) -> str:
        """Extract empathetic support from analysis."""
        # Look for supportive language
        if "you're not alone" in content.lower():
            return "Remember, you're not alone in this creative challenge. Every artist faces blocks."
        elif "normal" in content.lower():
            return "Creative blocks are a normal part of the creative process. They're signs you're pushing boundaries."
        else:
            return "Your creative block is temporary. With patience and the right techniques, you can break through."
    
    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt for creativity surge."""
        return """You are an enthusiastic and empathetic creativity coach who helps people 
        break through creative blocks and unleash their creative potential. Your approach is:
        
        - **Encouraging**: Celebrate all creative attempts and build confidence
        - **Supportive**: Provide psychological safety for creative risk-taking
        - **Energizing**: Boost creative energy and motivation
        - **Innovative**: Introduce novel techniques and perspectives
        - **Empathetic**: Understand creative struggles and provide compassionate guidance
        
        Your goal is to help people overcome creative gridlock and experience the joy of creative flow."""
    
    def _get_divergent_thinking_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for divergent thinking."""
        base_prompt = self._get_base_system_prompt()
        
        style_additions = {
            "playful": "\n\nEmphasize fun, whimsy, and joyful exploration. Make creativity feel like play.",
            "analytical": "\n\nBalance creativity with logical structure. Provide systematic approaches.",
            "intuitive": "\n\nTrust instincts and feelings. Embrace non-linear creative processes.",
            "balanced": "\n\nCombine structure with freedom, logic with intuition."
        }
        
        intensity_additions = {
            "low": "\n\nGentle creative exploration with comfortable challenges.",
            "medium": "\n\nModerate creative push with balanced support.",
            "high": "\n\nBold creative challenges with strong encouragement.",
            "extreme": "\n\nMaximum creative intensity with maximum support."
        }
        
        return base_prompt + style_additions.get(style, "") + intensity_additions.get(intensity, "")
    
    def _get_random_stimulation_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for random stimulation."""
        return self._get_divergent_thinking_prompt(intensity, style) + "\n\nFocus on unexpected connections and serendipitous discoveries."
    
    def _get_constraint_removal_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for constraint removal."""
        return self._get_divergent_thinking_prompt(intensity, style) + "\n\nEmphasize freedom and limitless possibilities."
    
    def _get_metaphor_thinking_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for metaphor thinking."""
        return self._get_divergent_thinking_prompt(intensity, style) + "\n\nCelebrate the power of metaphor and analogy in creative thinking."
    
    def _get_what_if_scenarios_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for what-if scenarios."""
        return self._get_divergent_thinking_prompt(intensity, style) + "\n\nEncourage imagination and speculative thinking."
    
    def _get_assumption_reversal_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for assumption reversal."""
        return self._get_divergent_thinking_prompt(intensity, style) + "\n\nGently challenge assumptions while maintaining support."
    
    def _get_creative_combinations_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for creative combinations."""
        return self._get_divergent_thinking_prompt(intensity, style) + "\n\nCelebrate synthesis and hybrid thinking."
    
    def _get_emotional_catalyst_prompt(self, intensity: str, style: str) -> str:
        """Get system prompt for emotional catalyst."""
        return self._get_divergent_thinking_prompt(intensity, style) + "\n\nHarness emotions as powerful creative fuel."
    
    def _get_creative_block_analysis_prompt(self) -> str:
        """Get system prompt for creative block analysis."""
        return self._get_base_system_prompt() + """
        
        When analyzing creative blocks:
        1. Be deeply empathetic and understanding
        2. Normalize the experience of creative blocks
        3. Provide specific, actionable strategies
        4. Offer hope and encouragement
        5. Focus on breakthrough rather than breakdown
        """
    
    def _get_technique_description(self, technique: CreativityTechnique) -> str:
        """Get description for a creativity technique."""
        descriptions = {
            CreativityTechnique.DIVERGENT_THINKING: "Generate multiple creative solutions through expansive thinking",
            CreativityTechnique.RANDOM_STIMULATION: "Use random words and objects to spark unexpected ideas",
            CreativityTechnique.CONSTRAINT_REMOVAL: "Break free from limiting assumptions and constraints",
            CreativityTechnique.METAPHOR_THINKING: "Use metaphors and analogies to explore new perspectives",
            CreativityTechnique.WHAT_IF_SCENARIOS: "Explore possibilities through hypothetical scenarios",
            CreativityTechnique.ASSUMPTION_REVERSAL: "Challenge assumptions by reversing them",
            CreativityTechnique.CREATIVE_COMBINATIONS: "Combine unrelated concepts for innovative solutions",
            CreativityTechnique.EMOTIONAL_CATALYST: "Use emotions as fuel for creative breakthrough"
        }
        return descriptions.get(technique, "Unknown creativity technique")
    
    def _get_technique_best_for(self, technique: CreativityTechnique) -> str:
        """Get what a technique is best for."""
        best_for = {
            CreativityTechnique.DIVERGENT_THINKING: "Generating many ideas quickly",
            CreativityTechnique.RANDOM_STIMULATION: "Breaking mental patterns and routines",
            CreativityTechnique.CONSTRAINT_REMOVAL: "Overcoming limiting beliefs",
            CreativityTechnique.METAPHOR_THINKING: "Finding new perspectives on familiar problems",
            CreativityTechnique.WHAT_IF_SCENARIOS: "Exploring possibilities and alternatives",
            CreativityTechnique.ASSUMPTION_REVERSAL: "Challenging conventional thinking",
            CreativityTechnique.CREATIVE_COMBINATIONS: "Innovation through synthesis",
            CreativityTechnique.EMOTIONAL_CATALYST: "Connecting with passion and motivation"
        }
        return best_for.get(technique, "General creative challenges")