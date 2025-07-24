"""
Rich themes and styling for Flamingo CLI

This module defines custom color schemes and styling for the Rich-based CLI interface.
"""

from rich.theme import Theme
from rich.style import Style

class FlamingoTheme:
    """Custom theme for Flamingo CLI with fire-inspired colors."""
    
    @classmethod
    def get_theme(cls) -> Theme:
        """Get the main Flamingo theme."""
        return Theme({
            # Core colors
            "primary": "bold red",
            "secondary": "bold orange1", 
            "accent": "bold yellow",
            "success": "bold green",
            "warning": "bold yellow",
            "error": "bold red",
            "info": "bold blue", 
            
            # Flamingo-specific
            "flamingo.fire": "bold red on black",
            "flamingo.ember": "orange1",
            "flamingo.spark": "yellow",
            "flamingo.ash": "bright_black",
            
            # UI elements
            "header": "bold white on red",
            "subheader": "bold orange1",
            "highlight": "black on yellow",
            "progress.bar": "red",
            "progress.percentage": "orange1",
            
            # Status indicators
            "status.running": "bold blue",
            "status.success": "bold green", 
            "status.failed": "bold red",
            "status.warning": "bold yellow",
            "status.info": "bold cyan",
            
            # Tables
            "table.header": "bold white on red",
            "table.row.even": "white",
            "table.row.odd": "bright_white",
            
            # Code syntax
            "code.keyword": "bold magenta",
            "code.string": "green",
            "code.number": "cyan",
            "code.comment": "bright_black italic",
        })
    
    def __call__(self) -> Theme:
        """Allow the class to be called like a function."""
        return self.get_theme()


class FlamingoStyles:
    """Pre-defined styles for common UI elements."""
    
    BANNER = Style(color="red", bold=True)
    VERSION = Style(color="orange1", bold=True)
    SUCCESS = Style(color="green", bold=True)
    ERROR = Style(color="red", bold=True)
    WARNING = Style(color="yellow", bold=True)
    INFO = Style(color="blue", bold=True)
    
    # Progress indicators
    PROGRESS_BAR = Style(color="red")
    PROGRESS_TEXT = Style(color="orange1")
    
    # Parameter display
    PARAM_NAME = Style(color="cyan", bold=True)
    PARAM_VALUE = Style(color="green")
    
    # Results
    RESULT_GOOD = Style(color="green", bold=True)
    RESULT_BAD = Style(color="red", bold=True)
    RESULT_NEUTRAL = Style(color="yellow")


# Color palettes for different themes
FIRE_PALETTE = [
    "#FF0000",  # Bright red
    "#FF4500",  # Orange red  
    "#FFA500",  # Orange
    "#FFD700",  # Gold
    "#FFFF00",  # Yellow
]

EMBER_PALETTE = [
    "#8B0000",  # Dark red
    "#A0522D",  # Sienna
    "#CD853F",  # Peru
    "#DAA520",  # Goldenrod
    "#F0E68C",  # Khaki
]

def get_gradient_colors(start_color: str, end_color: str, steps: int) -> list:
    """Generate gradient colors between two points."""
    # Simple gradient implementation
    # In a full implementation, you'd interpolate RGB values
    return [start_color] + [end_color] * (steps - 1)