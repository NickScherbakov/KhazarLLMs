"""Output formatters for different theatre mode formats."""

from typing import List, Dict, Any
from ..agents.base import Message
from .styles import (
    get_agent_identity,
    create_box,
    create_header,
    BoxChars,
    StageDirection,
    AgentColor,
)


class TerminalFormatter:
    """Format theatre output for terminal display."""
    
    def __init__(self, use_color: bool = True, width: int = 65):
        """Initialize the terminal formatter.
        
        Args:
            use_color: Whether to use ANSI color codes
            width: Width of the output
        """
        self.use_color = use_color
        self.width = width
    
    def format_session(
        self,
        task: str,
        messages: List[Message],
        metadata: Dict[str, Any] = None
    ) -> str:
        """Format a complete theatre session.
        
        Args:
            task: The creative task
            messages: List of messages in the conversation
            metadata: Optional session metadata
            
        Returns:
            Formatted string for terminal display
        """
        lines = []
        
        # Header
        lines.append(create_header("KHAZAR THEATRE", task[:50], self.width))
        lines.append("")
        
        # Opening stage direction
        lines.append("    [The stage is set. Lights dim. The performance begins...]")
        lines.append("")
        
        # Format each message
        current_speaker = None
        for i, msg in enumerate(messages):
            # Add entrance if new speaker
            if msg.sender != current_speaker:
                lines.append("")
                lines.append(f"    {StageDirection.get_entrance(msg.sender, i)}")
                lines.append("")
                current_speaker = msg.sender
            
            # Format the message
            lines.append(self._format_message(msg))
            lines.append("")
        
        # Closing
        lines.append("    [The lights fade. Curtain falls.]")
        lines.append("")
        lines.append(BoxChars.DOUBLE_HORIZONTAL * self.width)
        
        return "\n".join(lines)
    
    def _format_message(self, msg: Message) -> str:
        """Format a single message as a speech block.
        
        Args:
            msg: The message to format
            
        Returns:
            Formatted message string
        """
        identity = get_agent_identity(msg.role.value)
        
        # Create header with agent identity
        symbol = identity["symbol"]
        name = msg.sender.upper()
        header = f"{symbol} {name}"
        
        # Apply color if enabled
        if self.use_color:
            color = identity["color"]
            reset = AgentColor.RESET.value
            header = f"{color}{header}{reset}"
        
        # Create the speech box
        chars = BoxChars()
        lines = []
        
        # Top border with header
        lines.append(chars.SINGLE_TOP_LEFT + chars.SINGLE_HORIZONTAL * (self.width - 2) + chars.SINGLE_TOP_RIGHT)
        lines.append(chars.SINGLE_VERTICAL + " " + header.ljust(self.width - 3) + chars.SINGLE_VERTICAL)
        lines.append(chars.SINGLE_T_RIGHT + chars.SINGLE_HORIZONTAL * (self.width - 2) + chars.SINGLE_T_LEFT)
        
        # Content
        content_lines = self._wrap_text(msg.content, self.width - 4)
        for line in content_lines:
            lines.append(chars.SINGLE_VERTICAL + " " + line.ljust(self.width - 3) + chars.SINGLE_VERTICAL)
        
        # Bottom border
        lines.append(chars.SINGLE_BOTTOM_LEFT + chars.SINGLE_HORIZONTAL * (self.width - 2) + chars.SINGLE_BOTTOM_RIGHT)
        
        return "\n".join(lines)
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to fit within width.
        
        Args:
            text: Text to wrap
            width: Maximum width
            
        Returns:
            List of wrapped lines
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_len = len(word)
            
            # If word alone exceeds width, break it
            if word_len > width:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = []
                    current_length = 0
                # Break long word
                while word_len > width:
                    lines.append(word[:width])
                    word = word[width:]
                    word_len = len(word)
                if word:
                    current_line = [word]
                    current_length = word_len
                continue
            
            # Check if adding word would exceed width
            if current_length + word_len + len(current_line) > width:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_len
            else:
                current_line.append(word)
                current_length += word_len
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines if lines else [""]


class MarkdownFormatter:
    """Format theatre output as Markdown."""
    
    def format_session(
        self,
        task: str,
        messages: List[Message],
        metadata: Dict[str, Any] = None
    ) -> str:
        """Format a complete theatre session as Markdown.
        
        Args:
            task: The creative task
            messages: List of messages in the conversation
            metadata: Optional session metadata
            
        Returns:
            Formatted Markdown string
        """
        lines = []
        
        # Title
        lines.append("# 🎭 KHAZAR THEATRE 🎭")
        lines.append("")
        lines.append(f"## {task}")
        lines.append("")
        
        # Metadata if provided
        if metadata:
            lines.append("---")
            if "session_id" in metadata:
                lines.append(f"**Session ID:** {metadata['session_id']}")
            if "duration_seconds" in metadata:
                lines.append(f"**Duration:** {metadata['duration_seconds']:.2f} seconds")
            if "mode" in metadata:
                lines.append(f"**Mode:** {metadata['mode']}")
            lines.append("---")
            lines.append("")
        
        # Opening
        lines.append("*[The stage is set. Lights dim. The performance begins...]*")
        lines.append("")
        
        # Format each message
        current_speaker = None
        for i, msg in enumerate(messages):
            # Add entrance if new speaker
            if msg.sender != current_speaker:
                lines.append("")
                lines.append(f"*{StageDirection.get_entrance(msg.sender, i)}*")
                lines.append("")
                current_speaker = msg.sender
            
            # Format the message
            identity = get_agent_identity(msg.role.value)
            symbol = identity["symbol"]
            
            lines.append(f"### {symbol} {msg.sender}")
            lines.append("")
            lines.append(f"> {msg.content}")
            lines.append("")
        
        # Closing
        lines.append("*[The lights fade. Curtain falls.]*")
        lines.append("")
        lines.append("---")
        
        return "\n".join(lines)


class HTMLFormatter:
    """Format theatre output as HTML."""
    
    def format_session(
        self,
        task: str,
        messages: List[Message],
        metadata: Dict[str, Any] = None
    ) -> str:
        """Format a complete theatre session as HTML.
        
        Args:
            task: The creative task
            messages: List of messages in the conversation
            metadata: Optional session metadata
            
        Returns:
            Formatted HTML string
        """
        lines = []
        
        # HTML header with embedded CSS
        lines.append("<!DOCTYPE html>")
        lines.append("<html lang='en'>")
        lines.append("<head>")
        lines.append("    <meta charset='UTF-8'>")
        lines.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        lines.append("    <title>Khazar Theatre</title>")
        lines.append("    <style>")
        lines.append(self._get_css())
        lines.append("    </style>")
        lines.append("</head>")
        lines.append("<body>")
        
        # Main container
        lines.append("    <div class='theatre-container'>")
        
        # Header
        lines.append("        <header class='theatre-header'>")
        lines.append("            <h1>🎭 KHAZAR THEATRE 🎭</h1>")
        lines.append(f"            <h2>{self._escape_html(task)}</h2>")
        lines.append("        </header>")
        
        # Metadata if provided
        if metadata:
            lines.append("        <div class='metadata'>")
            if "session_id" in metadata:
                lines.append(f"            <span>Session: {metadata['session_id']}</span>")
            if "duration_seconds" in metadata:
                lines.append(f"            <span>Duration: {metadata['duration_seconds']:.2f}s</span>")
            if "mode" in metadata:
                lines.append(f"            <span>Mode: {metadata['mode']}</span>")
            lines.append("        </div>")
        
        # Stage
        lines.append("        <div class='stage'>")
        lines.append("            <div class='stage-direction'>")
        lines.append("                [The stage is set. Lights dim. The performance begins...]")
        lines.append("            </div>")
        
        # Messages
        current_speaker = None
        for i, msg in enumerate(messages):
            # Add entrance if new speaker
            if msg.sender != current_speaker:
                lines.append("            <div class='stage-direction'>")
                lines.append(f"                {StageDirection.get_entrance(msg.sender, i)}")
                lines.append("            </div>")
                current_speaker = msg.sender
            
            # Format the message
            identity = get_agent_identity(msg.role.value)
            symbol = identity["symbol"]
            role_class = msg.role.value.lower()
            
            lines.append(f"            <div class='dialogue {role_class}'>")
            lines.append(f"                <div class='speaker'>{symbol} {msg.sender}</div>")
            lines.append(f"                <div class='speech'>{self._escape_html(msg.content)}</div>")
            lines.append("            </div>")
        
        # Closing
        lines.append("            <div class='stage-direction'>")
        lines.append("                [The lights fade. Curtain falls.]")
        lines.append("            </div>")
        lines.append("        </div>")
        
        lines.append("    </div>")
        lines.append("</body>")
        lines.append("</html>")
        
        return "\n".join(lines)
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
    
    def _get_css(self) -> str:
        """Get embedded CSS for the HTML output."""
        return """
        body {
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #f0f0f0;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        
        .theatre-container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        
        .theatre-header {
            text-align: center;
            border-bottom: 3px double #ffd700;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .theatre-header h1 {
            color: #ffd700;
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        .theatre-header h2 {
            color: #f0f0f0;
            font-size: 1.3em;
            margin: 10px 0 0;
            font-weight: normal;
            font-style: italic;
        }
        
        .metadata {
            text-align: center;
            margin-bottom: 20px;
            font-size: 0.9em;
            color: #aaa;
        }
        
        .metadata span {
            margin: 0 15px;
        }
        
        .stage {
            margin-top: 30px;
        }
        
        .stage-direction {
            text-align: center;
            font-style: italic;
            color: #888;
            margin: 30px 0;
            font-size: 0.95em;
        }
        
        .dialogue {
            margin: 25px 0;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid;
            background: rgba(255, 255, 255, 0.05);
        }
        
        .dialogue.dreamer { border-left-color: #ff6ec7; }
        .dialogue.critic { border-left-color: #ffd93d; }
        .dialogue.synthesizer { border-left-color: #6bcfff; }
        .dialogue.philosopher { border-left-color: #6fa8dc; }
        .dialogue.rebel { border-left-color: #ff6b6b; }
        .dialogue.architect { border-left-color: #7fdb6b; }
        .dialogue.poet { border-left-color: #da6bff; }
        
        .speaker {
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #ffd700;
        }
        
        .speech {
            padding-left: 15px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        """
