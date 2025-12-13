# KhazarLLMs 🌟

> 🌐 **Languages:** [English](README.md) | [العربية](i18n/ar/README.md) | [中文](i18n/zh/README.md) | [Русский](i18n/ru/README.md)

**A System for Collective Creativity Management of Ensemble LLMs**

> 🌐 **[View Landing Page](docs/index.html)** | 📜 **[Read the Manifesto](MANIFESTO.md)** | 📚 **[Documentation](USAGE_GUIDE.md)** | 💻 **[Examples](examples/)**

Inspired by Milorad Pavić's *Khazar Dictionary* and its exploration of multiple perspectives, KhazarLLMs orchestrates an ensemble of AI agents with distinct personalities and roles to collaborate on creative tasks. Like the polyphonic structure of the Khazar Dictionary, where multiple voices tell interconnected stories, this system brings together diverse AI perspectives to explore ideas from many angles.

> 📜 **New!** Read our **[Manifesto](MANIFESTO.md)** — *A declaration of collective intelligence and the future of AI collaboration*

## 🎭 Philosophy

In the Khazar Dictionary, truth emerges not from a single perspective but from the interplay of many voices - Christian, Islamic, and Jewish sources telling overlapping yet distinct stories. Similarly, KhazarLLMs believes that the most creative and insightful solutions emerge from the collision and synthesis of multiple AI perspectives, each with its own role and personality:

- **The Dreamer** - Generates wild, unbounded creative visions
- **The Critic** - Analyzes with sharp insight and constructive challenge
- **The Synthesizer** - Weaves disparate ideas into coherent wholes  
- **The Philosopher** - Explores deep meanings and broader contexts
- **The Rebel** - Challenges assumptions and breaks conventions
- **The Architect** - Structures and organizes ideas into implementable forms
- **The Poet** - Adds beauty and emotional resonance

## ✨ Features

- 🤖 **Multiple Agent Personas** - Each with unique creative roles and personalities
- 🎯 **Flexible Orchestration** - Sequential, parallel, debate, and consensus modes
- 🔄 **Iterative Refinement** - Multiple conversation rounds to develop ideas
- 💾 **Session Management** - Save and review creative sessions
- 🎨 **Provider Agnostic** - Works with OpenAI, Anthropic, or mock mode
- 🛠️ **CLI & Python API** - Use via command line or integrate into your code
- 📜 **KPS Compliant** - Follows the Khazar Protocol Specification for interoperability

## 📜 Khazar Protocol Specification (KPS)

KhazarLLMs implements and serves as the **reference implementation** for the **Khazar Protocol Specification (KPS)** - an open standard for multi-agent creative collaboration.

**What is KPS?**
- A formal protocol defining how AI agents communicate and collaborate
- Standard message formats, agent personas, and session management
- JSON schemas for validation and interoperability
- Extension mechanisms for custom implementations

**Why KPS Matters:**
- First open standard for multi-agent creative systems
- Enables session portability between implementations
- Promotes best practices in ensemble AI design
- Positions KhazarLLMs as an industry standard setter

**Learn More:**
- 📖 Read the full [Protocol Specification](PROTOCOL.md)
- 🔧 See the [Implementation Guide](docs/PROTOCOL.md)
- ✅ Validate KPS compliance: `python -m khazar_llms.cli protocol validate <file>`
- 📊 Export sessions to KPS format via Python API

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/KhazarLLMs.git
cd KhazarLLMs

# Install dependencies
pip install -r requirements.txt

# Optional: Set up API keys
cp .env.example .env
# Edit .env with your API keys
```

### Basic Usage

```python
import asyncio
from khazar_llms.agents.personas import DreamerAgent, CriticAgent, SynthesizerAgent
from khazar_llms.orchestration.ensemble import Ensemble
from khazar_llms.orchestration.session import CreativeSession

async def main():
    # Create agents
    agents = [
        DreamerAgent(provider="mock"),
        CriticAgent(provider="mock"),
        SynthesizerAgent(provider="mock"),
    ]
    
    # Create ensemble
    ensemble = Ensemble(agents=agents, max_iterations=3)
    
    # Run creative session
    session = CreativeSession(ensemble)
    results = await session.run("Design a new form of communication")
    
    # View results
    for msg in results["conversation"]:
        print(f"{msg.sender}: {msg.content}")

asyncio.run(main())
```

### CLI Usage

```bash
# Get help
python -m khazar_llms.cli info

# List available agents
python -m khazar_llms.cli list-agents

# Run a creative task
python -m khazar_llms.cli create-task "Imagine a library that exists in multiple dimensions"

# Use parallel mode with specific agents
python -m khazar_llms.cli --mode parallel --agents dreamer rebel poet create-task "Create a new musical instrument"

# Use with real LLM provider
python -m khazar_llms.cli --provider openai create-task "Design an education system for the future"
```

## 📖 Examples

See the `examples/` directory for detailed examples:

- `basic_ensemble.py` - Basic ensemble creation and execution
- `parallel_debate.py` - Advanced orchestration modes

Run examples:
```bash
python examples/basic_ensemble.py
python examples/parallel_debate.py
```

## 🏗️ Architecture

### Core Components

1. **Agents** (`khazar_llms/agents/`)
   - Base agent class with memory and response logic
   - Specialized personas with unique system prompts
   - LLM client abstraction for multiple providers

2. **Orchestration** (`khazar_llms/orchestration/`)
   - Ensemble management for coordinating agents
   - Session management for running and saving collaborations
   - Multiple conversation modes (sequential, parallel, debate, consensus)

3. **Utilities** (`khazar_llms/utils/`)
   - LLM client with provider abstraction
   - Mock provider for testing without API costs

## 🎨 Conversation Modes

- **Sequential** - Agents respond one after another, building on previous responses
- **Parallel** - All agents respond simultaneously to the same context
- **Debate** - Agents engage in structured back-and-forth exchanges
- **Consensus** - Agents explicitly work toward agreement and synthesis

## 🧪 Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black khazar_llms/
flake8 khazar_llms/
```

## 🌈 Use Cases

- **Creative Writing** - Generate stories from multiple narrative perspectives
- **Product Design** - Explore product ideas through different lenses
- **Problem Solving** - Approach complex problems from multiple angles
- **Art & Poetry** - Create multi-layered artistic works
- **Philosophy** - Explore philosophical questions through dialogue
- **Education** - Learn topics by seeing multiple explanatory approaches

## 🤝 Contributing

Contributions are welcome! This project is an experiment in collective AI creativity. Feel free to:

- Add new agent personas
- Implement new orchestration modes
- Improve the conversation dynamics
- Add visualization tools
- Create new examples

See our [Contributing Guide](CONTRIBUTING.md) for more details.

## 🌐 Landing Page

A professional landing page for this project is available in the `docs/` directory. To view it:

```bash
# Open directly in browser
open docs/index.html

# Or serve with a local server
cd docs
python -m http.server 8000
# Visit http://localhost:8000
```

### Deploy Landing Page

You can deploy the landing page to GitHub Pages, Netlify, or Vercel. See [docs/README.md](docs/README.md) for deployment instructions.

## 📜 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Inspired by Milorad Pavić's *Dictionary of the Khazar*
- Built on the shoulders of amazing LLM providers
- For everyone exploring the creative potential of AI ensembles

---

*"The Khazars were a people who disappeared from history, leaving behind only fragments and conflicting accounts. From these fragments, we can imagine infinite stories. Similarly, from diverse AI perspectives, infinite creative possibilities emerge."*
