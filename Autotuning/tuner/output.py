"""
CUDA Autotuning System - Output Control

output.py

Controls what kind of output is produced by the system and where it is sent.
(i.e. to a log file, to the screen or ignored)

PYTHON 2 TO 3 CONVERSION NOTES:
- Changed print __doc__ to print(__doc__) (line 136)
- Added comprehensive type hints throughout
- Enhanced error handling with context managers
- Added proper resource management for files
- Modernized class definitions with proper docstrings
- Added protocol typing for better type safety
- Enhanced exception handling and logging
"""

import sys
from pathlib import Path
from typing import TextIO, Union, List, Optional, Protocol
from contextlib import contextmanager
import logging


class Writable(Protocol):
    """
    Protocol for objects that support writing.
    
    PYTHON 2 CONVERSION: This is a new addition using Python 3's Protocol typing.
    Provides better type safety for writer objects.
    """
    def write(self, data: str) -> None: ...
    def flush(self) -> None: ...


# Module-level variables for output handling
# PYTHON 2 CONVERSION: Added type annotations for module-level variables
short: Optional[Writable] = None
full: Optional[Writable] = None  
all: Optional[Writable] = None


class WriteMult:
    """
    WriteMult objects are writable objects which pass write() calls to all arguments.
    
    PYTHON 2 CONVERSION: Enhanced with proper type hints and better error handling.
    Original class was functional but lacked type safety and comprehensive validation.
    """
    
    def __init__(self, *writers: Writable) -> None:
        """
        Initialize with multiple writer objects.
        
        Args:
            *writers: Variable number of objects that support write() and flush()
            
        Raises:
            TypeError: If any writer doesn't support write() method
        """
        self.writers: List[Writable] = list(writers)
        
        # PYTHON 2 CONVERSION: Enhanced validation with better error messages
        invalid_writers = []
        for i, writer in enumerate(self.writers):
            if not callable(getattr(writer, 'write', None)):
                invalid_writers.append(f"writer {i} ({type(writer).__name__})")
        
        if invalid_writers:
            raise TypeError(
                f"The following objects passed to WriteMult are not writable: "
                f"{', '.join(invalid_writers)}. All objects must have a write() method."
            )
    
    def write(self, data: str) -> None:
        """
        Write data to all registered writers.
        
        PYTHON 2 CONVERSION: Added type hints and better error resilience.
        
        Args:
            data: String data to write
        """
        if not isinstance(data, str):
            data = str(data)
            
        for writer in self.writers:
            try:
                writer.write(data)
            except Exception as e:
                # Log the error but continue with other writers
                logging.warning(f"Failed to write to {type(writer).__name__}: {e}")
    
    def flush(self) -> None:
        """
        Flush all registered writers.
        
        PYTHON 2 CONVERSION: Enhanced with error handling for individual flushes.
        """
        for writer in self.writers:
            try:
                if hasattr(writer, 'flush'):
                    writer.flush()
            except Exception as e:
                logging.warning(f"Failed to flush {type(writer).__name__}: {e}")
    
    def close(self) -> None:
        """
        Close all registered writers that support closing.
        
        PYTHON 2 CONVERSION: This is a new method for better resource management.
        """
        for writer in self.writers:
            try:
                if hasattr(writer, 'close') and writer != sys.stdout and writer != sys.stderr:
                    writer.close()
            except Exception as e:
                logging.warning(f"Failed to close {type(writer).__name__}: {e}")


class WriteNull:
    """
    WriteNull objects are writable but ignore any data written (null sink).
    
    PYTHON 2 CONVERSION: Enhanced with type hints and additional methods.
    Original was minimal but functional.
    """
    
    def __init__(self) -> None:
        """Initialize the null writer."""
        pass
    
    def write(self, data: str) -> None:
        """
        Write data (ignored).
        
        Args:
            data: String data to ignore
        """
        pass
    
    def flush(self) -> None:
        """Flush operation (no-op)."""
        pass
    
    def close(self) -> None:
        """Close operation (no-op)."""
        pass


class FileWriter:
    """
    A wrapper for file objects with enhanced error handling.
    
    PYTHON 2 CONVERSION: This is a new class providing better file management
    and error handling than the original simple file opening approach.
    """
    
    def __init__(self, filepath: Union[str, Path], mode: str = 'w') -> None:
        """
        Initialize file writer.
        
        Args:
            filepath: Path to the file
            mode: File opening mode (default: 'w')
            
        Raises:
            OSError: If file cannot be opened
        """
        self.filepath = Path(filepath)
        self.mode = mode
        self._file: Optional[TextIO] = None
        self._open_file()
    
    def _open_file(self) -> None:
        """Open the file for writing."""
        try:
            self._file = open(self.filepath, self.mode, encoding='utf-8')
        except OSError as e:
            raise OSError(f"Cannot open file '{self.filepath}' for writing: {e}")
    
    def write(self, data: str) -> None:
        """Write data to file."""
        if self._file is None:
            raise RuntimeError("File is not open")
        self._file.write(data)
    
    def flush(self) -> None:
        """Flush file buffer."""
        if self._file is not None:
            self._file.flush()
    
    def close(self) -> None:
        """Close the file."""
        if self._file is not None:
            self._file.close()
            self._file = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


@contextmanager
def output_context(mode: str, log_file: Optional[Union[str, Path]] = None):
    """
    Context manager for output configuration.
    
    PYTHON 2 CONVERSION: This is a new context manager providing automatic
    cleanup of resources, which wasn't available in the original.
    
    Args:
        mode: Output mode ('screen', 'production', 'verbose')
        log_file: Optional log file path for production/verbose modes
        
    Yields:
        None
    """
    old_short, old_full, old_all = short, full, all
    
    try:
        if mode == 'screen':
            output_screen()
        elif mode == 'production':
            if log_file is None:
                raise ValueError("log_file required for production mode")
            if not output_production(log_file):
                raise RuntimeError(f"Failed to set up production output to {log_file}")
        elif mode == 'verbose':
            if log_file is None:
                raise ValueError("log_file required for verbose mode")
            if not output_verbose(log_file):
                raise RuntimeError(f"Failed to set up verbose output to {log_file}")
        else:
            raise ValueError(f"Unknown output mode: {mode}")
        
        yield
        
    finally:
        # Restore previous settings and clean up
        global short, full, all
        
        # Close any file resources
        for output_obj in [short, full, all]:
            if hasattr(output_obj, 'close') and output_obj not in [sys.stdout, sys.stderr]:
                try:
                    output_obj.close()
                except:
                    pass
        
        short, full, all = old_short, old_full, old_all


def output_screen() -> None:
    """
    Output everything to the screen (default mode).
    
    PYTHON 2 CONVERSION: Added type hints and enhanced documentation.
    Original function logic preserved.
    """
    global short, full, all
    
    short = WriteNull()
    full = sys.stdout
    all = full


def output_production(log_file: Union[str, Path]) -> bool:
    """
    Production mode: write short output to screen and full output to log file.
    
    PYTHON 2 CONVERSION: Enhanced with better error handling and pathlib support.
    Original used basic file opening with minimal error handling.
    
    Args:
        log_file: Path to the log file
        
    Returns:
        True if setup successful, False otherwise
    """
    global short, full, all
    
    try:
        # PYTHON 2 CONVERSION: Enhanced file opening with proper error handling
        file_writer = FileWriter(log_file, 'w')
        
        short = sys.stdout
        full = file_writer
        all = WriteMult(short, full)
        
        return True
        
    except (OSError, IOError) as e:
        logging.error(f"Failed to set up production output: {e}")
        return False


def output_verbose(log_file: Union[str, Path]) -> bool:
    """
    Verbose mode: print full output to screen and log it to file.
    Ignore the short output.
    
    PYTHON 2 CONVERSION: Enhanced with better error handling and pathlib support.
    Fixed typo in original comment ("shot output" -> "short output").
    
    Args:
        log_file: Path to the log file
        
    Returns:
        True if setup successful, False otherwise
    """
    global short, full, all
    
    try:
        # PYTHON 2 CONVERSION: Enhanced file opening with proper error handling
        file_writer = FileWriter(log_file, 'w')
        
        short = WriteNull()
        full = WriteMult(sys.stdout, file_writer)
        all = full
        
        return True
        
    except (OSError, IOError) as e:
        logging.error(f"Failed to set up verbose output: {e}")
        return False


def output_custom(short_writer: Optional[Writable] = None,
                 full_writer: Optional[Writable] = None,
                 all_writer: Optional[Writable] = None) -> None:
    """
    Set up custom output writers.
    
    PYTHON 2 CONVERSION: This is a new function providing more flexibility
    than the original three fixed modes.
    
    Args:
        short_writer: Writer for short output (default: WriteNull)
        full_writer: Writer for full output (default: sys.stdout) 
        all_writer: Writer for all output (default: same as full_writer)
    """
    global short, full, all
    
    short = short_writer or WriteNull()
    full = full_writer or sys.stdout
    all = all_writer or full


def get_current_writers() -> tuple:
    """
    Get current output writers.
    
    PYTHON 2 CONVERSION: This is a new utility function for introspection.
    
    Returns:
        Tuple of (short, full, all) writers
    """
    return short, full, all


def cleanup_output() -> None:
    """
    Clean up any open file resources.
    
    PYTHON 2 CONVERSION: This is a new function for proper resource management.
    """
    global short, full, all
    
    for output_obj in [short, full, all]:
        if (hasattr(output_obj, 'close') and 
            output_obj not in [sys.stdout, sys.stderr, None]):
            try:
                output_obj.close()
            except Exception as e:
                logging.warning(f"Error closing output: {e}")
    
    # Reset to default
    output_screen()


if __name__ == "__main__":
    # PYTHON 2 CONVERSION: Changed print __doc__ to print(__doc__)
    print(__doc__)
    
    # Demonstration of the output system
    print("\\nOutput system demonstration:")
    
    # Test screen output
    print("Setting up screen output...")
    output_screen()
    all.write("This goes to stdout\\n")
    
    # Test null writer
    print("Testing null writer...")
    null_writer = WriteNull()
    null_writer.write("This is ignored\\n")
    
    # Test multi writer with stdout
    print("Testing multi-writer...")
    multi = WriteMult(sys.stdout)
    multi.write("This goes to stdout via multi-writer\\n")
    
    print("Output system demonstration complete.")