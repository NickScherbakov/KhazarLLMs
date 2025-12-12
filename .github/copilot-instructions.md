# GitHub Copilot Instructions for KhazarLLMs

## Repository Purpose

**KhazarLLMs** is a system for collective creativity management using ensemble LLMs. This repository contains:
- LLM experiments and tools for multi-agent AI collaboration
- An ensemble orchestration framework inspired by Milorad Pavić's *Dictionary of the Khazar*
- Multiple AI agent personas with distinct creative roles working together
- Tools for sequential, parallel, debate, and consensus-based AI conversations

## Directory Structure

- `/khazar_llms` – Source code for models and pipelines
  - `/agents` – Agent framework and persona implementations  
  - `/orchestration` – Ensemble management and session control
  - `/utils` – LLM client abstraction and utilities
- `/tests` – Unit and integration tests
- `/docs` – Project documentation
- `/examples` – Example scripts demonstrating various use cases
- `/i18n` – Internationalization and localized documentation

## Coding Guidelines

- **Follow PEP8 for Python code** - Use standard Python style conventions
- **All new code must include unit tests in `/tests`** - Maintain test coverage with pytest
- **Update `/docs` if public APIs or logic change** - Keep documentation synchronized
- **Write clear, descriptive commit messages** - Follow conventional commit format

## Copilot Agent Tasks

GitHub Copilot is permitted and encouraged to:

- **Refactor code for clarity and efficiency** - Improve code structure and performance
- **Add missing docstrings and comments** - Document complex logic and public APIs
- **Write and improve tests** - Create comprehensive unit and integration tests
- **Suggest bug fixes and optimizations** - Identify and resolve issues
- **Automate repetitive tasks** - Create scripts for common operations (e.g., updating configs)
- **Generate initial documentation drafts** - Write documentation for new features

## Restrictions

GitHub Copilot should **NOT**:

- **Commit directly to the `main` branch** - Always use Pull Requests for code changes
- **Remove critical code or files without review** - Never delete production code without explicit approval
- **Never commit secrets, credentials, or private keys** - Keep API keys and sensitive data out of the repository

## PR Requirements

When creating Pull Requests:

- **PRs should reference related issue numbers** - Use "Fixes #N" or "Closes #N" in PR description
- **Use environment variables and `.env.example` for configuration** - Never hardcode API keys or credentials
  - Set up environment variables following the pattern in `.env.example`
  - Load variables using `python-dotenv` library
  - Keep actual API keys in `.env` (which is gitignored)
