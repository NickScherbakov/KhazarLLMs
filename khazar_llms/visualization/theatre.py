"""Core theatre mode implementation."""

from typing import List, Dict, Any, Optional
from pathlib import Path

from ..agents.base import Agent, Message
from ..orchestration.ensemble import Ensemble
from .formatters import TerminalFormatter, MarkdownFormatter, HTMLFormatter


class Actor:
    """Wraps an agent with visual representation for theatre mode."""
    
    def __init__(self, agent: Agent):
        """Initialize an actor from an agent.
        
        Args:
            agent: The agent to wrap
        """
        self.agent = agent
        self.entrance_count = 0
    
    @property
    def name(self) -> str:
        """Get the actor's name."""
        return self.agent.name
    
    @property
    def role(self) -> str:
        """Get the actor's role."""
        return self.agent.role.value
    
    def mark_entrance(self):
        """Mark that the actor has entered the stage."""
        self.entrance_count += 1


class Scene:
    """Represents a segment of dialogue in the performance."""
    
    def __init__(self, iteration: int, messages: List[Message]):
        """Initialize a scene.
        
        Args:
            iteration: The iteration number this scene represents
            messages: Messages that occurred in this scene
        """
        self.iteration = iteration
        self.messages = messages
    
    def __len__(self) -> int:
        """Get the number of messages in the scene."""
        return len(self.messages)


class Stage:
    """Represents the visual 'stage' for the performance."""
    
    def __init__(self, actors: List[Actor]):
        """Initialize the stage with actors.
        
        Args:
            actors: List of actors that will perform
        """
        self.actors = actors
        self.scenes: List[Scene] = []
        self.current_speaker: Optional[str] = None
    
    def add_scene(self, scene: Scene):
        """Add a scene to the stage.
        
        Args:
            scene: The scene to add
        """
        self.scenes.append(scene)
    
    def get_actor_by_name(self, name: str) -> Optional[Actor]:
        """Get an actor by name.
        
        Args:
            name: The actor's name
            
        Returns:
            The actor if found, None otherwise
        """
        for actor in self.actors:
            if actor.name == name:
                return actor
        return None


class TheatreMode:
    """Main orchestrator for theatre mode visualization."""
    
    def __init__(
        self,
        ensemble: Ensemble,
        use_color: bool = True,
        width: int = 65,
    ):
        """Initialize theatre mode.
        
        Args:
            ensemble: The ensemble to visualize
            use_color: Whether to use ANSI colors in terminal output
            width: Width of the output (for terminal and wrapped text)
        """
        self.ensemble = ensemble
        self.use_color = use_color
        self.width = width
        
        # Create actors from agents
        self.actors = [Actor(agent) for agent in ensemble.agents]
        
        # Create stage
        self.stage = Stage(self.actors)
        
        # Create formatters
        self.terminal_formatter = TerminalFormatter(use_color=use_color, width=width)
        self.markdown_formatter = MarkdownFormatter()
        self.html_formatter = HTMLFormatter()
    
    async def perform(self, task: str) -> Dict[str, Any]:
        """Run the ensemble collaboration and capture it as a performance.
        
        Args:
            task: The creative task for the ensemble
            
        Returns:
            Dictionary containing the performance results
        """
        # Run the ensemble collaboration
        results = await self.ensemble.collaborate(task)
        
        # Organize messages into scenes by iteration
        messages_by_iteration: Dict[int, List[Message]] = {}
        for msg in results["conversation"]:
            iteration = msg.iteration
            if iteration not in messages_by_iteration:
                messages_by_iteration[iteration] = []
            messages_by_iteration[iteration].append(msg)
        
        # Create scenes
        for iteration in sorted(messages_by_iteration.keys()):
            scene = Scene(iteration, messages_by_iteration[iteration])
            self.stage.add_scene(scene)
        
        return results
    
    def display(
        self,
        task: str,
        messages: List[Message],
        format: str = "terminal",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Display the performance in the specified format.
        
        Args:
            task: The creative task
            messages: List of messages to display
            format: Output format ('terminal', 'markdown', or 'html')
            metadata: Optional metadata about the session
            
        Returns:
            Formatted output string
        """
        if format == "terminal":
            return self.terminal_formatter.format_session(task, messages, metadata)
        elif format == "markdown":
            return self.markdown_formatter.format_session(task, messages, metadata)
        elif format == "html":
            return self.html_formatter.format_session(task, messages, metadata)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def save(
        self,
        task: str,
        messages: List[Message],
        output_path: Path,
        format: str = "markdown",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Save the performance to a file.
        
        Args:
            task: The creative task
            messages: List of messages to save
            output_path: Path to save the output
            format: Output format ('markdown' or 'html')
            metadata: Optional metadata about the session
        """
        content = self.display(task, messages, format, metadata)
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def print_performance(
        self,
        task: str,
        messages: List[Message],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Print the performance to console.
        
        Args:
            task: The creative task
            messages: List of messages to display
            metadata: Optional metadata about the session
        """
        output = self.display(task, messages, "terminal", metadata)
        print(output)
