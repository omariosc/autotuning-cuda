"""
Flamingo CUDA Autotuning System

A modern, fully-featured CUDA parameter optimization framework with rich CLI,
plugin architecture, and containerization support.

This is the Python 3.10+ modernized version of the original Python 2.5+ system.
"""

__version__ = "1.0.0"
__author__ = "Flamingo Development Team"
__email__ = "team@flamingo-autotuner.org"
__description__ = "Modern CUDA Autotuning System with Rich CLI and Plugin Architecture"

from typing import Dict, Any

# Core version info accessible to all modules
VERSION_INFO: Dict[str, Any] = {
    "version": __version__,
    "python_version_required": "3.10+",
    "original_version": "0.16 (Python 2.5+)",
    "conversion_date": "2024",
    "features": [
        "Rich CLI with colors and formatting",
        "Plugin architecture",
        "Docker containerization",
        "Migration tools",
        "TUI interface",
        "Modern Python 3.10+ codebase"
    ]
}

# Re-export key classes and functions for convenience
from .core.autotuner import AutotuningSystem
from .core.config import FlamingoConfig
from .plugins.manager import PluginManager

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    "VERSION_INFO",
    "AutotuningSystem",
    "FlamingoConfig", 
    "PluginManager"
]