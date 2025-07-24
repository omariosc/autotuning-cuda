"""
Configuration Management for Flamingo

This module provides modern configuration handling with validation and type safety.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field
import configparser

from ..tuner.tune_conf import get_settings, ConfigurationError


@dataclass
class FlamingoConfig:
    """Modern configuration data structure for Flamingo."""
    
    variables: List[str] = field(default_factory=list)
    variable_values: Dict[str, List[str]] = field(default_factory=dict)
    test_command: str = ""
    compile_command: str = ""
    clean_command: str = ""
    optimization_direction: str = "min"
    repetitions: int = 1
    log_file: Optional[str] = None
    script_file: Optional[str] = None
    importance_file: Optional[str] = None
    
    @classmethod
    def from_file(cls, config_path: Path) -> "FlamingoConfig":
        """Load configuration from file."""
        try:
            # Use the legacy configuration loader
            settings = get_settings(config_path)
            
            # Extract variables from vartree
            from ..tuner.vartree import get_variables
            variables = get_variables(settings['vartree'])
            
            # Create modern config object
            return cls(
                variables=variables,
                variable_values=settings['possValues'],
                test_command=settings.get('test', ''),
                compile_command=settings.get('compile', ''),
                clean_command=settings.get('clean', ''),
                optimization_direction=settings.get('optimal', 'min'),
                repetitions=settings.get('repeat', 1),
                log_file=settings.get('log'),
                script_file=settings.get('script'),
                importance_file=settings.get('importance')
            )
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
    
    def save(self, config_path: Path) -> None:
        """Save configuration to file."""
        # Implementation would convert back to INI format
        # For now, just placeholder
        pass