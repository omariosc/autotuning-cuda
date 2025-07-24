# Examples Guide

**Original Author**: Ben Spencer  
**Python 3 Status**: All examples converted and enhanced  

This directory provides several example programs which demonstrate the autotuning system's capabilities. These examples are designed to show different aspects of the system and provide templates for your own optimization projects.

**Note**: These examples are described in detail in the original User's Guide: `doc/user.pdf`

## Available Examples

### hello/ - Simple Compilation Example

**Type**: Basic demonstration  
**Complexity**: Beginner  
**Purpose**: Simple test case that compiles a 'hello world' program

This example demonstrates the basic functionality of the autotuning system using a minimal C program. It's perfect for:

- Learning the configuration file format
- Understanding the basic optimization workflow
- Testing your installation
- First-time users getting familiar with the system

**Key Features:**

- Simple parameter space (compilation flags)
- Fast execution for quick testing
- Clear, understandable output

**Usage:**

```bash
cd examples/hello
flamingo run hello.conf
# or with legacy interface:
autotune hello.conf
```

### laplace3d/ - CUDA Test Case

**Type**: GPU optimization  
**Complexity**: Intermediate  
**Purpose**: A CUDA test case demonstrating GPU parameter tuning

This example shows how to optimize CUDA kernel parameters such as:

- Thread block dimensions
- Grid dimensions
- Memory access patterns
- Shared memory usage

**Key Features:**

- Real CUDA code optimization
- Multiple parameter interactions
- Performance measurement techniques
- GPU-specific considerations

**Requirements:**

- CUDA toolkit installed
- NVIDIA GPU with compute capability support
- NVCC compiler

**Usage:**

```bash
cd examples/laplace3d
flamingo run laplace3d.conf
```

### looping/ - Iteration Parameter Tuning

**Type**: Algorithmic optimization  
**Complexity**: Beginner-Intermediate  
**Purpose**: Simple test case where parameters control the number of loop iterations

This example demonstrates:

- Algorithm parameter optimization
- Performance scaling analysis
- Multiple repetition handling
- Statistical significance testing

**Key Features:**

- Clear parameter-performance relationship
- Educational value for understanding optimization
- Variable execution time demonstration

**Usage:**

```bash
cd examples/looping
flamingo run looping.conf
```

### maths/ - Custom Figure of Merit

**Type**: Custom optimization  
**Complexity**: Intermediate  
**Purpose**: Simple test case where parameters are processed using 'expr' with a custom figure of merit

This example shows:

- Custom scoring functions beyond simple timing
- Mathematical parameter combinations
- Complex optimization objectives
- Advanced configuration techniques

**Key Features:**

- Demonstrates custom figure of merit usage
- Mathematical expression evaluation
- Non-timing optimization objectives

**Usage:**

```bash
cd examples/maths
flamingo run maths.conf
```

### matlab/ - MATLAB Vectorization

**Type**: MATLAB optimization  
**Complexity**: Intermediate  
**Purpose**: A MATLAB program to determine the optimum level of 'strip-mining' vectorization

This example demonstrates:

- MATLAB integration with the autotuning system
- Vectorization optimization
- MATLAB-specific performance considerations
- Cross-language optimization support

**Requirements:**

- MATLAB installation
- MATLAB accessible from command line

**Key Features:**

- MATLAB code optimization
- Vectorization parameter tuning
- Performance analysis techniques

**Usage:**

```bash
cd examples/matlab
flamingo run matlab_test.conf
```

### matrix/ - Blocked Matrix Multiplication

**Type**: Algorithm optimization  
**Complexity**: Advanced  
**Purpose**: Blocked matrix multiplication test case with multiple sub-examples

This is the most comprehensive example, containing three sub-directories:

#### matrix/comparison/

**Purpose**: Compares the blocked and naive implementations

- Performance comparison tools
- Baseline establishment
- Optimization validation

#### matrix/modified/

**Purpose**: The modified, tunable version after changes from the tutorial

- Fully parameterized implementation
- Ready for optimization
- Tutorial integration

#### matrix/original/

**Purpose**: The original version, not ready for tuning (used by the tutorial)

- Shows transformation process
- Educational baseline
- Tutorial starting point

**Key Features:**

- Complex parameter interactions
- Real-world optimization scenario
- Multiple implementation variants
- Performance analysis tools

**Usage:**

```bash
# Run the tunable version
cd examples/matrix/modified
flamingo run matrix_tune.conf

# Compare implementations
cd examples/matrix/comparison
./compare_implementations.sh
```

## Python 3 Enhancements

All examples have been enhanced in the Python 3 version:

### Modern Configuration

- **Enhanced config validation** with detailed error messages
- **Type checking** for parameter values
- **Improved parameter space definition** syntax
- **Better error reporting** for configuration issues

### Enhanced Execution

- **Rich progress indicators** during optimization
- **Real-time performance monitoring**
- **Interactive execution** with user prompts
- **Graceful interruption** handling (Ctrl+C)

### Better Results

- **Comprehensive result logging** with metadata
- **Automatic visualization** generation
- **Statistical analysis** integration
- **Export to multiple formats** (CSV, JSON, HTML reports)

## Running Examples

### Modern CLI Interface

```bash
# Run with rich interface (from Autotuning directory)
flamingo run examples/hello/hello.conf

# Interactive mode with guidance
flamingo run examples/hello/hello.conf --interactive

# Run demo with automatic setup
flamingo demo --example hello

# Dry run to validate configuration
flamingo validate examples/hello/hello.conf
```

### Legacy Interface (Still Supported)

```bash
# Traditional method
cd examples/hello
autotune hello.conf

# Direct Python execution
python -m tuner.tune hello.conf
```

### Docker Execution

```bash
# Run in containerized environment (from Autotuning directory)
docker run -v $(pwd)/examples:/examples flamingo:latest run /examples/hello/hello.conf
```

## Creating Your Own Examples

### Basic Template

```ini
[variables]
variables = param1{val1,val2} * param2{val3,val4}

[values]
param1 = val1, val2, val3
param2 = val3, val4, val5

[testing]
compile = gcc -DPARAM1=%param1% -DPARAM2=%param2% -o program program.c
test = time ./program
clean = rm -f program

[scoring]
optimal = min_time
repeat = 5, avg

[output]
log = results.csv
```

### Best Practices

1. **Start simple** - Begin with a few parameters and expand
2. **Clear parameter names** - Use descriptive variable names
3. **Validate ranges** - Ensure parameter values make sense
4. **Test incrementally** - Verify each parameter works individually
5. **Document expectations** - Include comments about expected behavior

### Integration with Modern Features

```ini
[advanced]
parallel_evaluation = true
max_workers = 4
progress_callback = true

[plugins]
enabled = gpu-optimization, advanced-plotting

[visualization]
generate_plots = true
plot_format = png,pdf
interactive_plots = false
```

## Troubleshooting

### Common Issues

1. **Compilation errors** - Check compiler installation and flags
2. **Permission issues** - Ensure execute permissions on scripts
3. **Path problems** - Use absolute paths or correct relative paths
4. **CUDA issues** - Verify CUDA toolkit installation and GPU availability

### Getting Help

```bash
# Validate configuration
flamingo validate examples/hello/hello.conf

# Run in verbose mode
flamingo run examples/hello/hello.conf --verbose

# Check system requirements
flamingo --version
```

## Educational Value

These examples serve multiple educational purposes:

### For Beginners

- **hello/**: Learn basic concepts and configuration
- **looping/**: Understand parameter-performance relationships
- **maths/**: Explore custom optimization objectives

### For Intermediate Users

- **laplace3d/**: GPU optimization techniques
- **matlab/**: Cross-language integration
- **matrix/comparison**: Performance analysis methods

### For Advanced Users

- **matrix/modified**: Complex parameter interactions
- All examples: **Plugin development** and **custom optimization strategies**

## See Also

- **[User Guide](user-guide.md)**: Complete user documentation
- **[CLI Guide](cli-guide.md)**: Command-line interface documentation
- **[Migration Guide](migration-guide.md)**: Upgrading from Python 2 version
- **[Credits](credits.md)**: Acknowledgments to Ben Spencer and contributors

## Contributing Examples

We welcome new examples that demonstrate:

- Novel optimization scenarios
- Different programming languages
- Specialized hardware (GPUs, FPGAs, etc.)
- Custom optimization objectives

See the [Developer Guide](developer-guide.md) for contribution guidelines.
