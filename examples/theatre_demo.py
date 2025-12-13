"""
Theatre Mode demonstration script.

This example shows how to use KhazarLLMs Theatre Mode to create
beautiful, theatrical visualizations of agent conversations.

Run this script to see:
- Agents performing on a virtual stage
- Different visual output formats
- Theatrical stage directions and formatting
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
from khazar_llms.visualization.theatre import TheatreMode


async def main():
    """Run a theatre mode demonstration."""
    
    print("\n" + "=" * 80)
    print("🎭 KHAZAR THEATRE MODE DEMONSTRATION 🎭")
    print("=" * 80 + "\n")
    
    # Create a diverse ensemble of agents
    # Using 'mock' provider for demo (no API keys needed)
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
        PhilosopherAgent(provider="mock"),
        RebelAgent(provider="mock"),
        ArchitectAgent(provider="mock"),
        PoetAgent(provider="mock"),
    ]

    # Create an ensemble in sequential mode
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.SEQUENTIAL,
        max_iterations=2,  # Keep it short for demo
    )

    # Create theatre mode
    theatre = TheatreMode(
        ensemble=ensemble,
        use_color=True,  # Enable colors for terminal
        width=65,
    )

    # Define a creative task
    task = "Design a new form of communication that transcends language barriers"

    print(f"Task: {task}\n")
    print(f"Ensemble: {len(agents)} agents in {ensemble.mode.value} mode")
    print(f"Iterations: {ensemble.max_iterations}")
    print("\nStarting performance...\n")
    print("=" * 80 + "\n")

    # Run the performance
    results = await theatre.perform(task)

    # Display in terminal
    print("\n" + "=" * 80)
    print("TERMINAL OUTPUT")
    print("=" * 80 + "\n")
    
    theatre.print_performance(
        task,
        results["conversation"],
        metadata=results,
    )

    # Save outputs in different formats
    output_dir = Path("./output/theatre_demo")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save as Markdown
    markdown_path = output_dir / "performance.md"
    theatre.save(
        task,
        results["conversation"],
        markdown_path,
        format="markdown",
        metadata=results,
    )
    print(f"\n✨ Markdown saved to: {markdown_path}")

    # Save as HTML
    html_path = output_dir / "performance.html"
    theatre.save(
        task,
        results["conversation"],
        html_path,
        format="html",
        metadata=results,
    )
    print(f"✨ HTML saved to: {html_path}")

    # Show some statistics
    print("\n" + "=" * 80)
    print("PERFORMANCE STATISTICS")
    print("=" * 80)
    print(f"Total messages: {len(results['conversation'])}")
    print(f"Actors: {results['agent_count']}")
    print(f"Duration: {results.get('duration_seconds', 0):.2f} seconds")
    
    # Count messages per agent
    message_counts = {}
    for msg in results["conversation"]:
        message_counts[msg.sender] = message_counts.get(msg.sender, 0) + 1
    
    print("\nMessages per agent:")
    for agent_name, count in sorted(message_counts.items()):
        print(f"  {agent_name}: {count}")
    
    print("\n" + "=" * 80)
    print("✅ Demo complete! Check the output directory for saved files.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
