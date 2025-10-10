"""
Basic example of creating and running a KhazarLLMs ensemble.

This demonstrates how to create agents, assemble them into an ensemble,
and run a creative collaboration session.
"""

import asyncio
from pathlib import Path

from khazar_llms.agents.personas import (
    DreamerAgent,
    CriticAgent,
    SynthesizerAgent,
    PhilosopherAgent,
)
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode
from khazar_llms.orchestration.session import CreativeSession


async def main():
    """Run a basic ensemble example."""
    
    # Create agents with different personas
    # Using 'mock' provider for demo (no API keys needed)
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
        PhilosopherAgent(provider="mock"),
    ]

    # Create an ensemble in sequential mode
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.SEQUENTIAL,
        max_iterations=3,
    )

    # Create a creative session
    session = CreativeSession(
        ensemble=ensemble,
        output_dir=Path("./output/sessions"),
    )

    # Define a creative task
    task = """
    Design a new form of social network that prioritizes human connection 
    over engagement metrics. How would it work? What makes it different?
    """

    print("\n" + "=" * 80)
    print("STARTING KHAZAR LLMs CREATIVE SESSION")
    print("=" * 80)
    print(f"\nTask: {task.strip()}")
    print(f"\nAgents: {len(agents)}")
    for agent in agents:
        print(f"  - {agent.name} ({agent.role.value})")
    print(f"\nMode: {ensemble.mode}")
    print(f"Iterations: {ensemble.max_iterations}")
    print("\nRunning collaboration...\n")

    # Run the session
    results = await session.run(task)

    # Print results
    session.print_summary(results)

    # Save outputs
    json_path = session.save_session(results, format="json")
    txt_path = session.save_session(results, format="txt")

    print(f"\nSession saved:")
    print(f"  JSON: {json_path}")
    print(f"  Text: {txt_path}")

    # Display conversation
    print("\n" + "=" * 80)
    print("CONVERSATION TRANSCRIPT")
    print("=" * 80 + "\n")
    
    for i, msg in enumerate(results["conversation"], 1):
        print(f"\n[{i}] {msg.sender} ({msg.role.value}) - Iteration {msg.iteration}")
        print("-" * 40)
        print(msg.content)


if __name__ == "__main__":
    asyncio.run(main())
