# Contributing to KhazarLLMs

Thank you for your interest in contributing to KhazarLLMs! This project explores the creative potential of ensemble AI systems, and we welcome contributions that expand this vision.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/NickScherbakov/KhazarLLMs.git
cd KhazarLLMs
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest tests/
```

## Ways to Contribute

### 1. New Agent Personas

Add new agent types with unique creative perspectives:

- Implement in `khazar_llms/agents/personas.py`
- Extend the `Agent` base class
- Define a unique system prompt
- Implement the `respond()` method
- Add tests in `tests/test_agents.py`

### 2. Orchestration Modes

Create new conversation patterns:

- Add to `ConversationMode` enum in `ensemble.py`
- Implement the mode logic in `Ensemble.run_iteration()`
- Add examples demonstrating the new mode
- Document the mode's behavior

### 3. LLM Provider Support

Add support for new LLM providers:

- Implement a new provider class in `utils/llm_client.py`
- Extend `BaseLLMProvider`
- Add provider to `LLMClient.__init__()`
- Test with the provider's API

### 4. Examples and Use Cases

Share creative applications:

- Create example scripts in `examples/`
- Document interesting use cases
- Share session outputs demonstrating creative results

### 5. Documentation

Improve clarity and accessibility:

- Fix typos and clarify explanations
- Add code comments where helpful
- Create tutorials or guides
- Translate documentation

## Code Style

- Follow PEP 8 style guidelines
- Use Black for formatting: `black khazar_llms/`
- Run flake8 for linting: `flake8 khazar_llms/`
- Write docstrings for public functions and classes
- Keep functions focused and composable

## Testing

- Write tests for new features
- Maintain test coverage
- Use pytest and pytest-asyncio
- Test with mock provider before real APIs

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Update documentation
7. Submit a pull request

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Celebrate creativity and experimentation

## Questions?

Open an issue for discussion or to ask questions. We're here to help!

---

*"Like the Khazar Dictionary itself, this project is a collaborative work - many voices contributing to a shared creative vision."*
