# Khazar Protocol Specification - Implementation Guide

This guide explains how to implement and use the Khazar Protocol Specification (KPS) in your projects.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Working with Agents](#working-with-agents)
5. [Working with Messages](#working-with-messages)
6. [Working with Sessions](#working-with-sessions)
7. [Validation](#validation)
8. [Exporting to KPS Format](#exporting-to-kps-format)
9. [CLI Tools](#cli-tools)
10. [Custom Extensions](#custom-extensions)

## Overview

The Khazar Protocol Specification (KPS) provides a standard format for multi-agent creative collaboration. KhazarLLMs is the reference implementation of KPS.

**Key Components:**
- **Agents**: AI entities with distinct personas
- **Messages**: Structured communication between agents
- **Sessions**: Bounded collaborative interactions
- **Synthesis**: Combined output from multiple perspectives

## Installation

```bash
# Clone the repository
git clone https://github.com/NickScherbakov/KhazarLLMs.git
cd KhazarLLMs

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Creating a KPS-Compliant Session

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
    ensemble = Ensemble(agents=agents, max_iterations=2)
    
    # Run session
    session = CreativeSession(ensemble)
    results = await session.run("Design a new form of art")
    
    # Export to KPS format
    kps_export = session.to_kps(results)
    
    # Save as JSON
    import json
    with open("session_kps.json", "w") as f:
        json.dump(kps_export, f, indent=2)

asyncio.run(main())
```

## Working with Agents

### Standard Agent Archetypes

KPS defines seven standard archetypes:

```python
from khazar_llms.agents.personas import (
    DreamerAgent,      # creative_visionary
    CriticAgent,       # analytical_challenger
    SynthesizerAgent,  # integrative_harmonizer
    PhilosopherAgent,  # contextual_thinker
    RebelAgent,        # disruptive_iconoclast
    ArchitectAgent,    # structural_organizer
    PoetAgent,         # aesthetic_artisan
)
```

### Exporting Agent to KPS Format

```python
agent = DreamerAgent(provider="openai")
kps_agent = agent.to_kps(agent_id="dreamer-001")

# kps_agent is now a KPS-compliant dictionary
print(kps_agent["persona"]["archetype"])  # "creative_visionary"
print(kps_agent["capabilities"])          # ["generate", "respond"]
```

### Creating Custom Agents

```python
from khazar_llms.agents.base import Agent, AgentRole

class CustomAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            name="Custom",
            role=AgentRole.DREAMER,  # or create custom role
            temperature=0.8,
            **kwargs
        )
    
    def get_system_prompt(self) -> str:
        return "Your custom system prompt..."
    
    async def respond(self, task, context, iteration):
        # Implementation
        pass
```

## Working with Messages

### KPS Message Format

Every message in KPS has the following structure:

```python
{
    "message_id": "uuid",
    "session_id": "uuid",
    "timestamp": "ISO-8601",
    "sender": {
        "agent_id": "dreamer-001",
        "persona_name": "The Dreamer"
    },
    "content": {
        "text": "Message content",
        "format": "plain",
        "language": "en"
    },
    "metadata": {
        "round": 0,
        "turn": 0,
        "mode": "sequential",
        "responding_to": [],
        "stage_direction": null
    },
    "annotations": {
        "sentiment": "positive",
        "intent": "propose",
        "confidence": 0.9
    }
}
```

### Converting Messages to KPS

```python
from khazar_llms.agents.base import Message, AgentRole

msg = Message(
    sender="Dreamer",
    role=AgentRole.DREAMER,
    content="Imagine a world...",
    iteration=0,
)

kps_msg = msg.to_kps(
    session_id="session-123",
    agent_id="dreamer-001",
    mode="sequential",
    turn=0,
    intent="propose",
)
```

### Message Intents

Standard KPS intents:
- `propose`: Introducing a new idea
- `challenge`: Questioning or critiquing
- `support`: Agreeing or building upon
- `synthesize`: Combining multiple ideas
- `question`: Seeking clarification
- `redirect`: Changing direction
- `conclude`: Offering final thoughts
- `acknowledge`: Recognizing contribution

## Working with Sessions

### Session States

KPS sessions follow this lifecycle:

```
INITIALIZED → ACTIVE → SYNTHESIZING → COMPLETED
                ↓
            PAUSED → RESUMED
                ↓
            TERMINATED
```

### Orchestration Modes

KPS supports four standard modes:

1. **Sequential**: Agents respond one after another
2. **Parallel**: Agents respond simultaneously
3. **Debate**: Structured back-and-forth exchanges
4. **Consensus**: Iterative refinement toward agreement

```python
from khazar_llms.orchestration.ensemble import Ensemble, ConversationMode

ensemble = Ensemble(
    agents=agents,
    mode=ConversationMode.PARALLEL,
    max_iterations=3,
)
```

## Validation

### Using the Validator

```python
from khazar_llms.protocol import KPSValidator

validator = KPSValidator()

# Validate an agent
result = validator.validate_agent(agent_data)
if result.valid:
    print("✓ Agent is KPS-compliant")
else:
    print("✗ Errors:", result.errors)

# Validate a message
result = validator.validate_message(message_data)

# Validate a session
result = validator.validate_session(session_data)

# Validate a complete export
result = validator.validate_session_export(export_data)
```

### Validation Results

```python
result = validator.validate_agent(agent_data)

print(result.valid)      # True or False
print(result.errors)     # List of error messages
print(result.warnings)   # List of warnings

# Convert to dict
data = result.to_dict()
```

## Exporting to KPS Format

### Export a Complete Session

```python
async def export_session():
    # Run session
    session = CreativeSession(ensemble)
    results = await session.run("Your task")
    
    # Export to KPS format
    kps_export = session.to_kps(results)
    
    # The export includes:
    # - session: Session configuration
    # - agents: All participating agents
    # - messages: All messages exchanged
    
    # Validate the export
    validator = KPSValidator()
    validation = validator.validate_session_export(kps_export)
    
    if validation.valid:
        # Save to file
        import json
        with open("session.kps.json", "w") as f:
            json.dump(kps_export, f, indent=2)
```

### Export Individual Components

```python
# Export just an agent
agent = DreamerAgent(provider="mock")
agent_kps = agent.to_kps(agent_id="dreamer-001")

# Export a message
message = Message(...)
msg_kps = message.to_kps(
    session_id="session-id",
    agent_id="agent-id",
    ...
)
```

## CLI Tools

### Protocol Commands

```bash
# Show protocol information
python -m khazar_llms.cli protocol info

# Validate a KPS file
python -m khazar_llms.cli protocol validate session.kps.json

# Show validation results
python -m khazar_llms.cli protocol validate my_export.json
```

### Running Sessions

```bash
# Run a session (automatically KPS-compliant)
python -m khazar_llms.cli create-task "Design a new musical instrument"

# Different modes
python -m khazar_llms.cli --mode parallel create-task "Your task"
python -m khazar_llms.cli --mode debate create-task "Your task"
python -m khazar_llms.cli --mode consensus create-task "Your task"
```

## Custom Extensions

### Creating Custom Archetypes

```python
# Define custom archetype
custom_agent_data = {
    "agent_id": "historian-001",
    "persona": {
        "name": "The Historian",
        "archetype": "com.example.historian",  # Use reverse DNS
        "system_prompt": "You connect ideas to historical precedents...",
        "communication_style": "narrative, contextual",
    },
    "capabilities": ["respond", "generate"],
    "provider": "openai",
    "temperature": 0.6,
}

# Validate (will show warning about custom archetype)
validator = KPSValidator()
result = validator.validate_agent(custom_agent_data)
# Result: valid=True, warnings=["Using custom archetype: com.example.historian"]
```

### Custom Orchestration Modes

```python
# Custom modes should use reverse DNS notation
custom_session = {
    "session_id": "session-001",
    "prompt": "Task",
    "state": "ACTIVE",
    "config": {
        "mode": "com.example.round_robin",  # Custom mode
        "max_rounds": 5,
        "synthesis_strategy": "final_agent",
    },
    "participants": ["agent-001"],
    "created_at": "2024-12-13T14:30:00.000Z",
}
```

### Extension Metadata

Add custom metadata to any KPS structure:

```python
kps_message = {
    # ... standard fields ...
    "metadata": {
        "round": 0,
        "turn": 0,
        "mode": "sequential",
        # Custom extension fields
        "theatre:stage_direction": "[Enter dramatically]",
        "benchmark:creativity_score": 0.85,
    }
}
```

## JSON Schemas

All KPS structures have formal JSON schemas in the `schemas/` directory:

- `agent.schema.json` - Agent specification
- `message.schema.json` - Message format
- `session.schema.json` - Session configuration
- `synthesis.schema.json` - Synthesis output
- `kps.schema.json` - Combined schema

You can use these for validation in any language that supports JSON Schema.

## Best Practices

1. **Always validate** exports before sharing
2. **Use standard archetypes** when possible
3. **Document custom extensions** clearly
4. **Include metadata** for debugging
5. **Version your exports** with KPS version
6. **Test interoperability** with other implementations

## Examples

See the `examples/` directory for complete examples:
- `basic_ensemble.py` - Basic KPS session
- `parallel_debate.py` - Different orchestration modes

## Further Reading

- `PROTOCOL.md` - Full KPS specification
- `README.md` - Project overview
- `ARCHITECTURE.md` - System architecture

## Support

For questions and contributions:
- GitHub Issues: https://github.com/NickScherbakov/KhazarLLMs/issues
- Documentation: See repository docs/

---

**KhazarLLMs** - Reference implementation of the Khazar Protocol Specification
