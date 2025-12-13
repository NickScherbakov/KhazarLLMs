"""Visual styles and themes for theatre mode."""

from typing import Dict, Any
from enum import Enum


class AgentSymbol(str, Enum):
    """Emojis/symbols for each agent role."""
    DREAMER = "🌙"
    CRITIC = "🔍"
    SYNTHESIZER = "🔄"
    PHILOSOPHER = "📚"
    REBEL = "⚡"
    ARCHITECT = "🏛️"
    POET = "🎭"


class AgentColor(str, Enum):
    """ANSI color codes for each agent role (for terminals that support it)."""
    DREAMER = "\033[95m"  # Magenta
    CRITIC = "\033[93m"  # Yellow
    SYNTHESIZER = "\033[96m"  # Cyan
    PHILOSOPHER = "\033[94m"  # Blue
    REBEL = "\033[91m"  # Red
    ARCHITECT = "\033[92m"  # Green
    POET = "\033[35m"  # Purple
    RESET = "\033[0m"  # Reset


class StageDirection:
    """Stage direction templates."""
    
    TEMPLATES = {
        "entrance": [
            "[{name} steps into the light...]",
            "[{name} emerges from the shadows...]",
            "[{name} takes center stage...]",
            "[The spotlight finds {name}...]",
        ],
        "exit": [
            "[{name} steps back into the shadows...]",
            "[{name} bows and withdraws...]",
        ],
        "thinking": [
            "[{name} pauses, contemplating...]",
            "[{name} considers deeply...]",
        ],
    }
    
    @classmethod
    def get_entrance(cls, agent_name: str, index: int = 0) -> str:
        """Get an entrance direction for an agent."""
        templates = cls.TEMPLATES["entrance"]
        template = templates[index % len(templates)]
        return template.format(name=agent_name)
    
    @classmethod
    def get_exit(cls, agent_name: str) -> str:
        """Get an exit direction for an agent."""
        import random
        template = random.choice(cls.TEMPLATES["exit"])
        return template.format(name=agent_name)


def get_agent_identity(role: str) -> Dict[str, Any]:
    """Get complete visual identity for an agent role.
    
    Args:
        role: The agent role (e.g., 'dreamer', 'critic')
        
    Returns:
        Dictionary with symbol, color, and display name
    """
    role_upper = role.upper()
    
    # Get the enum values, with fallback defaults
    symbol_enum = getattr(AgentSymbol, role_upper, None)
    color_enum = getattr(AgentColor, role_upper, None)
    
    identity = {
        "symbol": symbol_enum.value if symbol_enum else "🎭",
        "color": color_enum.value if color_enum else AgentColor.RESET.value,
        "display_name": role.replace("_", " ").title(),
    }
    
    return identity


# Box drawing characters for ASCII frames
class BoxChars:
    """Box drawing characters for creating frames."""
    
    # Double-line box
    DOUBLE_TOP_LEFT = "╔"
    DOUBLE_TOP_RIGHT = "╗"
    DOUBLE_BOTTOM_LEFT = "╚"
    DOUBLE_BOTTOM_RIGHT = "╝"
    DOUBLE_HORIZONTAL = "═"
    DOUBLE_VERTICAL = "║"
    DOUBLE_T_DOWN = "╦"
    DOUBLE_T_UP = "╩"
    DOUBLE_T_RIGHT = "╠"
    DOUBLE_T_LEFT = "╣"
    DOUBLE_CROSS = "╬"
    
    # Single-line box
    SINGLE_TOP_LEFT = "┌"
    SINGLE_TOP_RIGHT = "┐"
    SINGLE_BOTTOM_LEFT = "└"
    SINGLE_BOTTOM_RIGHT = "┘"
    SINGLE_HORIZONTAL = "─"
    SINGLE_VERTICAL = "│"
    SINGLE_T_DOWN = "┬"
    SINGLE_T_UP = "┴"
    SINGLE_T_RIGHT = "├"
    SINGLE_T_LEFT = "┤"
    SINGLE_CROSS = "┼"


def create_box(content: str, width: int = 65, style: str = "single") -> str:
    """Create a box around content.
    
    Args:
        content: The text content to box
        width: Width of the box
        style: 'single' or 'double' line style
        
    Returns:
        Boxed text
    """
    chars = BoxChars()
    
    if style == "double":
        tl, tr = chars.DOUBLE_TOP_LEFT, chars.DOUBLE_TOP_RIGHT
        bl, br = chars.DOUBLE_BOTTOM_LEFT, chars.DOUBLE_BOTTOM_RIGHT
        h, v = chars.DOUBLE_HORIZONTAL, chars.DOUBLE_VERTICAL
    else:
        tl, tr = chars.SINGLE_TOP_LEFT, chars.SINGLE_TOP_RIGHT
        bl, br = chars.SINGLE_BOTTOM_LEFT, chars.SINGLE_BOTTOM_RIGHT
        h, v = chars.SINGLE_HORIZONTAL, chars.SINGLE_VERTICAL
    
    lines = []
    
    # Top border
    lines.append(tl + h * (width - 2) + tr)
    
    # Content lines
    for line in content.split('\n'):
        # Word wrap if needed
        while len(line) > width - 4:
            # Find last space before width
            wrap_at = line.rfind(' ', 0, width - 4)
            if wrap_at == -1:
                wrap_at = width - 4
            lines.append(v + " " + line[:wrap_at].ljust(width - 3) + v)
            line = line[wrap_at:].lstrip()
        
        lines.append(v + " " + line.ljust(width - 3) + v)
    
    # Bottom border
    lines.append(bl + h * (width - 2) + br)
    
    return "\n".join(lines)


def create_header(title: str, subtitle: str = "", width: int = 65) -> str:
    """Create a theatrical header.
    
    Args:
        title: Main title text
        subtitle: Optional subtitle
        width: Width of the header
        
    Returns:
        Formatted header
    """
    chars = BoxChars()
    lines = []
    
    # Top border
    lines.append(chars.DOUBLE_TOP_LEFT + chars.DOUBLE_HORIZONTAL * (width - 2) + chars.DOUBLE_TOP_RIGHT)
    
    # Title
    title_line = f"🎭 {title} 🎭"
    padding = (width - 2 - len(title_line)) // 2
    lines.append(chars.DOUBLE_VERTICAL + " " * padding + title_line + " " * (width - 2 - padding - len(title_line)) + chars.DOUBLE_VERTICAL)
    
    # Subtitle if provided
    if subtitle:
        subtitle_line = f'"{subtitle}"'
        if len(subtitle_line) > width - 4:
            subtitle_line = subtitle_line[:width - 7] + "..."
        padding = (width - 2 - len(subtitle_line)) // 2
        lines.append(chars.DOUBLE_VERTICAL + " " * padding + subtitle_line + " " * (width - 2 - padding - len(subtitle_line)) + chars.DOUBLE_VERTICAL)
    
    # Bottom border
    lines.append(chars.DOUBLE_T_RIGHT + chars.DOUBLE_HORIZONTAL * (width - 2) + chars.DOUBLE_T_LEFT)
    
    return "\n".join(lines)
