# Utilities Guide

**Original Author**: Ben Spencer  
**Python 3 Status**: Converted to Python 3 with enhanced functionality  

These utilities provide different methods to visualize and analyze the results of the tuning process.

## Available Utilities

### output_gnuplot.py

This script converts a CSV log file into a gnuplot PLT file. This PLT file can be used with the gnuplot plotting program to produce a detailed graph of the testing process. If required, the PLT file can be modified by hand.

**Features:**

- Converts CSV results to gnuplot format
- Reference score plotting for comparison
- Customizable output formatting

**Usage:**

```bash
./output_gnuplot.py [-h] [-r SCORE] mylog.csv myplot.plt
```

**Options:**

- `-h, --help`: Print usage information
- `-r SCORE, --reference SCORE`: Plot a reference score for comparison with the tuner's results

**Example:**

```bash
# Basic conversion (from Autotuning directory)
python utilities/output_gnuplot.py results.csv plot.plt

# With reference score
python utilities/output_gnuplot.py -r 0.05 results.csv plot.plt
```

### output_screen.py

This script reads a CSV log file and produces a graph displayed on the screen. The graph can then be saved if needed. The `matplotlib` Python library is required.

**Features:**

- Interactive on-screen plotting
- Standard deviation visualization
- Reference score comparison
- Save capability

**Usage:**

```bash
./output_screen.py [-h] [-r SCORE] [-s] mylog.csv
```

**Options:**

- `-h, --help`: Print usage information
- `-r SCORE, --reference SCORE`: Plot a reference score for comparison
- `-s, --stddev`: Add standard deviation from the mean to the plot

**Example:**

```bash
# Basic plotting (from Autotuning directory)
python utilities/output_screen.py results.csv

# With reference and standard deviation
python utilities/output_screen.py -r 0.05 -s results.csv
```

### csv_plot.m

This is a MATLAB program which can be used to display a graph of the testing process.

**Usage:**

- Modify the file as needed for your specific analysis
- Load your CSV data and customize the plotting parameters

**Example:**

```matlab
% Load and plot CSV data
data = csvread('results.csv', 1, 0);  % Skip header row
plot(data(:,1), data(:,2));
xlabel('Test Number');
ylabel('Score');
title('Optimization Progress');
```

## Supporting Files

### common.py

Defines common functions for the Python utilities, particularly functions to read CSV files and process results data.

**Key Functions:**

- CSV file reading and parsing
- Data validation and preprocessing
- Common plotting utilities
- Statistical analysis helpers

## Python 3 Enhancements

The utilities have been enhanced in the Python 3 version with:

### Modern Features

- **Type hints** for better code clarity and IDE support
- **Pathlib** for robust file path handling
- **Enhanced error handling** with detailed error messages
- **Improved matplotlib integration** with modern plotting features

### Enhanced Visualization

- **Rich CLI output** with colored progress indicators
- **Interactive plotting** with zoom and pan capabilities
- **Export options** to multiple formats (PNG, PDF, SVG)
- **Customizable themes** and styling options

### Performance Improvements

- **Faster CSV parsing** with pandas integration
- **Memory-efficient** processing for large result files
- **Parallel processing** options for batch analysis

## Modern Usage Examples

### Using with Modern CLI

```bash
# Run optimization and generate plots automatically
flamingo run config.conf --output-dir results/
flamingo analyze results/optimization.csv --plot --save

# Interactive analysis
flamingo analyze results/optimization.csv --interactive
```

### Python API Usage

```python
from flamingo.utilities import ResultsAnalyzer

# Load and analyze results
analyzer = ResultsAnalyzer('results.csv')
analyzer.plot_optimization_progress()
analyzer.analyze_parameter_importance()
analyzer.export_summary_report('analysis_report.html')
```

## Integration with Main System

The utilities are now integrated with the main Flamingo system:

- **Automatic result processing** after optimization completion
- **Built-in visualization** through the CLI
- **Plugin system** for custom analysis tools
- **Export capabilities** to various formats

## Requirements

### Python Dependencies

```bash
pip install matplotlib numpy pandas scipy
```

### System Requirements

- **Python 3.10+** (originally required Python 2.5)
- **Matplotlib** for plotting
- **NumPy** for numerical computations
- **Pandas** for data manipulation (Python 3 version)

### Optional Dependencies

- **Gnuplot** (for gnuplot output)
- **MATLAB** (for MATLAB scripts)
- **Jupyter** (for interactive analysis notebooks)

## Migration from Python 2

The utilities maintain backward compatibility with Python 2 result files while providing enhanced functionality:

- **CSV format compatibility** preserved
- **Command-line interface** remains the same
- **Output formats** are compatible
- **Enhanced error handling** and validation

## See Also

- **[User Guide](user-guide.md)**: Complete user documentation
- **[Developer Guide](developer-guide.md)**: Development and contribution guidelines
- **[Testing Guide](testing-guide.md)**: Testing and validation procedures
- **[Credits](credits.md)**: Acknowledgments to Ben Spencer and contributors
