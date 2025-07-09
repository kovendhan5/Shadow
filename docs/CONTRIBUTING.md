# Contributing to Shadow AI

Thank you for your interest in contributing to Shadow AI! This guide will help you get started.

## 🤝 How to Contribute

### Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? Please report it!
- ✨ **Feature Requests**: Have an idea? We'd love to hear it!
- 📖 **Documentation**: Help improve our docs
- 🧪 **Testing**: Help us test new features
- 💻 **Code**: Submit bug fixes or new features

### Before You Start

1. Check existing [issues](https://github.com/yourusername/shadow-ai/issues)
2. Read our [Code of Conduct](CODE_OF_CONDUCT.md)
3. Review this contributing guide

## 🚀 Getting Started

### 1. Fork & Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/yourusername/shadow-ai.git
cd shadow-ai
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Add your API keys for testing
# GEMINI_API_KEY=your_test_key_here
```

## 🔧 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 2. Make Changes

- Follow our coding standards
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run tests
python -m pytest test_shadow.py -v

# Run functionality tests
python test_functionality.py

# Test manually
python main.py --demo
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new voice command feature"
```

### 5. Push & Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📝 Coding Standards

### Python Style

- Follow PEP 8
- Use type hints where possible
- Write descriptive docstrings
- Keep functions small and focused

### Code Example

```python
def process_voice_command(audio_input: str) -> Dict[str, Any]:
    """
    Process voice command and return structured action data.

    Args:
        audio_input: Raw audio input from microphone

    Returns:
        Dictionary containing action type, parameters, and description

    Raises:
        ValueError: If audio input is invalid
    """
    if not audio_input or not audio_input.strip():
        raise ValueError("Empty audio input")

    # Process the command
    return parse_command(audio_input.strip().lower())
```

### File Structure

```
new_feature/
├── __init__.py
├── main_module.py
├── helpers.py
└── tests/
    └── test_main_module.py
```

## 🧪 Testing Guidelines

### Writing Tests

- Add tests for all new features
- Test edge cases and error conditions
- Use descriptive test names
- Mock external dependencies

### Test Example

```python
def test_voice_command_processing():
    """Test that voice commands are processed correctly"""
    # Arrange
    command = "open notepad"
    expected_action = "open_application"

    # Act
    result = process_voice_command(command)

    # Assert
    assert result['action'] == expected_action
    assert result['parameters']['app_name'] == 'notepad'
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_shadow.py

# Run with coverage
python -m pytest --cov=shadow_ai
```

## 📚 Documentation

### What to Document

- New features and APIs
- Configuration options
- Usage examples
- Breaking changes

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep README up to date

## 🐛 Bug Reports

### Good Bug Reports Include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages and logs

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**Steps to Reproduce**

1. Go to '...'
2. Click on '...'
3. Enter '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**

- OS: [e.g., Windows 11]
- Python: [e.g., 3.11.9]
- Shadow AI version: [e.g., 1.0.0]

**Additional Context**
Any other context about the problem.
```

## ✨ Feature Requests

### Good Feature Requests Include:

- Clear description of the feature
- Use case and motivation
- Possible implementation approach
- Examples of similar features

### Feature Request Template

```markdown
**Feature Description**
A clear description of what you want to happen.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How do you think this should work?

**Alternatives**
Any alternative solutions you've considered?

**Additional Context**
Any other context about the feature request.
```

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Steps

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create release tag
4. Update documentation

## 🏆 Recognition

Contributors are recognized in:

- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

## 📞 Getting Help

### Ways to Get Help

- 💬 [GitHub Discussions](https://github.com/yourusername/shadow-ai/discussions)
- 🐛 [Issues](https://github.com/yourusername/shadow-ai/issues)
- 📧 Email: maintainers@shadow-ai.com

### Questions?

Don't hesitate to ask! We're here to help.

## 🙏 Thank You

Thank you for contributing to Shadow AI! Your help makes this project better for everyone.

---

_This contributing guide is a living document. Feel free to suggest improvements!_
