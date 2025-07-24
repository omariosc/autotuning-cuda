"""
Configuration and Code Conversion Tools

This module provides tools to convert Python 2 configuration files and code
to the new Python 3 format with modern features.
"""

import re
import configparser
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import logging

from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table

logger = logging.getLogger(__name__)
console = Console()


@dataclass
class ConversionResult:
    """Results of a conversion operation."""
    success: bool
    original_file: Path
    converted_file: Optional[Path] = None
    changes: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class ConfigConverter:
    """
    Convert Python 2 configuration files to Python 3 format.
    
    Handles the conversion of old INI-style configuration files to the new
    enhanced format with additional validation and modern features.
    """
    
    def __init__(self):
        self.changes_made: List[str] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []
    
    def convert_file(self, input_file: Path, output_file: Optional[Path] = None) -> ConversionResult:
        """
        Convert a Python 2 configuration file to Python 3 format.
        
        Args:
            input_file: Path to the original configuration file
            output_file: Path for the converted file (defaults to input_file.py3.conf)
            
        Returns:
            ConversionResult with details of the conversion
        """
        self.changes_made.clear()
        self.warnings.clear()
        self.errors.clear()
        
        if not input_file.exists():
            error = f"Input file does not exist: {input_file}"
            self.errors.append(error)
            return ConversionResult(False, input_file, errors=[error])
        
        if output_file is None:
            output_file = input_file.with_suffix('.py3.conf')
        
        try:
            # Read original configuration
            original_config = self._read_legacy_config(input_file)
            
            # Convert to new format
            new_config = self._convert_config_format(original_config)
            
            # Add modern enhancements
            enhanced_config = self._add_modern_features(new_config)
            
            # Write converted configuration
            self._write_modern_config(enhanced_config, output_file)
            
            return ConversionResult(
                success=True,
                original_file=input_file,
                converted_file=output_file,
                changes=self.changes_made.copy(),
                warnings=self.warnings.copy(),
                errors=self.errors.copy()
            )
            
        except Exception as e:
            error = f"Conversion failed: {str(e)}"
            self.errors.append(error) 
            logger.error(error, exc_info=True)
            
            return ConversionResult(
                success=False,
                original_file=input_file,
                errors=self.errors.copy()
            )
    
    def _read_legacy_config(self, config_file: Path) -> Dict[str, Any]:
        """Read legacy Python 2 configuration file."""
        config = configparser.RawConfigParser()
        
        # Handle potential encoding issues from Python 2 files
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config.read_file(f)
        except UnicodeDecodeError:
            # Try with latin-1 encoding (common in older files)
            with open(config_file, 'r', encoding='latin-1') as f:
                config.read_file(f)
            self.warnings.append("File encoding converted from latin-1 to utf-8")
        
        # Convert to dictionary format
        result = {}
        for section_name in config.sections():
            result[section_name] = {}
            for key in config.options(section_name):
                result[section_name][key] = config.get(section_name, key)
        
        return result
    
    def _convert_config_format(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert configuration format with Python 2 to 3 changes."""
        new_config = {}
        
        # Process each section
        for section, items in config.items():
            new_section = {}
            
            if section == "variables":
                new_section = self._convert_variables_section(items)
            elif section == "values": 
                new_section = self._convert_values_section(items)
            elif section == "testing":
                new_section = self._convert_testing_section(items)
            elif section == "scoring":
                new_section = self._convert_scoring_section(items)
            elif section == "output":
                new_section = self._convert_output_section(items)
            else:
                # Copy unknown sections as-is with warning
                new_section = items.copy()
                self.warnings.append(f"Unknown section '{section}' copied as-is")
            
            new_config[section] = new_section
        
        return new_config
    
    def _convert_variables_section(self, items: Dict[str, str]) -> Dict[str, str]:
        """Convert variables section."""
        new_section = {}
        
        for key, value in items.items():
            if key == "variables":
                # Update variable syntax if needed
                new_value = self._update_variable_syntax(value)
                new_section[key] = new_value
                if new_value != value:
                    self.changes_made.append(f"Updated variable syntax: {value} -> {new_value}")
            else:
                new_section[key] = value
        
        return new_section
    
    def _convert_values_section(self, items: Dict[str, str]) -> Dict[str, str]:
        """Convert values section."""
        new_section = {}
        
        for key, value in items.items():
            # Clean up value lists (remove extra whitespace, normalize separators)
            cleaned_value = self._clean_value_list(value)
            new_section[key] = cleaned_value
            
            if cleaned_value != value:
                self.changes_made.append(f"Cleaned value list for {key}: {value} -> {cleaned_value}")
        
        return new_section
    
    def _convert_testing_section(self, items: Dict[str, str]) -> Dict[str, str]:
        """Convert testing section."""
        new_section = {}
        
        for key, value in items.items():
            if key in ["compile", "test", "clean"]:
                # Update command syntax for Python 3
                new_value = self._update_command_syntax(value)
                new_section[key] = new_value
                if new_value != value:
                    self.changes_made.append(f"Updated {key} command syntax")
            else:
                new_section[key] = value
        
        return new_section
    
    def _convert_scoring_section(self, items: Dict[str, str]) -> Dict[str, str]:
        """Convert scoring section."""
        new_section = {}
        
        for key, value in items.items():
            if key == "optimal":
                # Validate and normalize optimal values
                if value.lower() in ["min", "max", "min_time", "max_time"]:
                    new_section[key] = value.lower()
                else:
                    self.warnings.append(f"Unknown optimal value '{value}', defaulting to 'min'")
                    new_section[key] = "min"
                    self.changes_made.append("Set optimal to 'min' due to invalid value")
            elif key == "repeat":
                # Validate repeat syntax
                new_value = self._validate_repeat_syntax(value)
                new_section[key] = new_value
                if new_value != value:
                    self.changes_made.append(f"Fixed repeat syntax: {value} -> {new_value}")
            else:
                new_section[key] = value
        
        return new_section
    
    def _convert_output_section(self, items: Dict[str, str]) -> Dict[str, str]:
        """Convert output section."""
        new_section = {}
        
        for key, value in items.items():
            if key in ["log", "script", "importance"]:
                # Update file paths to use modern conventions
                new_value = self._modernize_file_path(value)
                new_section[key] = new_value
                if new_value != value:
                    self.changes_made.append(f"Modernized {key} file path")
            else:
                new_section[key] = value
        
        return new_section
    
    def _add_modern_features(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Add modern features and enhancements to the configuration."""
        
        # Add new sections for modern features
        if "advanced" not in config:
            config["advanced"] = {
                "parallel_evaluation": "false",
                "plugin_support": "true",
                "rich_output": "true",
                "type_checking": "true"
            }
            self.changes_made.append("Added [advanced] section with modern features")
        
        if "plugins" not in config:
            config["plugins"] = {
                "enabled": "",
                "search_paths": "~/.flamingo/plugins,./plugins"
            }
            self.changes_made.append("Added [plugins] section for plugin support")
        
        if "logging" not in config:
            config["logging"] = {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": ""
            }
            self.changes_made.append("Added [logging] section for enhanced logging")
        
        return config
    
    def _update_variable_syntax(self, variables: str) -> str:
        """Update variable syntax for modern format."""
        # Handle common patterns that might need updating
        updated = variables
        
        # Example transformations (customize based on actual needs)
        # Replace old bracket syntax with new if needed
        if "{" in updated and "}" in updated:
            # Validate bracket syntax is correct
            if not self._validate_bracket_syntax(updated):
                self.warnings.append("Variable syntax may need manual review")
        
        return updated
    
    def _clean_value_list(self, value_list: str) -> str:
        """Clean up value lists by normalizing whitespace and separators."""
        # Split by comma, strip whitespace, rejoin
        values = [v.strip() for v in value_list.split(",")]
        return ", ".join(v for v in values if v)  # Remove empty values
    
    def _update_command_syntax(self, command: str) -> str:
        """Update command syntax for Python 3 compatibility."""
        updated = command
        
        # Replace python2 with python3 if found
        updated = re.sub(r'\\bpython2\\b', 'python3', updated)
        updated = re.sub(r'\\bpython\\b(?!3)', 'python3', updated)
        
        # Update print statements in commands (if any Python code)
        if 'print ' in updated:
            self.warnings.append("Command contains 'print' statement - manual review recommended")
        
        return updated
    
    def _validate_repeat_syntax(self, repeat_value: str) -> str:
        """Validate and fix repeat syntax."""
        # Handle "number, aggregation" format
        if "," in repeat_value:
            parts = repeat_value.split(",", 1)
            try:
                num = int(parts[0].strip())
                agg = parts[1].strip().lower()
                
                if agg not in ["min", "max", "avg", "med"]:
                    self.warnings.append(f"Unknown aggregation '{agg}', defaulting to 'avg'")
                    agg = "avg"
                
                return f"{num}, {agg}"
            except ValueError:
                self.warnings.append(f"Invalid repeat format '{repeat_value}', defaulting to '1'")
                return "1"
        else:
            # Just a number
            try:
                num = int(repeat_value.strip())
                return str(num)
            except ValueError:
                self.warnings.append(f"Invalid repeat number '{repeat_value}', defaulting to '1'")
                return "1"
    
    def _modernize_file_path(self, file_path: str) -> str:
        """Modernize file paths using current conventions."""
        # Convert to use modern path separators and conventions
        path = Path(file_path)
        
        # Use .csv extension for log files if not specified
        if path.suffix == "" and "log" in file_path:
            return str(path.with_suffix(".csv"))
        
        return file_path
    
    def _validate_bracket_syntax(self, variables: str) -> bool:
        """Validate that bracket syntax is correct."""
        # Simple bracket matching
        bracket_count = 0
        for char in variables:
            if char == "{":
                bracket_count += 1
            elif char == "}":
                bracket_count -= 1
                if bracket_count < 0:
                    return False
        
        return bracket_count == 0
    
    def _write_modern_config(self, config: Dict[str, Any], output_file: Path) -> None:
        """Write the converted configuration to file."""
        
        # Create new config parser
        parser = configparser.ConfigParser()
        
        # Add header comment
        header_comment = f"""# Flamingo CUDA Autotuning System Configuration (Python 3)
# Converted from Python 2 configuration
# 
# This configuration file has been automatically converted to work with
# the Python 3.10+ version of Flamingo. Please review the changes and
# update any paths or commands as needed.
#
# Changes made during conversion:
"""
        
        for change in self.changes_made:
            header_comment += f"#   - {change}\\n"
        
        if self.warnings:
            header_comment += "#\\n# Warnings:\\n"
            for warning in self.warnings:
                header_comment += f"#   - {warning}\\n"
        
        header_comment += "\\n"
        
        # Add sections
        for section_name, section_data in config.items():
            parser.add_section(section_name)
            for key, value in section_data.items():
                parser.set(section_name, key, str(value))
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(header_comment)
            parser.write(f, space_around_delimiters=True)
    
    def get_conversion_summary(self) -> List[str]:
        """Get a summary of changes made during conversion."""
        return self.changes_made.copy()


class CodeConverter:
    """
    Convert Python 2 code snippets and scripts to Python 3.
    
    Provides automated conversion of common Python 2 to 3 patterns found
    in user scripts and configuration templates.
    """
    
    def __init__(self):
        self.conversion_rules = [
            # Print statements
            (r'print\\s+([^\\n]+)', r'print(\\1)'),
            
            # String exceptions
            (r'except\\s+(\\w+),\\s*(\\w+):', r'except \\1 as \\2:'),
            
            # Dictionary methods
            (r'\\.iteritems\\(\\)', '.items()'),
            (r'\\.iterkeys\\(\\)', '.keys()'),
            (r'\\.itervalues\\(\\)', '.values()'),
            
            # Input function
            (r'raw_input\\(', 'input('),
            
            # Integer division (context-dependent, may need manual review)
            (r'(\\w+)\\s*/\\s*(\\w+)(?!\\w)', r'\\1 // \\2  # Review: was / in Python 2'),
            
            # Import statements
            (r'import ConfigParser', 'import configparser'),
            (r'from ConfigParser import', 'from configparser import'),
            
            # Unicode strings (u'' prefix no longer needed in Python 3)
            (r"u['\"]([^'\"]*)['\"]", r"'\\1'"),
        ]
    
    def convert_code(self, code: str) -> Tuple[str, List[str]]:
        """
        Convert Python 2 code to Python 3.
        
        Args:
            code: Python 2 code string
            
        Returns:
            Tuple of (converted_code, list_of_changes)
        """
        converted = code
        changes = []
        
        for pattern, replacement in self.conversion_rules:
            matches = re.findall(pattern, converted)
            if matches:
                converted = re.sub(pattern, replacement, converted)
                changes.append(f"Applied rule: {pattern} -> {replacement}")
        
        return converted, changes
    
    def convert_file(self, input_file: Path, output_file: Optional[Path] = None) -> ConversionResult:
        """
        Convert a Python 2 script file to Python 3.
        
        Args:
            input_file: Path to Python 2 script
            output_file: Path for converted script (defaults to input_file.py3.py)
            
        Returns:
            ConversionResult with conversion details
        """
        if not input_file.exists():
            return ConversionResult(False, input_file, errors=[f"File not found: {input_file}"])
        
        if output_file is None:
            output_file = input_file.with_suffix('.py3.py')
        
        try:
            # Read original code
            with open(input_file, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            # Convert code
            converted_code, changes = self.convert_code(original_code)
            
            # Write converted code
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"#!/usr/bin/env python3\\n")
                f.write(f"# Converted from Python 2: {input_file.name}\\n")
                f.write(f"# Conversion changes:\\n")
                for change in changes:
                    f.write(f"#   - {change}\\n")
                f.write("\\n")
                f.write(converted_code)
            
            return ConversionResult(
                success=True,
                original_file=input_file,
                converted_file=output_file,
                changes=changes
            )
            
        except Exception as e:
            return ConversionResult(
                success=False,
                original_file=input_file,
                errors=[f"Conversion failed: {str(e)}"]
            )


def main():
    """Command-line interface for migration tools."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flamingo Migration Tools")
    parser.add_argument("input_file", type=Path, help="File to convert")
    parser.add_argument("-o", "--output", type=Path, help="Output file")
    parser.add_argument("-t", "--type", choices=["config", "code"], 
                       default="config", help="Type of conversion")
    
    args = parser.parse_args()
    
    if args.type == "config":
        converter = ConfigConverter()
    else:
        converter = CodeConverter()
    
    result = converter.convert_file(args.input_file, args.output)
    
    if result.success:
        console.print(f"[green]✅ Conversion successful![/green]")
        console.print(f"Output: {result.converted_file}")
        
        if result.changes:
            console.print("\\n[blue]Changes made:[/blue]")
            for change in result.changes:
                console.print(f"  • {change}")
        
        if result.warnings:
            console.print("\\n[yellow]Warnings:[/yellow]")
            for warning in result.warnings:
                console.print(f"  ⚠️  {warning}")
    else:
        console.print(f"[red]❌ Conversion failed![/red]")
        for error in result.errors:
            console.print(f"  {error}")


if __name__ == "__main__":
    main()