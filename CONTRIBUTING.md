# 🤝 Contributing to Chatbot SI

First off, thank you for considering contributing to Chatbot SI! It's people like you that make this chatbot better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Project Structure](#project-structure)

## 📜 Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this code.

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:

1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**

- OS: [e.g. Windows 11]
- Python Version: [e.g. 3.11]
- MySQL Version: [e.g. 8.0]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Current behavior vs. proposed behavior**
- **Why this enhancement would be useful**
- **Possible implementation approach**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request**

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/chatbot_SI.git
cd chatbot_SI
```

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

### 3. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

### 4. Setup Database

```bash
# Create test database
mysql -u root -p -e "CREATE DATABASE chatbot_si_dev;"

# Copy env file
cp .config/.env.example .env

# Update .env with development database
MYSQL_DATABASE=chatbot_si_dev

# Run migration
python scripts/migration_script.py
```

### 5. Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_chatbot_filtering.py
```

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commit messages are clear

### PR Title Format

```
type(scope): short description

Examples:
feat(chatbot): add sentiment analysis
fix(admin): resolve login timeout issue
docs(readme): update installation guide
style(ui): improve responsive design
refactor(core): optimize database queries
test(filters): add topic filtering tests
```

### PR Description Template

```markdown
## Description

Brief description of changes made.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

Describe how you tested your changes.

## Screenshots

If applicable, add screenshots.

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
```

## 💻 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

```python
# Good: Clear variable names
def calculate_response_confidence(intent_score, topic_score):
    return (intent_score + topic_score) / 2

# Bad: Unclear variable names
def calc(x, y):
    return (x + y) / 2
```

### File Organization

```python
# Import order:
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Third-party
import flask
from flask import Flask, request
import mysql.connector

# 3. Local imports
from core.database import Database
from models.admin_api import AdminAPI
```

### Code Formatting

```bash
# Use Black for formatting (line length 88)
black .

# Use flake8 for linting
flake8 .
```

### Naming Conventions

- **Files:** `lowercase_with_underscores.py`
- **Classes:** `PascalCase`
- **Functions:** `snake_case`
- **Constants:** `UPPER_CASE`
- **Variables:** `snake_case`

### Documentation

```python
def process_compound_question(question: str, intents: list) -> dict:
    """
    Process a compound question containing multiple intents.

    Args:
        question (str): The user's compound question
        intents (list): List of detected intents with confidence scores

    Returns:
        dict: Combined response with metadata

    Example:
        >>> process_compound_question(
        ...     "Apa itu SI dan berapa biayanya?",
        ...     [{'tag': 'definisi_si'}, {'tag': 'biaya'}]
        ... )
        {'response': '...', 'intents': [...]}
    """
    # Implementation
    pass
```

### Comments

```python
# Good: Explain WHY, not WHAT
# Calculate weighted average to prioritize recent responses
weighted_score = (recent_score * 0.7) + (overall_score * 0.3)

# Bad: Just describes what code does
# Multiply recent_score by 0.7 and add to overall_score times 0.3
weighted_score = (recent_score * 0.7) + (overall_score * 0.3)
```

## 📂 Project Structure

Understanding the project structure helps you contribute effectively:

```
chatbot_SI/
├── api/              # Flask route handlers
│   ├── chat_routes.py
│   └── admin_routes.py
├── core/             # Core chatbot logic
│   ├── database.py
│   ├── ml_model.py
│   ├── groq_client.py
│   ├── filters.py
│   └── response_handler.py
├── models/           # Database models
├── utils/            # Utility functions
├── static/           # Frontend files
├── tests/            # Test files
└── docs/             # Documentation
```

### Where to Make Changes

**Adding new features:**

- Chatbot logic → `core/`
- API endpoints → `api/`
- Database models → `models/`
- Frontend → `static/`

**Fixing bugs:**

- Check logs in `logs/` first
- Related files based on error trace

**Improving docs:**

- General docs → `docs/`
- Installation → `INSTALLATION.md`
- API docs → `docs/api/` (create if needed)

## ✅ Testing Guidelines

### Writing Tests

```python
# tests/test_your_feature.py
import pytest
from core.your_module import your_function

def test_your_function_basic():
    """Test basic functionality."""
    result = your_function("input")
    assert result == "expected_output"

def test_your_function_edge_case():
    """Test edge cases."""
    result = your_function("")
    assert result is None
```

### Test Coverage

Aim for:

- **Core modules:** 80%+ coverage
- **Critical paths:** 90%+ coverage
- **New features:** 100% coverage

```bash
# Check coverage
pytest --cov=core --cov-report=html tests/
```

## 🐛 Debugging Tips

### Enable Debug Mode

```env
# .env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Check Logs

```bash
# Application logs
tail -f logs/app.log

# Security logs
tail -f logs/security.log
```

### Use Python Debugger

```python
# Add to your code
import pdb; pdb.set_trace()
```

## 📝 Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples

```bash
feat(chatbot): add multi-intent detection

- Implemented compound question parsing
- Added intent combination logic
- Updated response handler

Closes #123
```

## 🎉 Recognition

Contributors will be:

- Listed in project README
- Mentioned in release notes
- Given credit in commit history

## 📞 Getting Help

- **Questions:** [GitHub Discussions](https://github.com/your-username/chatbot_SI/discussions)
- **Chat:** [Join our Discord](#) (if available)
- **Email:** your.email@example.com

## 📚 Additional Resources

- [Python Style Guide](https://pep8.org/)
- [Flask Best Practices](https://flask.palletsprojects.com/en/latest/patterns/)
- [Git Workflow](https://guides.github.com/introduction/flow/)

---

## 🙏 Thank You!

Your contributions make this project better. We appreciate your time and effort!

**Happy Coding!** 🚀
