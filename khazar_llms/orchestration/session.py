"""Creative session management with rich output."""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..agents.base import Message
from .ensemble import Ensemble


class CreativeSession:
    """Manages a creative session with output formatting."""

    def __init__(
        self,
        ensemble: Ensemble,
        output_dir: Optional[Path] = None,
    ):
        """
        Initialize a creative session.
        
        Args:
            ensemble: The ensemble to manage
            output_dir: Optional directory for saving session outputs
        """
        self.ensemble = ensemble
        self.output_dir = output_dir or Path("./sessions")
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    async def run(self, task: str) -> Dict[str, Any]:
        """
        Run a creative session and return results.
        
        Args:
            task: The creative task to work on
            
        Returns:
            Dictionary containing session results
        """
        self.start_time = datetime.now()
        
        # Run the ensemble collaboration
        results = await self.ensemble.collaborate(task)
        
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()

        # Add session metadata
        session_data = {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": duration,
            **results,
        }

        return session_data

    def save_session(self, session_data: Dict[str, Any], format: str = "json"):
        """
        Save session results to disk.
        
        Args:
            session_data: The session data to save
            format: Output format ('json' or 'txt')
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if format == "json":
            filepath = self.output_dir / f"session_{self.session_id}.json"
            # Convert Message objects to dicts for JSON serialization
            serializable_data = self._prepare_for_serialization(session_data)
            with open(filepath, "w") as f:
                json.dump(serializable_data, f, indent=2)

        elif format == "txt":
            filepath = self.output_dir / f"session_{self.session_id}.txt"
            with open(filepath, "w") as f:
                f.write(self._format_as_text(session_data))

        return filepath

    def _prepare_for_serialization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Message objects to dicts for JSON serialization."""
        serializable = data.copy()
        
        if "conversation" in serializable:
            serializable["conversation"] = [
                {
                    "sender": msg.sender,
                    "role": msg.role.value,
                    "content": msg.content,
                    "iteration": msg.iteration,
                    "metadata": msg.metadata,
                }
                for msg in serializable["conversation"]
            ]
        
        return serializable

    def _format_as_text(self, data: Dict[str, Any]) -> str:
        """Format session data as readable text."""
        lines = []
        lines.append("=" * 80)
        lines.append("KHAZAR LLMs CREATIVE SESSION")
        lines.append("=" * 80)
        lines.append(f"Session ID: {data.get('session_id', 'N/A')}")
        lines.append(f"Task: {data.get('task', 'N/A')}")
        lines.append(f"Mode: {data.get('mode', 'N/A')}")
        lines.append(f"Duration: {data.get('duration_seconds', 0):.2f} seconds")
        lines.append("=" * 80)
        lines.append("")

        if "conversation" in data:
            lines.append("CONVERSATION")
            lines.append("-" * 80)
            
            for i, msg in enumerate(data["conversation"], 1):
                if isinstance(msg, Message):
                    lines.append(f"\n[{i}] {msg.sender} ({msg.role.value}) - Iteration {msg.iteration}")
                    lines.append("-" * 40)
                    lines.append(msg.content)
                else:
                    lines.append(f"\n[{i}] {msg['sender']} ({msg['role']}) - Iteration {msg['iteration']}")
                    lines.append("-" * 40)
                    lines.append(msg['content'])

        lines.append("\n" + "=" * 80)
        lines.append("END OF SESSION")
        lines.append("=" * 80)

        return "\n".join(lines)

    def print_summary(self, session_data: Dict[str, Any]):
        """Print a summary of the session to console."""
        print("\n" + "=" * 80)
        print("SESSION SUMMARY")
        print("=" * 80)
        print(f"Task: {session_data.get('task', 'N/A')}")
        print(f"Agents: {session_data.get('agent_count', 0)}")
        print(f"Iterations: {session_data.get('iterations', 0)}")
        print(f"Messages: {len(session_data.get('conversation', []))}")
        print(f"Duration: {session_data.get('duration_seconds', 0):.2f} seconds")
        print("=" * 80 + "\n")
