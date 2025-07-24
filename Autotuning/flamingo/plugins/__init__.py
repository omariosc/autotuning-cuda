"""
Plugin Architecture for Flamingo CUDA Autotuning System

This module provides a comprehensive plugin architecture that allows extending
Flamingo's functionality through external plugins.

PYTHON 2 CONVERSION: Original system had no plugin support.
This is a completely new modern plugin architecture using pluggy.
"""

from .manager import PluginManager
from .interface import (
    FlamingoPlugin, 
    OptimizationPlugin,
    EvaluationPlugin, 
    OutputPlugin,
    ConfigPlugin
)
from .registry import PluginRegistry
from .loader import PluginLoader

__all__ = [
    "PluginManager",
    "FlamingoPlugin", 
    "OptimizationPlugin",
    "EvaluationPlugin",
    "OutputPlugin", 
    "ConfigPlugin",
    "PluginRegistry",
    "PluginLoader"
]