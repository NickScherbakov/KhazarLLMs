"""Agent implementations for the KhazarLLMs ensemble."""

from .base import Agent, AgentRole
from .personas import (
    DreamerAgent,
    CriticAgent,
    SynthesizerAgent,
    PhilosopherAgent,
    RebelAgent,
)

__all__ = [
    "Agent",
    "AgentRole",
    "DreamerAgent",
    "CriticAgent",
    "SynthesizerAgent",
    "PhilosopherAgent",
    "RebelAgent",
]
