"""
Showcase of creative tasks demonstrating KhazarLLMs capabilities.

This script runs several interesting creative challenges to show
the range of what the ensemble can do.
"""

import asyncio
from pathlib import Path

from khazar_llms.agents.personas import (
    DreamerAgent,
    CriticAgent,
    SynthesizerAgent,
    PhilosopherAgent,
    RebelAgent,
    ArchitectAgent,
    PoetAgent,
)
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode
from khazar_llms.orchestration.session import CreativeSession


async def run_task(name, task, agents, mode, iterations=2):
    """Run a single creative task and display results."""
    print("\n" + "=" * 80)
    print(f"CREATIVE CHALLENGE: {name}")
    print("=" * 80)
    print(f"\nTask: {task}")
    print(f"Agents: {', '.join(a.name for a in agents)}")
    print(f"Mode: {mode.value}")
    print("\n" + "-" * 80 + "\n")

    ensemble = Ensemble(agents=agents, mode=mode, max_iterations=iterations)
    session = CreativeSession(ensemble)
    results = await session.run(task)

    # Show each response
    for msg in results["conversation"]:
        print(f"{msg.sender}: {msg.content[:300]}...")
        print()


async def main():
    """Run showcase of creative tasks."""
    
    print("\n" + "=" * 80)
    print("KHAZAR LLMs CREATIVE SHOWCASE")
    print("=" * 80)
    print("\nDemonstrating the collective creativity of an AI ensemble\n")

    # Task 1: Philosophical exploration
    await run_task(
        name="The Nature of Reality",
        task="Is reality fundamentally made of information or matter?",
        agents=[
            PhilosopherAgent(provider="mock"),
            RebelAgent(provider="mock"),
        ],
        mode=ConversationMode.DEBATE,
        iterations=1,
    )

    # Task 2: Creative writing
    await run_task(
        name="Opening Line",
        task="Write the first sentence of a novel about a city that dreams",
        agents=[
            DreamerAgent(provider="mock"),
            PoetAgent(provider="mock"),
            CriticAgent(provider="mock"),
        ],
        mode=ConversationMode.SEQUENTIAL,
        iterations=1,
    )

    # Task 3: Product design
    await run_task(
        name="Future of Transportation",
        task="Design a personal transportation device for the year 2050",
        agents=[
            DreamerAgent(provider="mock"),
            ArchitectAgent(provider="mock"),
            CriticAgent(provider="mock"),
        ],
        mode=ConversationMode.SEQUENTIAL,
        iterations=1,
    )

    # Task 4: Problem solving
    await run_task(
        name="Social Connection",
        task="How can we help people form deeper connections in a digital age?",
        agents=[
            PhilosopherAgent(provider="mock"),
            ArchitectAgent(provider="mock"),
            SynthesizerAgent(provider="mock"),
        ],
        mode=ConversationMode.SEQUENTIAL,
        iterations=1,
    )

    # Task 5: Wild creativity
    await run_task(
        name="Impossible Inventions",
        task="Invent something that shouldn't exist but would be beautiful if it did",
        agents=[
            DreamerAgent(provider="mock"),
            RebelAgent(provider="mock"),
            PoetAgent(provider="mock"),
        ],
        mode=ConversationMode.PARALLEL,
        iterations=1,
    )

    print("\n" + "=" * 80)
    print("SHOWCASE COMPLETE")
    print("=" * 80)
    print("\nThese examples demonstrate different combinations of agents,")
    print("conversation modes, and creative challenges. Try your own!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
