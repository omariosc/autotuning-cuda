"""
Plugin Manager for Flamingo

This module manages the loading, unloading, and lifecycle of plugins.
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, Union
import logging
from dataclasses import dataclass, field
import json
import pluggy

from .interface import (
    FlamingoPlugin, 
    OptimizationPlugin, 
    EvaluationPlugin,
    OutputPlugin,
    ConfigPlugin,
    VisualizationPlugin,
    PluginMetadata,
    flamingo_spec
)
from .registry import PluginRegistry
from .loader import PluginLoader

logger = logging.getLogger(__name__)


@dataclass
class PluginInfo:
    """Information about a loaded plugin."""
    name: str
    version: str
    description: str
    author: str
    plugin_type: str
    module_path: Optional[Path] = None
    enabled: bool = True
    loaded: bool = False
    instance: Optional[Any] = None
    metadata: Optional[PluginMetadata] = None
    error: Optional[str] = None


class PluginManager:
    """
    Central manager for all Flamingo plugins.
    
    Handles plugin discovery, loading, unloading, and lifecycle management.
    """
    
    def __init__(self, plugin_dirs: Optional[List[Path]] = None):
        """
        Initialize the plugin manager.
        
        Args:
            plugin_dirs: List of directories to search for plugins
        """
        self.plugin_dirs = plugin_dirs or self._get_default_plugin_dirs()
        self.registry = PluginRegistry()
        self.loader = PluginLoader()
        
        # Plugin manager using pluggy
        self.pm = pluggy.PluginManager("flamingo")
        self.pm.add_hookspecs(flamingo_spec)
        
        # Track loaded plugins
        self._loaded_plugins: Dict[str, PluginInfo] = {}
        self._plugin_instances: Dict[str, Any] = {}
        
        # Plugin type mappings
        self._plugin_types = {
            "optimization": OptimizationPlugin,
            "evaluation": EvaluationPlugin, 
            "output": OutputPlugin,
            "config": ConfigPlugin,
            "visualization": VisualizationPlugin
        }
    
    def _get_default_plugin_dirs(self) -> List[Path]:
        """Get default plugin directories."""
        dirs = []
        
        # Built-in plugins directory
        builtin_dir = Path(__file__).parent / "builtin"
        if builtin_dir.exists():
            dirs.append(builtin_dir)
        
        # User plugins directory
        user_dir = Path.home() / ".flamingo" / "plugins"
        if user_dir.exists():
            dirs.append(user_dir)
        
        # System plugins directory
        system_dir = Path("/usr/local/share/flamingo/plugins")
        if system_dir.exists():
            dirs.append(system_dir)
        
        return dirs
    
    def discover_plugins(self) -> List[Path]:
        """
        Discover all available plugins in the plugin directories.
        
        Returns:
            List of plugin file paths
        """
        plugin_files = []
        
        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                continue
            
            # Look for Python files
            for py_file in plugin_dir.rglob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                plugin_files.append(py_file)
            
            # Look for plugin packages
            for pkg_dir in plugin_dir.iterdir():
                if pkg_dir.is_dir() and (pkg_dir / "__init__.py").exists():
                    plugin_files.append(pkg_dir / "__init__.py")
        
        return plugin_files
    
    def load_plugins(self, plugin_names: Optional[List[str]] = None) -> None:
        """
        Load plugins from the plugin directories.
        
        Args:
            plugin_names: Specific plugin names to load. If None, loads all discovered plugins.
        """
        plugin_files = self.discover_plugins()
        
        for plugin_file in plugin_files:
            try:
                plugin_info = self.loader.load_plugin_file(plugin_file)
                
                if plugin_names and plugin_info.name not in plugin_names:
                    continue
                
                self._loaded_plugins[plugin_info.name] = plugin_info
                
                # Register with pluggy if it's a hookimpl
                if hasattr(plugin_info.instance, '__pluggy_hookimpls__'):
                    self.pm.register(plugin_info.instance, name=plugin_info.name)
                
                logger.info(f"Loaded plugin: {plugin_info.name} v{plugin_info.version}")
                
            except Exception as e:
                logger.error(f"Failed to load plugin from {plugin_file}: {e}")
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a specific plugin.
        
        Args:
            plugin_name: Name of plugin to unload
            
        Returns:
            True if unloaded successfully, False otherwise
        """
        if plugin_name not in self._loaded_plugins:
            logger.warning(f"Plugin not loaded: {plugin_name}")
            return False
        
        try:
            plugin_info = self._loaded_plugins[plugin_name]
            
            # Cleanup plugin instance
            if plugin_info.instance and hasattr(plugin_info.instance, 'cleanup'):
                plugin_info.instance.cleanup()
            
            # Unregister from pluggy
            if hasattr(plugin_info.instance, '__pluggy_hookimpls__'):
                self.pm.unregister(plugin_info.instance)
            
            # Remove from loaded plugins
            del self._loaded_plugins[plugin_name]
            
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a specific plugin.
        
        Args:
            plugin_name: Name of plugin to reload
            
        Returns:
            True if reloaded successfully, False otherwise
        """
        if plugin_name in self._loaded_plugins:
            if not self.unload_plugin(plugin_name):
                return False
        
        self.load_plugins([plugin_name])
        return plugin_name in self._loaded_plugins
    
    def get_plugin(self, plugin_name: str) -> Optional[Any]:
        """
        Get a loaded plugin instance by name.
        
        Args:
            plugin_name: Name of plugin to get
            
        Returns:
            Plugin instance or None if not found
        """
        plugin_info = self._loaded_plugins.get(plugin_name)
        return plugin_info.instance if plugin_info else None
    
    def list_plugins(self) -> List[PluginInfo]:
        """
        List all loaded plugins.
        
        Returns:
            List of plugin information
        """
        return list(self._loaded_plugins.values())
    
    def get_plugins_by_type(self, plugin_type: str) -> List[Any]:
        """
        Get all loaded plugins of a specific type.
        
        Args:
            plugin_type: Type of plugins to get (optimization, evaluation, etc.)
            
        Returns:
            List of plugin instances
        """
        plugins = []
        
        for plugin_info in self._loaded_plugins.values():
            if plugin_info.plugin_type == plugin_type and plugin_info.instance:
                plugins.append(plugin_info.instance)
        
        return plugins
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """
        Enable a plugin.
        
        Args:
            plugin_name: Name of plugin to enable
            
        Returns:
            True if enabled successfully, False otherwise
        """
        if plugin_name not in self._loaded_plugins:
            logger.warning(f"Plugin not loaded: {plugin_name}")
            return False
        
        plugin_info = self._loaded_plugins[plugin_name]
        plugin_info.enabled = True
        
        logger.info(f"Enabled plugin: {plugin_name}")
        return True
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        Disable a plugin.
        
        Args:
            plugin_name: Name of plugin to disable
            
        Returns:
            True if disabled successfully, False otherwise
        """
        if plugin_name not in self._loaded_plugins:
            logger.warning(f"Plugin not loaded: {plugin_name}")
            return False
        
        plugin_info = self._loaded_plugins[plugin_name]
        plugin_info.enabled = False
        
        logger.info(f"Disabled plugin: {plugin_name}")
        return True
    
    def install_plugin(self, plugin_source: Union[str, Path]) -> bool:
        """
        Install a plugin from a source (file, URL, or package name).
        
        Args:
            plugin_source: Source to install plugin from
            
        Returns:
            True if installed successfully, False otherwise
        """
        try:
            # Convert source to Path if it's a string
            if isinstance(plugin_source, str):
                # Check if it's a URL or package name
                if plugin_source.startswith(('http://', 'https://')):
                    # TODO: Implement URL download functionality
                    logger.error("URL-based plugin installation not yet supported")
                    return False
                elif '/' not in plugin_source and '\\' not in plugin_source:
                    # Assume it's a package name - could be implemented with pip in future
                    logger.error("Package-based plugin installation not yet supported")
                    return False
                else:
                    plugin_source = Path(plugin_source)
            
            source_path = Path(plugin_source)
            
            # Validate source exists
            if not source_path.exists():
                logger.error(f"Plugin source not found: {source_path}")
                return False
            
            # Determine installation directory (use first user plugin dir)
            install_dir = Path.home() / ".flamingo" / "plugins"
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # Handle different source types
            if source_path.is_file():
                # Single file plugin
                target_path = install_dir / source_path.name
                import shutil
                shutil.copy2(source_path, target_path)
                logger.info(f"Installed plugin file: {target_path}")
                
            elif source_path.is_dir():
                # Plugin package directory
                target_dir = install_dir / source_path.name
                if target_dir.exists():
                    logger.error(f"Plugin already exists: {target_dir}")
                    return False
                
                import shutil
                shutil.copytree(source_path, target_dir)
                logger.info(f"Installed plugin package: {target_dir}")
            
            else:
                logger.error(f"Invalid plugin source: {source_path}")
                return False
            
            # Try to load the newly installed plugin
            plugin_files = self.discover_plugins()
            newly_installed = [f for f in plugin_files if install_dir in f.parents]
            
            if newly_installed:
                # Load the new plugin
                for plugin_file in newly_installed:
                    try:
                        plugin_info = self.loader.load_plugin_file(plugin_file)
                        self._loaded_plugins[plugin_info.name] = plugin_info
                        logger.info(f"Successfully installed and loaded plugin: {plugin_info.name}")
                        return True
                    except Exception as e:
                        logger.error(f"Failed to load newly installed plugin: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to install plugin from {plugin_source}: {e}")
            return False
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """
        Uninstall a plugin completely.
        
        Args:
            plugin_name: Name of plugin to uninstall
            
        Returns:
            True if uninstalled successfully, False otherwise
        """
        # Unload plugin first
        if plugin_name in self._loaded_plugins:
            if not self.unload_plugin(plugin_name):
                return False
        
        # Remove plugin files from filesystem
        try:
            plugin_info = self._loaded_plugins.get(plugin_name)
            if not plugin_info or not plugin_info.module_path:
                logger.error(f"Cannot find plugin files for: {plugin_name}")
                return False
            
            plugin_path = plugin_info.module_path
            
            # Remove plugin file or directory
            import shutil
            if plugin_path.is_file():
                plugin_path.unlink()
                logger.info(f"Removed plugin file: {plugin_path}")
            elif plugin_path.is_dir():
                shutil.rmtree(plugin_path)
                logger.info(f"Removed plugin directory: {plugin_path}")
            else:
                # Check if it's part of a package
                parent_dir = plugin_path.parent
                if parent_dir.name != "__pycache__" and (parent_dir / "__init__.py").exists():
                    # Remove entire plugin package
                    shutil.rmtree(parent_dir)
                    logger.info(f"Removed plugin package: {parent_dir}")
                else:
                    logger.warning(f"Could not determine how to remove plugin: {plugin_path}")
                    return False
            
            logger.info(f"Successfully uninstalled plugin: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall plugin {plugin_name}: {e}")
            return False
    
    def get_available_optimization_algorithms(self) -> List[str]:
        """Get list of available optimization algorithm names."""
        plugins = self.get_plugins_by_type("optimization")
        return [plugin.get_name() for plugin in plugins]
    
    def get_available_evaluation_strategies(self) -> List[str]:
        """Get list of available evaluation strategy names."""
        plugins = self.get_plugins_by_type("evaluation")
        return [plugin.get_name() for plugin in plugins]
    
    def get_available_output_formats(self) -> List[str]:
        """Get list of available output format names."""
        plugins = self.get_plugins_by_type("output")
        return [plugin.get_name() for plugin in plugins]
    
    def create_optimization_algorithm(self, name: str, **kwargs) -> Optional[OptimizationPlugin]:
        """
        Create an instance of an optimization algorithm plugin.
        
        Args:
            name: Name of the optimization algorithm
            **kwargs: Additional parameters for the algorithm
            
        Returns:
            Algorithm instance or None if not found
        """
        plugins = self.get_plugins_by_type("optimization")
        
        for plugin in plugins:
            if plugin.get_name() == name:
                return plugin
        
        return None
    
    def save_plugin_state(self, config_file: Path) -> bool:
        """
        Save the current plugin state to a configuration file.
        
        Args:
            config_file: Path to save configuration to
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            state = {
                "plugin_dirs": [str(d) for d in self.plugin_dirs],
                "loaded_plugins": {},
                "enabled_plugins": []
            }
            
            for name, info in self._loaded_plugins.items():
                state["loaded_plugins"][name] = {
                    "name": info.name,
                    "version": info.version,
                    "plugin_type": info.plugin_type,
                    "module_path": str(info.module_path) if info.module_path else None
                }
                
                if info.enabled:
                    state["enabled_plugins"].append(name)
            
            with open(config_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save plugin state: {e}")
            return False
    
    def load_plugin_state(self, config_file: Path) -> bool:
        """
        Load plugin state from a configuration file.
        
        Args:
            config_file: Path to load configuration from
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(config_file, 'r') as f:
                state = json.load(f)
            
            # Update plugin directories
            if "plugin_dirs" in state:
                self.plugin_dirs = [Path(d) for d in state["plugin_dirs"]]
            
            # Load specified plugins
            if "loaded_plugins" in state:
                plugin_names = list(state["loaded_plugins"].keys())
                self.load_plugins(plugin_names)
            
            # Set enabled state
            if "enabled_plugins" in state:
                for name in self._loaded_plugins:
                    if name in state["enabled_plugins"]:
                        self.enable_plugin(name)
                    else:
                        self.disable_plugin(name)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load plugin state: {e}")
            return False
    
    def cleanup(self) -> None:
        """Cleanup all plugins and resources."""
        # Unload all plugins
        plugin_names = list(self._loaded_plugins.keys())
        for name in plugin_names:
            self.unload_plugin(name)
        
        # Clear registries
        self.registry.clear()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()