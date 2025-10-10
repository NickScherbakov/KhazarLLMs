"""Base agent class and role definitions."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    """Different roles agents can take in the creative ensemble."""

    DREAMER = "dreamer"  # Generates wild, creative ideas
    CRITIC = "critic"  # Analyzes and critiques ideas
    SYNTHESIZER = "synthesizer"  # Combines ideas into coherent wholes
    PHILOSOPHER = "philosopher"  # Provides deep context and meaning
    REBEL = "rebel"  # Challenges assumptions and breaks rules
    ARCHITECT = "architect"  # Structures and organizes ideas
    POET = "poet"  # Adds beauty and emotional resonance


class Message(BaseModel):
    """A message in the creative conversation."""

    sender: str
    role: AgentRole
    content: str
    iteration: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Agent(ABC):
    """Base class for all creative agents in the ensemble."""

    def __init__(
        self,
        name: str,
        role: AgentRole,
        temperature: float = 0.8,
        model: str = "gpt-4",
        provider: str = "openai",
    ):
        self.name = name
        self.role = role
        self.temperature = temperature
        self.model = model
        self.provider = provider
        self.memory: List[Message] = []

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt that defines this agent's personality."""
        pass

    @abstractmethod
    async def respond(
        self, task: str, context: List[Message], iteration: int
    ) -> Message:
        """Generate a response to the creative task given the conversation context."""
        pass

    def add_to_memory(self, message: Message):
        """Add a message to the agent's memory."""
        self.memory.append(message)

    def get_context_summary(self, context: List[Message], max_messages: int = 5) -> str:
        """Get a summary of recent conversation context."""
        recent = context[-max_messages:] if len(context) > max_messages else context
        summary = []
        for msg in recent:
            summary.append(f"{msg.sender} ({msg.role}): {msg.content[:200]}...")
        return "\n".join(summary)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', role={self.role})>"
