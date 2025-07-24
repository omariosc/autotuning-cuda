# Migration Guide: Python 2 to Python 3

This comprehensive guide helps you migrate from the original Python 2.5+ Flamingo CUDA Autotuning System to the modern Python 3.10+ version.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start Migration](#quick-start-migration)
3. [Configuration File Changes](#configuration-file-changes)
4. [Command Line Interface Changes](#command-line-interface-changes)
5. [Code Changes](#code-changes)
6. [New Features](#new-features)
7. [Docker Migration](#docker-migration)
8. [Plugin Migration](#plugin-migration)
9. [Troubleshooting](#troubleshooting)
10. [Migration Tools](#migration-tools)

## Overview

The Python 3 version of Flamingo is a complete modernization that maintains backward compatibility while adding powerful new features:

### What's New

- 🎨 **Rich CLI** with colors, progress bars, and enhanced UX
- 🔌 **Plugin Architecture** for extensible functionality
- 🐳 **Docker Support** with multi-stage builds
- 🔄 **Migration Tools** for automated conversion
- 📱 **TUI Interface** for interactive usage
- 🚀 **Modern Python** with type hints and async support
- 📊 **Enhanced Visualization** and reporting
- 🛡️ **Better Error Handling** and validation

### Breaking Changes

- **Python Version**: Requires Python 3.10+ (was 2.5+)
- **Import Names**: Some module names have changed
- **CLI Interface**: Enhanced with new commands and options
- **Configuration**: Extended format with new sections

## Quick Start Migration

### 1. Install Python 3 Version

```bash
# Uninstall old version (if installed via pip)
pip uninstall flamingo-autotuner

# Install new version
pip install flamingo-autotuner>=1.0.0

# Or from source
git clone https://github.com/example/flamingo-autotuner.git
cd flamingo-autotuner
pip install -e .
```

### 2. Migrate Configuration Files

```bash
# Automatic migration
flamingo migrate old_config.conf -o new_config.conf

# Interactive migration with review
flamingo migrate old_config.conf --interactive
```

### 3. Test Your Setup

```bash
# Validate migrated configuration
flamingo validate new_config.conf

# Run a test optimization
flamingo run new_config.conf --dry-run
```

## Configuration File Changes

### Section Changes

#### [variables] - No Changes

The variables section remains compatible:

```ini
[variables]
variables = threads{1,2,4,8} * blocks{16,32,64}
```

#### [values] - Enhanced Validation

Values are now validated more strictly:

```ini
[values]
# Python 2 (loose formatting)
threads = 1,2 , 4, 8

# Python 3 (cleaned automatically)
threads = 1, 2, 4, 8
```

#### [testing] - Command Updates

Commands may need Python 3 updates:

```ini
[testing]
# Python 2
compile = python setup.py build
test = python run_test.py %threads%

# Python 3 (auto-converted)
compile = python3 setup.py build  
test = python3 run_test.py %threads%
```

#### [scoring] - Enhanced Options

New aggregation methods available:

```ini
[scoring]
optimal = min_time
repeat = 5, avg  # avg, min, max, med supported
```

#### [output] - Enhanced Formats

New output options:

```ini
[output]
log = results.csv
script = session.log
importance = param_analysis.csv

# New in Python 3
format = csv  # csv, json, yaml, hdf5
visualization = true
```

### New Sections

#### [advanced] - Modern Features

```ini
[advanced]
parallel_evaluation = true
plugin_support = true
rich_output = true
type_checking = true
max_workers = 4
```

#### [plugins] - Plugin Configuration

```ini
[plugins]
enabled = optimization-gpu, visualization-3d
search_paths = ~/.flamingo/plugins, ./plugins
```

#### [logging] - Enhanced Logging

```ini
[logging]
level = INFO
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
file = flamingo.log
```

## Command Line Interface Changes

### Old CLI (Python 2)

```bash
# Python 2 usage
python tuner/tune.py config.conf
python utilities/output_gnuplot.py results.csv
```

### New CLI (Python 3)

```bash
# Python 3 usage - much more powerful!
flamingo run config.conf
flamingo plot results.csv
flamingo migrate old_config.conf
flamingo plugins list
flamingo tui  # Launch TUI
```

### New Commands Available

#### Core Commands

```bash
# Run optimization
flamingo run config.conf [options]

# Validate configuration  
flamingo validate config.conf

# Interactive demo
flamingo demo --example matrix

# Migration tools
flamingo migrate old_config.conf

# Plugin management
flamingo plugins list|install|enable|disable

# Launch TUI
flamingo tui
```

#### Advanced Options

```bash
# Rich output with progress bars
flamingo run config.conf --interactive

# Parallel execution
flamingo run config.conf --parallel --max-workers 8

# Resume interrupted runs
flamingo run config.conf --resume results.csv

# Container execution  
flamingo run config.conf --docker

# Custom output directory
flamingo run config.conf --output-dir ./results
```

## Code Changes

### Python Language Changes

#### Print Statements

```python
# Python 2
print "Hello, world!"
print "Score:", score

# Python 3 (auto-converted)
print("Hello, world!")
print("Score:", score)
```

#### Exception Handling

```python
# Python 2
try:
    do_something()
except ValueError, e:
    print "Error:", e

# Python 3 (auto-converted)
try:
    do_something()
except ValueError as e:
    print("Error:", e)
```

#### Dictionary Methods

```python
# Python 2
for key, value in config.iteritems():
    print key, value

# Python 3 (auto-converted)
for key, value in config.items():
    print(key, value)
```

#### Import Changes

```python
# Python 2
import ConfigParser
from ConfigParser import RawConfigParser

# Python 3 (auto-converted)
import configparser
from configparser import RawConfigParser
```

### Custom Code Migration

If you have custom evaluation scripts or plugins:

#### 1. Use Migration Tools

```bash
# Convert Python scripts
flamingo migrate my_script.py --type code
```

#### 2. Manual Updates Needed

- Update shebang: `#!/usr/bin/env python3`
- Check integer division: `/` vs `//`
- Update string handling for Unicode
- Review any C extensions for Python 3 compatibility

## New Features

### Rich CLI Interface

The new CLI provides a beautiful, colorful interface:

```bash
# Rich progress bars
flamingo run config.conf
🔥 Running optimization... ████████████████████ 100% 0:02:30

# Colored output with status indicators
✅ Configuration loaded: config.conf  
🚀 Starting optimization with 1,024 parameter combinations
📊 Best score so far: 0.001234 (threads=32, blocks=64)
```

### Plugin System

Extend Flamingo with custom plugins:

```python
# Create optimization plugin
from flamingo.plugins import OptimizationPlugin, plugin_metadata

@plugin_metadata(
    name="MyOptimizer",
    version="1.0.0", 
    description="Custom optimization algorithm"
)
class MyOptimizer(OptimizationPlugin):
    def optimize(self, parameter_space, evaluator, **kwargs):
        # Your custom optimization logic
        pass
```

### Docker Integration

Run Flamingo in containers:

```bash
# Build and run in Docker
docker build -t flamingo .
docker run --gpus all -v ./data:/data flamingo run /data/config.conf

# Use docker-compose for full stack
docker-compose --profile dev up
```

### Terminal User Interface (TUI)

Interactive terminal interface:

```bash
flamingo tui
```

This launches a full-screen interface with:

- Parameter space visualization
- Real-time optimization progress
- Interactive configuration editing
- Results analysis and plotting

## Docker Migration

### Development Environment

```bash
# Clone and setup development environment
git clone https://github.com/example/flamingo-autotuner.git
cd flamingo-autotuner

# Launch development container
docker-compose --profile dev up -d

# Access development environment
docker exec -it flamingo-development bash
```

### Production Deployment

```bash
# Production deployment
docker-compose --profile prod up -d

# With monitoring stack
docker-compose --profile all up -d
```

### Jupyter Environment

```bash
# Launch Jupyter notebooks
docker-compose --profile notebook up -d

# Access at http://localhost:8888
# Token: flamingo-notebook-token
```

## Plugin Migration

### Creating Plugins

1. **Optimization Algorithms**

```python
from flamingo.plugins import create_optimization_plugin

def my_algorithm(parameter_space, evaluator, max_iterations=None, **kwargs):
    # Your algorithm implementation
    return results

plugin = create_optimization_plugin(
    name="MyAlgorithm",
    version="1.0.0",
    description="My custom optimization algorithm",
    author="Your Name",
    optimize_func=my_algorithm,
    supports_parallel=True
)
```

2. **Evaluation Strategies**

```python
from flamingo.plugins import EvaluationPlugin

class MyEvaluator(EvaluationPlugin):
    def evaluate(self, configuration, test_commands, repetitions=1, **kwargs):
        # Your evaluation logic
        return {"score": score, "time": elapsed_time}
```

3. **Output Formats**

```python
from flamingo.plugins import OutputPlugin

class MyOutputFormat(OutputPlugin):
    def save_results(self, results, output_path, **kwargs):
        # Save in your custom format
        return True
```

### Plugin Management

```bash
# List available plugins
flamingo plugins list

# Install plugin
flamingo plugins install my-optimization-plugin

# Enable/disable plugins
flamingo plugins enable my-plugin
flamingo plugins disable my-plugin
```

## Troubleshooting

### Common Issues

#### 1. Python Version Mismatch

```bash
# Error: "This script requires Python version 2.5"
# Solution: Install Python 3.10+
python3 --version  # Should be 3.10+
pip install flamingo-autotuner>=1.0.0
```

#### 2. Configuration Syntax Errors

```bash
# Error: "Configuration validation failed"
# Solution: Use migration tool
flamingo migrate old_config.conf
flamingo validate new_config.conf
```

#### 3. Import Errors

```bash
# Error: "No module named 'ConfigParser'"
# Solution: Update Python 2 scripts
flamingo migrate my_script.py --type code
```

#### 4. Command Not Found

```bash
# Error: "flamingo: command not found"  
# Solution: Reinstall or fix PATH
pip install -e .
# Or add to PATH: ~/.local/bin
```

### Performance Issues

#### 1. Slow Optimization

```ini
# Enable parallel evaluation
[advanced]
parallel_evaluation = true
max_workers = 4
```

#### 2. Memory Usage

```ini
# Reduce memory usage
[advanced]
batch_size = 100
memory_limit = 4GB
```

### Docker Issues

#### 1. GPU Access

```bash
# Install nvidia-docker
sudo apt install nvidia-docker2
sudo systemctl restart docker

# Run with GPU support
docker run --gpus all flamingo
```

#### 2. Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER ./data ./results
```

## Migration Tools

### Automated Conversion

The migration tools provide automated conversion with detailed reporting:

```bash
# Convert configuration
flamingo migrate config.conf
# Output: config.py3.conf with conversion report

# Convert Python code
flamingo migrate script.py --type code
# Output: script.py3.py with conversion notes

# Interactive migration with review
flamingo migrate config.conf --interactive
```

### Manual Review Items

After automated migration, manually review:

1. **File Paths**: Update any hardcoded paths
2. **Commands**: Verify compile/test commands work  
3. **Custom Scripts**: Test any custom evaluation scripts
4. **Plugins**: Port any custom plugins to new API
5. **Performance**: Compare performance with Python 2 version

### Validation Tools

```bash
# Comprehensive validation
flamingo validate config.conf

# Test optimization (dry run)
flamingo run config.conf --dry-run

# Compare with Python 2 results
flamingo run config.conf --compare legacy_results.csv
```

## Support and Resources

### Documentation

- 📖 [Full Documentation](https://flamingo-autotuner.readthedocs.io/)
- 🎓 [Tutorial](docs/tutorial.md)
- 📚 [API Reference](docs/api/)
- 🔧 [Plugin Development Guide](docs/plugins.md)

### Community

- 💬 [GitHub Discussions](https://github.com/example/flamingo-autotuner/discussions)
- 🐛 [Issue Tracker](https://github.com/example/flamingo-autotuner/issues)
- 📧 [Mailing List](mailto:users@flamingo-autotuner.org)

### Migration Support

- 🔄 [Migration Tools](flamingo/migration/)
- 📋 [Migration Checklist](docs/MIGRATION_CHECKLIST.md)
- 🆘 [Migration Support](mailto:support@flamingo-autotuner.org)

---

**Need Help?** If you encounter issues during migration, please:

1. Check this guide and the troubleshooting section
2. Use the automated migration tools
3. Search existing GitHub issues
4. Create a new issue with details about your specific case

The Python 3 version of Flamingo is designed to be a significant upgrade while maintaining compatibility with your existing workflows. Take advantage of the new features to make your CUDA autotuning more efficient and enjoyable!
