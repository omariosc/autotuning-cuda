# Flamingo CUDA Autotuning System - Developer Guide

**Version 1.0.0 (Python 3.10+ Modernized)**

## Credits and Acknowledgments

This project is built upon the exceptional foundational work of **Ben Spencer**, who designed and implemented the original Python 2.5+ autotuning system. His innovative algorithms, comprehensive architecture, and thoughtful design patterns form the core of this modernized version.

**Original Author**: Ben Spencer  
**Python 3 Modernization**: Claude Code (Anthropic)  
**Conversion Type**: Complete architectural modernization to Python 3.10+

## Project Overview

The Flamingo CUDA Autotuning System automatically finds optimal configurations for CUDA programs through intelligent parameter space exploration. This modernized version maintains Ben Spencer's core algorithmic innovations while adding contemporary Python development practices and tools.

## Architecture Overview

### Core Components (Ben Spencer's Original Design)

The system architecture follows Ben Spencer's well-designed modular approach:

#### Legacy Core (`tuner/` directory)

- **`tune.py`**: Main orchestration (converted to Python 3)
- **`optimisation.py`**: Core optimization algorithms
- **`evaluator.py`**: Test execution and measurement
- **`vartree.py`**: Parameter space representation
- **`tune_conf.py`**: Configuration file parsing
- **`output.py`**: Logging and output management

#### Modern Framework (`flamingo/` directory)

- **`cli/`**: Rich CLI interface with Typer and Rich
- **`core/`**: Modern wrappers for core functionality
- **`plugins/`**: Extensible plugin architecture
- **`migration/`**: Python 2 to 3 conversion tools
- **`tui/`**: Terminal User Interface components

### File Structure

```bash
flamingo-autotuner/
├── README.md                     # Main documentation  
├── docs/                        # Comprehensive documentation
│
└── Autotuning/                  # Main codebase directory
    ├── pyproject.toml           # Modern dependency management
    ├── Dockerfile               # Multi-stage container builds
    ├── docker-compose.yml       # Full stack deployment
    │
    ├── flamingo/                # Modern Python 3 framework
    │   ├── __init__.py
    │   ├── cli/                     # Rich CLI interface
    │   │   ├── main.py             # CLI entry point with Typer
    │   │   ├── themes.py           # Fire-inspired color themes
    │   │   └── utils.py            # CLI utilities
    │   ├── core/                   # Core system wrappers
    │   │   ├── autotuner.py        # Main system interface
    │   │   └── config.py           # Modern configuration handling
    │   ├── plugins/                # Plugin architecture
    │   │   ├── interface.py        # Plugin interfaces
    │   │   ├── manager.py          # Plugin lifecycle management
    │   │   ├── registry.py         # Plugin registration
    │   │   └── builtin/            # Built-in plugins
    │   ├── migration/              # Python 2 to 3 migration tools
    │   │   ├── converter.py        # Configuration converter
    │   │   └── analyzer.py         # Code analysis tools
    │   └── tui/                    # Terminal User Interface
    │       └── app.py              # TUI application
    │
    ├── tuner/                      # Ben Spencer's original core (Python 3 converted)
    │   ├── tune.py                 # Main entry point
    │   ├── optimisation.py         # Optimization algorithms
    │   ├── optimisation_bf.py      # Brute force optimizer
    │   ├── evaluator.py            # Test evaluation system
    │   ├── vartree.py              # Variable tree representation
    │   ├── vartree_parser.py       # Variable tree parser
    │   ├── tune_conf.py            # Configuration parsing
    │   ├── output.py               # Output management
    │   ├── helpers.py              # Utility functions
    │   └── test_evaluations.py     # Testing framework
    │
    ├── examples/                   # Demonstration programs
    │   ├── hello/                  # Simple compilation example
    │   ├── matrix/                 # Matrix multiplication
    │   ├── laplace3d/              # CUDA 3D Laplace solver
    │   ├── looping/                # Loop parameter tuning
    │   └── matlab/                 # MATLAB optimization
    │
    ├── utilities/                  # Analysis tools (Ben Spencer's design)
    │   ├── common.py               # CSV reading helpers
    │   ├── output_gnuplot.py       # Gnuplot script generation
    │   ├── output_screen.py        # Matplotlib visualization
    │   └── parameter_importance.py # Parameter analysis
    │
    └── tests/                      # Comprehensive test suite
        ├── unit/                   # Unit tests
        ├── integration/            # Integration tests
        └── fixtures/               # Test data
```

## Development Setup

### Prerequisites

- **Python 3.10+** (originally Python 2.5)
- **CUDA toolkit** (for CUDA examples)
- **Docker** (optional, for containerized development)
- **Git** for version control

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd flamingo-autotuner/Autotuning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev,docs,tui]"

# Set up pre-commit hooks for code quality
pre-commit install
```

### Development Dependencies

The `pyproject.toml` includes comprehensive development tools:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "isort>=5.12",
    "mypy>=1.0",
    "flake8>=6.0",
    "pre-commit>=3.0"
]
```

## Code Quality Standards

### Type Hints

All code includes comprehensive type hints following PEP 484:

```python
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

def process_config(
    config_path: Path,
    variables: Dict[str, List[str]],
    max_tests: Optional[int] = None
) -> Dict[str, Any]:
    """Process configuration with full type safety."""
    pass
```

### Code Formatting

- **Black**: Automatic code formatting
- **isort**: Import statement organization
- **Flake8**: Linting and style checking
- **MyPy**: Static type checking

```bash
# Format code
black .
isort .

# Check types
mypy .

# Lint code
flake8 .

# Run all quality checks
pre-commit run --all-files
```

### Error Handling

Modern exception handling with custom exception types:

```python
class FlamingoError(Exception):
    """Base exception for Flamingo errors."""
    pass

class ConfigurationError(FlamingoError):
    """Configuration parsing or validation error."""
    pass

# Usage with context managers
try:
    with open(config_path) as f:
        config = load_config(f)
except ConfigurationError as e:
    logger.error(f"Configuration error: {e}")
    raise
```

## Testing Framework

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=flamingo --cov=tuner --cov=utilities

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m slow          # Slow/expensive tests

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_config.py
```

### Test Structure

```bash
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Fast, isolated unit tests
│   ├── test_config.py       # Configuration handling tests
│   ├── test_vartree.py      # Variable tree tests
│   └── test_plugins.py      # Plugin system tests
├── integration/             # End-to-end integration tests
│   ├── test_optimization.py # Full optimization workflow
│   └── test_cli.py          # CLI interface tests
└── fixtures/                # Test data and configurations
    ├── configs/             # Sample configuration files
    └── data/                # Test datasets
```

### Writing Tests

```python
import pytest
from pathlib import Path
from flamingo.core.config import FlamingoConfig

def test_config_loading(tmp_path: Path):
    """Test configuration file loading."""
    config_content = """
    [variables]
    variables = threads{1,2} * blocks{16,32}
    
    [values]
    threads = 1, 2
    blocks = 16, 32
    """
    
    config_file = tmp_path / "test.conf"
    config_file.write_text(config_content)
    
    config = FlamingoConfig.from_file(config_file)
    assert len(config.variables) == 2
    assert "threads" in config.variable_values
```

## Plugin Development

### Plugin Interface

```python
from flamingo.plugins.interface import OptimizationPlugin, PluginMetadata

class MyOptimizer(OptimizationPlugin):
    """Custom optimization algorithm plugin."""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="my-optimizer",
            version="1.0.0",
            description="Custom optimization algorithm",
            author="Your Name"
        )
    
    def optimize(self, parameter_space, evaluator):
        """Implement optimization logic."""
        # Your optimization algorithm here
        pass
```

### Installing Plugins

```bash
# Install plugin from file
flamingo plugins install my_plugin.py

# List available plugins
flamingo plugins list

# Enable/disable plugins
flamingo plugins enable my-optimizer
flamingo plugins disable my-optimizer
```

## Docker Development

### Building Containers

```bash
# Build development image
docker build --target development -t flamingo:dev .

# Build production image
docker build --target production -t flamingo:prod .

# Build with GPU support
docker build --build-arg CUDA_VERSION=11.8 -t flamingo:gpu .
```

### Docker Compose Development

```bash
# Start development environment
docker-compose --profile dev up -d

# Start with monitoring stack
docker-compose --profile monitoring up -d

# View logs
docker-compose logs -f flamingo

# Run tests in container
docker-compose exec flamingo pytest
```

## Contributing Guidelines

### Workflow

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** with proper tests and documentation
4. **Run quality checks**: `pre-commit run --all-files`
5. **Ensure tests pass**: `pytest`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Commit Message Format

```bash
type(scope): description

Longer explanation if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Code Review Checklist

- [ ] Code follows style guidelines (Black, isort, flake8)
- [ ] Type hints are comprehensive and accurate
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact is considered
- [ ] Security implications are reviewed

## Architecture Decisions

### Python 2 to 3 Conversion Strategy

**Ben Spencer's original design patterns were preserved** while modernizing:

1. **Core Algorithms**: Maintained Ben's optimization logic exactly
2. **Interface Design**: Enhanced Ben's modular approach with modern patterns
3. **Configuration Format**: Backward compatible with Ben's original format
4. **Plugin Architecture**: Built on Ben's extensible design philosophy

### Modern Python Features Used

- **Type Hints**: Full typing support with `typing` module
- **Dataclasses**: Structured data with `@dataclass` decorator
- **Path Handling**: `pathlib.Path` instead of string paths
- **Context Managers**: Proper resource management with `with` statements
- **F-strings**: Modern string formatting
- **Async Support**: Where beneficial for parallel operations

### Key Design Principles

1. **Backward Compatibility**: Existing configurations continue to work
2. **Gradual Migration**: Old and new interfaces coexist
3. **Type Safety**: Comprehensive type hints throughout
4. **Extensibility**: Plugin architecture for customization
5. **Developer Experience**: Rich CLI and comprehensive tooling
6. **Performance**: Improved efficiency while maintaining correctness

## Debugging and Profiling

### Logging

```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use throughout code
logger.info("Starting optimization")
logger.debug(f"Parameter space: {parameter_space}")
logger.error(f"Optimization failed: {error}")
```

### Profiling

```bash
# Profile script execution
python -m cProfile -o profile.stats -m flamingo.cli.main run config.conf

# Analyze profile
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

# Memory profiling with memory_profiler
pip install memory_profiler
python -m memory_profiler -m flamingo.cli.main run config.conf
```

### Debugging

```python
# Use built-in debugger
import pdb; pdb.set_trace()

# Or use ipdb for enhanced debugging
import ipdb; ipdb.set_trace()

# Rich traceback for better error display (already configured)
from rich.traceback import install
install(show_locals=True)
```

## Release Process

### Version Management

```bash
# Update version in pyproject.toml and __init__.py
# Create git tag
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1

# Build package
python -m build

# Upload to PyPI (when ready)
python -m twine upload dist/*
```

### Documentation Updates

```bash
# Build documentation
cd docs/
make html

# Serve locally for review
python -m http.server 8000 -d _build/html
```

## Legacy Code Maintenance

### Ben Spencer's Original Modules

When modifying the core optimization logic in `tuner/`, **preserve Ben Spencer's algorithmic innovations**:

- **Optimization algorithms** in `optimisation.py` and `optimisation_bf.py`
- **Variable tree logic** in `vartree.py` and `vartree_parser.py`
- **Evaluation strategies** in `evaluator.py`
- **Configuration parsing** in `tune_conf.py`

### Migration Considerations

When updating legacy code:

1. **Maintain API compatibility** where possible
2. **Add type hints** without changing behavior
3. **Preserve algorithmic correctness** from Ben's original implementation
4. **Add comprehensive tests** to prevent regressions
5. **Document changes** clearly in commit messages

## Support and Maintenance

### Getting Help

- **Documentation**: Full API documentation in `docs/`
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Technical discussions via GitHub Discussions
- **Code Review**: Pull requests welcome

### Maintenance Philosophy

This project aims to honor **Ben Spencer's exceptional original work** while providing modern Python developers with contemporary tools and practices. All changes should respect the foundational design while enhancing usability, maintainability, and extensibility.

The core algorithms and design patterns that make this system effective are Ben Spencer's contributions, and this modernization effort ensures they remain accessible and usable for current and future Python developers.
