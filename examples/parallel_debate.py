"""
Example of parallel and debate modes in KhazarLLMs.

This demonstrates different conversation patterns and how agents
can interact in various orchestration modes.
"""

import asyncio
from pathlib import Path

from khazar_llms.agents.personas import (
    DreamerAgent,
    CriticAgent,
    RebelAgent,
    PhilosopherAgent,
    ArchitectAgent,
    PoetAgent,
)
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode
from khazar_llms.orchestration.session import CreativeSession


async def run_parallel_session():
    """Run a session in parallel mode."""
    
    agents = [
        DreamerAgent(provider="mock"),
        RebelAgent(provider="mock"),
        PoetAgent(provider="mock"),
    ]

    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.PARALLEL,
        max_iterations=2,
    )

    session = CreativeSession(ensemble=ensemble)

    task = "Imagine a new art form that exists in the space between dreams and reality."

    print("\n" + "=" * 80)
    print("PARALLEL MODE - All agents speak simultaneously")
    print("=" * 80 + "\n")

    results = await session.run(task)
    
    for msg in results["conversation"]:
        print(f"\n{msg.sender}: {msg.content[:200]}...")

    return results


async def run_debate_session():
    """Run a session in debate mode."""
    
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        PhilosopherAgent(provider="mock"),
        ArchitectAgent(provider="mock"),
    ]

    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.DEBATE,
        max_iterations=2,
    )

    session = CreativeSession(ensemble=ensemble)

    task = "Should AI systems be designed to maximize efficiency or to embrace uncertainty?"

    print("\n" + "=" * 80)
    print("DEBATE MODE - Agents engage in structured dialogue")
    print("=" * 80 + "\n")

    results = await session.run(task)
    
    for msg in results["conversation"]:
        print(f"\n{msg.sender}: {msg.content[:200]}...")

    return results


async def main():
    """Run all example sessions."""
    
    print("\n" + "=" * 80)
    print("KHAZAR LLMs - ADVANCED ORCHESTRATION EXAMPLES")
    print("=" * 80)

    # Run parallel session
    await run_parallel_session()

    # Run debate session
    await run_debate_session()

    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
