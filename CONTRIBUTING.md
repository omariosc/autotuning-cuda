# Contributing to Flamingo CUDA Autotuning System

Thank you for your interest in contributing! This project modernizes the exceptional original work of **Ben Spencer**, and we welcome contributions that enhance and extend his foundational design.

## Code of Conduct

This project adheres to a code of conduct that promotes respectful and inclusive collaboration. By participating, you agree to uphold these standards.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include configuration files** and error messages
4. **Specify your environment** (OS, Python version, CUDA version)

### Suggesting Features

1. **Use the feature request template**
2. **Explain the use case** and why it would be valuable
3. **Consider compatibility** with Ben Spencer's original design
4. **Discuss implementation approach** if you have ideas

### Contributing Code

#### Development Setup

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/flamingo-autotuner.git
cd flamingo-autotuner/Autotuning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev,docs,tui]"

# Set up pre-commit hooks
pre-commit install
```

#### Making Changes

1. **Create a branch** from main: `git checkout -b feature/my-feature`
2. **Follow coding standards**:
   - Use Black for formatting: `black .`
   - Sort imports with isort: `isort .`
   - Add type hints throughout
   - Follow existing patterns and conventions
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Run quality checks**:
   ```bash
   # Format and check code
   black .
   isort .
   mypy .
   flake8 .
   
   # Run tests
   pytest
   
   # Or run everything
   pre-commit run --all-files
   ```

#### Commit Guidelines

Use clear, descriptive commit messages:

```
type(scope): description

Longer explanation if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

#### Pull Request Process

1. **Ensure tests pass** and code quality checks succeed
2. **Update documentation** for any user-facing changes
3. **Fill out the PR template** completely
4. **Reference related issues** with "Fixes #123" or "Closes #123"
5. **Be responsive** to review feedback

## Contribution Guidelines

### Respecting Ben Spencer's Original Work

This project is built upon Ben Spencer's exceptional foundation. When contributing:

- **Preserve core algorithms**: Don't modify optimization logic without compelling reasons
- **Maintain design principles**: Follow the modular, extensible architecture Ben created
- **Ensure compatibility**: Existing configuration files should continue to work
- **Document changes**: Explain how changes relate to the original design
- **Add rather than replace**: Enhance functionality rather than replacing it

### Areas for Contribution

We welcome contributions in these areas:

#### High Priority
- **Testing**: Comprehensive test coverage for all modules
- **Documentation**: Examples, tutorials, and guides
- **Examples**: New demonstration programs and use cases
- **Plugin development**: Custom optimization algorithms and evaluators

#### Medium Priority
- **CLI enhancements**: Additional commands and interactive features
- **Visualization improvements**: Better plots and analysis tools
- **Performance optimizations**: Speed and memory improvements
- **Platform support**: Windows, macOS, different CUDA versions

#### Low Priority (Careful Consideration Required)
- **Core algorithm changes**: Only with strong justification
- **Configuration format changes**: Must maintain backward compatibility
- **Breaking API changes**: Generally discouraged

### Code Style

- **Type hints**: All functions and methods must have type annotations
- **Documentation**: Docstrings for all public functions and classes
- **Error handling**: Comprehensive error checking with meaningful messages
- **Testing**: Unit tests for new functionality, integration tests for workflows
- **Compatibility**: Support Python 3.10+ and maintain backward compatibility

### Testing Requirements

All contributions must include appropriate tests:

```bash
# Run specific test categories
pytest -m unit          # Fast unit tests
pytest -m integration   # Full workflow tests
pytest -m slow          # Long-running tests

# Run with coverage
pytest --cov=flamingo --cov=tuner
```

### Documentation Requirements

- **User-facing changes**: Update relevant documentation in `docs/`
- **New features**: Add examples and usage instructions
- **API changes**: Update docstrings and type hints
- **Configuration changes**: Update example config files

## Recognition

Contributors will be acknowledged in:
- **Contributors section** of README.md
- **Release notes** for significant contributions
- **Documentation credits** where appropriate

We maintain Ben Spencer's primary credit while recognizing all contributors who help modernize and enhance the system.

## Getting Help

- **Documentation**: Start with files in `docs/`
- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Create issues for bugs or feature requests
- **Code review**: We provide helpful feedback on pull requests

## Development Philosophy

This project aims to:
1. **Honor Ben Spencer's original vision** while modernizing for current Python practices
2. **Maintain backward compatibility** wherever possible
3. **Provide excellent documentation** and examples
4. **Foster a welcoming community** for researchers and developers
5. **Enable advanced optimization research** through extensible architecture

Thank you for contributing to the preservation and modernization of this valuable optimization tool!