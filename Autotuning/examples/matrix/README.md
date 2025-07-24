# Matrix Multiplication Example

**Original Author**: Ben Spencer  
**Example Type**: Advanced algorithm optimization  
**Python 3 Status**: Fully converted and enhanced

This example demonstrates advanced parameter optimization using blocked matrix multiplication. It's one of the most comprehensive examples in the autotuning system, showing real-world optimization techniques and performance analysis.

## Overview

This example is featured in the tutorial (`docs/tutorial.pdf`) and provides a complete workflow for optimizing blocked matrix multiplication algorithms. It demonstrates:

- **Algorithm parameter optimization** (block sizes, loop ordering)
- **Performance comparison** techniques
- **Baseline establishment** and validation
- **Step-by-step optimization** process

## Directory Structure

### original/
**Purpose**: Tutorial starting point  
**Status**: Original, unoptimized code

The code that the tutorial begins with. This represents a typical starting point before optimization:
- Basic matrix multiplication implementation
- No parameter substitution
- Fixed algorithm parameters
- Serves as educational baseline

**Usage**: Follow the tutorial to transform this code into the tunable version.

### modified/
**Purpose**: Fully tunable implementation  
**Status**: Ready for optimization

The final code used for tuning in the tutorial. This version includes:
- **Parameterized block sizes** for optimization
- **Configurable loop ordering** strategies
- **Performance measurement** integration
- **Parameter substitution** throughout the code

**Usage**:
```bash
cd modified/
flamingo run matrix_tune.conf
# or with legacy interface:
autotune matrix_tune.conf
```

### comparison/
**Purpose**: Performance validation and comparison  
**Status**: Comparative analysis tools

This version performs both naive and blocked multiplication and compares them. This demonstrates a common pattern in high-performance computing:
- **Naive implementation** as baseline
- **Optimized blocked implementation** for comparison  
- **Gold standard verification** ensuring correctness
- **Performance analysis** between approaches

This pattern is especially common in GPU code development, where:
- CPU implementation serves as the "gold" reference
- GPU implementation is developed and tuned
- Correctness is validated against the reference
- Performance improvements are quantified

**Usage**:
```bash
cd comparison/
./run_comparison.sh
```

## Tutorial Integration

This example is designed to work with Ben Spencer's comprehensive tutorial:

1. **Start with `original/`** - Understand the baseline algorithm
2. **Follow tutorial steps** - Learn optimization techniques
3. **Transform to `modified/`** - Apply parameterization
4. **Use `comparison/`** - Validate and analyze results

The tutorial covers:
- **Parameter identification** - Which values to optimize
- **Configuration setup** - How to write effective config files
- **Result interpretation** - Understanding optimization outcomes
- **Performance analysis** - Measuring and comparing improvements

## Key Learning Objectives

### Algorithm Optimization
- **Block size selection** for cache efficiency
- **Loop ordering** for memory access patterns
- **Parameter interactions** and their effects
- **Search space exploration** strategies

### Performance Engineering
- **Baseline establishment** for comparison
- **Measurement techniques** for accurate timing
- **Statistical significance** in performance testing
- **Optimization validation** methods

### Practical Skills
- **Code parameterization** techniques
- **Configuration file design** best practices
- **Result analysis** and interpretation
- **Performance debugging** approaches

## Python 3 Enhancements

The matrix example has been enhanced in the Python 3 version:

### Modern Build System
- **Enhanced Makefile** with modern compiler flags
- **Improved error handling** during compilation
- **Better dependency management** 
- **Cross-platform compatibility** improvements

### Advanced Configuration
- **Extended parameter ranges** for modern hardware
- **GPU-aware optimization** options
- **Parallel compilation** support
- **Enhanced validation** checks

### Rich Analysis
- **Automatic performance profiling**
- **Memory usage analysis**
- **Cache behavior investigation** 
- **Advanced visualization** of results

## Configuration Examples

### Basic Optimization
```ini
[variables]
variables = block_size{16,32,64} * tile_size{4,8,16}

[values]
block_size = 16, 32, 64, 128
tile_size = 4, 8, 16, 32

[testing]
compile = gcc -O3 -DBLOCK_SIZE=%block_size% -DTILE_SIZE=%tile_size% -o matrix matrix.c
test = time ./matrix 1024 1024 1024
clean = rm -f matrix

[scoring]
optimal = min_time
repeat = 5, avg
```

### Advanced Configuration
```ini
[variables]
variables = block_i{16,32,64} * block_j{16,32,64} * block_k{16,32,64} * unroll{2,4,8}

[advanced]
parallel_evaluation = true
max_workers = 4

[plugins]
enabled = cache-analyzer, memory-profiler
```

## Expected Results

### Performance Improvements
- **Typical speedup**: 2-5x over naive implementation
- **Cache efficiency**: Significant reduction in cache misses
- **Memory bandwidth**: Better utilization of available bandwidth
- **Scalability**: Improved performance across different matrix sizes

### Parameter Insights
- **Block size sweet spots** around 32-64 for many architectures
- **Cache line alignment** effects on performance
- **Memory hierarchy** optimization opportunities
- **Architecture-specific** optimal configurations

## Troubleshooting

### Common Issues
1. **Compilation errors**: Check compiler version and flags
2. **Memory issues**: Ensure sufficient RAM for large matrices
3. **Performance variations**: Run multiple repetitions for stability
4. **Platform differences**: Results vary across different hardware

### Performance Tips
1. **Use appropriate matrix sizes** for your hardware
2. **Consider cache sizes** when selecting block dimensions
3. **Monitor memory usage** during optimization
4. **Validate results** against reference implementation

## See Also

- **[Examples Guide](../docs/examples-guide.md)**: Complete guide to all examples
- **[User Guide](../docs/user-guide.md)**: General usage documentation
- **[Tutorial](../docs/tutorial.pdf)**: Ben Spencer's comprehensive tutorial
- **[Credits](../docs/credits.md)**: Acknowledgments to Ben Spencer

## Contributing

This example serves as a template for creating advanced optimization scenarios. Consider contributing:
- **New algorithms** for optimization
- **Different programming languages** (C++, CUDA, OpenMP)
- **Platform-specific optimizations** 
- **Enhanced analysis tools**

The matrix multiplication example represents the gold standard for demonstrating the autotuning system's capabilities, thanks to Ben Spencer's thoughtful design and comprehensive tutorial integration.