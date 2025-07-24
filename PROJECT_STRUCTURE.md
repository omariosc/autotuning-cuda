# Project Structure

This repository contains the Flamingo CUDA Autotuning System with a clean, organized structure:

## Directory Layout

```
flamingo-autotuner/
├── README.md                 # Main project documentation
├── PROJECT_STRUCTURE.md     # This file - explains the layout
├── docs/                    # All documentation files
│   ├── user-guide.md        # User documentation
│   ├── developer-guide.md   # Developer documentation  
│   ├── credits.md           # Credits to Ben Spencer
│   └── ...                  # Other guides
│
└── Autotuning/             # Main codebase directory
    ├── flamingo/           # Modern Python 3 framework
    ├── tuner/              # Ben Spencer's original core (converted)
    ├── examples/           # Demonstration programs
    ├── utilities/          # Analysis tools
    ├── tests/              # Test suite
    ├── pyproject.toml      # Python project configuration
    ├── Dockerfile          # Container configuration
    └── ...                 # Other code files
```

## Quick Start

1. **Read the documentation**: Start with [README.md](README.md)
2. **Navigate to code**: `cd Autotuning/`
3. **Install the system**: `pip install -e .`
4. **Run examples**: `cd examples/hello && flamingo run hello.conf`

## Documentation

All documentation is in the `docs/` folder for easy browsing and reference. The code is organized in the `Autotuning/` directory to keep the project structure clean and professional.

This structure ensures:
- **Clean separation** between documentation and code
- **Easy navigation** with logical grouping
- **Professional presentation** without long path names in examples
- **Simple setup** - just `cd Autotuning` to start working

## Credits

This project modernizes the exceptional original work of **Ben Spencer**. See [docs/credits.md](docs/credits.md) for full acknowledgments.