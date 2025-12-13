# Khazar Protocol Specification (KPS)
## Version 1.0.0-draft

**Status:** Draft  
**Date:** December 2024  
**Authors:** KhazarLLMs Project Contributors

---

## Abstract

The Khazar Protocol Specification (KPS) defines a standard for multi-agent creative collaboration using Large Language Models (LLMs). Inspired by Milorad Pavić's *Dictionary of the Khazar*, which presents truth through multiple overlapping perspectives, KPS establishes a formal protocol for how AI agents with distinct personalities communicate, collaborate, and reach creative consensus.

KPS provides:
- **Standard agent identity and persona definitions**
- **Message format specifications for agent communication**
- **Session management and lifecycle protocols**
- **Orchestration modes for different collaboration patterns**
- **Synthesis strategies for combining multiple perspectives**
- **Extensibility mechanisms for custom implementations**

The goal of KPS is to become the industry standard for multi-agent creative systems, enabling interoperability between implementations and fostering innovation in collective AI creativity.

---

## 1. Introduction

### 1.1 Purpose and Scope

The Khazar Protocol Specification defines how multiple AI agents with distinct personas can collaborate on creative tasks. This specification covers:

- Agent identity and behavioral definitions
- Message structure and intent classification
- Session lifecycle management
- Orchestration patterns for agent interaction
- Synthesis protocols for combining perspectives
- Error handling and conformance requirements

KPS is designed to be:
- **Implementation-agnostic**: Works with any LLM provider (OpenAI, Anthropic, etc.)
- **Language-neutral**: Applicable to any programming language
- **Extensible**: Supports custom agents, modes, and synthesis strategies
- **Interoperable**: Enables session sharing between implementations

### 1.2 Design Philosophy

KPS is inspired by the polyphonic structure of the Khazar Dictionary, where truth emerges not from a single authoritative source but from the interplay of multiple voices. Key principles:

1. **Diversity of Perspective**: Multiple agents with distinct roles create richer outcomes
2. **Structured Collaboration**: Formal protocols enable meaningful interaction
3. **Emergent Synthesis**: Collective intelligence emerges from orchestrated dialogue
4. **Creative Freedom**: Agents maintain distinct personalities while working toward shared goals

### 1.3 Relationship to Existing Standards

KPS builds upon and complements existing standards:

- **JSON-RPC 2.0**: For structured message passing (when applicable)
- **ISO 8601**: For timestamp formatting
- **RFC 4122**: For UUID generation
- **JSON Schema**: For validation

KPS is designed to coexist with other multi-agent frameworks (AutoGen, CrewAI, LangGraph) while providing a specific focus on creative collaboration with distinct agent personas.

---

## 2. Terminology

This specification uses the following terms:

- **Agent**: An AI entity with a defined persona, capabilities, and communication style
- **Persona**: The behavioral characteristics, role, and personality of an agent
- **Archetype**: A standard persona template with predefined characteristics
- **Ensemble**: A group of agents working together on a shared task
- **Session**: A bounded creative collaboration with a defined lifecycle
- **Turn**: A single agent's contribution within a round
- **Round**: A complete cycle where all participating agents contribute once
- **Iteration**: Synonym for round (used interchangeably)
- **Synthesis**: The process of combining multiple agent perspectives into a unified output
- **Consensus**: A state of agreement among agents
- **Stage Direction**: Optional narrative context or meta-instructions for agent behavior
- **Intent**: The communicative purpose of a message (propose, challenge, support, etc.)
- **Mode**: The orchestration pattern governing agent interaction (sequential, parallel, etc.)
- **Provider**: The underlying LLM service (OpenAI, Anthropic, etc.)

**Key words** for requirement levels: "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are to be interpreted as described in RFC 2119.

---

## 3. Agent Specification

### 3.1 Agent Identity

Every KPS-compliant agent MUST have a unique identity defined by the following structure:

```json
{
  "agent_id": "unique-identifier",
  "persona": {
    "name": "The Dreamer",
    "archetype": "creative_visionary",
    "symbol": "🌙",
    "color": "#9333ea",
    "system_prompt": "You are the Dreamer - a boundlessly creative agent...",
    "traits": ["imaginative", "unbounded", "visionary"],
    "communication_style": "poetic, metaphorical"
  },
  "capabilities": ["generate", "respond", "synthesize"],
  "provider": "openai",
  "model": "gpt-4",
  "temperature": 0.95,
  "metadata": {
    "version": "1.0.0",
    "created_at": "2024-12-13T00:00:00Z"
  }
}
```

**Field Definitions:**

- `agent_id` (REQUIRED, string): Unique identifier for this agent instance (UUID v4 recommended)
- `persona` (REQUIRED, object): The agent's personality and role definition
  - `name` (REQUIRED, string): Human-readable name
  - `archetype` (REQUIRED, string): Standard or custom archetype identifier
  - `symbol` (OPTIONAL, string): Unicode symbol representing the agent
  - `color` (OPTIONAL, string): Hex color code for visual representation
  - `system_prompt` (REQUIRED, string): The prompt defining agent behavior
  - `traits` (OPTIONAL, array): List of personality traits
  - `communication_style` (OPTIONAL, string): Description of communication approach
- `capabilities` (REQUIRED, array): List of agent capabilities (see §3.1.1)
- `provider` (REQUIRED, string): LLM provider identifier
- `model` (OPTIONAL, string): Specific model identifier
- `temperature` (OPTIONAL, number): Sampling temperature (0.0-1.0)
- `metadata` (OPTIONAL, object): Additional implementation-specific data

#### 3.1.1 Standard Capabilities

KPS defines the following standard capabilities:

- `generate`: Generate original responses to prompts
- `respond`: Respond to other agents' messages
- `synthesize`: Combine multiple perspectives into synthesis
- `critique`: Analyze and provide feedback on ideas
- `vote`: Participate in voting-based synthesis
- `moderate`: Guide conversation flow

Implementations MAY define custom capabilities.

### 3.2 Standard Archetypes

KPS defines seven standard archetypes with expected behaviors:

#### 3.2.1 The Dreamer (creative_visionary)
- **Role**: Generate wild, imaginative ideas without constraints
- **Temperature**: 0.9-1.0 (high creativity)
- **Communication Style**: Poetic, metaphorical, expansive
- **Primary Capability**: generate
- **Symbol**: 🌙
- **Color**: #9333ea (purple)

#### 3.2.2 The Critic (analytical_challenger)
- **Role**: Analyze ideas with sharp insight and constructive feedback
- **Temperature**: 0.3-0.5 (analytical precision)
- **Communication Style**: Direct, incisive, constructive
- **Primary Capability**: critique
- **Symbol**: 🔍
- **Color**: #dc2626 (red)

#### 3.2.3 The Synthesizer (integrative_harmonizer)
- **Role**: Combine disparate ideas into coherent wholes
- **Temperature**: 0.6-0.8 (balanced)
- **Communication Style**: Integrative, bridging, unifying
- **Primary Capability**: synthesize
- **Symbol**: 🌊
- **Color**: #2563eb (blue)

#### 3.2.4 The Philosopher (contextual_thinker)
- **Role**: Explore deeper meanings and broader contexts
- **Temperature**: 0.5-0.7 (thoughtful)
- **Communication Style**: Contemplative, profound, questioning
- **Primary Capability**: respond
- **Symbol**: 🦉
- **Color**: #7c3aed (indigo)

#### 3.2.5 The Rebel (disruptive_iconoclast)
- **Role**: Challenge assumptions and break conventions
- **Temperature**: 0.8-1.0 (high disruption)
- **Communication Style**: Provocative, contrarian, bold
- **Primary Capability**: critique
- **Symbol**: ⚡
- **Color**: #ea580c (orange)

#### 3.2.6 The Architect (structural_organizer)
- **Role**: Structure and organize ideas into implementable forms
- **Temperature**: 0.4-0.6 (structured)
- **Communication Style**: Systematic, logical, methodical
- **Primary Capability**: synthesize
- **Symbol**: 🏛️
- **Color**: #059669 (green)

#### 3.2.7 The Poet (aesthetic_artisan)
- **Role**: Add beauty and emotional resonance
- **Temperature**: 0.7-0.9 (artistic)
- **Communication Style**: Lyrical, evocative, emotive
- **Primary Capability**: generate
- **Symbol**: 🎭
- **Color**: #db2777 (pink)

### 3.3 Custom Archetype Guidelines

Implementations MAY create custom archetypes. To be KPS-compliant, custom archetypes MUST:

1. Define a unique `archetype` identifier (reverse DNS notation recommended)
2. Specify a clear `system_prompt` that defines behavior
3. Declare `capabilities` from the standard set or custom extensions
4. Document expected `communication_style`
5. Specify recommended `temperature` range

Example custom archetype:

```json
{
  "archetype": "com.example.historian",
  "name": "The Historian",
  "system_prompt": "You are the Historian - an agent who connects ideas to historical precedents...",
  "communication_style": "Narrative, contextual, reference-rich",
  "temperature": 0.5,
  "capabilities": ["generate", "respond"]
}
```

---

## 4. Message Format

### 4.1 Message Structure

All messages in KPS MUST conform to the following structure:

```json
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "timestamp": "2024-12-13T14:30:00.000Z",
  "sender": {
    "agent_id": "dreamer-001",
    "persona_name": "The Dreamer"
  },
  "content": {
    "text": "Imagine a library that exists simultaneously in past, present, and future...",
    "format": "plain",
    "language": "en"
  },
  "metadata": {
    "round": 1,
    "turn": 1,
    "mode": "sequential",
    "responding_to": [],
    "stage_direction": null
  },
  "annotations": {
    "sentiment": "positive",
    "intent": "propose",
    "confidence": 0.92
  }
}
```

**Field Definitions:**

- `message_id` (REQUIRED, string): Unique identifier (UUID v4)
- `session_id` (REQUIRED, string): Reference to parent session
- `timestamp` (REQUIRED, string): ISO 8601 timestamp with timezone
- `sender` (REQUIRED, object):
  - `agent_id` (REQUIRED, string): Sending agent's identifier
  - `persona_name` (REQUIRED, string): Human-readable persona name
- `content` (REQUIRED, object):
  - `text` (REQUIRED, string): The message content
  - `format` (OPTIONAL, string): Content format (plain|markdown|structured)
  - `language` (OPTIONAL, string): ISO 639-1 language code
- `metadata` (REQUIRED, object):
  - `round` (REQUIRED, integer): Round number (starting from 0)
  - `turn` (REQUIRED, integer): Turn within round (starting from 0)
  - `mode` (REQUIRED, string): Orchestration mode
  - `responding_to` (OPTIONAL, array): Message IDs being responded to
  - `stage_direction` (OPTIONAL, string): Narrative context
- `annotations` (OPTIONAL, object):
  - `sentiment` (OPTIONAL, string): positive|negative|neutral
  - `intent` (REQUIRED, string): Message intent (see §4.2)
  - `confidence` (OPTIONAL, number): Confidence score (0.0-1.0)

### 4.2 Intent Types

KPS defines the following standard intent types:

- `propose`: Introducing a new idea or suggestion
- `challenge`: Questioning or critiquing an existing idea
- `support`: Agreeing with or building upon an idea
- `synthesize`: Combining multiple ideas into one
- `question`: Seeking clarification or elaboration
- `redirect`: Changing conversation direction
- `conclude`: Offering final thoughts or summary
- `acknowledge`: Recognizing another agent's contribution

Each message MUST specify exactly one primary intent. Implementations MAY extend with custom intents using reverse DNS notation (e.g., `com.example.custom_intent`).

### 4.3 Stage Directions

Stage directions provide narrative context for agent behavior. They are OPTIONAL and primarily used for theatrical or enhanced visualization modes.

Example:
```json
{
  "stage_direction": "[The Dreamer gazes at distant stars, voice filled with wonder]"
}
```

---

## 5. Session Management

### 5.1 Session Lifecycle

KPS sessions follow a defined state machine:

```
INITIALIZED → ACTIVE → SYNTHESIZING → COMPLETED
                ↓
            PAUSED → RESUMED
                ↓
            TERMINATED
```

**State Definitions:**

- `INITIALIZED`: Session created, agents assigned, ready to start
- `ACTIVE`: Agents are actively exchanging messages
- `PAUSED`: Session temporarily suspended, can be resumed
- `RESUMED`: Session reactivated after pause
- `SYNTHESIZING`: Final synthesis being generated
- `COMPLETED`: Session finished normally with results
- `TERMINATED`: Session stopped abnormally or by request

### 5.2 Session Configuration

Every KPS session MUST be defined by the following structure:

```json
{
  "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "prompt": "Design a new form of communication that transcends language barriers",
  "state": "INITIALIZED",
  "config": {
    "mode": "sequential",
    "max_rounds": 5,
    "max_tokens_per_turn": 500,
    "synthesis_strategy": "final_agent",
    "consensus_threshold": 0.7,
    "timeout_seconds": 300
  },
  "participants": [
    "dreamer-001",
    "critic-002",
    "synthesizer-003"
  ],
  "created_at": "2024-12-13T14:30:00.000Z",
  "started_at": null,
  "completed_at": null,
  "metadata": {
    "version": "1.0.0",
    "creator": "user@example.com"
  }
}
```

**Field Definitions:**

- `session_id` (REQUIRED, string): Unique session identifier
- `prompt` (REQUIRED, string): The creative task or question
- `state` (REQUIRED, string): Current session state
- `config` (REQUIRED, object):
  - `mode` (REQUIRED, string): Orchestration mode (see §6)
  - `max_rounds` (REQUIRED, integer): Maximum number of rounds
  - `max_tokens_per_turn` (OPTIONAL, integer): Token limit per message
  - `synthesis_strategy` (REQUIRED, string): How to synthesize (see §7.1)
  - `consensus_threshold` (OPTIONAL, number): Required agreement (0.0-1.0)
  - `timeout_seconds` (OPTIONAL, integer): Maximum session duration
- `participants` (REQUIRED, array): List of agent IDs
- `created_at` (REQUIRED, string): ISO 8601 timestamp
- `started_at` (OPTIONAL, string): When session became active
- `completed_at` (OPTIONAL, string): When session ended
- `metadata` (OPTIONAL, object): Additional data

---

## 6. Orchestration Modes

KPS defines four standard orchestration modes that govern how agents interact.

### 6.1 Sequential Mode

**Identifier:** `sequential`

Agents respond one after another in a defined order, with each agent building on all previous responses.

**Characteristics:**
- Agents respond in order defined by `participants` array
- Each agent has full context of all prior messages
- Promotes narrative building and progressive refinement

**Message Order:**
```
Round 0: Agent1 → Agent2 → Agent3
Round 1: Agent1 → Agent2 → Agent3
...
```

### 6.2 Parallel Mode

**Identifier:** `parallel`

All agents respond simultaneously to the same context without seeing each other's current responses.

**Characteristics:**
- Agents respond independently in parallel
- Each sees context only from previous rounds, not current round
- Maximizes perspective diversity
- Requires asynchronous processing capability

**Message Order:**
```
Round 0: [Agent1 || Agent2 || Agent3]
Round 1: [Agent1 || Agent2 || Agent3]
...
```

### 6.3 Debate Mode

**Identifier:** `debate`

Agents engage in structured back-and-forth exchanges with explicit challenges and defenses.

**Characteristics:**
- Agents paired for direct interaction
- Encourages critical examination of ideas
- May include designated "for" and "against" positions
- Turn order alternates between opposing perspectives

**Message Order:**
```
Round 0: Agent1 ⇄ Agent2, Agent3 ⇄ Agent4
Round 1: Agent2 ⇄ Agent1, Agent4 ⇄ Agent3
...
```

### 6.4 Consensus Mode

**Identifier:** `consensus`

Agents explicitly work toward agreement through iterative refinement.

**Characteristics:**
- Similar to sequential but with consensus checking
- Session continues until consensus threshold reached or max rounds exceeded
- Agents explicitly state agreement/disagreement
- May use voting or similarity metrics

**Consensus Detection:**
Implementations SHOULD track:
- Explicit agreement statements
- Semantic similarity of proposals
- Convergence metrics

### 6.5 Custom Mode Definition

Implementations MAY define custom orchestration modes. Custom modes MUST:

1. Use reverse DNS notation (e.g., `com.example.custom_mode`)
2. Document turn-taking rules
3. Specify termination conditions
4. Define context visibility rules

Example:
```json
{
  "mode": "com.example.round_robin",
  "description": "Agents take turns responding to each other in round-robin fashion",
  "turn_order": "circular",
  "context_visibility": "full"
}
```

---

## 7. Synthesis Protocol

### 7.1 Synthesis Strategies

Synthesis combines multiple agent perspectives into a unified output. KPS defines four standard strategies:

#### 7.1.1 Final Agent Strategy

**Identifier:** `final_agent`

A designated agent (typically a Synthesizer) creates the final synthesis.

```json
{
  "strategy": "final_agent",
  "synthesizer_agent_id": "synthesizer-003"
}
```

**Process:**
1. All agents complete their rounds
2. Designated synthesizer receives all messages
3. Synthesizer generates unified synthesis
4. Synthesis marked as final output

#### 7.1.2 Voting Strategy

**Identifier:** `voting`

Agents vote on key points, and majority decisions are compiled.

```json
{
  "strategy": "voting",
  "voting_method": "ranked_choice",
  "min_votes": 3
}
```

**Process:**
1. Extract key proposals from messages
2. Agents vote on proposals
3. Compile winning proposals
4. Generate synthesis from winners

#### 7.1.3 Merge Strategy

**Identifier:** `merge`

Algorithmic combination of outputs using text similarity and clustering.

```json
{
  "strategy": "merge",
  "algorithm": "semantic_clustering",
  "similarity_threshold": 0.75
}
```

**Process:**
1. Analyze semantic similarity of messages
2. Cluster similar ideas
3. Extract representative points
4. Generate cohesive narrative

#### 7.1.4 Iterative Strategy

**Identifier:** `iterative`

Multiple rounds of synthesis with agent feedback.

```json
{
  "strategy": "iterative",
  "max_synthesis_rounds": 3,
  "convergence_threshold": 0.8
}
```

**Process:**
1. Initial synthesis generated
2. Agents provide feedback
3. Synthesis refined based on feedback
4. Repeat until convergence or max rounds

### 7.2 Synthesis Output Format

Synthesis output MUST conform to:

```json
{
  "synthesis_id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "strategy": "final_agent",
  "synthesizer_agent_id": "synthesizer-003",
  "content": {
    "text": "The collective vision that emerged combines...",
    "format": "markdown",
    "language": "en"
  },
  "sources": [
    "message-id-1",
    "message-id-2",
    "message-id-3"
  ],
  "metrics": {
    "agreement_score": 0.82,
    "diversity_score": 0.68,
    "coherence_score": 0.91
  },
  "dissenting_views": [
    {
      "agent_id": "rebel-004",
      "message_id": "message-id-4",
      "summary": "Alternative perspective on implementation approach"
    }
  ],
  "created_at": "2024-12-13T15:00:00.000Z"
}
```

**Field Definitions:**

- `synthesis_id` (REQUIRED, string): Unique identifier
- `session_id` (REQUIRED, string): Parent session reference
- `strategy` (REQUIRED, string): Strategy used
- `synthesizer_agent_id` (OPTIONAL, string): Agent that created synthesis
- `content` (REQUIRED, object): The synthesis content
- `sources` (REQUIRED, array): Source message IDs
- `metrics` (OPTIONAL, object): Quality metrics
- `dissenting_views` (OPTIONAL, array): Minority perspectives
- `created_at` (REQUIRED, string): ISO 8601 timestamp

---

## 8. Events and Hooks

### 8.1 Standard Events

KPS implementations SHOULD emit the following events:

| Event ID | Description | Payload |
|----------|-------------|---------|
| `session.initialized` | Session created | Session config |
| `session.started` | Session became active | Session ID, timestamp |
| `agent.joined` | Agent added to session | Agent ID, session ID |
| `agent.left` | Agent removed from session | Agent ID, session ID |
| `turn.started` | Agent begins response | Agent ID, round, turn |
| `turn.completed` | Agent finished response | Message object |
| `round.started` | New round begins | Round number, participants |
| `round.completed` | All agents finished round | Round number, message count |
| `synthesis.started` | Synthesis generation begins | Strategy, session ID |
| `synthesis.completed` | Synthesis finished | Synthesis object |
| `session.paused` | Session paused | Session ID, timestamp |
| `session.resumed` | Session resumed | Session ID, timestamp |
| `session.completed` | Session ended normally | Final results |
| `session.terminated` | Session ended abnormally | Reason, session ID |
| `error.occurred` | Error during processing | Error object |

### 8.2 Hook Interface

Implementations MAY provide hooks for extending behavior:

**Python Example:**
```python
@kps_hook("turn.completed")
def on_turn_completed(event: TurnEvent):
    """Called when an agent completes a turn."""
    log_message(event.message)
    update_metrics(event.session_id)
```

**JavaScript Example:**
```javascript
kps.on('turn.completed', (event) => {
  logMessage(event.message);
  updateMetrics(event.sessionId);
});
```

**Event Object Structure:**
```json
{
  "event_type": "turn.completed",
  "timestamp": "2024-12-13T14:35:00.000Z",
  "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "data": {
    "agent_id": "dreamer-001",
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "round": 0,
    "turn": 0
  }
}
```

---

## 9. Error Handling

### 9.1 Standard Error Codes

KPS defines standard error codes for common failure scenarios:

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| KPS-001 | Agent Timeout | Agent failed to respond within timeout | Skip turn or retry |
| KPS-002 | Invalid Message Format | Message doesn't conform to schema | Reject message |
| KPS-003 | Session Not Found | Referenced session doesn't exist | Create new session |
| KPS-004 | Consensus Not Reached | Failed to achieve consensus threshold | Continue or terminate |
| KPS-005 | Provider Error | LLM provider returned error | Retry or fallback |
| KPS-006 | Invalid Agent Configuration | Agent config fails validation | Reject agent |
| KPS-007 | Max Rounds Exceeded | Reached max_rounds limit | Force synthesis |
| KPS-008 | Unauthorized Access | Insufficient permissions | Deny action |
| KPS-009 | Invalid Session State | Operation invalid for current state | Reject operation |
| KPS-010 | Synthesis Failed | Synthesis generation failed | Retry with fallback |

### 9.2 Error Response Format

Errors MUST be reported in the following format:

```json
{
  "error": {
    "code": "KPS-001",
    "message": "Agent 'dreamer-001' failed to respond within 300 seconds",
    "timestamp": "2024-12-13T14:40:00.000Z",
    "session_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "context": {
      "agent_id": "dreamer-001",
      "round": 2,
      "timeout_seconds": 300
    },
    "recovery_suggestion": "Skip this turn and continue with next agent"
  }
}
```

---

## 10. Extensions

### 10.1 Extension Mechanism

KPS supports extensions through:

1. **Custom Archetypes** (§3.3)
2. **Custom Orchestration Modes** (§6.5)
3. **Custom Synthesis Strategies** (§7.1)
4. **Custom Events** (§8.2)
5. **Custom Metadata Fields**

Extensions MUST:
- Use namespaced identifiers (reverse DNS recommended)
- Not conflict with standard KPS fields
- Document their behavior and requirements
- Degrade gracefully when not supported

### 10.2 Registered Extensions

Implementations MAY register extensions with the KPS community. Currently recognized extensions:

#### kps-theatre
**Namespace:** `theatre.kps.khazarllms.org`  
**Purpose:** Theatrical visualization with stage directions and dramatic formatting  
**Status:** Official extension in KhazarLLMs reference implementation

**Additional Fields:**
```json
{
  "metadata": {
    "theatre:stage_direction": "[The Dreamer enters, eyes bright with visions]",
    "theatre:tone": "wonder",
    "theatre:intensity": 0.8
  }
}
```

#### kps-benchmark
**Namespace:** `benchmark.kps.khazarllms.org`  
**Purpose:** Creativity and quality metrics for sessions  
**Status:** Experimental

**Additional Fields:**
```json
{
  "metrics": {
    "benchmark:creativity_score": 0.85,
    "benchmark:coherence_score": 0.78,
    "benchmark:novelty_score": 0.92
  }
}
```

---

## 11. Security Considerations

### 11.1 Agent Authentication

Implementations SHOULD authenticate agents to prevent:
- Unauthorized agent impersonation
- Message injection attacks
- Session hijacking

Recommended approaches:
- Agent ID signing with cryptographic keys
- Session tokens with expiration
- API key authentication for external agents

### 11.2 Message Integrity

Messages SHOULD include integrity checks:

```json
{
  "signature": {
    "algorithm": "HMAC-SHA256",
    "value": "a1b2c3d4...",
    "key_id": "agent-key-001"
  }
}
```

### 11.3 Session Isolation

Sessions MUST be isolated to prevent:
- Cross-session data leakage
- Unauthorized session access
- Context pollution

Implementations SHOULD:
- Validate session_id on all operations
- Implement access control lists
- Clear session data on completion

### 11.4 Content Safety

Implementations SHOULD implement content safety measures:
- Input validation and sanitization
- Output filtering for harmful content
- Rate limiting to prevent abuse
- Audit logging for compliance

### 11.5 Privacy

Implementations MUST respect privacy by:
- Not logging sensitive prompts without consent
- Allowing session deletion
- Supporting data export for portability
- Complying with applicable data protection laws

---

## 12. Conformance

### 12.1 Conformance Levels

KPS defines three conformance levels:

#### Level 1: Basic Conformance
MUST support:
- Agent identity structure (§3.1)
- At least one standard archetype (§3.2)
- Message format (§4.1)
- Session configuration (§5.2)
- Sequential mode (§6.1)
- At least one synthesis strategy (§7.1)

#### Level 2: Standard Conformance
MUST support Level 1 plus:
- All seven standard archetypes (§3.2)
- All standard orchestration modes (§6)
- Final agent and voting synthesis (§7.1.1-7.1.2)
- Standard events (§8.1)
- Standard error codes (§9.1)

#### Level 3: Full Conformance
MUST support Level 2 plus:
- Custom archetype support (§3.3)
- All synthesis strategies (§7.1)
- Hook interface (§8.2)
- Extension mechanism (§10.1)
- Security features (§11)

### 12.2 Validation

Implementations SHOULD provide:
- JSON Schema validation for all structures
- Session state validation
- Message format validation
- Agent configuration validation

### 12.3 Interoperability

To ensure interoperability, implementations MUST:
- Accept sessions exported by other KPS implementations
- Produce valid KPS output that others can consume
- Document any custom extensions used
- Gracefully handle unknown extensions

---

## Appendix A: JSON Schema

Complete JSON schemas for KPS structures are provided in the `schemas/` directory:

- `agent.schema.json` - Agent identity and persona
- `message.schema.json` - Message format
- `session.schema.json` - Session configuration
- `synthesis.schema.json` - Synthesis output
- `kps.schema.json` - Combined schema

See the schemas directory for full definitions.

---

## Appendix B: Reference Implementation

The reference implementation of KPS is **KhazarLLMs**, available at:
- GitHub: https://github.com/NickScherbakov/KhazarLLMs
- Documentation: See repository README.md and docs/

The reference implementation:
- Achieves Level 3 (Full Conformance)
- Includes Python SDK and CLI
- Provides validation tools
- Demonstrates all standard features
- Includes the `kps-theatre` extension

---

## Appendix C: Examples

### C.1 Simple Sequential Session

```json
{
  "session_id": "session-001",
  "prompt": "Design a new musical instrument",
  "state": "ACTIVE",
  "config": {
    "mode": "sequential",
    "max_rounds": 2,
    "synthesis_strategy": "final_agent"
  },
  "participants": ["dreamer-001", "critic-002", "synthesizer-003"]
}
```

**Round 0:**
```json
[
  {
    "message_id": "msg-001",
    "session_id": "session-001",
    "sender": {"agent_id": "dreamer-001", "persona_name": "The Dreamer"},
    "content": {"text": "Imagine an instrument that translates emotions directly into sound..."},
    "metadata": {"round": 0, "turn": 0, "mode": "sequential"},
    "annotations": {"intent": "propose"}
  },
  {
    "message_id": "msg-002",
    "session_id": "session-001",
    "sender": {"agent_id": "critic-002", "persona_name": "The Critic"},
    "content": {"text": "While emotionally resonant, we need to consider practical constraints..."},
    "metadata": {"round": 0, "turn": 1, "mode": "sequential", "responding_to": ["msg-001"]},
    "annotations": {"intent": "challenge"}
  },
  {
    "message_id": "msg-003",
    "session_id": "session-001",
    "sender": {"agent_id": "synthesizer-003", "persona_name": "The Synthesizer"},
    "content": {"text": "Combining the emotional vision with practical needs, we could create..."},
    "metadata": {"round": 0, "turn": 2, "mode": "sequential", "responding_to": ["msg-001", "msg-002"]},
    "annotations": {"intent": "synthesize"}
  }
]
```

### C.2 Parallel Mode with Synthesis

```json
{
  "session_id": "session-002",
  "prompt": "Reimagine education for the 22nd century",
  "config": {
    "mode": "parallel",
    "max_rounds": 1,
    "synthesis_strategy": "voting"
  },
  "participants": ["dreamer-001", "philosopher-002", "architect-003"]
}
```

All agents respond simultaneously with different perspectives, then vote on key elements for synthesis.

### C.3 Consensus Session

```json
{
  "session_id": "session-003",
  "prompt": "Create ethical guidelines for AI creativity",
  "config": {
    "mode": "consensus",
    "max_rounds": 5,
    "consensus_threshold": 0.85,
    "synthesis_strategy": "iterative"
  },
  "participants": ["philosopher-001", "critic-002", "rebel-003", "synthesizer-004"]
}
```

Agents iterate until consensus threshold reached or max rounds exceeded.

---

## Appendix D: Version History

### Version 1.0.0-draft (December 2024)
- Initial draft specification
- Seven standard archetypes defined
- Four orchestration modes specified
- Four synthesis strategies documented
- Event system defined
- Security considerations added
- Three conformance levels established

---

## Appendix E: Contributing

The Khazar Protocol Specification is an open standard. Contributions are welcome:

1. **Suggest improvements** via GitHub issues
2. **Propose extensions** for community review
3. **Implement and test** in your own projects
4. **Share feedback** from real-world usage

Governance:
- Specification maintained by KhazarLLMs project
- Major changes require community review
- Extension registry open to all implementations

---

## Appendix F: Acknowledgments

The Khazar Protocol Specification was inspired by:
- Milorad Pavić's *Dictionary of the Khazar*
- RFC standards tradition
- W3C specification practices
- The multi-agent AI research community

Special thanks to all contributors and early adopters.

---

**End of Specification**

*This is a living document. Feedback and contributions are welcome.*
