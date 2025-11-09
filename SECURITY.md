# Security Policy

## Supported Versions

We actively support the following versions of KhazarLLMs:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security vulnerabilities through one of the following methods:

1. **GitHub Security Advisories** (Preferred)
   - Go to https://github.com/NickScherbakov/KhazarLLMs/security/advisories
   - Click "Report a vulnerability"
   - Fill in the details

2. **Email**
   - Send an email to: nick@example.com
   - Use subject line: "[SECURITY] KhazarLLMs Vulnerability Report"

### What to Include

Please include the following information in your report:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** of the vulnerability
- **Affected versions** (if known)
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next regular release

## Security Best Practices

### For Users

When using KhazarLLMs:

1. **API Keys**
   - Never commit API keys to version control
   - Use environment variables or `.env` files
   - Keep `.env` files out of version control (in `.gitignore`)
   - Rotate API keys regularly

2. **Dependencies**
   - Keep dependencies up to date
   - Run `pip install --upgrade -r requirements.txt` regularly
   - Monitor for security advisories

3. **Data Privacy**
   - Be aware that prompts and responses are sent to LLM providers
   - Don't include sensitive information in prompts
   - Review your LLM provider's privacy policy

4. **Network Security**
   - Use HTTPS for API calls (handled by default)
   - Consider using a firewall or VPN for sensitive work

### For Contributors

When contributing code:

1. **Code Review**
   - All code must be reviewed before merging
   - Security-sensitive changes require extra scrutiny
   - Use automated security scanning tools

2. **Dependency Management**
   - Pin dependency versions in `requirements.txt`
   - Review dependency security advisories
   - Keep dependencies minimal and well-maintained

3. **Input Validation**
   - Validate all user inputs
   - Sanitize data before processing
   - Use type hints and pydantic for validation

4. **Secrets Management**
   - Never hardcode secrets
   - Use environment variables
   - Add security checks in CI/CD

## Known Security Considerations

### API Key Exposure

- **Risk**: API keys could be accidentally committed
- **Mitigation**: `.env` is in `.gitignore`, pre-commit hooks recommended
- **Detection**: GitHub secret scanning enabled

### Prompt Injection

- **Risk**: Malicious prompts could manipulate agent behavior
- **Mitigation**: Input validation, agent system prompts include safety guidelines
- **Status**: Ongoing monitoring

### Dependency Vulnerabilities

- **Risk**: Third-party dependencies may have vulnerabilities
- **Mitigation**: Regular dependency updates, automated scanning
- **Tools**: Dependabot enabled, regular security audits

### LLM Provider Security

- **Risk**: Data sent to LLM providers could be stored or logged
- **Mitigation**: User responsibility to review provider policies
- **Documentation**: Privacy considerations documented in README

## Security Updates

Security updates will be:

1. Released as soon as possible after discovery
2. Documented in release notes
3. Announced through GitHub Security Advisories
4. Tagged with semantic versioning (patch for security fixes)

## Disclosure Policy

We follow **coordinated disclosure**:

1. Vulnerability reported privately
2. Fix developed and tested
3. Security advisory published
4. Fix released
5. Public disclosure after fix is available

## Security Tools

We use the following tools to maintain security:

- **GitHub Dependabot**: Automatic dependency updates
- **GitHub Code Scanning**: Static analysis
- **Bandit**: Python security linting
- **flake8**: Code quality and security checks
- **pytest**: Security-focused test cases

## Compliance

KhazarLLMs aims to follow:

- **OWASP Top 10**: Web application security risks
- **CWE Top 25**: Most dangerous software weaknesses
- **NIST Guidelines**: Secure software development

## Contact

For security concerns:
- **Security Issues**: Use GitHub Security Advisories or email
- **General Questions**: Open a regular GitHub issue
- **Urgent Matters**: Email with [URGENT] in subject

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities. Recognized contributors will be:

- Credited in release notes (with permission)
- Listed in SECURITY.md acknowledgments
- Thanked in the project community

---

Thank you for helping keep KhazarLLMs and its users secure! 🔒
