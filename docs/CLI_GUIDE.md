# CLI Guide: Modern Flamingo Interface

This guide covers the powerful new command-line interface (CLI) with Rich formatting, colors, and enhanced user experience.

## Table of Contents

1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
3. [Core Commands](#core-commands)
4. [Advanced Features](#advanced-features)
5. [Rich UI Elements](#rich-ui-elements)
6. [Configuration](#configuration)
7. [Customization](#customization)
8. [Examples](#examples)

## Overview

The Flamingo CLI has been completely redesigned with modern UX principles:

### Key Features

- 🎨 **Rich Formatting**: Colors, progress bars, tables, and panels
- 🖥️ **Interactive Mode**: Prompts, confirmations, and guided workflows
- 📊 **Real-time Progress**: Live updates during optimization
- 🔧 **Comprehensive Help**: Context-aware help and documentation
- 🚀 **Performance**: Fast startup and responsive interface
- 🎯 **Intuitive**: Discoverable commands with clear feedback

### Visual Design

- **Fire Theme**: Red, orange, and yellow color scheme inspired by "Flamingo"
- **Status Indicators**: ✅ ❌ ⚠️ 🔄 icons for clear status feedback
- **Progress Bars**: Animated progress with time estimates
- **Structured Output**: Tables, panels, and formatted text

## Installation and Setup

### Basic Installation

```bash
pip install flamingo-autotuner>=1.0.0
```

### Development Installation

```bash
git clone https://github.com/example/flamingo-autotuner.git
cd flamingo-autotuner
pip install -e ".[dev]"
```

### Verify Installation

```bash
flamingo --version
```

### Shell Completion

```bash
# Bash
flamingo --install-completion bash

# Zsh  
flamingo --install-completion zsh

# Fish
flamingo --install-completion fish
```

## Core Commands

### Global Options

Available for all commands:

```bash
flamingo [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]

Global Options:
  --version, -v          Show version and exit
  --verbose, -V          Enable verbose output  
  --quiet, -q            Suppress all output except errors
  --no-color             Disable colored output
  --config-dir PATH      Custom configuration directory
  --plugin-dir PATH      Custom plugin directory
  --help                 Show help message
```

### Main Commands

#### `flamingo run` - Run Optimization

Execute CUDA parameter optimization:

```bash
flamingo run CONFIG_FILE [OPTIONS]

Arguments:
  CONFIG_FILE    Path to configuration file [required]

Options:
  --dry-run, -n           Validate configuration without running
  --interactive, -i       Run in interactive mode with prompts
  --output-dir, -o PATH   Custom output directory for results
  --max-tests, -m INT     Maximum number of tests to run
  --parallel              Enable parallel execution
  --resume PATH           Resume from previous log file
  --docker                Run in Docker container
  --help                  Show command help

Examples:
  flamingo run config.conf
  flamingo run config.conf --interactive --max-tests 1000
  flamingo run config.conf --parallel --output-dir ./results
  flamingo run config.conf --resume previous_run.csv
```

**Interactive Mode Features:**

- Parameter space visualization
- Confirmation prompts before execution
- Real-time progress with estimates
- Interrupt handling with partial results

#### `flamingo validate` - Validate Configuration

Check configuration files for syntax and compatibility:

```bash
flamingo validate CONFIG_FILE [OPTIONS]

Arguments:
  CONFIG_FILE    Configuration file to validate [required]

Options:
  --strict       Use strict validation mode
  --fix          Automatically fix common issues
  --report PATH  Save validation report to file

Examples:
  flamingo validate config.conf
  flamingo validate config.conf --strict --report validation.txt
```

**Validation Checks:**

- ✅ Configuration file syntax
- ✅ Required sections and options
- ✅ Parameter value formats
- ✅ Command syntax validation
- ✅ File path accessibility
- ✅ Python 3 compatibility

#### `flamingo demo` - Interactive Demonstration

Run built-in examples and tutorials:

```bash
flamingo demo [OPTIONS]

Options:
  --example, -e NAME     Demo example to run [default: hello]
  --list                 List available examples
  --interactive          Run in interactive tutorial mode

Available Examples:
  hello        Simple compilation example
  matrix       Matrix multiplication optimization  
  laplace3d    3D Laplace solver (CUDA)
  looping      Loop iteration parameter tuning
  matlab       MATLAB vectorization optimization

Examples:
  flamingo demo
  flamingo demo --example matrix --interactive
  flamingo demo --list
```

#### `flamingo migrate` - Migration Tools

Convert Python 2 configurations and code:

```bash
flamingo migrate INPUT_FILE [OPTIONS]

Arguments:
  INPUT_FILE     Python 2 file to migrate [required]

Options:
  --output, -o PATH      Output file for migrated content
  --type TYPE            Migration type: config|code [default: config]
  --interactive          Interactive migration with review
  --backup               Create backup of original file
  --report PATH          Save migration report

Examples:
  flamingo migrate old_config.conf
  flamingo migrate old_config.conf --output new_config.conf --interactive
  flamingo migrate script.py --type code --backup
```

#### `flamingo plugins` - Plugin Management

Manage and configure plugins:

```bash
flamingo plugins ACTION [PLUGIN_NAME] [OPTIONS]

Actions:
  list                   List all available plugins
  install PLUGIN_NAME    Install a plugin
  uninstall PLUGIN_NAME  Uninstall a plugin  
  enable PLUGIN_NAME     Enable a plugin
  disable PLUGIN_NAME    Disable a plugin
  info PLUGIN_NAME       Show plugin information

Options:
  --search PATH          Additional plugin search paths
  --force                Force operation without confirmation

Examples:
  flamingo plugins list
  flamingo plugins install optimization-gpu
  flamingo plugins enable visualization-3d
  flamingo plugins info my-custom-plugin
```

#### `flamingo tui` - Terminal User Interface

Launch the interactive TUI:

```bash
flamingo tui [OPTIONS]

Options:
  --config PATH          Default configuration file to load
  --theme THEME          UI theme: fire|ember|classic [default: fire]

Examples:
  flamingo tui
  flamingo tui --config my_config.conf --theme ember
```

### Utility Commands

#### `flamingo plot` - Visualization

Generate plots and visualizations:

```bash
flamingo plot INPUT_FILE [OPTIONS]

Arguments:
  INPUT_FILE     Results file to visualize [required]

Options:
  --type TYPE            Plot type: line|scatter|heatmap|3d
  --output, -o PATH      Output file for plot
  --interactive          Show interactive plot
  --theme THEME          Plot theme

Examples:
  flamingo plot results.csv --type heatmap --output plot.png
  flamingo plot results.csv --interactive
```

#### `flamingo export` - Data Export

Export results in different formats:

```bash
flamingo export INPUT_FILE [OPTIONS]

Arguments:
  INPUT_FILE     Results file to export [required]

Options:
  --format FORMAT        Export format: json|yaml|hdf5|xlsx
  --output, -o PATH      Output file
  --filter FILTER        Filter expression for data

Examples:
  flamingo export results.csv --format json --output results.json
  flamingo export results.csv --format xlsx --filter "score < 0.01"
```

## Advanced Features

### Rich Progress Display

During optimization, Flamingo shows detailed progress:

```bash
🔥 Flamingo CUDA Autotuning System

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                🚀 Running Optimization                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔥 Running optimization...    ████████████████████████████████ 68% 0:02:15
🔨 Compiling...              ████████████████████████████████ 100% 
🧪 Testing...                ████████████████████████████████ 100%
📊 Analyzing...              ██████████████████████████░░░░░░ 75%

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                    📊 Progress Summary                               ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Progress          │ 692/1024 (67.6%)                                                 ┃
┃ Best Score        │ 0.001234                                                         ┃
┃ Current Config    │ threads=32, blocks=64                                            ┃
┃ Elapsed Time      │ 2m 15s                                                           ┃
┃ Est. Remaining    │ 1m 8s                                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Interactive Parameter Review

Before starting optimization:

```bash
🌳 Parameter Space

├── threads (6 values)
│   ├── 1
│   ├── 2  
│   ├── 4
│   ├── 8
│   ├── 16
│   └── 32
└── blocks (4 values)
    ├── 16
    ├── 32
    ├── 64
    └── 128

📊 Parameter Space Analysis
  • Total variables: 2
  • Total combinations: 24
  • Estimated runtime: 2m 30s

Proceed with optimization? [Y/n]:
```

### Results Display

After completion:

```bash
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                            🎉 Optimization Complete!                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                                 📊 Optimization Results                                
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric               ┃ Value                                                      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Best Score           │ 0.001234                                                   │
│ Best Configuration   │ threads=32, blocks=64, opt=O3                             │
│ Total Tests          │ 1,024                                                      │
│ Duration             │ 3m 23s                                                     │
│ Success Rate         │ 98.4%                                                      │
└──────────────────────┴────────────────────────────────────────────────────────────┘

📁 Output Files:
  • Log file: results.csv
  • Plot: optimization_plot.png  
  • Report: summary_report.html
```

## Rich UI Elements

### Color Scheme

Flamingo uses a fire-inspired color theme:

- 🔥 **Primary**: Bold red for headers and important info
- 🧡 **Secondary**: Orange for progress and highlights  
- 💛 **Accent**: Yellow for warnings and emphasis
- 💚 **Success**: Green for successful operations
- 🔴 **Error**: Red for errors and failures
- 🔵 **Info**: Blue for informational messages

### Status Indicators

- ✅ **Success**: Operation completed successfully
- ❌ **Error**: Operation failed
- ⚠️ **Warning**: Potential issues or important notes
- 🔄 **Running**: Operation in progress
- ⏳ **Waiting**: Queued or waiting for resources
- ℹ️ **Info**: General information

### Progress Elements

- **Bars**: `████████████████████████████████ 100%`
- **Spinners**: `⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏` (animated)
- **Time**: `0:02:15` (elapsed) / `Est. 1m 8s` (remaining)

## Configuration

### Global Configuration

Create `~/.flamingo/config.toml`:

```toml
[cli]
theme = "fire"  # fire, ember, classic
no_color = false
progress_style = "rich"  # rich, simple, none
default_parallel = true

[output]
default_format = "csv"
auto_plot = true
save_logs = true

[plugins]
auto_update = false
search_paths = [
    "~/.flamingo/plugins",
    "./plugins"
]

[docker]
default_image = "flamingo:latest"
gpu_support = true
```

### Environment Variables

```bash
# Disable colors
export NO_COLOR=1

# Custom configuration directory
export FLAMINGO_CONFIG_DIR=~/.config/flamingo

# Custom plugin directory  
export FLAMINGO_PLUGIN_DIR=~/.local/share/flamingo/plugins

# Log level
export FLAMINGO_LOG_LEVEL=DEBUG
```

## Customization

### Custom Themes

Create custom color themes:

```python
# ~/.flamingo/themes/my_theme.py
from rich.theme import Theme

my_theme = Theme({
    "primary": "bold blue",
    "secondary": "cyan", 
    "accent": "magenta",
    "success": "green",
    "error": "red",
    "warning": "yellow",
})
```

### Custom Commands

Add custom commands via plugins:

```python
# ~/.flamingo/plugins/my_commands.py
import typer
from flamingo.cli.main import app

@app.command("my-command")
def my_command(arg: str):
    """My custom command."""
    typer.echo(f"Hello {arg}!")
```

### Output Formatting

Customize output formats:

```python
# ~/.flamingo/formatters/my_formatter.py
from flamingo.cli.utils import ProgressTracker

class MyProgressTracker(ProgressTracker):
    def display(self):
        # Custom progress display
        pass
```

## Examples

### Basic Usage

```bash
# Simple optimization
flamingo run config.conf

# With validation first
flamingo validate config.conf && flamingo run config.conf

# Interactive mode with custom output
flamingo run config.conf --interactive --output-dir ./my_results
```

### Advanced Workflows

```bash
# Migration workflow
flamingo migrate old_config.conf --backup --interactive
flamingo validate old_config.py3.conf
flamingo run old_config.py3.conf --dry-run
flamingo run old_config.py3.conf

# Plugin workflow
flamingo plugins list
flamingo plugins install gpu-optimization
flamingo plugins enable gpu-optimization
flamingo run config.conf --parallel

# Docker workflow  
flamingo run config.conf --docker
# Or with custom image
docker run -v ./data:/data flamingo:custom run /data/config.conf
```

### Batch Processing

```bash
# Process multiple configurations
for config in configs/*.conf; do
    echo "Processing $config..."
    flamingo run "$config" --output-dir "results/$(basename "$config" .conf)"
done

# Parallel processing with xargs
find configs/ -name "*.conf" | xargs -P 4 -I {} flamingo run {} --quiet
```

### Results Analysis

```bash
# Generate visualization
flamingo plot results.csv --type heatmap --output analysis.png

# Export for further analysis
flamingo export results.csv --format json | jq '.best_results[] | select(.score < 0.01)'

# Compare multiple runs
flamingo plot results1.csv results2.csv --type comparison
```

---

The modern Flamingo CLI provides a powerful, intuitive interface that makes CUDA parameter optimization both efficient and enjoyable. The rich visual feedback and interactive features help you understand your optimization process better and achieve optimal results faster.
