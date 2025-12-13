#!/usr/bin/env python3
"""
Command-line interface for KhazarLLMs.

Usage:
    python -m khazar_llms.cli create-task "Your creative task here"
    python -m khazar_llms.cli --mode parallel --iterations 5 create-task "Your task"
"""

import argparse
import asyncio
import json
from pathlib import Path
from typing import Optional

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
        choices=["create-task", "list-agents", "info", "protocol"],
        help="Command to execute",
    )

    parser.add_argument(
        "task",
        nargs="?",
        help="The creative task for the ensemble (required for create-task) or subcommand for protocol",
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="File path for protocol commands (validate, export)",
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
        choices=["terminal", "markdown", "html"],
        default="terminal",
        help="Output format for theatre mode (default: terminal)",
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
    print("\nProtocol Commands:")
    print("  python -m khazar_llms.cli protocol info - Show KPS information")
    print("  python -m khazar_llms.cli protocol validate <file> - Validate KPS file")
    print("  python -m khazar_llms.cli protocol export <session-file> - Export to KPS format")
    print("\nExample usage:")
    print('  python -m khazar_llms.cli create-task "Design a new social network"')
    print('  python -m khazar_llms.cli --mode parallel create-task "Imagine a new art form"')
    print('  python -m khazar_llms.cli --theatre create-task "Create a new language"')
    print('  python -m khazar_llms.cli --theatre --output theatre.html create-task "Your task"')
    print("\n" + "=" * 80 + "\n")


def protocol_info():
    """Show information about KPS."""
    print("\n" + "=" * 80)
    print("KHAZAR PROTOCOL SPECIFICATION (KPS)")
    print("=" * 80 + "\n")
    print("Version: 1.0.0-draft")
    print("\nThe Khazar Protocol Specification defines a standard for multi-agent")
    print("creative collaboration using LLMs. KPS enables interoperability between")
    print("implementations and provides a formal protocol for agent communication.")
    print("\nKey Features:")
    print("  - Standard agent personas and archetypes")
    print("  - Message format for agent communication")
    print("  - Session lifecycle management")
    print("  - Multiple orchestration modes")
    print("  - Synthesis strategies for combining perspectives")
    print("\nStandard Archetypes:")
    print("  - creative_visionary (Dreamer)")
    print("  - analytical_challenger (Critic)")
    print("  - integrative_harmonizer (Synthesizer)")
    print("  - contextual_thinker (Philosopher)")
    print("  - disruptive_iconoclast (Rebel)")
    print("  - structural_organizer (Architect)")
    print("  - aesthetic_artisan (Poet)")
    print("\nFor full specification, see PROTOCOL.md in repository root.")
    print("\nKhazarLLMs is the reference implementation of KPS.")
    print("=" * 80 + "\n")


def protocol_validate(filepath: Path):
    """Validate a file against KPS specification."""
    from .protocol import KPSValidator
    
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return
    
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        return
    
    print(f"\nValidating {filepath} against KPS specification...\n")
    
    validator = KPSValidator()
    
    # Determine what type of data this is
    if "session" in data and "agents" in data and "messages" in data:
        result = validator.validate_session_export(data)
        data_type = "Session Export"
    elif "session_id" in data and "config" in data:
        result = validator.validate_session(data)
        data_type = "Session"
    elif "message_id" in data and "sender" in data:
        result = validator.validate_message(data)
        data_type = "Message"
    elif "agent_id" in data and "persona" in data:
        result = validator.validate_agent(data)
        data_type = "Agent"
    elif "synthesis_id" in data:
        result = validator.validate_synthesis(data)
        data_type = "Synthesis"
    else:
        print("Error: Could not determine data type")
        return
    
    print(f"Data Type: {data_type}")
    print(f"Status: {'✓ VALID' if result.valid else '✗ INVALID'}")
    
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    if result.valid and not result.warnings:
        print("\n✓ File is fully KPS-compliant!")
    
    print()


def protocol_export(session_file: Path, output_file: Optional[Path] = None):
    """Export a session to KPS format."""
    if not session_file.exists():
        print(f"Error: File not found: {session_file}")
        return
    
    try:
        with open(session_file, "r") as f:
            session_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        return
    
    # Note: This is informational. Full export requires running a live session.
    # The session.to_kps() method requires access to the ensemble object.
    print("\n" + "=" * 80)
    print("KPS Export Information")
    print("=" * 80)
    print("\nTo export a session to KPS format, you need to:")
    print("\n1. Run a session using the Python API:")
    print("   from khazar_llms.orchestration.session import CreativeSession")
    print("   session = CreativeSession(ensemble)")
    print("   results = await session.run(task)")
    print("   kps_export = session.to_kps(results)")
    print("\n2. Or create a session and save directly:")
    print("   import json")
    print("   with open('output.kps.json', 'w') as f:")
    print("       json.dump(kps_export, f, indent=2)")
    print("\nNote: Command-line export from saved sessions requires agent")
    print("      reconstruction, which is planned for a future version.")
    print("\n" + "=" * 80 + "\n")
    
    # Show what's in the file
    if "session_id" in session_data:
        print(f"Session file contains:")
        print(f"  Session ID: {session_data.get('session_id', 'N/A')}")
        print(f"  Task: {session_data.get('task', 'N/A')}")
        print(f"  Messages: {len(session_data.get('conversation', []))}")
        print()


async def handle_protocol_command(args):
    """Handle protocol subcommands."""
    subcommand = args.task
    
    if subcommand == "info":
        protocol_info()
    elif subcommand == "validate":
        if not args.file:
            print("Error: File path required for validate command")
            print("Usage: python -m khazar_llms.cli protocol validate <file>")
            return
        protocol_validate(Path(args.file))
    elif subcommand == "export":
        if not args.file:
            print("Error: File path required for export command")
            print("Usage: python -m khazar_llms.cli protocol export <session-file>")
            return
        protocol_export(Path(args.file))
    else:
        print(f"Unknown protocol subcommand: {subcommand}")
        print("Available subcommands: info, validate, export")


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


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "list-agents":
        list_agents()
    elif args.command == "info":
        show_info()
    elif args.command == "protocol":
        asyncio.run(handle_protocol_command(args))
    elif args.command == "create-task":
        asyncio.run(run_creative_task(args))


if __name__ == "__main__":
    main()
