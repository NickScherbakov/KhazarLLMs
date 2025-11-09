# Changelog

All notable changes to KhazarLLMs will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD workflows
- Code quality checks and automated testing
- Issue and PR templates
- Copilot Coding Agent instructions
- Security policy and disclosure process
- CODEOWNERS file for review automation

## [0.1.0] - 2025-11-09

### Added
- Initial release of KhazarLLMs
- Base agent framework with memory and context management
- 7 distinct agent personas (Dreamer, Critic, Synthesizer, Philosopher, Rebel, Architect, Poet)
- Ensemble orchestration system with 4 conversation modes
- Sequential, Parallel, Debate, and Consensus conversation patterns
- Multi-provider LLM support (OpenAI, Anthropic, Mock)
- Command-line interface (CLI) for easy usage
- Python API for programmatic access
- Session management with JSON and text output
- Creative session tracking with metadata and timing
- Mock provider for testing without API costs
- Environment variable configuration with `.env` support
- Comprehensive documentation (README, CONTRIBUTING, ARCHITECTURE, USAGE_GUIDE)
- Example scripts demonstrating various use cases
- Full test suite with pytest and pytest-asyncio (15 tests)
- Type hints throughout codebase
- Async/await patterns for efficient LLM interactions

### Documentation
- README.md with project overview and quick start
- CONTRIBUTING.md with contribution guidelines
- PROJECT_SUMMARY.md with complete project overview
- docs/ARCHITECTURE.md with system design principles
- docs/USAGE_GUIDE.md with complete usage documentation
- Example scripts with detailed comments

### Testing
- Unit tests for agent creation and behavior
- Integration tests for ensemble orchestration
- LLM client provider tests
- Mock provider for testing without API costs
- Async test support with pytest-asyncio

---

## Version History

### Version Format
- **Major.Minor.Patch** (e.g., 1.2.3)
- **Major**: Breaking changes
- **Minor**: New features (backwards compatible)
- **Patch**: Bug fixes and minor improvements

### Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

## Links
- [0.1.0]: https://github.com/NickScherbakov/KhazarLLMs/releases/tag/v0.1.0
- [Unreleased]: https://github.com/NickScherbakov/KhazarLLMs/compare/v0.1.0...HEAD
