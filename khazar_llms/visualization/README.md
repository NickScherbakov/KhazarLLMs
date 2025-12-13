# Theatre Mode Visualization

Theatre Mode transforms KhazarLLMs conversations into beautiful theatrical performances.

## Features

- **Visual Agent Identities**: Each agent has a unique emoji and color
  - 🌙 Dreamer - Magenta
  - 🔍 Critic - Yellow
  - 🔄 Synthesizer - Cyan
  - 📚 Philosopher - Blue
  - ⚡ Rebel - Red
  - 🏛️ Architect - Green
  - 🎭 Poet - Purple

- **Stage Directions**: Theatrical entrance/exit animations
- **Multiple Output Formats**:
  - Terminal (with ANSI colors)
  - Markdown (for documentation)
  - HTML (for web viewing)

## Usage

### Command Line

```bash
# Basic theatre mode
python -m khazar_llms.cli --theatre create-task "Your creative task"

# Save to markdown
python -m khazar_llms.cli --theatre --output performance.md create-task "Your task"

# Save to HTML
python -m khazar_llms.cli --theatre --output performance.html create-task "Your task"

# Disable colors
python -m khazar_llms.cli --theatre --no-color create-task "Your task"
```

### Python API

```python
from khazar_llms.visualization.theatre import TheatreMode
from khazar_llms.orchestration.ensemble import Ensemble
from khazar_llms.agents.personas import DreamerAgent, CriticAgent

# Create ensemble
agents = [DreamerAgent(), CriticAgent()]
ensemble = Ensemble(agents=agents)

# Create theatre mode
theatre = TheatreMode(ensemble)

# Run and display
results = await theatre.perform("Your creative task")
theatre.print_performance("Your creative task", results["conversation"])
```

## Examples

See `examples/theatre_demo.py` for a complete working example.

## Architecture

- `theatre.py` - Core theatre mode classes (TheatreMode, Stage, Actor, Scene)
- `formatters.py` - Output formatters (Terminal, Markdown, HTML)
- `styles.py` - Visual styles, colors, and ASCII art utilities
