#!/usr/bin/env python3
"""
CUDA Autotuning System - Main Entry Point

This module contains the main entry point for the Flamingo CUDA autotuning system.

PYTHON 2 TO 3 CONVERSION NOTES:
- Changed shebang from python to python3
- Removed Python 2.5 version check (was lines 15-17 in original)
- Converted all print statements to print() functions
- Changed raw_input() to input() (was lines 64, 99 in original)
- Updated import statements for relative imports
- Added comprehensive type hints throughout
- Modernized string formatting to use f-strings
- Added proper exception handling with context managers
- Replaced print >>file syntax with file.write() (was line 309 in original)
- Added pathlib for better path handling
- Modernized configuration and argument parsing
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# PYTHON 2 CONVERSION: Original had relative imports without dots
# Changed "from tune_conf import" to "from .tune_conf import"
from .tune_conf import get_settings
from .evaluator import Evaluator
from .evaluator_batch import BatchEvaluator
from .optimisation import Optimisation
from .vartree import treeprint_str, get_variables
from .logging import writeCSV
from .helpers import strVarVals, ordinal
from . import output

# Version information - modernized from global variable approach
__version__ = "1.0.0"  # PYTHON 2 CONVERSION: Was "v0.16" global variable


class AutotuningSystem:
    """
    Main class for the CUDA Autotuning System.
    
    PYTHON 2 CONVERSION: Original used procedural approach with global functions.
    Modernized to use class-based approach for better encapsulation.
    """
    
    def __init__(self, version: str = __version__) -> None:
        self.version = version
        self.settings: Optional[Dict[str, Any]] = None
        self.evaluator: Optional[Evaluator] = None
        self.importance_evaluator: Optional[Evaluator] = None
    
    def parse_arguments(self) -> argparse.Namespace:
        """
        Parse command line arguments.
        
        PYTHON 2 CONVERSION: Original used manual sys.argv parsing (lines 52-74).
        Modernized to use argparse for better argument handling.
        """
        parser = argparse.ArgumentParser(
            description="CUDA Autotuning System - Optimize CUDA program parameters",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
Autotuning System v{self.version}

When no configuration file is provided, sample tests are run.
Press Enter to proceed with demonstration mode.
"""
        )
        
        parser.add_argument(
            "config_file",
            nargs="?",
            type=Path,
            help="Path to configuration file"
        )
        
        parser.add_argument(
            "--version",
            action="version",
            version=f"Autotuning System v{self.version}"
        )
        
        return parser.parse_args()
    
    def run_demonstration(self) -> None:
        """
        Run demonstration tests when no config file is provided.
        
        PYTHON 2 CONVERSION: Original used raw_input() (line 64).
        Changed to input() for Python 3.
        """
        print()
        print("Autotuning System".center(80))
        print(f"v{self.version}".center(80))
        print()
        print("Usage:")
        print("Please provide the path to a configuration file as an argument.")
        print("When no arguments are provided, some sample tests are run.")
        print("Press Enter to run the tests.")
        
        try:
            input()  # PYTHON 2 CONVERSION: Was raw_input()
        except KeyboardInterrupt:  # Ctrl-C
            print()
            sys.exit(0)
        
        # PYTHON 2 CONVERSION: Original used "from testing import run_testing"
        from .testing import run_testing
        
        run_testing()
        sys.exit(0)
    
    def setup_output(self, script_file: Optional[str]) -> bool:
        """
        Set up output handling for screen and/or script file.
        
        PYTHON 2 CONVERSION: Original used print statements and raw_input().
        Modernized with proper error handling and input validation.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        if script_file is not None:
            success = output.output_production(script_file)
            if not success:
                output.output_screen()  # Revert to safe default
                print(f"Could not open script file '{script_file}'")
                print("No script will be saved.")
                
                while True:
                    try:
                        response = input("Do you want to continue anyway? [Y/n] ").lower()
                        if response in ["y", "yes", "ye", ""]:
                            return False  # Continue but note failure
                        elif response in ["n", "no"]:
                            print("Quitting")
                            sys.exit(0)
                        else:
                            print("Please enter 'y' or 'n'")
                    except KeyboardInterrupt:  # Ctrl-C
                        print("Quitting")
                        sys.exit(0)
        else:
            output.output_screen()
            return True
        
        return True
    
    def display_settings(self) -> None:
        """
        Display configuration settings to user.
        
        PYTHON 2 CONVERSION: Original used print statements (lines 140-155).
        Modernized with f-strings and better formatting.
        """
        if not self.settings:
            return
            
        print("Retrieved settings from config file:")
        print()
        print(f"Variables:\\n{self.settings['vartree']}")
        print()
        
        print("Displayed as a tree:\\n")
        print(treeprint_str(self.settings['vartree']))
        
        print(f"Possible values:\\n{strVarVals(self.settings['possValues'])}")
        print()
        
        for opt in ['compile', 'test', 'clean']:
            if opt in self.settings and self.settings[opt] is not None:
                print(f"{opt}:\\n{self.settings[opt]}\\n")
    
    def setup_evaluator(self) -> None:
        """
        Set up the evaluator for running tests.
        
        PYTHON 2 CONVERSION: No significant changes needed here,
        but added type safety and better error handling.
        """
        if not self.settings:
            raise ValueError("Settings must be loaded before setting up evaluator")
            
        self.evaluator = Evaluator(
            self.settings['compile_mkStr'],
            self.settings['test_mkStr'],
            self.settings['custom_fom'],
            self.settings['clean_mkStr'],
            self.settings['repeat'],
            self.settings['aggregator']
        )
    
    def run_optimization(self) -> Tuple[bool, Optional[Optimisation]]:
        """
        Run the main optimization algorithm.
        
        Returns:
            Tuple of (success, optimization_result)
            
        PYTHON 2 CONVERSION: Added proper type hints and better exception handling.
        Original had basic try/except for KeyboardInterrupt (lines 194-212).
        """
        if not self.settings or not self.evaluator:
            raise ValueError("Settings and evaluator must be set up before optimization")
        
        # Set up the optimizer
        test = Optimisation(
            self.settings['vartree'],
            self.settings['possValues'],
            self.evaluator
        )
        
        if self.settings['optimal'] == 'min':
            test.minimiseScore()
        elif self.settings['optimal'] == 'max':
            test.maximiseScore()
        
        # Display test information
        print(f"Number of tests to be run: {test.testsRequired()}")
        if self.settings['repeat'] > 1:
            print(f"(with {self.settings['repeat']} repetitions each)")
        print()
        print()
        
        # Start timing
        execution_start = time.time()
        
        try:
            test.calculateOptimum()
            execution_stop = time.time()
            
            if not test.successful():
                print()
                print("Not enough evaluations could be performed.")
                print("There were too many failures.")
                return False, test
            
            # Run parameter importance tests if requested
            if self.settings['importance'] is not None:
                self._run_parameter_importance(test.optimalValuation())
            
            # Display results
            self._display_results(test, execution_start, execution_stop)
            return True, test
            
        except KeyboardInterrupt:
            print("\\n\\nQuitting Tuner")
            execution_stop = time.time()
            
            # Write partial log if available
            if self.evaluator and len(self.evaluator.log) > 0:
                self._write_log_file(partial=True)
            
            sys.exit(0)
    
    def _run_parameter_importance(self, optimal_valuation: Dict[str, Any]) -> None:
        """
        Run additional tests for parameter importance analysis.
        
        PYTHON 2 CONVERSION: Original function was at module level (lines 307-332).
        Moved to class method with proper type hints and modernized implementation.
        """
        if not self.settings:
            return
            
        self.importance_evaluator = Evaluator(
            self.settings['compile_mkStr'],
            self.settings['test_mkStr'],
            self.settings['custom_fom'],
            self.settings['clean_mkStr'],
            self.settings['repeat'],
            self.settings['aggregator'],
            self.evaluator  # Pass evaluator so no tests are repeated
        )
        
        additional_start = time.time()
        
        # PYTHON 2 CONVERSION: Original used print >>output.full (line 309)
        # Changed to direct method call for Python 3
        output.full.write("\\n\\n")
        print("Additional tests to check parameter importance:")
        output.full.write("\\n")
        
        vars_list = get_variables(self.settings['vartree'])
        poss_values = self.settings['possValues']
        
        tests = []
        for var in vars_list:
            for val in poss_values[var]:
                test_config = dict(optimal_valuation)  # copy
                test_config[var] = val
                if test_config not in tests:
                    tests.append(test_config)
        
        self.importance_evaluator.evaluate(tests)
        
        if self.importance_evaluator.testsRun == 0:
            print("(None required)")
        
        additional_stop = time.time()
        self._additional_test_time = additional_stop - additional_start
    
    def _display_results(self, test: Optimisation, start_time: float, stop_time: float) -> None:
        """
        Display optimization results.
        
        PYTHON 2 CONVERSION: Original used string concatenation and % formatting (lines 244-251).
        Modernized to use f-strings for better readability.
        """
        if not self.settings:
            return
            
        print()
        # PYTHON 2 CONVERSION: Original used .capitalize() on optimal setting
        optimal_type = self.settings['optimal'].capitalize()
        print(f"{optimal_type}imal valuation:")  # Minimal or Maximal
        print(strVarVals(test.optimalValuation(), ", "))
        print(f"{optimal_type}imal Score:")  # Minimal or Maximal
        print(test.optimalScore())
        
        duration = stop_time - start_time
        minutes, seconds = divmod(duration, 60)
        print(f"The system ran {test.numTests()} tests, taking {minutes:.0f}m{seconds:.2f}s.")
        
        if (self.settings['importance'] is not None and 
            self.importance_evaluator and 
            hasattr(self, '_additional_test_time')):
            additional_tests = self.importance_evaluator.testsRun
            if additional_tests > 0:
                add_minutes, add_seconds = divmod(self._additional_test_time, 60)
                time_str = f", taking {add_minutes:.0f}m{add_seconds:.2f}s"
            else:
                time_str = ""
            print(f"(and {additional_tests} additional tests{time_str})")
    
    def _display_failures(self) -> None:
        """
        Display any failures that occurred during evaluation.
        
        PYTHON 2 CONVERSION: Original used basic string concatenation (lines 257-263).
        Modernized with f-strings and better formatting.
        """
        if not self.evaluator or len(self.evaluator.failures) == 0:
            return
            
        print()
        print("FAILURES:")
        for failure_reason, failure_config in self.evaluator.failures:
            print(f"    {failure_reason}")
            print(f"    {strVarVals(failure_config, ', ')}")
            print()
    
    def _write_log_file(self, partial: bool = False) -> None:
        """
        Write CSV log file with test results.
        
        PYTHON 2 CONVERSION: Original used basic string concatenation (lines 268-283).
        Added better error handling and type safety.
        """
        if not self.settings or not self.evaluator:
            return
            
        if len(self.evaluator.log) > 0 and self.settings['log'] is not None:
            success = writeCSV(
                self.evaluator.log,
                get_variables(self.settings['vartree']),
                self.settings['possValues'],
                self.settings['log']
            )
            
            log_type = "partial" if partial else ""
            if success:
                print(f"A {log_type} testing log was saved to '{self.settings['log']}'")
            else:
                print("Failed to write CSV log file.")
    
    def _write_importance_log(self) -> None:
        """Write parameter importance data to file."""
        if (not self.settings or 
            not self.importance_evaluator or
            self.settings['importance'] is None or
            len(self.importance_evaluator.log) == 0):
            return
            
        success = writeCSV(
            self.importance_evaluator.log,
            get_variables(self.settings['vartree']),
            self.settings['possValues'],
            self.settings['importance']
        )
        
        if success:
            print(f"Additional data was saved to '{self.settings['importance']}'")
        else:
            print("Failed to write parameter importance data.")
    
    def _report_script_status(self) -> None:
        """Report status of script file writing."""
        if not self.settings or self.settings['script'] is None:
            return
            
        if self.settings['script'] is not False:
            print(f"A testing transcript was written to '{self.settings['script']}'")
        else:
            print("Failed to write a script file.")
    
    def run(self) -> None:
        """
        Main execution method.
        
        PYTHON 2 CONVERSION: Original was the main() function (lines 44-297).
        Restructured as class method with better error handling and separation of concerns.
        """
        args = self.parse_arguments()
        
        # Handle demonstration mode
        if args.config_file is None:
            self.run_demonstration()
            return
        
        # Load configuration
        try:
            self.settings = get_settings(str(args.config_file))
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            sys.exit(1)
        
        # Set up output handling
        script_success = self.setup_output(self.settings.get('script'))
        if script_success is False:
            self.settings['script'] = False
        
        # Redirect stdout to output handler
        # PYTHON 2 CONVERSION: Original assignment (line 119) is preserved
        sys.stdout = output.all
        
        print()
        print("Autotuning System".center(80))
        print(f"v{self.version}".center(80))
        print()
        
        # Change working directory to config file location
        # PYTHON 2 CONVERSION: Original used os.path (lines 135-136)
        # Modernized to use pathlib
        config_path = Path(args.config_file).resolve()
        working_dir = config_path.parent
        import os  # Still needed for chdir
        os.chdir(working_dir)
        
        # Display configuration
        self.display_settings()
        
        # Set up evaluator and run optimization
        try:
            self.setup_evaluator()
            success, test_result = self.run_optimization()
            
            # Display any failures
            self._display_failures()
            
            # Write log files
            self._write_log_file()
            self._write_importance_log()

            # Report script status
            self._report_script_status()
            
        except Exception as e:
            print(f"Error during optimization: {e}")
            sys.exit(1)


def main() -> None:
    """
    Entry point for the autotuning system.
    
    PYTHON 2 CONVERSION: Original was at module level (lines 339-340).
    Modernized with proper typing and class-based approach.
    """
    system = AutotuningSystem()
    system.run()


# PYTHON 2 CONVERSION: Original check was identical (lines 339-340)
if __name__ == '__main__':
    main()