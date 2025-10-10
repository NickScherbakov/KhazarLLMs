"""Tests for agent functionality."""

import pytest
from khazar_llms.agents.base import AgentRole, Message
from khazar_llms.agents.personas import (
    DreamerAgent,
    CriticAgent,
    SynthesizerAgent,
    PhilosopherAgent,
)


def test_agent_creation():
    """Test creating agents with different personas."""
    dreamer = DreamerAgent(provider="mock")
    assert dreamer.name == "Dreamer"
    assert dreamer.role == AgentRole.DREAMER
    assert dreamer.temperature == 0.95

    critic = CriticAgent(provider="mock")
    assert critic.name == "Critic"
    assert critic.role == AgentRole.CRITIC
    assert critic.temperature == 0.4


def test_agent_system_prompts():
    """Test that agents have unique system prompts."""
    dreamer = DreamerAgent(provider="mock")
    critic = CriticAgent(provider="mock")
    
    dreamer_prompt = dreamer.get_system_prompt()
    critic_prompt = critic.get_system_prompt()
    
    assert len(dreamer_prompt) > 0
    assert len(critic_prompt) > 0
    assert dreamer_prompt != critic_prompt
    assert "Dreamer" in dreamer_prompt
    assert "Critic" in critic_prompt


@pytest.mark.asyncio
async def test_agent_response():
    """Test agent response generation."""
    agent = DreamerAgent(provider="mock")
    context = []
    
    message = await agent.respond(
        task="Test task",
        context=context,
        iteration=0
    )
    
    assert isinstance(message, Message)
    assert message.sender == "Dreamer"
    assert message.role == AgentRole.DREAMER
    assert message.iteration == 0
    assert len(message.content) > 0


def test_agent_memory():
    """Test agent memory functionality."""
    agent = DreamerAgent(provider="mock")
    
    msg1 = Message(
        sender="Test",
        role=AgentRole.DREAMER,
        content="Test content",
        iteration=0
    )
    
    agent.add_to_memory(msg1)
    assert len(agent.memory) == 1
    assert agent.memory[0] == msg1


def test_context_summary():
    """Test context summary generation."""
    agent = DreamerAgent(provider="mock")
    
    messages = [
        Message(sender="Agent1", role=AgentRole.DREAMER, content="A" * 300, iteration=0),
        Message(sender="Agent2", role=AgentRole.CRITIC, content="B" * 300, iteration=0),
    ]
    
    summary = agent.get_context_summary(messages, max_messages=2)
    assert "Agent1" in summary
    assert "Agent2" in summary
    # Content should be truncated
    assert len(summary) < len(messages[0].content) + len(messages[1].content)
