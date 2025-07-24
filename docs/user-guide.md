# Flamingo CUDA Autotuning System - User Guide

**Version 1.0.0 (Python 3.10+ Modernized)**

## Credits and Acknowledgments

This project is built upon the outstanding foundational work of **Ben Spencer**, who created the original Python 2.5+ autotuning system. His innovative approach to CUDA parameter optimization and the comprehensive design of the core algorithms form the backbone of this modernized version.

**Original Author**: Ben Spencer  
**Python 3 Modernization**: Claude Code (Anthropic)  
**Conversion Status**: Complete rewrite and modernization to Python 3.10+

## Python 2 to 3 Conversion Notice

This system has been completely converted from Python 2.5+ to Python 3.10+ with full modernization including:

- **Type hints** throughout the codebase
- **Enhanced error handling** with custom exception types
- **Modern Python best practices** and idioms
- **Rich CLI interface** with colors and interactive features
- **Plugin architecture** for extensibility
- **Docker containerization** support
- **Comprehensive testing** with pytest
- **Migration tools** to help transition from the original system

## Getting Started

### Quick Installation

```bash
# Clone the repository
git clone <repository-url>
cd flamingo-autotuner/Autotuning

# Install in development mode
pip install -e .

# Or install with all features
pip install -e ".[dev,tui,docs]"
```

### Basic Usage

#### Modern CLI Interface

The new Rich-based CLI provides a beautiful, interactive experience:

```bash
# Run optimization with rich progress bars and colors
flamingo run config.conf

# Interactive mode with guided workflow
flamingo run config.conf --interactive

# Launch the Terminal User Interface (TUI)
flamingo tui

# Run a demo to see the system in action
flamingo demo --example hello
```

#### Configuration Format

Create a configuration file (e.g., `myconfig.conf`) with these sections:

```ini
[variables]
variables = threads{1,2,4,8} * blocks{16,32,64}

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
```

### System Requirements

- **Python 3.10 or higher** (originally required Python 2.5)
- **CUDA toolkit** (for CUDA examples)
- **C/C++ compiler** (for compilation examples)

### Key Improvements in Python 3 Version

#### 🎨 Rich CLI Experience

- Colorful terminal output with fire-inspired theme
- Interactive progress bars with real-time updates
- Structured tables and panels for clear information display
- Status indicators (✅ ❌ ⚠️ 🔄) for immediate feedback

#### 🔌 Plugin Architecture

- Extensible plugin system for custom optimization algorithms
- Hot-pluggable evaluators and output formats
- Plugin manager with install/enable/disable capabilities

#### 🐳 Docker Support

- Multi-stage Docker builds for development and production
- Docker Compose setup with full monitoring stack
- GPU-enabled containers with CUDA support

#### 🔄 Migration Tools

- Automated configuration conversion from Python 2 to 3
- Code migration assistance with detailed change reports
- Interactive migration workflow with validation

#### 💪 Core Technical Improvements

- **Modern type system** with comprehensive type hints
- **Enhanced error handling** and validation
- **Better resource management** with context managers
- **Improved performance** and memory usage
- **Modern dependency management** with pyproject.toml
- **Comprehensive test suite** with pytest
- **Code quality tools** integration (black, mypy, isort)

## Documentation Structure

- **Main Documentation**: See [README.md](../README.md) for comprehensive overview
- **Developer Guide**: [developer-guide.md](./developer-guide.md) for contributing and development
- **Migration Guide**: [migration-guide.md](./migration-guide.md) for upgrading from Python 2
- **CLI Guide**: [cli-guide.md](./cli-guide.md) for command-line interface documentation
- **Testing Guide**: [testing-guide.md](./testing-guide.md) for running tests and validation

## Legacy Documentation

The original system documentation (created by Ben Spencer) is still available and provides valuable insights into the core concepts:

- `docs/user.pdf` - Original user documentation
- `docs/tutorial.pdf` - Beginner's tutorial
- `docs/dev.pdf` - Developer documentation

## Code Structure

- **Core Code**: All main code is in the `tuner/` directory (legacy) and `flamingo/` directory (modern)
- **Main Program**:
  - Legacy: `tuner/tune.py` (now Python 3)
  - Modern: `flamingo/cli/main.py` with Rich CLI
- **Examples**: `examples/` directory shows system usage
- **Plugins**: `flamingo/plugins/` for extensible functionality
- **Migration Tools**: `flamingo/migration/` for Python 2 to 3 conversion

## Quick Start Commands

```bash
# Install the system
pip install -e .

# Run a demo
flamingo demo --example hello

# Run with your configuration
flamingo run myconfig.conf

# Validate configuration without running
flamingo validate myconfig.conf

# Migrate from Python 2 configuration
flamingo migrate old_config.conf

# Launch interactive TUI
flamingo tui

# Manage plugins
flamingo plugins list
flamingo plugins install my-plugin.py
```

## Examples and Demonstrations

The system includes several example programs to demonstrate functionality:

- **hello/**: Simple "Hello World" compilation example
- **matrix/**: Matrix multiplication optimization
- **laplace3d/**: 3D Laplace solver CUDA example
- **looping/**: Loop iteration parameter tuning
- **matlab/**: MATLAB vectorization optimization

To run an example:

```bash
cd examples/hello
autotune hello.conf
# or with modern CLI:
flamingo run hello.conf
```

## Getting Help

- **Built-in Help**: Use `flamingo --help` or `flamingo [command] --help`
- **Interactive Mode**: Run `flamingo run --interactive` for guided workflow
- **Documentation**: Full documentation available in the `docs/` directory
- **Issues**: Report bugs and request features via GitHub Issues

## What's New vs Original

This modernized version maintains full compatibility with Ben Spencer's original design while adding:

1. **Modern Python 3.10+** features and syntax
2. **Rich CLI interface** with colors and progress bars
3. **Plugin system** for extensibility
4. **Docker support** for containerized workflows
5. **Migration tools** for easy upgrading
6. **Comprehensive type hints** for better IDE support
7. **Enhanced testing** with pytest framework
8. **Code quality tools** integration

The core optimization algorithms and parameter space exploration logic remain faithful to Ben Spencer's original innovative design, ensuring that existing configurations and workflows continue to work while providing modern conveniences and enhanced capabilities.
