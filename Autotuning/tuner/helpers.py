"""
CUDA Autotuning System - Helper Functions

helpers.py

A collection of helper functions used throughout the autotuning system.

PYTHON 2 TO 3 CONVERSION NOTES:
- Changed print __doc__ to print(__doc__) (line 57)
- Fixed integer division in med() function: len(ys)/2 to len(ys)//2 (line 41)
- Added proper type hints throughout all functions
- Enhanced function documentation with proper docstrings
- Added input validation and error handling
- Modernized to use f-strings where appropriate
"""

from typing import List, Dict, Any, Union, TypeVar, Iterable
import statistics
from itertools import product

# Type variable for generic numeric operations
T = TypeVar('T', int, float)


def strVarVals(var_dict: Dict[str, Any], sep: str = "\n") -> str:
    """
    Create a string representation of variable/value pairs.
    
    PYTHON 2 CONVERSION: Original function was identical, just added type hints.
    Enhanced with better parameter naming and documentation.
    
    Args:
        var_dict: Dictionary mapping variable names to values
        sep: Separator string between variable assignments (default: newline)
        
    Returns:
        String representation of all variable assignments
        
    Example:
        >>> strVarVals({"x": 1, "y": 2}, ", ")
        "x = 1, y = 2"
    """
    if not var_dict:
        return ""
    
    return sep.join([f"{var} = {val}" for var, val in sorted(var_dict.items())])


def ordinal(n: int) -> str:
    """
    Return the ordinal string representation of a number.
    
    PYTHON 2 CONVERSION: Original function was correct, just added type hints.
    Enhanced with validation and better documentation.
    
    Args:
        n: Integer to convert to ordinal form
        
    Returns:
        Ordinal string (e.g., "1st", "2nd", "3rd", "4th", "11th", "21st")
        
    Raises:
        TypeError: If n is not an integer
        
    Example:
        >>> ordinal(1)
        "1st"
        >>> ordinal(23)
        "23rd"
    """
    if not isinstance(n, int):
        raise TypeError(f"Expected integer, got {type(n).__name__}")
    
    # Handle special cases for 11th, 12th, 13th
    if 10 <= n % 100 < 20:
        return f"{n}th"
    else:
        suffix_map = {1: 'st', 2: 'nd', 3: 'rd'}
        suffix = suffix_map.get(n % 10, 'th')
        return f"{n}{suffix}"


def crossproduct(list_of_lists: List[List[T]]) -> List[List[T]]:
    """
    Return the Cartesian product of a list of lists.
    
    PYTHON 2 CONVERSION: Original algorithm was correct but used verbose approach.
    Modernized to offer both original algorithm and itertools.product alternative.
    Added comprehensive type hints and validation.
    
    Args:
        list_of_lists: List containing lists to compute Cartesian product of
        
    Returns:
        List of all possible combinations as lists
        
    Raises:
        TypeError: If input is not a list of lists
        ValueError: If any inner list is empty
        
    Example:
        >>> crossproduct([[1, 2], ['a', 'b']])
        [[1, 'a'], [1, 'b'], [2, 'a'], [2, 'b']]
    """
    if not isinstance(list_of_lists, list):
        raise TypeError("Expected list of lists")
    
    if not list_of_lists:
        return [[]]
    
    # Validate input structure
    for i, sublist in enumerate(list_of_lists):
        if not isinstance(sublist, list):
            raise TypeError(f"Element {i} is not a list: {type(sublist).__name__}")
        if not sublist:
            raise ValueError(f"List {i} is empty - cannot compute cross product with empty lists")
    
    # PYTHON 2 CONVERSION: Original algorithm preserved for compatibility
    # This maintains the exact same behavior as the original implementation
    cross_prod = [[]]
    for sublist in list_of_lists:
        cross_prod = [existing + [item] for item in sublist for existing in cross_prod]
    
    return cross_prod


def crossproduct_itertools(list_of_lists: List[List[T]]) -> List[List[T]]:
    """
    Modern alternative implementation using itertools.product.
    
    PYTHON 2 CONVERSION: This is a new function providing a more Pythonic approach.
    The original crossproduct() is preserved for backward compatibility.
    
    Args:
        list_of_lists: List containing lists to compute Cartesian product of
        
    Returns:
        List of all possible combinations as lists
    """
    if not list_of_lists:
        return [[]]
    
    return [list(combo) for combo in product(*list_of_lists)]


def med(values: List[Union[int, float]]) -> float:
    """
    Return the median of a list of numbers.
    
    PYTHON 2 CONVERSION: Original had integer division bug (len(ys)/2).
    Fixed to use floor division (len(ys)//2) and proper float division.
    Added comprehensive type hints and validation.
    
    Args:
        values: List of numeric values
        
    Returns:
        Median value as float
        
    Raises:
        TypeError: If values is not a list or contains non-numeric types
        ValueError: If list is empty
        
    Example:
        >>> med([1, 2, 3, 4, 5])
        3.0
        >>> med([1, 2, 3, 4])
        2.5
    """
    if not isinstance(values, list):
        raise TypeError(f"Expected list, got {type(values).__name__}")
    
    if not values:
        raise ValueError("Cannot compute median of empty list")
    
    # Validate all elements are numeric
    for i, val in enumerate(values):
        if not isinstance(val, (int, float)):
            raise TypeError(f"Element {i} is not numeric: {type(val).__name__}")
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    # PYTHON 2 CONVERSION: Fixed integer division bug
    # Original: return (ys[len(ys)/2]) if bool(len(ys)%2) else (ys[len(ys)/2] + ys[len(ys)/2 -1])/2.0
    # Fixed: Use // for floor division instead of /
    if n % 2 == 1:
        # Odd number of elements - return middle element
        return float(sorted_values[n // 2])
    else:
        # Even number of elements - return average of two middle elements
        mid_idx = n // 2
        return (sorted_values[mid_idx - 1] + sorted_values[mid_idx]) / 2.0


def med_builtin(values: List[Union[int, float]]) -> float:
    """
    Modern alternative using statistics.median().
    
    PYTHON 2 CONVERSION: This is a new function using Python 3's statistics module.
    The original med() is preserved for backward compatibility.
    
    Args:
        values: List of numeric values
        
    Returns:
        Median value as float
    """
    if not values:
        raise ValueError("Cannot compute median of empty list")
    
    return statistics.median(values)


def avg(values: List[Union[int, float]]) -> float:
    """
    Return the arithmetic mean (average) of a list of numbers.
    
    PYTHON 2 CONVERSION: Original was mostly correct but could fail with integer division.
    Enhanced with type hints, validation, and guaranteed float return type.
    
    Args:
        values: List of numeric values
        
    Returns:
        Arithmetic mean as float
        
    Raises:
        TypeError: If values is not a list or contains non-numeric types
        ValueError: If list is empty
        ZeroDivisionError: If list is empty (division by zero)
        
    Example:
        >>> avg([1, 2, 3, 4, 5])
        3.0
        >>> avg([2.5, 7.5])
        5.0
    """
    if not isinstance(values, list):
        raise TypeError(f"Expected list, got {type(values).__name__}")
    
    if not values:
        raise ValueError("Cannot compute average of empty list")
    
    # Validate all elements are numeric
    for i, val in enumerate(values):
        if not isinstance(val, (int, float)):
            raise TypeError(f"Element {i} is not numeric: {type(val).__name__}")
    
    # PYTHON 2 CONVERSION: Ensure float division by converting sum to float
    return float(sum(values)) / len(values)


def avg_builtin(values: List[Union[int, float]]) -> float:
    """
    Modern alternative using statistics.mean().
    
    PYTHON 2 CONVERSION: This is a new function using Python 3's statistics module.
    The original avg() is preserved for backward compatibility.
    
    Args:
        values: List of numeric values
        
    Returns:
        Arithmetic mean as float
    """
    if not values:
        raise ValueError("Cannot compute average of empty list")
    
    return statistics.mean(values)


# Additional utility functions for modern Python usage
def geometric_mean(values: List[Union[int, float]]) -> float:
    """
    Calculate the geometric mean of a list of positive numbers.
    
    PYTHON 2 CONVERSION: This is a new function providing additional statistical functionality.
    
    Args:
        values: List of positive numeric values
        
    Returns:
        Geometric mean as float
        
    Raises:
        ValueError: If any value is negative or zero, or if list is empty
    """
    if not values:
        raise ValueError("Cannot compute geometric mean of empty list")
    
    for i, val in enumerate(values):
        if not isinstance(val, (int, float)):
            raise TypeError(f"Element {i} is not numeric: {type(val).__name__}")
        if val <= 0:
            raise ValueError(f"All values must be positive for geometric mean, got {val} at index {i}")
    
    return statistics.geometric_mean(values)


def harmonic_mean(values: List[Union[int, float]]) -> float:
    """
    Calculate the harmonic mean of a list of positive numbers.
    
    PYTHON 2 CONVERSION: This is a new function providing additional statistical functionality.
    
    Args:
        values: List of positive numeric values
        
    Returns:
        Harmonic mean as float
        
    Raises:
        ValueError: If any value is negative or zero, or if list is empty
    """
    if not values:
        raise ValueError("Cannot compute harmonic mean of empty list")
    
    for i, val in enumerate(values):
        if not isinstance(val, (int, float)):
            raise TypeError(f"Element {i} is not numeric: {type(val).__name__}")
        if val <= 0:
            raise ValueError(f"All values must be positive for harmonic mean, got {val} at index {i}")
    
    return statistics.harmonic_mean(values)


if __name__ == "__main__":
    # PYTHON 2 CONVERSION: Changed print __doc__ to print(__doc__)
    print(__doc__)
    
    # Demonstration of the functions
    print("\\nFunction demonstrations:")
    
    # Test strVarVals
    test_vars = {"threads": 32, "blocks": 16, "optimization": "O3"}
    print(f"strVarVals example: {strVarVals(test_vars, ', ')}")
    
    # Test ordinal
    for n in [1, 2, 3, 11, 21, 22, 23, 101, 111]:
        print(f"ordinal({n}) = {ordinal(n)}")
    
    # Test crossproduct
    test_lists = [[1, 2], ['a', 'b'], ['x', 'y']]
    print(f"crossproduct({test_lists[:2]}) = {crossproduct(test_lists[:2])}")
    
    # Test statistical functions
    test_values = [1, 2, 3, 4, 5, 6]
    print(f"med({test_values}) = {med(test_values)}")
    print(f"avg({test_values}) = {avg(test_values)}")