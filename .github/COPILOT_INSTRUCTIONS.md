# Copilot Coding Agent Instructions

Welcome to the `KhazarLLMs` repository!  
This guide provides best practices and instructions for GitHub Copilot Coding Agent and contributors.

---

## 1. Repository Purpose

This repository contains **a system for collective creativity management using ensemble LLMs**, inspired by Milorad Pavić's *Dictionary of the Khazar* and its exploration of multiple perspectives.

**Main goals:**
- Orchestrate ensembles of AI agents with distinct personalities and creative roles
- Enable diverse AI perspectives to collaborate on creative tasks
- Provide flexible conversation modes (sequential, parallel, debate, consensus)
- Support multiple LLM providers (OpenAI, Anthropic, Mock)
- Offer both CLI and Python API interfaces for accessibility

---

## 2. Directory Structure

- `/khazar_llms` – Core source code for agents and orchestration
  - `/agents` – Agent framework and persona implementations
  - `/orchestration` – Ensemble management and session control
  - `/utils` – LLM client abstraction and utilities
- `/tests` – Unit and integration tests (pytest + pytest-asyncio)
- `/docs` – Project documentation (ARCHITECTURE.md, USAGE_GUIDE.md)
- `/examples` – Demonstration scripts for various use cases
- `.github/` – GitHub configuration (workflows, templates)

---

## 3. Contribution Guidelines

### Code Standards
- Follow **PEP 8** style guidelines for Python code
- Use **Black** for automatic formatting (line length: 100)
- Run **flake8** for linting before committing
- Use **type hints** for all function signatures
- Write **docstrings** for all public classes and functions
- Use **async/await** patterns for LLM interactions

### Git Workflow
- All code changes must be submitted via **Pull Request (PR)**
- PRs should reference related issue numbers (e.g., "Fixes #42")
- Write **clear, descriptive commit messages**
- Never commit directly to the `main` branch
- Keep PRs focused on a single feature or fix

### Testing Requirements
- All new code must include **unit tests** in `/tests`
- Maintain or improve test coverage
- Use **pytest** and **pytest-asyncio** for async testing
- Test with **mock provider** before testing with real APIs
- Run full test suite before submitting PR: `pytest tests/`

### Documentation
- Update `/docs` if public APIs or architecture changes
- Add docstrings to all new classes and methods
- Update README.md for new features
- Create examples for significant new functionality

---

## 4. Automated Workflows

**CI/CD** is configured with GitHub Actions (`.github/workflows/`):

On each Pull Request:
- ✅ Run linting checks (flake8)
- ✅ Execute full test suite (pytest)
- ✅ Verify code formatting (black --check)
- ✅ Check for Python version compatibility (3.8+)

On merge to `main`:
- 📦 Build package
- 📚 Generate documentation
- 🏷️ Tag releases (if version updated)

---

## 5. Copilot Coding Agent Tasks

### ✅ Copilot IS Permitted and Encouraged To:

1. **Code Quality Improvements**
   - Refactor code for clarity and efficiency
   - Add missing docstrings and type hints
   - Improve error handling and edge cases
   - Optimize async/await patterns

2. **Testing**
   - Write comprehensive unit tests
   - Add integration tests for new features
   - Improve test coverage
   - Create test fixtures and utilities

3. **New Features**
   - Implement new agent personas with unique characteristics
   - Add new orchestration modes
   - Support additional LLM providers
   - Create new conversation patterns

4. **Documentation**
   - Generate initial documentation drafts
   - Add code comments for complex logic
   - Create usage examples
   - Update API documentation

5. **Automation**
   - Create GitHub Actions workflows
   - Add pre-commit hooks
   - Generate boilerplate code
   - Automate repetitive tasks

6. **Bug Fixes**
   - Fix identified bugs with tests
   - Improve error messages
   - Handle edge cases
   - Resolve deprecation warnings

### ❌ Copilot Should NOT:

- ❌ Commit directly to the `main` branch (always use PRs)
- ❌ Remove critical code or files without explicit review
- ❌ Change core architecture without discussion
- ❌ Commit API keys, credentials, or secrets
- ❌ Break existing tests without fixing them
- ❌ Remove or weaken type hints
- ❌ Ignore linting or formatting standards

---

## 6. Sensitive Information & Security

- **Never commit** secrets, API keys, credentials, or private keys
- Use **environment variables** for configuration
- Reference `.env.example` for environment setup
- Use `python-dotenv` for loading environment variables
- Keep API keys in `.env` (which is gitignored)
- Sanitize any logs or outputs that might contain sensitive data

### Environment Variables
```bash
# Required for real LLM usage
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Optional configuration
LOG_LEVEL=INFO
DEFAULT_PROVIDER=mock
```

---

## 7. Code Architecture Principles

### Agent Design
- Extend the `Agent` base class from `khazar_llms/agents/base.py`
- Each agent persona should have a **unique system prompt**
- Use appropriate **temperature settings** for agent personality
- Implement the `respond()` method with proper async patterns
- Maintain agent memory for context-aware conversations

### Orchestration Patterns
- Support multiple conversation modes in `Ensemble` class
- Keep orchestration logic separate from agent logic
- Use `CreativeSession` for managing complete creative workflows
- Store session metadata (timing, iterations, results)

### LLM Client Abstraction
- Maintain provider-agnostic interfaces
- Support multiple providers through common API
- Use mock provider for testing without API costs
- Handle rate limiting and API errors gracefully

### Async/Await Best Practices
- Use `async def` for all I/O operations
- Await all LLM API calls
- Use `asyncio.gather()` for parallel operations
- Handle async exceptions properly

---

## 8. Adding New Features

### Creating a New Agent Persona

1. Add to `khazar_llms/agents/personas.py`:
```python
class YourAgent(Agent):
    """Brief description of the agent's role."""
    
    def __init__(self, provider: str = "mock", api_key: Optional[str] = None):
        system_prompt = "Your unique system prompt defining the agent's personality"
        super().__init__(
            name="YourAgentName",
            system_prompt=system_prompt,
            temperature=0.7,  # Adjust based on desired creativity
            provider=provider,
            api_key=api_key,
        )
```

2. Add tests in `tests/test_agents.py`
3. Update documentation in `docs/USAGE_GUIDE.md`
4. Add example usage in `examples/`

### Adding a New Conversation Mode

1. Add to `ConversationMode` enum in `orchestration/ensemble.py`
2. Implement logic in `Ensemble.run_iteration()`
3. Document behavior in `docs/ARCHITECTURE.md`
4. Create example demonstrating the mode
5. Add tests in `tests/test_ensemble.py`

### Supporting a New LLM Provider

1. Create provider class in `utils/llm_client.py`:
```python
class NewProvider(BaseLLMProvider):
    async def generate(self, messages, temperature, max_tokens):
        # Implementation
        pass
```

2. Register in `LLMClient.__init__()`
3. Update documentation
4. Add provider-specific tests

---

## 9. Testing Guidelines

### Test Structure
```python
import pytest
from khazar_llms.agents.personas import DreamerAgent

@pytest.mark.asyncio
async def test_dreamer_agent_creation():
    """Test that DreamerAgent can be created with mock provider."""
    agent = DreamerAgent(provider="mock")
    assert agent.name == "Dreamer"
    assert agent.temperature == 0.95
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=khazar_llms tests/

# Run in verbose mode
pytest -v tests/
```

### Test Categories
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Async Tests**: Use `@pytest.mark.asyncio` decorator
- **Mock Tests**: Use mock provider to avoid API costs

---

## 10. Issue & PR Templates

### Issue Template
When creating issues, include:
- Clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs. actual behavior
- Relevant code snippets or error messages
- Environment details (Python version, OS)

### PR Template
When submitting PRs, include:
- Reference to related issue(s)
- Description of changes made
- Testing performed
- Breaking changes (if any)
- Documentation updates
- Screenshots/examples (if applicable)

---

## 11. Development Workflow

### Initial Setup
```bash
# Clone repository
git clone https://github.com/NickScherbakov/KhazarLLMs.git
cd KhazarLLMs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-asyncio black flake8

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

### Making Changes
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# ... edit files ...
pytest tests/

# Format and lint
black khazar_llms/
flake8 khazar_llms/

# Commit and push
git add .
git commit -m "Add feature: description"
git push origin feature/your-feature-name

# Open PR on GitHub
```

---

## 12. Helpful Resources

### Project Documentation
- [README.md](../README.md) - Project overview and quick start
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md) - Complete project summary
- [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) - System architecture
- [docs/USAGE_GUIDE.md](../docs/USAGE_GUIDE.md) - Complete usage guide

### External Resources
- [GitHub Copilot Coding Agent Tips](https://gh.io/copilot-coding-agent-tips)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Async/Await Tutorial](https://realpython.com/async-io-python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)

### Key Dependencies
- **anthropic** - Anthropic Claude API client
- **openai** - OpenAI API client
- **pydantic** - Data validation and settings management
- **python-dotenv** - Environment variable management
- **rich** - Terminal output formatting
- **pytest** - Testing framework
- **pytest-asyncio** - Async testing support

---

## 13. Philosophy & Design Principles

### The Khazar Spirit
This project is inspired by Milorad Pavić's *Dictionary of the Khazar*, which tells stories through multiple perspectives. Similarly:
- **Multiple Voices**: Embrace diverse AI perspectives
- **Collective Creativity**: Solutions emerge from dialogue, not monologue
- **Polyphonic Structure**: Many agents working together, not one
- **Emergent Insight**: Truth appears through synthesis of perspectives

### Code Design Principles
- **Modularity**: Keep components focused and composable
- **Extensibility**: Easy to add new agents, modes, providers
- **Clarity**: Code should be readable and well-documented
- **Testability**: All code should be testable
- **Async-First**: Use async patterns for I/O operations
- **Provider Agnostic**: Don't lock into a single LLM provider

---

## 14. Common Tasks & Commands

### Quick Reference
```bash
# Run CLI
python -m khazar_llms.cli info
python -m khazar_llms.cli list-agents
python -m khazar_llms.cli create-task "Your task"

# Run examples
python examples/basic_ensemble.py
python examples/parallel_debate.py

# Testing
pytest tests/
pytest tests/test_agents.py -v
pytest --cov=khazar_llms tests/

# Code formatting
black khazar_llms/
black --check khazar_llms/  # Check without modifying

# Linting
flake8 khazar_llms/

# Install in development mode
pip install -e .
```

---

## 15. Contact & Support

### Getting Help
- 📝 **Open an issue** for bugs, feature requests, or questions
- 💬 **Tag @NickScherbakov** for urgent matters
- 📚 **Check documentation** in `/docs` first
- 🔍 **Search existing issues** before creating new ones

### Community
- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Celebrate creativity and experimentation

---

## 16. Version Information

- **Current Version**: 0.1.0
- **Python Version**: >=3.8
- **License**: MIT
- **Repository**: https://github.com/NickScherbakov/KhazarLLMs

---

## 17. Quick Checklist for PRs

Before submitting a Pull Request:

- [ ] Tests pass: `pytest tests/`
- [ ] Code formatted: `black khazar_llms/`
- [ ] Linting clean: `flake8 khazar_llms/`
- [ ] Type hints added to new code
- [ ] Docstrings added to new functions/classes
- [ ] Tests written for new functionality
- [ ] Documentation updated (if needed)
- [ ] No secrets or API keys committed
- [ ] PR description complete
- [ ] Related issue(s) referenced

---

Thank you for contributing to KhazarLLMs! 🌟

*"Like the Khazar Dictionary itself, this project is a collaborative work - many voices contributing to a shared creative vision."*
