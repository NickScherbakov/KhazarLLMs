# Quick Reference Card

## 🚀 For Copilot Coding Agent

### Must Read First
📖 `.github/COPILOT_INSTRUCTIONS.md` - Your comprehensive guide

### Key Guidelines
✅ Always use PRs, never commit to `main`  
✅ Follow PEP 8 and use Black (line length: 100)  
✅ Write tests for all new code  
✅ Add type hints and docstrings  
✅ Use async/await for LLM calls  

### Before Submitting
```bash
black khazar_llms/ tests/
flake8 khazar_llms/ tests/
pytest tests/
```

## 👨‍💻 For Contributors

### Getting Started
```bash
git clone https://github.com/NickScherbakov/KhazarLLMs.git
cd KhazarLLMs
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Development Loop
```bash
# 1. Create branch
git checkout -b feature/your-feature

# 2. Make changes
# ... edit files ...

# 3. Format & test
black khazar_llms/
pytest tests/

# 4. Commit & push
git add .
git commit -m "Add: description"
git push origin feature/your-feature

# 5. Open PR on GitHub
```

### Adding New Agent
```python
class YourAgent(Agent):
    def __init__(self, provider="mock", api_key=None):
        super().__init__(
            name="YourAgent",
            system_prompt="Your unique prompt",
            temperature=0.7,
            provider=provider,
            api_key=api_key,
        )
```

## 🔧 Common Commands

### Testing
```bash
pytest tests/              # Run all tests
pytest tests/test_agents.py  # Specific file
pytest -v                  # Verbose
pytest --cov=khazar_llms   # With coverage
```

### Code Quality
```bash
black khazar_llms/         # Format
black --check khazar_llms/ # Check only
flake8 khazar_llms/        # Lint
mypy khazar_llms/          # Type check
```

### CLI Usage
```bash
python -m khazar_llms.cli info
python -m khazar_llms.cli list-agents
python -m khazar_llms.cli create-task "Your task"
python -m khazar_llms.cli --mode parallel --agents dreamer critic create-task "Task"
```

## 📋 Templates

### Bug Report
Use: `.github/ISSUE_TEMPLATE/bug_report.md`

### Feature Request
Use: `.github/ISSUE_TEMPLATE/feature_request.md`

### Pull Request
Auto-populated from: `.github/pull_request_template.md`

## 🔐 Security

### Reporting Vulnerabilities
❌ DON'T create public issues  
✅ DO use GitHub Security Advisories  
✅ DO email: nick@example.com  

### Best Practices
- Never commit API keys
- Use `.env` for secrets
- Keep dependencies updated
- Review SECURITY.md

## 🤖 Automated Checks

Every PR runs:
- ✅ Black formatting
- ✅ flake8 linting
- ✅ mypy type checking
- ✅ bandit security scan
- ✅ pytest test suite
- ✅ Multi-version Python (3.8-3.11)

## 📚 Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `CONTRIBUTING.md` | How to contribute |
| `SECURITY.md` | Security policy |
| `CHANGELOG.md` | Version history |
| `.github/COPILOT_INSTRUCTIONS.md` | Copilot guide |
| `docs/ARCHITECTURE.md` | System design |
| `docs/USAGE_GUIDE.md` | Usage documentation |

## 🎯 Project Structure

```
khazar_llms/
├── agents/         # Agent framework & personas
├── orchestration/  # Ensemble & session management
└── utils/          # LLM client & utilities

tests/              # Test suite
examples/           # Usage examples
docs/               # Documentation
```

## 🏷️ Version Tags

```bash
# Create release
git tag -a v0.2.0 -m "Release 0.2.0"
git push origin v0.2.0

# This triggers:
# - Package build
# - GitHub release
# - PyPI publish (if configured)
```

## 🆘 Need Help?

1. Read `.github/COPILOT_INSTRUCTIONS.md`
2. Check existing issues
3. Review documentation in `docs/`
4. Open a new issue with template

## 🔗 Quick Links

- [Repository](https://github.com/NickScherbakov/KhazarLLMs)
- [Issues](https://github.com/NickScherbakov/KhazarLLMs/issues)
- [Pull Requests](https://github.com/NickScherbakov/KhazarLLMs/pulls)
- [Actions](https://github.com/NickScherbakov/KhazarLLMs/actions)

---

**Keep this card handy for quick reference!**

*"Like the Khazar Dictionary - many perspectives, one vision."*
