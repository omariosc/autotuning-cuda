# Flamingo CUDA Autotuning System 🦩

**Fully Modernized Python 3.10+ Version** | Version 1.0.0

**Credits**: This project is built upon the exceptional foundational work of **Ben Spencer**, who created the original Python 2.5+ CUDA autotuning system. His innovative algorithms and comprehensive design form the core of this modernized version. See [Credits](docs/credits.md) for detailed acknowledgments.

**Note: This codebase was modernized by Claude Code from Ben Spencer's original Python 2 implementation. There may be bugs in the conversion. Please add issues to this repository as needed.**

A sophisticated CUDA parameter optimization framework with **Rich CLI**, **Plugin Architecture**, **Docker Support**, and **Migration Tools**. Automatically finds optimal configurations for CUDA programs through intelligent search algorithms.

## Overview

The Flamingo CUDA Autotuning System helps developers optimize CUDA applications by automatically exploring the parameter space to find optimal configurations. It supports various optimization algorithms and provides comprehensive logging and analysis capabilities.

### 🆕 New Features in Python 3 Version

This is a **complete modernization** of the original Python 2.5+ system with powerful new capabilities:

#### 🎨 Rich CLI Interface

- **Colorful terminal output** with fire-inspired theme
- **Interactive progress bars** with real-time updates
- **Structured tables and panels** for clear information display
- **Status indicators** (✅ ❌ ⚠️ 🔄) for immediate feedback

#### 🔌 Plugin Architecture

- **Extensible plugin system** for custom optimization algorithms
- **Hot-pluggable evaluators** and output formats
- **Plugin manager** with install/enable/disable capabilities
- **Rich plugin ecosystem** support

#### 🐳 Docker & Containerization

- **Multi-stage Docker builds** for development and production
- **Docker Compose** setup with full monitoring stack
- **GPU-enabled containers** with CUDA support
- **Jupyter notebook environment** for interactive analysis

#### 🔄 Migration Tools

- **Automated configuration conversion** from Python 2 to 3
- **Code migration assistance** with detailed change reports
- **Compatibility analyzer** for smooth transitions
- **Interactive migration workflow** with validation

#### 📱 Terminal User Interface (TUI)

- **Full-screen interactive interface** for advanced users
- **Real-time visualization** of optimization progress
- **Parameter space exploration** tools
- **Integrated configuration editor**

#### 💪 Core Improvements

- **Python 3.10+ compatibility** with modern features
- **Comprehensive type hints** for better IDE support
- **Enhanced error handling** with detailed diagnostics
- **Async support** for parallel operations
- **Modern testing** with pytest and comprehensive coverage

## Quick Start

### Prerequisites

- Python 3.10 or higher
- CUDA toolkit (for CUDA examples)
- C/C++ compiler (for compilation examples)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd flamingo-autotuner/Autotuning

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

#### 🚀 Modern CLI Experience

```bash
# Rich, colorful interface with progress bars
flamingo run config.conf

# Interactive mode with guided workflow  
flamingo run config.conf --interactive

# Launch beautiful TUI for advanced users
flamingo tui
```

#### 📝 Configuration (Enhanced Format)

```ini
[variables]
variables = threads{1,2,4,8,16} * blocks{16,32,64}

[values]
threads = 1, 2, 4, 8, 16, 32
blocks = 16, 32, 64, 128

[testing]
compile = nvcc -O3 -DTHREADS=%threads% -DBLOCKS=%blocks% kernel.cu -o kernel
test = ./kernel
clean = rm -f kernel

[scoring]
optimal = min_time
repeat = 5, avg

[output]
log = results.csv
format = csv
visualization = true

[advanced]
parallel_evaluation = true
max_workers = 4

[plugins]
enabled = gpu-optimization, advanced-plotting
```

#### 🔄 Migration from Python 2

```bash
# Automatically convert old configurations
flamingo migrate old_config.conf

# Interactive migration with detailed review
flamingo migrate old_config.conf --interactive

# Validate converted configuration
flamingo validate old_config.py3.conf
```

## Key Features

- **Multiple Optimization Algorithms**: Supports various search strategies including brute force and intelligent exploration
- **Flexible Parameter Spaces**: Define complex parameter relationships using tree structures
- **Comprehensive Logging**: Detailed CSV logs with timing and performance data
- **Parameter Importance Analysis**: Understand which parameters have the most impact
- **Visualization Tools**: Generate plots and graphs from optimization results
- **Batch Processing**: Support for parallel and batch evaluation modes
- **Custom Figure of Merit**: Define custom scoring functions beyond simple timing

## Examples

The `examples/` directory contains several demonstration programs:

- **hello/**: Simple "Hello World" compilation example
- **matrix/**: Matrix multiplication optimization
- **laplace3d/**: 3D Laplace solver CUDA example
- **looping/**: Loop iteration parameter tuning
- **matlab/**: MATLAB vectorization optimization

To run an example:

```bash
cd Autotuning/examples/hello
autotune hello.conf
```

## Configuration File Format

Configuration files use INI format with five required sections:

### [variables]

Define the parameter space structure:

```ini
variables = threads{1,2,4} * blocks{8,16,32}
```

### [values]

Specify possible values for each parameter:

```ini
threads = 1, 2, 4, 8, 16, 32
blocks = 8, 16, 32, 64
```

### [testing]

Define how to compile and test your program:

```ini
compile = gcc -DTHREADS=%threads% -o program program.c
test = time ./program
clean = rm -f program
```

### [scoring]

Configure optimization direction and repetitions:

```ini
optimal = min_time
repeat = 5, avg
```

### [output]

Set up logging and result files:

```ini
log = results.csv
script = session.log
importance = param_analysis.csv
```

## Architecture

The system consists of several key components:

- **`tune.py`**: Main entry point and orchestration
- **`optimisation.py`**: Core optimization algorithms
- **`evaluator.py`**: Test execution and measurement
- **`vartree.py`**: Parameter space representation
- **`tune_conf.py`**: Configuration file parsing
- **`output.py`**: Logging and output management

## Python 2 Conversion Notes

This codebase has been fully converted from Python 2.5+ to Python 3.10+. Major changes include:

### Core Language Changes

- All `print` statements converted to `print()` functions
- `raw_input()` changed to `input()`
- Integer division fixed (`/` vs `//`)
- Dictionary iteration methods updated (`.iteritems()` → `.items()`)
- Import system modernized with explicit relative imports
- Exception handling syntax updated (`except E, e:` → `except E as e:`)

### Modernization Enhancements

- **Type Hints**: Comprehensive type annotations throughout
- **Dataclasses**: Modern data structures where appropriate  
- **F-strings**: Modern string formatting
- **Pathlib**: Path handling with `pathlib.Path`
- **Context Managers**: Proper resource management
- **Error Handling**: Enhanced exception handling with custom exception types
- **Async Support**: Async patterns for parallel operations where beneficial

### Dependencies Updated

- `ConfigParser` → `configparser`
- Added `argparse` for command-line parsing
- Added `pathlib` for path operations
- Added `typing` for type hints
- Added `dataclasses` for structured data
- Modern testing with `pytest`
- Code quality tools (`black`, `mypy`, `isort`)

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev,docs]"

# Set up pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=flamingo --cov=tuner --cov=utilities

# Run specific test categories
pytest -m unit
pytest -m integration
```

### Code Quality

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
flake8 .
```

### Building Documentation

```bash
cd docs/
make html
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper tests and documentation
4. Ensure all tests pass and code quality checks pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the terms specified in `LICENCE.txt`.

## Citation

If you use this software in academic work, please cite:

```
@software{flamingo_autotuner,
  title={Flamingo CUDA Autotuning System},
  author={[Original Authors]},
  year={2024},
  version={1.0.0},
  url={https://github.com/example/flamingo-autotuner}
}
```

## Documentation

- 📖 **[User Guide](docs/user-guide.md)**: Complete user documentation and getting started guide
- 🔧 **[Developer Guide](docs/developer-guide.md)**: Development setup, architecture, and contributing guidelines  
- 🔄 **[Migration Guide](docs/migration-guide.md)**: Guide for migrating from Python 2 version
- 💻 **[CLI Guide](docs/cli-guide.md)**: Command-line interface documentation
- 🧪 **[Testing Guide](docs/testing-guide.md)**: Testing procedures and validation
- 🎯 **[Examples Guide](docs/examples-guide.md)**: Comprehensive guide to all example programs and use cases
- 🛠️ **[Utilities Guide](docs/utilities-guide.md)**: Analysis and visualization tools documentation
- 📋 **[Issues & TODO](docs/ISSUES.md)**: Known issues and enhancement opportunities from Ben Spencer's original development
- 🔄 **[Parallel Evaluation Design](docs/CHANGES_parallel_evaluation.md)**: Ben Spencer's design plans for parallel testing
- 🙏 **[Credits](docs/credits.md)**: Acknowledgments to Ben Spencer and contributors

## Support

- 🐛 **Issues**: Report bugs and request features via GitHub Issues  
- 💬 **Discussions**: Join the community discussions
- 📧 **Contact**: [maintainer@example.com]

## Changelog

### Version 1.0.0 (2024)

- **BREAKING**: Complete Python 3.10+ conversion from Python 2.5+
- **NEW**: Modern type system with comprehensive type hints
- **NEW**: Enhanced error handling and logging
- **NEW**: Modern dependency management with pyproject.toml
- **NEW**: Comprehensive test suite with pytest
- **NEW**: Code quality tools integration (black, mypy, isort)
- **IMPROVED**: Performance optimizations throughout
- **IMPROVED**: Better resource management with context managers
- **IMPROVED**: Enhanced documentation and examples

### Legacy Version 0.16 (Python 2)

- Original Python 2.5+ implementation
- Basic optimization algorithms
- CSV logging and gnuplot output
- Command-line interface
- Example programs for demonstration
