"""Tests for KPS protocol implementation."""

import pytest
import json
from datetime import datetime
from pathlib import Path

from khazar_llms.protocol import KPSValidator, ValidationResult
from khazar_llms.protocol.models import (
    KPSAgent,
    KPSMessage,
    KPSSession,
    KPSSynthesis,
    Archetype,
    Intent,
    SessionState,
)
from khazar_llms.agents.base import AgentRole, Message
from khazar_llms.agents.personas import DreamerAgent, CriticAgent


class TestKPSModels:
    """Test KPS data models."""

    def test_kps_agent_model(self):
        """Test KPS agent model."""
        agent_data = {
            "agent_id": "dreamer-001",
            "persona": {
                "name": "The Dreamer",
                "archetype": "creative_visionary",
                "system_prompt": "You are the Dreamer",
            },
            "capabilities": ["generate", "respond"],
            "provider": "mock",
        }
        agent = KPSAgent(**agent_data)
        assert agent.agent_id == "dreamer-001"
        assert agent.persona.name == "The Dreamer"
        assert "generate" in agent.capabilities

    def test_kps_message_model(self):
        """Test KPS message model."""
        message_data = {
            "message_id": "msg-001",
            "session_id": "session-001",
            "timestamp": "2024-12-13T14:30:00.000Z",
            "sender": {
                "agent_id": "dreamer-001",
                "persona_name": "The Dreamer",
            },
            "content": {
                "text": "Test message",
            },
            "metadata": {
                "round": 0,
                "turn": 0,
                "mode": "sequential",
            },
            "annotations": {
                "intent": "propose",
            },
        }
        message = KPSMessage(**message_data)
        assert message.message_id == "msg-001"
        assert message.content.text == "Test message"
        assert message.annotations.intent == "propose"

    def test_kps_session_model(self):
        """Test KPS session model."""
        session_data = {
            "session_id": "session-001",
            "prompt": "Test task",
            "state": "ACTIVE",
            "config": {
                "mode": "sequential",
                "max_rounds": 5,
                "synthesis_strategy": "final_agent",
            },
            "participants": ["agent-001", "agent-002"],
            "created_at": "2024-12-13T14:30:00.000Z",
        }
        session = KPSSession(**session_data)
        assert session.session_id == "session-001"
        assert session.config.mode == "sequential"
        assert len(session.participants) == 2


class TestKPSValidator:
    """Test KPS validator."""

    def test_validate_valid_agent(self):
        """Test validating a valid agent."""
        agent_data = {
            "agent_id": "dreamer-001",
            "persona": {
                "name": "The Dreamer",
                "archetype": "creative_visionary",
                "system_prompt": "You are the Dreamer",
            },
            "capabilities": ["generate", "respond"],
            "provider": "mock",
        }
        validator = KPSValidator()
        result = validator.validate_agent(agent_data)
        assert result.valid
        assert len(result.errors) == 0

    def test_validate_invalid_agent(self):
        """Test validating an invalid agent."""
        agent_data = {
            "agent_id": "dreamer-001",
            # Missing required persona field
            "capabilities": ["generate"],
            "provider": "mock",
        }
        validator = KPSValidator()
        result = validator.validate_agent(agent_data)
        assert not result.valid
        assert len(result.errors) > 0

    def test_validate_valid_message(self):
        """Test validating a valid message."""
        message_data = {
            "message_id": "550e8400-e29b-41d4-a716-446655440000",
            "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
            "timestamp": "2024-12-13T14:30:00.000Z",
            "sender": {
                "agent_id": "dreamer-001",
                "persona_name": "The Dreamer",
            },
            "content": {
                "text": "Test message",
            },
            "metadata": {
                "round": 0,
                "turn": 0,
                "mode": "sequential",
            },
            "annotations": {
                "intent": "propose",
            },
        }
        validator = KPSValidator()
        result = validator.validate_message(message_data)
        assert result.valid

    def test_validate_custom_archetype_warning(self):
        """Test that custom archetypes generate warnings."""
        agent_data = {
            "agent_id": "custom-001",
            "persona": {
                "name": "The Custom",
                "archetype": "com.example.custom",
                "system_prompt": "Custom agent prompt",
            },
            "capabilities": ["respond"],
            "provider": "mock",
        }
        validator = KPSValidator()
        result = validator.validate_agent(agent_data)
        assert result.valid
        assert len(result.warnings) > 0
        assert "custom archetype" in result.warnings[0].lower()

    def test_validate_session_export(self):
        """Test validating a complete session export."""
        export_data = {
            "version": "1.0.0-draft",
            "session": {
                "session_id": "session-001",
                "prompt": "Test task",
                "state": "COMPLETED",
                "config": {
                    "mode": "sequential",
                    "max_rounds": 3,
                    "synthesis_strategy": "final_agent",
                },
                "participants": ["agent-001"],
                "created_at": "2024-12-13T14:30:00.000Z",
            },
            "agents": [
                {
                    "agent_id": "agent-001",
                    "persona": {
                        "name": "Test Agent",
                        "archetype": "creative_visionary",
                        "system_prompt": "Test prompt",
                    },
                    "capabilities": ["generate"],
                    "provider": "mock",
                }
            ],
            "messages": [
                {
                    "message_id": "msg-001",
                    "session_id": "session-001",
                    "timestamp": "2024-12-13T14:30:00.000Z",
                    "sender": {
                        "agent_id": "agent-001",
                        "persona_name": "Test Agent",
                    },
                    "content": {"text": "Test"},
                    "metadata": {
                        "round": 0,
                        "turn": 0,
                        "mode": "sequential",
                    },
                    "annotations": {
                        "intent": "propose",
                    },
                }
            ],
        }
        validator = KPSValidator()
        result = validator.validate_session_export(export_data)
        assert result.valid


class TestKPSExport:
    """Test KPS export functionality."""

    def test_message_to_kps(self):
        """Test converting Message to KPS format."""
        msg = Message(
            sender="Dreamer",
            role=AgentRole.DREAMER,
            content="Test content",
            iteration=0,
        )
        
        kps_msg = msg.to_kps(
            session_id="test-session",
            agent_id="dreamer-001",
            mode="sequential",
            intent="propose",
        )
        
        assert kps_msg["session_id"] == "test-session"
        assert kps_msg["sender"]["agent_id"] == "dreamer-001"
        assert kps_msg["content"]["text"] == "Test content"
        assert kps_msg["metadata"]["round"] == 0
        assert kps_msg["annotations"]["intent"] == "propose"

    def test_agent_to_kps(self):
        """Test converting Agent to KPS format."""
        agent = DreamerAgent(provider="mock")
        kps_agent = agent.to_kps(agent_id="dreamer-001")
        
        assert kps_agent["agent_id"] == "dreamer-001"
        assert kps_agent["persona"]["name"] == "Dreamer"
        assert kps_agent["persona"]["archetype"] == "creative_visionary"
        assert kps_agent["provider"] == "mock"
        assert "generate" in kps_agent["capabilities"]

    def test_agent_to_kps_different_roles(self):
        """Test that different agent roles export correctly."""
        critic = CriticAgent(provider="mock")
        kps_critic = critic.to_kps()
        
        assert kps_critic["persona"]["archetype"] == "analytical_challenger"
        assert "critique" in kps_critic["capabilities"]
        assert kps_critic["persona"]["symbol"] == "🔍"


class TestValidationResult:
    """Test ValidationResult class."""

    def test_validation_result_valid(self):
        """Test valid result."""
        result = ValidationResult(valid=True)
        assert result.valid
        assert bool(result)
        assert len(result.errors) == 0

    def test_validation_result_invalid(self):
        """Test invalid result."""
        result = ValidationResult(valid=False, errors=["Error 1", "Error 2"])
        assert not result.valid
        assert not bool(result)
        assert len(result.errors) == 2

    def test_validation_result_with_warnings(self):
        """Test result with warnings."""
        result = ValidationResult(
            valid=True,
            warnings=["Warning 1"],
        )
        assert result.valid
        assert len(result.warnings) == 1

    def test_validation_result_to_dict(self):
        """Test converting result to dict."""
        result = ValidationResult(
            valid=False,
            errors=["Error"],
            warnings=["Warning"],
        )
        data = result.to_dict()
        assert data["valid"] is False
        assert len(data["errors"]) == 1
        assert len(data["warnings"]) == 1
