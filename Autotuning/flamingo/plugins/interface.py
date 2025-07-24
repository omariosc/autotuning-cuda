"""
Plugin Interface Definitions

This module defines the plugin interfaces and base classes that plugins must implement.
Uses modern Python protocols and abstract base classes for type safety.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
from pathlib import Path
import pluggy

# Plugin specification for Flamingo
flamingo_spec = pluggy.PluginSpec("flamingo")


@runtime_checkable
class FlamingoPlugin(Protocol):
    """
    Base protocol for all Flamingo plugins.
    
    All plugins must implement this interface to be recognized by the plugin system.
    """
    
    name: str
    version: str
    description: str
    author: str
    
    def initialize(self, context: Dict[str, Any]) -> None:
        """Initialize the plugin with the given context."""
        ...
    
    def cleanup(self) -> None:
        """Cleanup resources when plugin is unloaded."""
        ...


@flamingo_spec
class OptimizationPlugin(ABC):
    """
    Plugin interface for custom optimization algorithms.
    
    Allows users to implement custom optimization strategies beyond the built-in ones.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this optimization algorithm."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return a description of this optimization algorithm."""
        pass
    
    @abstractmethod
    def optimize(
        self, 
        parameter_space: Dict[str, List[Any]],
        evaluator_func: callable,
        max_iterations: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run the optimization algorithm.
        
        Args:
            parameter_space: Dictionary mapping parameter names to possible values
            evaluator_func: Function to evaluate parameter combinations
            max_iterations: Maximum number of iterations to run
            **kwargs: Additional algorithm-specific parameters
            
        Returns:
            Dictionary containing optimization results
        """
        pass
    
    @abstractmethod
    def supports_parallel(self) -> bool:
        """Return True if this algorithm supports parallel evaluation."""
        pass


@flamingo_spec
class EvaluationPlugin(ABC):
    """
    Plugin interface for custom evaluation strategies.
    
    Allows users to implement custom ways of running and scoring tests.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this evaluation strategy."""
        pass
    
    @abstractmethod
    def evaluate(
        self,
        configuration: Dict[str, Any],
        test_commands: Dict[str, str],
        repetitions: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluate a specific configuration.
        
        Args:
            configuration: Parameter configuration to test
            test_commands: Commands to compile/test/clean
            repetitions: Number of times to repeat the test
            **kwargs: Additional evaluation parameters
            
        Returns:
            Dictionary containing evaluation results (score, timing, etc.)
        """
        pass
    
    @abstractmethod
    def supports_batch(self) -> bool:
        """Return True if this evaluator supports batch evaluation."""
        pass


@flamingo_spec  
class OutputPlugin(ABC):
    """
    Plugin interface for custom output formats and visualization.
    
    Allows users to implement custom ways of saving and displaying results.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this output format."""
        pass
    
    @abstractmethod 
    def get_file_extensions(self) -> List[str]:
        """Return list of file extensions this plugin handles."""
        pass
    
    @abstractmethod
    def save_results(
        self,
        results: Dict[str, Any],
        output_path: Path,
        **kwargs
    ) -> bool:
        """
        Save optimization results to file.
        
        Args:
            results: Optimization results to save
            output_path: Path to save results to
            **kwargs: Additional format-specific parameters
            
        Returns:
            True if save was successful, False otherwise
        """
        pass


@flamingo_spec
class ConfigPlugin(ABC):
    """
    Plugin interface for custom configuration formats.
    
    Allows users to implement support for additional configuration file formats.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this configuration format."""
        pass
    
    @abstractmethod
    def get_file_extensions(self) -> List[str]:
        """Return list of file extensions this plugin handles."""
        pass
    
    @abstractmethod
    def load_config(self, config_path: Path) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dictionary containing configuration data
        """
        pass
    
    @abstractmethod
    def save_config(self, config: Dict[str, Any], config_path: Path) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration data to save
            config_path: Path to save configuration to
            
        Returns:
            True if save was successful, False otherwise
        """
        pass


@flamingo_spec
class VisualizationPlugin(ABC):
    """
    Plugin interface for custom visualization and plotting.
    
    Allows users to implement custom ways of visualizing optimization results.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this visualization plugin."""
        pass
    
    @abstractmethod
    def get_supported_plot_types(self) -> List[str]:
        """Return list of plot types this plugin supports."""
        pass
    
    @abstractmethod
    def create_plot(
        self,
        data: Dict[str, Any],
        plot_type: str,
        output_path: Optional[Path] = None,
        **kwargs
    ) -> Any:
        """
        Create a plot/visualization.
        
        Args:
            data: Data to visualize
            plot_type: Type of plot to create
            output_path: Optional path to save plot to
            **kwargs: Additional plot parameters
            
        Returns:
            Plot object or True if successful
        """
        pass


class PluginMetadata:
    """Metadata container for plugin information."""
    
    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        author: str,
        email: str = "",
        url: str = "",
        license: str = "",
        tags: List[str] = None,
        dependencies: List[str] = None,
        min_flamingo_version: str = "1.0.0",
        python_requires: str = ">=3.10"
    ):
        self.name = name
        self.version = version  
        self.description = description
        self.author = author
        self.email = email
        self.url = url
        self.license = license
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.min_flamingo_version = min_flamingo_version
        self.python_requires = python_requires
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "email": self.email,
            "url": self.url,
            "license": self.license,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "min_flamingo_version": self.min_flamingo_version,
            "python_requires": self.python_requires
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginMetadata":
        """Create metadata from dictionary."""
        return cls(**data)


class BasePlugin(ABC):
    """
    Base implementation for Flamingo plugins.
    
    Provides common functionality that most plugins will need.
    """
    
    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self._initialized = False
        self._context: Optional[Dict[str, Any]] = None
    
    @property
    def name(self) -> str:
        """Plugin name."""
        return self.metadata.name
    
    @property
    def version(self) -> str:
        """Plugin version."""
        return self.metadata.version
    
    @property
    def description(self) -> str:
        """Plugin description."""
        return self.metadata.description
    
    @property
    def author(self) -> str:
        """Plugin author."""
        return self.metadata.author
    
    @property
    def is_initialized(self) -> bool:
        """Check if plugin is initialized."""
        return self._initialized
    
    def initialize(self, context: Dict[str, Any]) -> None:
        """Initialize the plugin with the given context."""
        self._context = context
        self._initialized = True
        self.on_initialize(context)
    
    def cleanup(self) -> None:
        """Cleanup resources when plugin is unloaded."""
        if self._initialized:
            self.on_cleanup()
            self._initialized = False
            self._context = None
    
    def get_context(self) -> Optional[Dict[str, Any]]:
        """Get the plugin context."""
        return self._context
    
    @abstractmethod
    def on_initialize(self, context: Dict[str, Any]) -> None:
        """Called when plugin is initialized. Override in subclasses."""
        pass
    
    @abstractmethod
    def on_cleanup(self) -> None:
        """Called when plugin is cleaned up. Override in subclasses."""
        pass


# Convenience functions for plugin developers
def create_optimization_plugin(
    name: str,
    version: str,
    description: str,
    author: str,
    optimize_func: callable,
    supports_parallel: bool = False,
    **metadata_kwargs
) -> OptimizationPlugin:
    """
    Create an optimization plugin from a simple function.
    
    This is a convenience function for creating simple optimization plugins
    without having to implement the full class interface.
    """
    
    class FunctionOptimizationPlugin(BasePlugin, OptimizationPlugin):
        def __init__(self):
            metadata = PluginMetadata(name, version, description, author, **metadata_kwargs)
            super().__init__(metadata)
            self.optimize_func = optimize_func
            self.parallel_support = supports_parallel
        
        def get_name(self) -> str:
            return self.name
        
        def get_description(self) -> str:
            return self.description
        
        def optimize(self, parameter_space, evaluator_func, max_iterations=None, **kwargs):
            return self.optimize_func(parameter_space, evaluator_func, max_iterations, **kwargs)
        
        def supports_parallel(self) -> bool:
            return self.parallel_support
        
        def on_initialize(self, context):
            pass
        
        def on_cleanup(self):
            pass
    
    return FunctionOptimizationPlugin()


def plugin_metadata(**kwargs) -> callable:
    """
    Decorator for adding metadata to plugin classes.
    
    Usage:
        @plugin_metadata(name="MyPlugin", version="1.0.0", ...)
        class MyPlugin(BasePlugin, OptimizationPlugin):
            ...
    """
    def decorator(cls):
        # Store metadata on the class
        cls._plugin_metadata = kwargs
        return cls
    return decorator