"""Tests for LLM client functionality."""

import pytest
from khazar_llms.utils.llm_client import LLMClient, MockLLMProvider


@pytest.mark.asyncio
async def test_mock_provider():
    """Test mock LLM provider."""
    provider = MockLLMProvider()
    
    messages = [
        {"role": "system", "content": "You are the Dreamer"},
        {"role": "user", "content": "Tell me about dreams"}
    ]
    
    response = await provider.generate(messages, temperature=0.7, max_tokens=100)
    
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_llm_client_mock():
    """Test LLM client with mock provider."""
    client = LLMClient(provider="mock")
    
    response = await client.generate_response(
        system_prompt="You are the Dreamer",
        user_message="Generate a creative idea",
        temperature=0.8,
    )
    
    assert isinstance(response, str)
    assert len(response) > 0


def test_llm_client_invalid_provider():
    """Test creating client with invalid provider."""
    with pytest.raises(ValueError):
        LLMClient(provider="invalid_provider")


@pytest.mark.asyncio
async def test_mock_responses_vary_by_context():
    """Test that mock responses vary based on context."""
    client = LLMClient(provider="mock")
    
    dreamer_response = await client.generate_response(
        system_prompt="You are the Dreamer",
        user_message="Be creative",
    )
    
    critic_response = await client.generate_response(
        system_prompt="You are the Critic",
        user_message="Be critical",
    )
    
    # Responses should be different based on context
    assert dreamer_response != critic_response
