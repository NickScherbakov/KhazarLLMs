"""Tests for ensemble orchestration."""

import pytest
from khazar_llms.agents.personas import DreamerAgent, CriticAgent, SynthesizerAgent
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode


def test_ensemble_creation():
    """Test creating an ensemble."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.SEQUENTIAL,
        max_iterations=3
    )
    
    assert len(ensemble.agents) == 2
    assert ensemble.mode == ConversationMode.SEQUENTIAL
    assert ensemble.max_iterations == 3


@pytest.mark.asyncio
async def test_ensemble_collaboration():
    """Test running a full collaboration."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(agents=agents, max_iterations=2)
    
    results = await ensemble.collaborate("Test task")
    
    assert "task" in results
    assert "conversation" in results
    assert results["agent_count"] == 2
    # 2 agents * 2 iterations = 4 messages in sequential mode
    assert len(results["conversation"]) == 4


@pytest.mark.asyncio
async def test_parallel_mode():
    """Test parallel conversation mode."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.PARALLEL,
        max_iterations=2
    )
    
    results = await ensemble.collaborate("Test task")
    
    # In parallel mode, all agents respond per iteration
    assert len(results["conversation"]) == 6  # 3 agents * 2 iterations


def test_get_agent_by_role():
    """Test retrieving agents by role."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(agents=agents)
    
    dreamer = ensemble.get_agent_by_role("dreamer")
    assert dreamer is not None
    assert dreamer.name == "Dreamer"
    
    missing = ensemble.get_agent_by_role("nonexistent")
    assert missing is None


def test_add_remove_agents():
    """Test adding and removing agents."""
    agents = [DreamerAgent(provider="mock")]
    ensemble = Ensemble(agents=agents)
    
    assert len(ensemble.agents) == 1
    
    # Add agent
    ensemble.add_agent(CriticAgent(provider="mock"))
    assert len(ensemble.agents) == 2
    
    # Remove agent
    result = ensemble.remove_agent("Critic")
    assert result is True
    assert len(ensemble.agents) == 1
    
    # Try removing non-existent agent
    result = ensemble.remove_agent("NonExistent")
    assert result is False


def test_ensemble_summary():
    """Test ensemble summary generation."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(agents=agents, max_iterations=5)
    summary = ensemble.get_summary()
    
    assert summary["max_iterations"] == 5
    assert len(summary["agents"]) == 2
    assert summary["conversation_length"] == 0
