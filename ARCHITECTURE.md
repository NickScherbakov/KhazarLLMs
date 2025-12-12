# KhazarLLMs Architecture

This document describes the architecture and design philosophy of KhazarLLMs.

## Core Concepts

### Agents
Agents are AI entities with distinct roles and personalities that form the creative ensemble.

### Orchestration
Manages how agents interact through different conversation modes (sequential, parallel, debate, consensus).

### LLM Client
Provider-agnostic interface supporting OpenAI, Anthropic, and Mock providers.

## Design Principles
- **Modularity**: Clear separation of concerns
- **Extensibility**: Easy to add new agents and modes
- **Composability**: Mix and match components
- **Testability**: Mock provider for testing

See full documentation in the repository.
