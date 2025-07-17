"""
Claude API Client
================

Handles communication with Claude Sonnet 3.7 via the Anthropic API.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, AsyncIterator

import httpx
from anthropic import AsyncAnthropic
from anthropic.types import MessageParam, Message
from pydantic import BaseModel

from .config import Settings

logger = logging.getLogger(__name__)


class ClaudeResponse(BaseModel):
    """Response model for Claude API calls."""
    content: str
    usage: Dict[str, Any]
    model: str
    role: str = "assistant"
    stop_reason: Optional[str] = None


class ClaudeClient:
    """
    Client for interacting with Claude Sonnet 3.7 via the Anthropic API.
    
    Supports both streaming and non-streaming responses, with built-in
    error handling and retry logic.
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature
        
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        **kwargs
    ) -> ClaudeResponse:
        """
        Complete a prompt using Claude.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            context: Optional context dictionary
            stream: Whether to stream the response
            **kwargs: Additional parameters for the API call
            
        Returns:
            ClaudeResponse object with the completion
        """
        try:
            # Prepare messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add context if provided
            if context:
                context_str = self._format_context(context)
                messages.append({"role": "user", "content": context_str})
            
            messages.append({"role": "user", "content": prompt})
            
            # Prepare API parameters
            api_params = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "messages": messages,
            }
            
            # Add system prompt if provided
            if system_prompt:
                api_params["system"] = system_prompt
                # Remove system message from messages
                messages = [msg for msg in messages if msg["role"] != "system"]
                api_params["messages"] = messages
            
            logger.info(f"Making Claude API call with model: {self.model}")
            
            if stream:
                return await self._stream_completion(api_params)
            else:
                return await self._complete_sync(api_params)
                
        except Exception as e:
            logger.error(f"Error in Claude completion: {str(e)}")
            raise
    
    async def _complete_sync(self, api_params: Dict[str, Any]) -> ClaudeResponse:
        """Complete synchronously."""
        try:
            response = await self.client.messages.create(**api_params)
            
            # Extract content
            content = ""
            if response.content:
                for block in response.content:
                    if hasattr(block, 'text'):
                        content += block.text
            
            return ClaudeResponse(
                content=content,
                usage=response.usage.model_dump() if response.usage else {},
                model=response.model,
                role="assistant",
                stop_reason=response.stop_reason
            )
            
        except Exception as e:
            logger.error(f"Error in sync completion: {str(e)}")
            raise
    
    async def _stream_completion(self, api_params: Dict[str, Any]) -> AsyncIterator[str]:
        """Stream completion."""
        try:
            api_params["stream"] = True
            
            async with self.client.messages.stream(**api_params) as stream:
                async for chunk in stream:
                    if chunk.type == "content_block_delta":
                        if hasattr(chunk.delta, 'text'):
                            yield chunk.delta.text
                            
        except Exception as e:
            logger.error(f"Error in stream completion: {str(e)}")
            raise
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary into a readable string."""
        if not context:
            return ""
        
        formatted = "Context:\n"
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                formatted += f"- {key}: {json.dumps(value, indent=2)}\n"
            else:
                formatted += f"- {key}: {value}\n"
        
        return formatted
    
    async def chat(
        self,
        messages: List[MessageParam],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> ClaudeResponse:
        """
        Chat with Claude using a list of messages.
        
        Args:
            messages: List of messages in the conversation
            system_prompt: Optional system prompt
            **kwargs: Additional parameters
            
        Returns:
            ClaudeResponse object
        """
        try:
            api_params = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "messages": messages,
            }
            
            if system_prompt:
                api_params["system"] = system_prompt
            
            logger.info(f"Making Claude chat API call with {len(messages)} messages")
            
            response = await self.client.messages.create(**api_params)
            
            # Extract content
            content = ""
            if response.content:
                for block in response.content:
                    if hasattr(block, 'text'):
                        content += block.text
            
            return ClaudeResponse(
                content=content,
                usage=response.usage.model_dump() if response.usage else {},
                model=response.model,
                role="assistant",
                stop_reason=response.stop_reason
            )
            
        except Exception as e:
            logger.error(f"Error in Claude chat: {str(e)}")
            raise
    
    async def analyze_code(
        self,
        code: str,
        language: str = "python",
        task: str = "analyze",
        **kwargs
    ) -> ClaudeResponse:
        """
        Analyze code using Claude with specialized prompts.
        
        Args:
            code: The code to analyze
            language: Programming language
            task: Type of analysis (analyze, review, improve, debug)
            **kwargs: Additional parameters
            
        Returns:
            ClaudeResponse object
        """
        system_prompt = f"""You are an expert {language} developer with deep knowledge of best practices, 
        design patterns, and code optimization. You provide thoughtful, detailed analysis with practical 
        suggestions for improvement."""
        
        task_prompts = {
            "analyze": f"Please analyze the following {language} code and provide insights on its structure, logic, and potential improvements:",
            "review": f"Please review the following {language} code for bugs, security issues, and code quality:",
            "improve": f"Please suggest improvements for the following {language} code, focusing on performance, readability, and maintainability:",
            "debug": f"Please help debug the following {language} code and identify potential issues:",
        }
        
        prompt = f"{task_prompts.get(task, task_prompts['analyze'])}\n\n```{language}\n{code}\n```"
        
        return await self.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            **kwargs
        )
    
    async def vibe_code(
        self,
        request: str,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> ClaudeResponse:
        """
        Generate code with the "vibe coding" approach - empathetic, understanding, and thoughtful.
        
        Args:
            request: The coding request
            context: Optional context about the project
            **kwargs: Additional parameters
            
        Returns:
            ClaudeResponse object
        """
        system_prompt = """You are a thoughtful, empathetic programming companion with deep technical expertise. 
        You understand that coding is both an art and a science, and you approach each request with:
        
        - Empathy: Understanding the developer's needs and frustrations
        - Reassurance: Providing confidence and encouragement
        - Kindness: Being patient and supportive in your explanations
        - Understanding: Grasping the broader context and goals
        - Appreciation: Recognizing the complexity and creativity in programming
        - Deep-dive modeling: Providing thorough, well-reasoned solutions
        - Strong reasoning: Explaining the "why" behind every recommendation
        
        You create code that is not just functional, but elegant, maintainable, and thoughtfully designed.
        You explain your reasoning clearly and offer alternatives when appropriate."""
        
        return await self.complete(
            prompt=request,
            system_prompt=system_prompt,
            context=context,
            **kwargs
        )
    
    async def health_check(self) -> bool:
        """
        Check if the Claude API is accessible.
        
        Returns:
            True if the API is accessible, False otherwise
        """
        try:
            response = await self.complete(
                prompt="Hello, please respond with 'OK' if you can hear me.",
                max_tokens=10
            )
            return "OK" in response.content.upper()
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False