"""Base agent class and role definitions."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


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

    def to_kps(
        self,
        session_id: str,
        agent_id: str,
        mode: str = "sequential",
        turn: int = 0,
        intent: str = "propose",
        message_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convert message to KPS-compliant format.
        
        Args:
            session_id: Session identifier
            agent_id: Agent identifier
            mode: Orchestration mode
            turn: Turn number within round
            intent: Message intent (propose, challenge, etc.)
            message_id: Optional message ID (generated if not provided)
            timestamp: Optional ISO 8601 timestamp (current time if not provided)
            
        Returns:
            KPS-compliant message dictionary
        """
        return {
            "message_id": message_id or str(uuid.uuid4()),
            "session_id": session_id,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "sender": {
                "agent_id": agent_id,
                "persona_name": self.sender,
            },
            "content": {
                "text": self.content,
                "format": "plain",
                "language": "en",
            },
            "metadata": {
                "round": self.iteration,
                "turn": turn,
                "mode": mode,
                "responding_to": self.metadata.get("responding_to", []),
                "stage_direction": self.metadata.get("stage_direction"),
            },
            "annotations": {
                "sentiment": self.metadata.get("sentiment"),
                "intent": intent,
                "confidence": self.metadata.get("confidence"),
            },
        }


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

    def to_kps(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert agent to KPS-compliant format.
        
        Args:
            agent_id: Optional agent ID (generated if not provided)
            
        Returns:
            KPS-compliant agent dictionary
        """
        # Map role to archetype
        role_to_archetype = {
            AgentRole.DREAMER: "creative_visionary",
            AgentRole.CRITIC: "analytical_challenger",
            AgentRole.SYNTHESIZER: "integrative_harmonizer",
            AgentRole.PHILOSOPHER: "contextual_thinker",
            AgentRole.REBEL: "disruptive_iconoclast",
            AgentRole.ARCHITECT: "structural_organizer",
            AgentRole.POET: "aesthetic_artisan",
        }
        
        # Map role to symbol and color
        role_attributes = {
            AgentRole.DREAMER: {"symbol": "🌙", "color": "#9333ea"},
            AgentRole.CRITIC: {"symbol": "🔍", "color": "#dc2626"},
            AgentRole.SYNTHESIZER: {"symbol": "🌊", "color": "#2563eb"},
            AgentRole.PHILOSOPHER: {"symbol": "🦉", "color": "#7c3aed"},
            AgentRole.REBEL: {"symbol": "⚡", "color": "#ea580c"},
            AgentRole.ARCHITECT: {"symbol": "🏛️", "color": "#059669"},
            AgentRole.POET: {"symbol": "🎭", "color": "#db2777"},
        }
        
        attrs = role_attributes.get(self.role, {"symbol": "✨", "color": "#6366f1"})
        
        return {
            "agent_id": agent_id or f"{self.role.value}-{uuid.uuid4()}",
            "persona": {
                "name": self.name,
                "archetype": role_to_archetype.get(self.role, "custom"),
                "symbol": attrs["symbol"],
                "color": attrs["color"],
                "system_prompt": self.get_system_prompt(),
                "traits": [],
                "communication_style": self._get_communication_style(),
            },
            "capabilities": self._get_capabilities(),
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "metadata": {
                "version": "1.0.0",
                "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        }

    def _get_communication_style(self) -> str:
        """Get communication style based on role."""
        styles = {
            AgentRole.DREAMER: "poetic, metaphorical, expansive",
            AgentRole.CRITIC: "direct, incisive, constructive",
            AgentRole.SYNTHESIZER: "integrative, bridging, unifying",
            AgentRole.PHILOSOPHER: "contemplative, profound, questioning",
            AgentRole.REBEL: "provocative, contrarian, bold",
            AgentRole.ARCHITECT: "systematic, logical, methodical",
            AgentRole.POET: "lyrical, evocative, emotive",
        }
        return styles.get(self.role, "thoughtful, clear")

    def _get_capabilities(self) -> List[str]:
        """Get capabilities based on role."""
        capabilities = {
            AgentRole.DREAMER: ["generate", "respond"],
            AgentRole.CRITIC: ["critique", "respond"],
            AgentRole.SYNTHESIZER: ["synthesize", "respond"],
            AgentRole.PHILOSOPHER: ["respond", "generate"],
            AgentRole.REBEL: ["critique", "respond"],
            AgentRole.ARCHITECT: ["synthesize", "respond"],
            AgentRole.POET: ["generate", "respond"],
        }
        return capabilities.get(self.role, ["respond"])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', role={self.role})>"
