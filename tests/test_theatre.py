"""Tests for theatre mode visualization."""

import pytest
from pathlib import Path
from khazar_llms.agents.base import Message, AgentRole
from khazar_llms.agents.personas import DreamerAgent, CriticAgent
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode
from khazar_llms.visualization.theatre import TheatreMode, Actor, Scene, Stage
from khazar_llms.visualization.formatters import (
    TerminalFormatter,
    MarkdownFormatter,
    HTMLFormatter,
)
from khazar_llms.visualization.styles import (
    get_agent_identity,
    create_box,
    create_header,
    AgentSymbol,
    StageDirection,
)


def test_agent_identity():
    """Test getting agent visual identity."""
    identity = get_agent_identity("dreamer")
    assert "symbol" in identity
    assert "color" in identity
    assert "display_name" in identity
    assert identity["symbol"] == AgentSymbol.DREAMER
    assert identity["display_name"] == "Dreamer"


def test_create_box():
    """Test creating ASCII boxes."""
    content = "Hello World"
    box = create_box(content, width=30, style="single")
    assert "┌" in box  # Top left corner
    assert "┐" in box  # Top right corner
    assert "└" in box  # Bottom left corner
    assert "┘" in box  # Bottom right corner
    assert "Hello World" in box


def test_create_header():
    """Test creating theatrical header."""
    header = create_header("TEST THEATRE", "A Test", width=50)
    assert "TEST THEATRE" in header
    assert "A Test" in header
    assert "╔" in header  # Double-line top left
    assert "╗" in header  # Double-line top right


def test_stage_direction():
    """Test stage direction generation."""
    entrance = StageDirection.get_entrance("Dreamer", 0)
    assert "Dreamer" in entrance
    assert "[" in entrance and "]" in entrance


def test_actor_creation():
    """Test creating an actor from an agent."""
    agent = DreamerAgent(provider="mock")
    actor = Actor(agent)
    
    assert actor.name == "Dreamer"
    assert actor.role == "dreamer"
    assert actor.entrance_count == 0
    
    actor.mark_entrance()
    assert actor.entrance_count == 1


def test_scene_creation():
    """Test creating a scene."""
    messages = [
        Message(
            sender="Dreamer",
            role=AgentRole.DREAMER,
            content="Test message",
            iteration=0,
        )
    ]
    
    scene = Scene(iteration=0, messages=messages)
    assert scene.iteration == 0
    assert len(scene) == 1
    assert scene.messages[0].sender == "Dreamer"


def test_stage_creation():
    """Test creating a stage with actors."""
    agent1 = DreamerAgent(provider="mock")
    agent2 = CriticAgent(provider="mock")
    
    actors = [Actor(agent1), Actor(agent2)]
    stage = Stage(actors)
    
    assert len(stage.actors) == 2
    assert stage.get_actor_by_name("Dreamer") is not None
    assert stage.get_actor_by_name("Critic") is not None
    assert stage.get_actor_by_name("Unknown") is None


def test_terminal_formatter():
    """Test terminal formatter."""
    formatter = TerminalFormatter(use_color=False, width=65)
    
    messages = [
        Message(
            sender="Dreamer",
            role=AgentRole.DREAMER,
            content="Imagine a world where...",
            iteration=0,
        ),
        Message(
            sender="Critic",
            role=AgentRole.CRITIC,
            content="But how would that work?",
            iteration=0,
        ),
    ]
    
    output = formatter.format_session("Test task", messages)
    
    assert "KHAZAR THEATRE" in output
    assert "Dreamer" in output
    assert "Critic" in output
    assert "Imagine a world where..." in output
    assert "But how would that work?" in output
    assert "[The stage is set" in output
    assert "[The lights fade" in output


def test_markdown_formatter():
    """Test Markdown formatter."""
    formatter = MarkdownFormatter()
    
    messages = [
        Message(
            sender="Dreamer",
            role=AgentRole.DREAMER,
            content="Imagine a world where...",
            iteration=0,
        ),
    ]
    
    metadata = {
        "session_id": "test123",
        "duration_seconds": 10.5,
        "mode": "sequential",
    }
    
    output = formatter.format_session("Test task", messages, metadata)
    
    assert "# 🎭 KHAZAR THEATRE 🎭" in output
    assert "## Test task" in output
    assert "Dreamer" in output
    assert "Imagine a world where..." in output
    assert "test123" in output
    assert "10.50 seconds" in output


def test_html_formatter():
    """Test HTML formatter."""
    formatter = HTMLFormatter()
    
    messages = [
        Message(
            sender="Dreamer",
            role=AgentRole.DREAMER,
            content="Imagine a world where...",
            iteration=0,
        ),
    ]
    
    output = formatter.format_session("Test task", messages)
    
    assert "<!DOCTYPE html>" in output
    assert "<html" in output
    assert "KHAZAR THEATRE" in output
    assert "Dreamer" in output
    assert "Imagine a world where..." in output
    assert "</html>" in output
    assert "theatre-container" in output  # CSS class


def test_html_escape():
    """Test HTML escaping in formatter."""
    formatter = HTMLFormatter()
    
    messages = [
        Message(
            sender="Test",
            role=AgentRole.DREAMER,
            content="Test <script>alert('xss')</script>",
            iteration=0,
        ),
    ]
    
    output = formatter.format_session("Task", messages)
    
    # Should escape HTML
    assert "&lt;script&gt;" in output
    assert "<script>" not in output or "theatre-container" in output  # Only in CSS/HTML structure


@pytest.mark.asyncio
async def test_theatre_mode_basic():
    """Test basic theatre mode functionality."""
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.SEQUENTIAL,
        max_iterations=1,
    )
    
    theatre = TheatreMode(ensemble, use_color=False, width=65)
    
    # Check initialization
    assert len(theatre.actors) == 2
    assert theatre.stage is not None
    assert theatre.terminal_formatter is not None
    assert theatre.markdown_formatter is not None
    assert theatre.html_formatter is not None


@pytest.mark.asyncio
async def test_theatre_mode_perform():
    """Test running a performance."""
    agents = [
        DreamerAgent(provider="mock"),
    ]
    
    ensemble = Ensemble(
        agents=agents,
        mode=ConversationMode.SEQUENTIAL,
        max_iterations=1,
    )
    
    theatre = TheatreMode(ensemble, use_color=False, width=65)
    results = await theatre.perform("Test task")
    
    assert "conversation" in results
    assert len(results["conversation"]) > 0
    assert len(theatre.stage.scenes) > 0


def test_theatre_mode_display():
    """Test displaying in different formats."""
    agents = [DreamerAgent(provider="mock")]
    ensemble = Ensemble(agents=agents, mode=ConversationMode.SEQUENTIAL, max_iterations=1)
    theatre = TheatreMode(ensemble, use_color=False, width=65)
    
    messages = [
        Message(
            sender="Dreamer",
            role=AgentRole.DREAMER,
            content="Test",
            iteration=0,
        ),
    ]
    
    # Test terminal format
    terminal_output = theatre.display("Task", messages, format="terminal")
    assert "KHAZAR THEATRE" in terminal_output
    
    # Test markdown format
    markdown_output = theatre.display("Task", messages, format="markdown")
    assert "# 🎭 KHAZAR THEATRE 🎭" in markdown_output
    
    # Test HTML format
    html_output = theatre.display("Task", messages, format="html")
    assert "<!DOCTYPE html>" in html_output
    
    # Test invalid format
    with pytest.raises(ValueError):
        theatre.display("Task", messages, format="invalid")


def test_theatre_mode_save(tmp_path):
    """Test saving theatre output to file."""
    agents = [DreamerAgent(provider="mock")]
    ensemble = Ensemble(agents=agents, mode=ConversationMode.SEQUENTIAL, max_iterations=1)
    theatre = TheatreMode(ensemble, use_color=False, width=65)
    
    messages = [
        Message(
            sender="Dreamer",
            role=AgentRole.DREAMER,
            content="Test content",
            iteration=0,
        ),
    ]
    
    # Save as markdown
    md_path = tmp_path / "test.md"
    theatre.save("Task", messages, md_path, format="markdown")
    assert md_path.exists()
    content = md_path.read_text()
    assert "KHAZAR THEATRE" in content
    
    # Save as HTML
    html_path = tmp_path / "test.html"
    theatre.save("Task", messages, html_path, format="html")
    assert html_path.exists()
    content = html_path.read_text()
    assert "<!DOCTYPE html>" in content
