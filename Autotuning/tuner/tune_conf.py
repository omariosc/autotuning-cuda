"""
CUDA Autotuning System - Configuration Management

tune_conf.py

Sets up the configuration for the optimization. The settings (variable names, 
testing methods, etc.) are read from a configuration file provided.

PYTHON 2 TO 3 CONVERSION NOTES:
- Changed from ConfigParser to configparser (lowercase module name in Python 3)
- Changed RawConfigParser to configparser.RawConfigParser  
- Converted all print statements to print() functions
- Changed .iteritems() to .items() for Python 3 dictionary iteration (lines 90, 102, 117)
- Changed exit() to sys.exit() for better practice
- Added comprehensive type hints throughout
- Modernized string formatting and error handling
- Added dataclass for configuration structure
- Enhanced error messages with f-strings
"""

import configparser
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Callable, Optional, Any, Union

from .vartree import get_variables
from .helpers import avg, med


@dataclass
class AutotuningConfig:
    """
    Configuration data structure for autotuning system.
    
    PYTHON 2 CONVERSION: Original used plain dictionary.
    Modernized to use dataclass for better type safety and validation.
    """
    vartree: str
    possValues: Dict[str, List[str]]
    compile: Optional[str] = None
    test: Optional[str] = None
    clean: Optional[str] = None
    compile_mkStr: Optional[Callable[[int, Dict[str, Any]], str]] = None
    test_mkStr: Optional[Callable[[int, Dict[str, Any]], str]] = None
    clean_mkStr: Optional[Callable[[int, Dict[str, Any]], str]] = None
    optimal: str = "min"
    custom_fom: bool = False
    repeat: int = 1
    overall: str = "min"
    aggregator: Callable[[List[float]], float] = min
    log: Optional[str] = None
    script: Optional[str] = None
    importance: Optional[str] = None


class ConfigurationError(Exception):
    """
    Custom exception for configuration-related errors.
    
    PYTHON 2 CONVERSION: Original used generic exit() calls.
    Modernized to use proper exception handling.
    """
    pass


def _create_command_function(template: str, command_type: str) -> Callable[[int, Dict[str, Any]], str]:
    """
    Create a command string function for compile/test/clean operations.
    
    PYTHON 2 CONVERSION: Original used nested function definitions with .iteritems().
    Modernized to use factory function with .items() and f-strings.
    
    Args:
        template: Command template string with placeholders
        command_type: Type of command (for error reporting)
        
    Returns:
        Function that generates command strings
    """
    def make_command_string(test_id: int, var_dict: Dict[str, Any]) -> str:
        """Generate command string by substituting variables."""
        command = template.replace("%%ID%%", str(test_id))
        
        # PYTHON 2 CONVERSION: Changed .iteritems() to .items()
        for var_name, var_value in var_dict.items():
            placeholder = f"%{var_name}%"
            command = command.replace(placeholder, str(var_value))
            
        return command
    
    make_command_string.__name__ = f"{command_type}_mkStr"
    return make_command_string


def _validate_required_sections(config: configparser.RawConfigParser, config_file: Union[str, Path]) -> None:
    """
    Validate that all required sections exist in the configuration file.
    
    PYTHON 2 CONVERSION: Original used print and exit() (lines 35-42).
    Modernized to use proper exception handling with detailed error messages.
    """
    required_sections = ['variables', 'values', 'testing', 'scoring', 'output']
    missing_sections = [section for section in required_sections if not config.has_section(section)]
    
    if missing_sections:
        raise ConfigurationError(
            f"Configuration file '{config_file}' is missing required sections: {', '.join(missing_sections)}\\n"
            f"Required sections: {', '.join(required_sections)}"
        )


def _validate_variables_section(config: configparser.RawConfigParser, config_file: Union[str, Path]) -> str:
    """
    Validate and extract the variables section.
    
    PYTHON 2 CONVERSION: Original used print and exit() (lines 46-48).
    Modernized with proper exception handling.
    """
    if not config.has_option("variables", "variables"):
        raise ConfigurationError(
            f"Configuration file '{config_file}' does not contain the option 'variables' "
            "in section [variables]."
        )
    
    return config.get("variables", "variables")


def _validate_and_extract_values(config: configparser.RawConfigParser, variables: List[str], 
                                config_file: Union[str, Path]) -> Dict[str, List[str]]:
    """
    Validate and extract possible values for all variables.
    
    PYTHON 2 CONVERSION: Original used list comprehension with all() (lines 60-62).
    Enhanced with better error reporting and type safety.
    """
    missing_variables = [var for var in variables if not config.has_option("values", var)]
    
    if missing_variables:
        raise ConfigurationError(
            f"Configuration file '{config_file}' does not contain possible values "
            f"(in [values] section) for variables: {', '.join(missing_variables)}"
        )
    
    poss_values = {}
    for var in variables:
        raw_values = config.get("values", var)
        poss_values[var] = [x.strip() for x in raw_values.split(",")]
    
    return poss_values


def _setup_commands(config: configparser.RawConfigParser, config_file: Union[str, Path]) -> tuple:
    """
    Set up compile, test, and clean command generators.
    
    PYTHON 2 CONVERSION: Original had inline function definitions (lines 85-122).
    Modernized to use factory function and better error handling.
    
    Returns:
        Tuple of (compile_info, test_info, clean_info) where each is (template, function)
    """
    compile_template = None
    compile_mkStr = None
    if config.has_option("testing", "compile"):
        compile_template = config.get('testing', 'compile')
        compile_mkStr = _create_command_function(compile_template, "compile")
    
    test_template = None
    test_mkStr = None
    if config.has_option('testing', 'test'):
        test_template = config.get('testing', 'test')
        test_mkStr = _create_command_function(test_template, "test")
    else:
        raise ConfigurationError(
            f"Configuration file '{config_file}' does not contain option 'test' "
            "in section [testing]."
        )
    
    clean_template = None
    clean_mkStr = None
    if config.has_option('testing', 'clean'):
        clean_template = config.get('testing', 'clean')
        clean_mkStr = _create_command_function(clean_template, "clean")
    
    return (
        (compile_template, compile_mkStr),
        (test_template, test_mkStr),
        (clean_template, clean_mkStr)
    )


def _setup_scoring(config: configparser.RawConfigParser, config_file: Union[str, Path]) -> tuple:
    """
    Set up scoring configuration (optimal direction and repetition settings).
    
    PYTHON 2 CONVERSION: Original had complex if/else logic (lines 127-173).
    Modernized with better validation and clearer structure.
    
    Returns:
        Tuple of (optimal, custom_fom, repeat, overall, aggregator)
    """
    # Handle optimal setting
    optimal = "min"
    custom_fom = False
    
    if config.has_option('scoring', 'optimal'):
        optimal_setting = config.get('scoring', 'optimal').lower()
        
        if optimal_setting in ['max_time', 'min_time', 'max', 'min']:
            optimal = optimal_setting[:3]
            custom_fom = len(optimal_setting) == 3
        else:
            raise ConfigurationError(
                f"Configuration file '{config_file}' contains an invalid setting for 'optimal' "
                f"in section [scoring]. Got '{optimal_setting}', expected one of: "
                "max_time, min_time, max, min"
            )
    
    # Handle repeat setting
    repeat = 1
    overall = "min"
    aggregator = min
    
    if config.has_option('scoring', 'repeat'):
        repeat_setting = config.get('scoring', 'repeat')
        
        # PYTHON 2 CONVERSION: Original used .partition() method (line 143)
        parts = repeat_setting.partition(',')
        
        try:
            repeat = int(parts[0])
            if repeat < 1:
                raise ValueError("Option 'repeat' must be at least 1.")
        except ValueError as e:
            raise ConfigurationError(
                f"Configuration file '{config_file}' contains an invalid setting for 'repeat' "
                f"in section [scoring]. {str(e)}"
            )
        
        if parts[1] == '':
            # Only number of repetitions specified, default to 'min'
            overall = 'min'
            aggregator = min
        else:
            # Aggregation method specified
            agg_method = parts[2].lower().strip()
            aggregator_map = {
                'max': max, 
                'min': min, 
                'med': med, 
                'avg': avg
            }
            
            if agg_method in aggregator_map:
                overall = agg_method
                aggregator = aggregator_map[agg_method]
            else:
                raise ConfigurationError(
                    f"Configuration file '{config_file}' contains an invalid aggregation method "
                    f"for 'repeat' in section [scoring]. Got '{agg_method}', "
                    "expected one of: max, min, med, avg"
                )
    
    return optimal, custom_fom, repeat, overall, aggregator


def _get_output_settings(config: configparser.RawConfigParser) -> tuple:
    """
    Extract output-related settings from configuration.
    
    PYTHON 2 CONVERSION: Original had simple if/else blocks (lines 178-204).
    Consolidated into single function for better organization.
    
    Returns:
        Tuple of (log_file, script_file, importance_file)
    """
    log_file = config.get('output', 'log') if config.has_option('output', 'log') else None
    script_file = config.get('output', 'script') if config.has_option('output', 'script') else None
    importance_file = config.get('output', 'importance') if config.has_option('output', 'importance') else None
    
    return log_file, script_file, importance_file


def get_settings(config_file: Union[str, Path]) -> Dict[str, Any]:
    """
    Load and validate configuration settings from a configuration file.
    
    PYTHON 2 CONVERSION: Original function had procedural approach (lines 18-209).
    Modernized with better error handling, type hints, and structured validation.
    
    Args:
        config_file: Path to the configuration file
        
    Returns:
        Dictionary containing all configuration settings
        
    Raises:
        ConfigurationError: If configuration file is invalid or missing required settings
        FileNotFoundError: If configuration file doesn't exist
    """
    config_path = Path(config_file)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    # PYTHON 2 CONVERSION: Changed from ConfigParser.RawConfigParser to configparser.RawConfigParser
    config = configparser.RawConfigParser()
    
    try:
        config.read(str(config_path))
    except Exception as e:
        raise ConfigurationError(f"Error reading configuration file '{config_file}': {e}")
    
    # Validate required sections
    _validate_required_sections(config, config_file)
    
    # Extract and validate variables
    var_tree = _validate_variables_section(config, config_file)
    variables = get_variables(var_tree)
    poss_values = _validate_and_extract_values(config, variables, config_file)
    
    # Set up commands
    compile_info, test_info, clean_info = _setup_commands(config, config_file)
    
    # Set up scoring
    optimal, custom_fom, repeat, overall, aggregator = _setup_scoring(config, config_file)
    
    # Get output settings
    log_file, script_file, importance_file = _get_output_settings(config)
    
    # Build settings dictionary for backward compatibility
    # PYTHON 2 CONVERSION: Original returned plain dictionary
    settings = {
        'vartree': var_tree,
        'possValues': poss_values,
        'compile': compile_info[0],
        'compile_mkStr': compile_info[1],
        'test': test_info[0],
        'test_mkStr': test_info[1],
        'clean': clean_info[0],
        'clean_mkStr': clean_info[1],
        'optimal': optimal,
        'custom_fom': custom_fom,
        'repeat': repeat,
        'overall': overall,
        'aggregator': aggregator,
        'log': log_file,
        'script': script_file,
        'importance': importance_file,
    }
    
    return settings


def load_config_as_dataclass(config_file: Union[str, Path]) -> AutotuningConfig:
    """
    Load configuration as a modern dataclass (alternative to dictionary approach).
    
    PYTHON 2 CONVERSION: This is a new function providing a more modern interface.
    Original only provided dictionary-based configuration.
    
    Args:
        config_file: Path to the configuration file
        
    Returns:
        AutotuningConfig dataclass instance
    """
    settings = get_settings(config_file)
    
    return AutotuningConfig(
        vartree=settings['vartree'],
        possValues=settings['possValues'],
        compile=settings['compile'],
        compile_mkStr=settings['compile_mkStr'],
        test=settings['test'],
        test_mkStr=settings['test_mkStr'],
        clean=settings['clean'],
        clean_mkStr=settings['clean_mkStr'],
        optimal=settings['optimal'],
        custom_fom=settings['custom_fom'],
        repeat=settings['repeat'],
        overall=settings['overall'],
        aggregator=settings['aggregator'],
        log=settings['log'],
        script=settings['script'],
        importance=settings['importance'],
    )


if __name__ == "__main__":
    # PYTHON 2 CONVERSION: Changed print __doc__ to print(__doc__)
    print(__doc__)