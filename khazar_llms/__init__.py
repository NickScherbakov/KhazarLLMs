"""
KhazarLLMs - A System for Collective Creativity Management

Inspired by the Khazar Dictionary's multiple perspectives and non-linear narratives,
this system orchestrates an ensemble of LLMs to work collectively on creative tasks.
"""

__version__ = "0.1.0"

from .agents.base import Agent, AgentRole
from .agents.personas import DreamerAgent, CriticAgent, SynthesizerAgent, PhilosopherAgent
from .orchestration.ensemble import Ensemble
from .orchestration.session import CreativeSession

__all__ = [
    "Agent",
    "AgentRole",
    "DreamerAgent",
    "CriticAgent",
    "SynthesizerAgent",
    "PhilosopherAgent",
    "Ensemble",
    "CreativeSession",
]
