"""LLM client for communicating with various providers."""

import os
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate a response from the LLM."""
        pass


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing without API calls."""

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate a mock response."""
        system_prompt = ""
        user_content = ""
        
        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "").lower()
            elif msg.get("role") == "user":
                user_content = msg.get("content", "").lower()
        
        # Generate contextual mock response based on agent role
        if "dreamer" in system_prompt:
            return (
                "I envision a world where ideas flow like rivers of light, "
                "where creativity manifests as living architecture, and where "
                "every thought births new possibilities. Imagine spaces that shift "
                "and transform based on the dreams they contain, where visitors "
                "walk through cascading memories and forgotten aspirations..."
            )
        elif "critic" in system_prompt:
            return (
                "While this idea has merit, we must examine its foundations. "
                "Are we considering the practical implications? What assumptions "
                "are we making that might not hold? I see potential issues with "
                "accessibility, sustainability, and the very nature of how we "
                "preserve ephemeral experiences. Let's dig deeper."
            )
        elif "synthesizer" in system_prompt:
            return (
                "Drawing together these diverse perspectives, I see a unified vision: "
                "we can combine the imaginative elements with structured implementation, "
                "creating something both beautiful and functional. The dreamer's vision "
                "of flowing spaces meets the critic's need for practicality in a design "
                "that honors both creativity and constraint."
            )
        elif "philosopher" in system_prompt:
            return (
                "What does it mean to preserve that which is forgotten? The paradox "
                "of remembering the forgotten touches on fundamental questions about "
                "memory, identity, and the nature of loss. This museum would be a "
                "meditation on impermanence and the stories we choose to keep alive."
            )
        elif "rebel" in system_prompt:
            return (
                "Why should forgotten dreams be preserved at all? Perhaps they should "
                "remain forgotten! What if instead we created a museum that actively "
                "destroys memories, that celebrates forgetting as liberation? Let's "
                "challenge the entire premise of preservation and archival."
            )
        elif "architect" in system_prompt:
            return (
                "Let me outline a concrete structure: Entry through a twilight portal, "
                "three main wings representing childhood, adult, and collective dreams, "
                "interconnected by spiral pathways. Each exhibit uses immersive "
                "technology while maintaining intimate, contemplative spaces. "
                "The building itself should reflect dream logic in its geometry."
            )
        elif "poet" in system_prompt:
            return (
                "This museum is itself a dream unfolding in stone and light. "
                "Each gallery a whispered memory, each corridor a breath between "
                "sleeping and waking. Visitors become characters in a story they've "
                "forgotten they knew, walking through chambers where the impossible "
                "becomes, for a moment, achingly real."
            )
        else:
            return (
                "This is a fascinating perspective that deserves deeper consideration. "
                "Let me reflect on how it connects to our broader goals and the "
                "creative challenge we're exploring together..."
            )


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
        
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate a response using OpenAI API."""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not found")
        
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate a response using Anthropic API."""
        # Convert OpenAI-style messages to Anthropic format
        system_message = next((m["content"] for m in messages if m["role"] == "system"), None)
        user_messages = [m for m in messages if m["role"] != "system"]
        
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            system=system_message,
            messages=user_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.content[0].text


class LLMClient:
    """Client for interacting with various LLM providers."""

    def __init__(self, provider: str = "mock", api_key: Optional[str] = None):
        """
        Initialize the LLM client.
        
        Args:
            provider: The LLM provider to use ('openai', 'anthropic', or 'mock')
            api_key: Optional API key (will use environment variable if not provided)
        """
        self.provider_name = provider.lower()
        
        if self.provider_name == "mock":
            self.provider = MockLLMProvider()
        elif self.provider_name == "openai":
            self.provider = OpenAIProvider(api_key)
        elif self.provider_name == "anthropic":
            self.provider = AnthropicProvider(api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            system_prompt: The system prompt defining agent behavior
            user_message: The user's message or task
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            The generated response text
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        
        return await self.provider.generate(messages, temperature, max_tokens)
