#!/usr/bin/env python3
"""
Command-line interface for KhazarLLMs.

Usage:
    python -m khazar_llms.cli create-task "Your creative task here"
    python -m khazar_llms.cli --mode parallel --iterations 5 create-task "Your task"
"""

import argparse
import asyncio
from pathlib import Path

from .agents.personas import (
    DreamerAgent,
    CriticAgent,
    SynthesizerAgent,
    PhilosopherAgent,
    RebelAgent,
    ArchitectAgent,
    PoetAgent,
)
from .orchestration.ensemble import Ensemble, ConversationMode
from .orchestration.session import CreativeSession


AVAILABLE_AGENTS = {
    "dreamer": DreamerAgent,
    "critic": CriticAgent,
    "synthesizer": SynthesizerAgent,
    "philosopher": PhilosopherAgent,
    "rebel": RebelAgent,
    "architect": ArchitectAgent,
    "poet": PoetAgent,
}


def create_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="KhazarLLMs - Collective Creativity Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "command",
        choices=["create-task", "list-agents", "info", "benchmark"],
        help="Command to execute",
    )

    parser.add_argument(
        "task",
        nargs="?",
        help="The creative task for the ensemble (required for create-task)",
    )

    parser.add_argument(
        "--agents",
        nargs="+",
        choices=list(AVAILABLE_AGENTS.keys()),
        default=["dreamer", "critic", "synthesizer", "philosopher"],
        help="Agents to include in the ensemble",
    )

    parser.add_argument(
        "--mode",
        choices=["sequential", "parallel", "debate", "consensus"],
        default="sequential",
        help="Conversation mode",
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Number of conversation iterations",
    )

    parser.add_argument(
        "--provider",
        choices=["mock", "openai", "anthropic"],
        default="mock",
        help="LLM provider to use",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./output/sessions"),
        help="Directory for session outputs",
    )

    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save session to disk",
    )

    parser.add_argument(
        "--theatre",
        action="store_true",
        help="Enable theatre mode visualization",
    )

    parser.add_argument(
        "--format",
        choices=["terminal", "markdown", "html", "json"],
        default="terminal",
        help="Output format (default: terminal)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Save theatre output to file (format auto-detected from extension or use --format)",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable color output in theatre mode",
    )

    # Benchmark-specific arguments
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full benchmark suite (for benchmark command)",
    )

    parser.add_argument(
        "--category",
        type=str,
        help="Run benchmark for specific category (for benchmark command)",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        help="Run benchmark on single custom prompt (for benchmark command)",
    )

    return parser


def list_agents():
    """List available agents."""
    print("\n" + "=" * 80)
    print("AVAILABLE AGENTS")
    print("=" * 80 + "\n")
    
    for name, agent_class in AVAILABLE_AGENTS.items():
        agent = agent_class(provider="mock")
        print(f"{name.upper()}")
        print(f"  Role: {agent.role.value}")
        print(f"  Description: {agent.__doc__}")
        print()


def show_info():
    """Show system information."""
    print("\n" + "=" * 80)
    print("KHAZAR LLMs - Collective Creativity Management")
    print("=" * 80 + "\n")
    print("A system for orchestrating ensemble LLMs in creative collaboration.")
    print("\nInspired by the Khazar Dictionary's multiple perspectives,")
    print("this system brings together agents with different roles and")
    print("personalities to explore creative tasks from many angles.")
    print("\nAvailable conversation modes:")
    print("  - sequential: Agents speak one after another")
    print("  - parallel: Agents respond simultaneously")
    print("  - debate: Agents engage in structured debate")
    print("  - consensus: Agents work toward agreement")
    print("\nTheatre Mode:")
    print("  Enable with --theatre flag to see conversations as a theatrical")
    print("  performance with visual formatting, stage directions, and colors.")
    print("  Save output as Markdown or HTML with --output and --format flags.")
    print("\nExample usage:")
    print('  python -m khazar_llms.cli create-task "Design a new social network"')
    print('  python -m khazar_llms.cli --mode parallel create-task "Imagine a new art form"')
    print('  python -m khazar_llms.cli --theatre create-task "Create a new language"')
    print('  python -m khazar_llms.cli --theatre --output theatre.html create-task "Your task"')
    print("\n" + "=" * 80 + "\n")


async def run_creative_task(args):
    """Run a creative task with the ensemble."""
    
    if not args.task:
        print("Error: Task is required for create-task command")
        return

    # Create agents
    agents = []
    for agent_name in args.agents:
        agent_class = AVAILABLE_AGENTS[agent_name]
        agents.append(agent_class(provider=args.provider))

    # Create ensemble
    mode = ConversationMode(args.mode)
    ensemble = Ensemble(
        agents=agents,
        mode=mode,
        max_iterations=args.iterations,
    )

    # Check if theatre mode is enabled
    if args.theatre:
        # Import theatre mode
        from .visualization.theatre import TheatreMode
        
        # Create theatre mode
        theatre = TheatreMode(
            ensemble=ensemble,
            use_color=not args.no_color,
            width=65,
        )
        
        # Run the performance
        print("\n🎭 Theatre Mode Enabled 🎭\n")
        results = await theatre.perform(args.task)
        
        # Determine output format
        output_format = args.format
        if args.output and not args.format == "terminal":
            # Auto-detect from extension
            ext = args.output.suffix.lower()
            if ext == ".md":
                output_format = "markdown"
            elif ext == ".html":
                output_format = "html"
        
        # Display to console (terminal format)
        if output_format == "terminal" or not args.output:
            theatre.print_performance(
                args.task,
                results["conversation"],
                metadata=results,
            )
        
        # Save to file if requested
        if args.output:
            theatre.save(
                args.task,
                results["conversation"],
                args.output,
                format=output_format if output_format != "terminal" else "markdown",
                metadata=results,
            )
            print(f"\n✨ Theatre output saved to: {args.output}")
        
        return
    
    # Original non-theatre mode behavior
    # Create session
    session = CreativeSession(
        ensemble=ensemble,
        output_dir=args.output_dir,
    )

    # Print header
    print("\n" + "=" * 80)
    print("KHAZAR LLMs CREATIVE SESSION")
    print("=" * 80)
    print(f"\nTask: {args.task}")
    print(f"\nAgents ({len(agents)}):")
    for agent in agents:
        print(f"  - {agent.name} ({agent.role.value})")
    print(f"\nMode: {mode.value}")
    print(f"Iterations: {args.iterations}")
    print(f"Provider: {args.provider}")
    print("\nRunning collaboration...")
    print("=" * 80 + "\n")

    # Run session
    results = await session.run(args.task)

    # Display conversation
    for i, msg in enumerate(results["conversation"], 1):
        print(f"\n[{i}] {msg.sender} ({msg.role.value})")
        print("-" * 40)
        print(msg.content)
        print()

    # Save session
    if not args.no_save:
        json_path = session.save_session(results, format="json")
        txt_path = session.save_session(results, format="txt")
        print("\n" + "=" * 80)
        print(f"Session saved to:")
        print(f"  JSON: {json_path}")
        print(f"  Text: {txt_path}")
        print("=" * 80 + "\n")


async def run_benchmark(args):
    """Run benchmark evaluation."""
    from .benchmark import BenchmarkRunner
    from .benchmark.test_cases import get_categories
    
    # Create agents
    agents = []
    for agent_name in args.agents:
        agent_class = AVAILABLE_AGENTS[agent_name]
        agents.append(agent_class(provider=args.provider))

    # Create ensemble
    mode = ConversationMode(args.mode)
    ensemble = Ensemble(
        agents=agents,
        mode=mode,
        max_iterations=args.iterations,
    )

    # Create benchmark runner
    runner = BenchmarkRunner(ensemble)

    # Print header
    print("\n" + "=" * 80)
    print("KHAZAR LLMs BENCHMARK")
    print("=" * 80)
    print(f"\nAgents ({len(agents)}):")
    for agent in agents:
        print(f"  - {agent.name} ({agent.role.value})")
    print(f"\nMode: {mode.value}")
    print(f"Iterations: {args.iterations}")
    print(f"Provider: {args.provider}")

    # Determine what to run
    if args.full:
        print("\nRunning full benchmark suite...")
        print("=" * 80 + "\n")
        report = await runner.run(iterations=args.iterations)
    elif args.category:
        print(f"\nRunning benchmark for category: {args.category}")
        print("=" * 80 + "\n")
        report = await runner.run(categories=[args.category], iterations=args.iterations)
    elif args.prompt:
        print(f"\nRunning benchmark on custom prompt: {args.prompt}")
        print("=" * 80 + "\n")
        report = await runner.run_single(args.prompt, category="custom")
    else:
        print("\nError: Must specify --full, --category, or --prompt")
        print("Available categories:", ", ".join(get_categories()))
        return

    # Print summary
    runner.print_summary(report)

    # Save report if output specified
    if args.output:
        # Determine format
        output_format = args.format
        if args.format == "terminal":
            # Auto-detect from file extension
            ext = args.output.suffix.lower()
            if ext == ".md":
                output_format = "markdown"
            elif ext == ".json":
                output_format = "json"
            elif ext == ".html":
                output_format = "html"
            else:
                output_format = "markdown"  # Default
        
        # Ensure output directory exists
        args.output.parent.mkdir(parents=True, exist_ok=True)
        
        # Save report
        saved_path = runner.save_report(report, args.output, format=output_format)
        print(f"✨ Benchmark report saved to: {saved_path}\n")


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "list-agents":
        list_agents()
    elif args.command == "info":
        show_info()
    elif args.command == "create-task":
        asyncio.run(run_creative_task(args))
    elif args.command == "benchmark":
        asyncio.run(run_benchmark(args))


if __name__ == "__main__":
    main()
