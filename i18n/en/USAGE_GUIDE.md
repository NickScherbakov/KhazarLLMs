# KhazarLLMs Usage Guide

A comprehensive guide to using the KhazarLLMs system for collective creativity.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Python API](#python-api)
3. [Command-Line Interface](#command-line-interface)
4. [Agent Personas](#agent-personas)
5. [Conversation Modes](#conversation-modes)
6. [Examples](#examples)
7. [Advanced Usage](#advanced-usage)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/KhazarLLMs.git
cd KhazarLLMs

# Install dependencies
pip install -r requirements.txt
```

### Your First Creative Session

Using the CLI (simplest):
```bash
python -m khazar_llms.cli create-task "Design a new kind of musical instrument"
```

Using Python:
```python
import asyncio
from khazar_llms.agents.personas import DreamerAgent, CriticAgent
from khazar_llms.orchestration.ensemble import Ensemble
from khazar_llms.orchestration.session import CreativeSession

async def main():
    agents = [DreamerAgent(provider="mock"), CriticAgent(provider="mock")]
    ensemble = Ensemble(agents=agents, max_iterations=2)
    session = CreativeSession(ensemble)
    results = await session.run("Design a new kind of musical instrument")
    
    for msg in results["conversation"]:
        print(f"{msg.sender}: {msg.content}\n")

asyncio.run(main())
```

## Python API

### Creating Agents

```python
from khazar_llms.agents.personas import (
    DreamerAgent, CriticAgent, SynthesizerAgent,
    PhilosopherAgent, RebelAgent, ArchitectAgent, PoetAgent
)

# Using mock provider (free, no API keys needed)
dreamer = DreamerAgent(provider="mock")

# Using OpenAI (requires OPENAI_API_KEY in .env)
critic = CriticAgent(provider="openai")

# Using Anthropic (requires ANTHROPIC_API_KEY in .env)
philosopher = PhilosopherAgent(provider="anthropic")
```

### Building an Ensemble

```python
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode

# Create with specific agents
agents = [DreamerAgent(provider="mock"), CriticAgent(provider="mock")]

# Configure the ensemble
ensemble = Ensemble(
    agents=agents,
    mode=ConversationMode.SEQUENTIAL,  # or PARALLEL, DEBATE, CONSENSUS
    max_iterations=5
)
```

### Running a Session

```python
from khazar_llms.orchestration.session import CreativeSession
from pathlib import Path

# Create session
session = CreativeSession(
    ensemble=ensemble,
    output_dir=Path("./my_sessions")
)

# Run the creative task
results = await session.run("Your creative task here")

# Save outputs
session.save_session(results, format="json")
session.save_session(results, format="txt")

# Print summary
session.print_summary(results)
```

### Accessing Results

```python
# Results dictionary contains:
results["task"]              # The original task
results["conversation"]      # List of Message objects
results["iterations"]        # Number of iterations run
results["agent_count"]       # Number of agents
results["duration_seconds"]  # How long it took

# Iterate through conversation
for message in results["conversation"]:
    print(f"[{message.iteration}] {message.sender} ({message.role.value})")
    print(message.content)
    print()
```

## Command-Line Interface

### Basic Commands

```bash
# Show system info
python -m khazar_llms.cli info

# List available agents
python -m khazar_llms.cli list-agents

# Run a creative task
python -m khazar_llms.cli create-task "Your task here"
```

### Options

```bash
# Select specific agents
python -m khazar_llms.cli create-task "Task" --agents dreamer critic poet

# Choose conversation mode
python -m khazar_llms.cli create-task "Task" --mode parallel

# Set number of iterations
python -m khazar_llms.cli create-task "Task" --iterations 5

# Use real LLM provider
python -m khazar_llms.cli create-task "Task" --provider openai

# Custom output directory
python -m khazar_llms.cli create-task "Task" --output-dir ./my_outputs

# Don't save to disk
python -m khazar_llms.cli create-task "Task" --no-save
```

### Complete Example

```bash
python -m khazar_llms.cli create-task \
  "Design a school that adapts to each student's learning style" \
  --agents dreamer critic architect philosopher \
  --mode debate \
  --iterations 3 \
  --provider mock \
  --output-dir ./education_sessions
```

## Agent Personas

### Dreamer (temperature: 0.95)
Generates wild, unbounded creative ideas. Best for brainstorming and exploring possibilities.

**Use when**: You want imaginative, unexpected ideas

### Critic (temperature: 0.4)
Analyzes ideas with sharp insight. Identifies weaknesses and challenges assumptions.

**Use when**: You need constructive feedback and reality checks

### Synthesizer (temperature: 0.7)
Combines disparate ideas into coherent wholes. Finds common threads and integration points.

**Use when**: You have multiple ideas that need unifying

### Philosopher (temperature: 0.6)
Explores deep meanings and broader contexts. Examines ethical and existential dimensions.

**Use when**: You want to understand deeper significance

### Rebel (temperature: 0.9)
Challenges assumptions and breaks rules. Introduces creative disruption.

**Use when**: Thinking has become too conventional

### Architect (temperature: 0.5)
Structures and organizes ideas. Creates frameworks and implementation plans.

**Use when**: Ideas need practical structure

### Poet (temperature: 0.85)
Adds beauty and emotional resonance. Makes ideas feel profound and moving.

**Use when**: You want emotional connection and artful expression

## Conversation Modes

### Sequential
Agents speak one after another, each building on previous responses.

**Best for**: Developing ideas progressively, logical flow

```python
ensemble = Ensemble(agents=agents, mode=ConversationMode.SEQUENTIAL)
```

### Parallel
All agents respond simultaneously to the same context.

**Best for**: Getting diverse perspectives quickly, exploring variety

```python
ensemble = Ensemble(agents=agents, mode=ConversationMode.PARALLEL)
```

### Debate
Agents engage in paired back-and-forth exchanges.

**Best for**: Exploring tensions, comparing approaches, dialectic

```python
ensemble = Ensemble(agents=agents, mode=ConversationMode.DEBATE)
```

### Consensus
Agents explicitly work toward agreement and synthesis.

**Best for**: Reaching conclusions, creating unified visions

```python
ensemble = Ensemble(agents=agents, mode=ConversationMode.CONSENSUS)
```

## Examples

### Creative Writing

```python
agents = [DreamerAgent(), PoetAgent(), PhilosopherAgent()]
task = "Write the opening paragraph of a novel about time"
```

### Product Design

```python
agents = [DreamerAgent(), CriticAgent(), ArchitectAgent()]
task = "Design a sustainable transportation system for cities"
```

### Problem Solving

```python
agents = [CriticAgent(), SynthesizerAgent(), ArchitectAgent()]
task = "How can we make online learning more engaging?"
```

### Philosophical Exploration

```python
agents = [PhilosopherAgent(), RebelAgent(), PoetAgent()]
task = "What is the meaning of creativity in the age of AI?"
```

## Advanced Usage

### Custom Agents

Create your own agent personas:

```python
from khazar_llms.agents.base import Agent, AgentRole, Message

class CustomAgent(Agent):
    def __init__(self, name="Custom", **kwargs):
        super().__init__(name=name, role=AgentRole.DREAMER, **kwargs)
    
    def get_system_prompt(self) -> str:
        return "Your unique system prompt here"
    
    async def respond(self, task, context, iteration):
        # Your custom logic
        pass
```

### Dynamic Agent Selection

```python
def select_agents(task_type):
    if task_type == "creative":
        return [DreamerAgent(), PoetAgent()]
    elif task_type == "analytical":
        return [CriticAgent(), ArchitectAgent()]
    else:
        return [DreamerAgent(), CriticAgent(), SynthesizerAgent()]

agents = select_agents("creative")
```

### Iteration Control

```python
# Run multiple sessions with increasing iterations
for iterations in [2, 4, 6]:
    ensemble = Ensemble(agents=agents, max_iterations=iterations)
    results = await session.run(task)
    print(f"With {iterations} iterations: {len(results['conversation'])} messages")
```

### Post-Processing Results

```python
# Extract insights by agent type
from collections import defaultdict

by_role = defaultdict(list)
for msg in results["conversation"]:
    by_role[msg.role].append(msg.content)

print("Dreamer ideas:", by_role[AgentRole.DREAMER])
print("Critic feedback:", by_role[AgentRole.CRITIC])
```

## Tips for Best Results

1. **Match agents to task**: Choose personas relevant to your creative challenge
2. **Start with 2-3 iterations**: More isn't always better
3. **Try different modes**: Different patterns yield different insights
4. **Use mock provider first**: Test ideas before spending on API calls
5. **Save interesting sessions**: Build a library of creative outputs
6. **Mix complementary agents**: Balance dreamers with critics, poets with architects

## Troubleshooting

### No output or empty responses
- Check API keys are set correctly in `.env`
- Verify provider is available (use mock for testing)
- Check network connectivity for real providers

### Repetitive responses
- Try different conversation modes
- Increase temperature for specific agents
- Use fewer iterations with same agents

### High API costs
- Use mock provider for development
- Limit max_iterations
- Choose fewer agents
- Cache results for reuse

---

*"The Khazar Dictionary is a lexicon of the possible. So too is KhazarLLMs - a system for exploring creative possibilities through multiple perspectives."*
