# Copilot Coding Agent Instructions

Welcome to the `KhazarLLMs` repository!  
This guide provides best practices and instructions for GitHub Copilot Coding Agent and contributors.

---

## 1. Repository Purpose

This repository contains a system of collective creativity management of the ensemble LLM for KhazarAI.  
Main goals:
- Implementing novel LLM architectures
- Evaluating model performance
- Managing ensemble LLM interactions

---

## 2. Directory Structure

- `/src` – Source code for models and pipelines  
- `/data` – Datasets and data processing scripts  
- `/docs` – Project documentation  
- `/tests` – Unit and integration tests  
- `/configs` – Configuration files for experiments

---

## 3. Contribution Guidelines

- All code changes must be submitted via Pull Request (PR).
- PRs should reference related issue numbers.
- Write clear, descriptive commit messages.
- Follow [PEP8](https://peps.python.org/pep-0008/) (for Python) or relevant language style guide.
- All new code must include unit tests in `/tests`.
- Update `/docs` if public APIs or logic change.

---

## 4. Automated Workflows

- **CI/CD** is configured with GitHub Actions (`.github/workflows/`).  
  On each PR:
  - Run lint checks
  - Execute all tests
  - Build documentation

---

## 5. Copilot Coding Agent Tasks

Copilot is permitted and encouraged to:
- Refactor code for clarity and efficiency.
- Add missing docstrings and comments.
- Write and improve tests.
- Suggest bug fixes and optimizations.
- Automate repetitive tasks (e.g., updating configs).
- Generate initial documentation drafts.

Copilot should NOT:
- Commit directly to the `main` branch (use PRs).
- Remove critical code or files without review.

---

## 6. Sensitive Information

- Never commit secrets, credentials, or private keys.
- Use environment variables and `.env.example` for configuration.

---

## 7. Issue & PR Templates

- Use the provided issue and PR templates in `.github/` for consistency.

---

## 8. Helpful Resources

- [Best practices for Copilot Coding Agent](https://gh.io/copilot-coding-agent-tips)
- Project Wiki
- Contribution Guide

---

## 9. Contact

For questions, open an issue and tag @NickScherbakov.

---

Thank you for contributing to KhazarLLMs!
