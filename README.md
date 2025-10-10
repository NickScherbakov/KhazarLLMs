# KhazarLLMs 🌟

**A System for Collective Creativity Management of Ensemble LLMs**

Inspired by Milorad Pavić's *Khazar Dictionary* and its exploration of multiple perspectives, KhazarLLMs orchestrates an ensemble of AI agents with distinct personalities and roles to collaborate on creative tasks. Like the polyphonic structure of the Khazar Dictionary, where multiple voices tell interconnected stories, this system brings together diverse AI perspectives to explore ideas from many angles.

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

## 📜 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Inspired by Milorad Pavić's *Dictionary of the Khazar*
- Built on the shoulders of amazing LLM providers
- For everyone exploring the creative potential of AI ensembles

---

*"The Khazars were a people who disappeared from history, leaving behind only fragments and conflicting accounts. From these fragments, we can imagine infinite stories. Similarly, from diverse AI perspectives, infinite creative possibilities emerge."*
