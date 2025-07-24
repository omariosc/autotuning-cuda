"""
Utility functions for the CLI interface

Helper functions for formatting, display, and common CLI operations.
"""

import time
from typing import Dict, Any, List
from pathlib import Path
from datetime import timedelta
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        return f"{hours}h {remaining_minutes}m {remaining_seconds:.1f}s"


def format_results(results: Dict[str, Any]) -> str:
    """Format optimization results for display."""
    if not results:
        return "No results available"
    
    lines = []
    lines.append(f"Best Score: {results.get('best_score', 'N/A')}")
    lines.append(f"Best Config: {results.get('best_config', 'N/A')}")
    lines.append(f"Total Tests: {results.get('total_tests', 0):,}")
    lines.append(f"Duration: {format_duration(results.get('duration', 0))}")
    
    return "\\n".join(lines)


def create_banner() -> Panel:
    """Create the main Flamingo banner."""
    
    logo = """
    🔥 FLAMINGO 🔥
    CUDA Autotuning System
    """
    
    banner_text = Text(logo, style="bold red", justify="center")
    
    return Panel(
        banner_text,
        title="Welcome",
        title_align="center",
        border_style="red",
        padding=(1, 2)
    )


def create_progress_table(
    current_test: int,
    total_tests: int, 
    best_score: float,
    current_config: Dict[str, Any],
    elapsed_time: float
) -> Table:
    """Create a progress summary table."""
    
    table = Table(show_header=False, border_style="blue")
    table.add_column("Metric", style="cyan", min_width=15)
    table.add_column("Value", style="green")
    
    progress_pct = (current_test / total_tests) * 100 if total_tests > 0 else 0
    
    table.add_row("Progress", f"{current_test}/{total_tests} ({progress_pct:.1f}%)")
    table.add_row("Best Score", f"{best_score:.6f}" if best_score else "N/A")
    table.add_row("Current Config", str(current_config)[:30] + "..." if current_config else "N/A")
    table.add_row("Elapsed Time", format_duration(elapsed_time))
    
    if total_tests > 0 and current_test > 0:
        avg_time_per_test = elapsed_time / current_test
        remaining_tests = total_tests - current_test
        estimated_remaining = avg_time_per_test * remaining_tests
        table.add_row("Est. Remaining", format_duration(estimated_remaining))
    
    return table


def format_config_diff(old_config: Dict[str, Any], new_config: Dict[str, Any]) -> str:
    """Format configuration differences for migration display."""
    
    lines = []
    
    # Find added keys
    added = set(new_config.keys()) - set(old_config.keys())
    if added:
        lines.append("Added:")
        for key in sorted(added):
            lines.append(f"  + {key}: {new_config[key]}")
    
    # Find removed keys  
    removed = set(old_config.keys()) - set(new_config.keys())
    if removed:
        lines.append("Removed:")
        for key in sorted(removed):
            lines.append(f"  - {key}: {old_config[key]}")
    
    # Find changed keys
    common = set(old_config.keys()) & set(new_config.keys())
    changed = {k for k in common if old_config[k] != new_config[k]}
    if changed:
        lines.append("Changed:")
        for key in sorted(changed):
            lines.append(f"  ~ {key}: {old_config[key]} → {new_config[key]}")
    
    return "\\n".join(lines)


def validate_file_path(path: str) -> Path:
    """Validate and convert string path to Path object."""
    file_path = Path(path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if not file_path.is_file():
        raise IsADirectoryError(f"Path is not a file: {path}")
    
    return file_path


def create_syntax_panel(code: str, language: str = "ini", title: str = "Configuration") -> Panel:
    """Create a syntax-highlighted panel for code display."""
    
    syntax = Syntax(
        code,
        language,
        theme="monokai",
        line_numbers=True,
        background_color="default"
    )
    
    return Panel(
        syntax,
        title=title,
        border_style="blue",
        expand=False
    )


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate string to specified length with suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def create_status_indicator(status: str, message: str = "") -> Text:
    """Create colored status indicator text."""
    
    indicators = {
        "success": ("✅", "green"),
        "error": ("❌", "red"),
        "warning": ("⚠️", "yellow"),
        "info": ("ℹ️", "blue"),
        "running": ("🔄", "blue"),
        "waiting": ("⏳", "yellow"),
    }
    
    if status not in indicators:
        status = "info"
    
    icon, color = indicators[status]
    
    text = Text()
    text.append(icon + " ", style=color)
    if message:
        text.append(message, style=color)
    
    return text


def format_parameter_summary(variables: Dict[str, List[str]]) -> Table:
    """Create a summary table of parameters and their values."""
    
    table = Table(title="Parameter Summary", show_header=True, header_style="bold magenta")
    table.add_column("Parameter", style="cyan", min_width=15)
    table.add_column("Values", style="green", min_width=10)  
    table.add_column("Count", justify="right", style="yellow")
    table.add_column("Sample Values", style="dim")
    
    total_combinations = 1
    
    for param, values in variables.items():
        count = len(values)
        total_combinations *= count
        
        # Show first few values as sample
        sample_values = ", ".join(str(v) for v in values[:3])
        if len(values) > 3:
            sample_values += f", ... (+{len(values) - 3} more)"
        
        table.add_row(param, str(count), str(count), sample_values)
    
    # Add total row
    table.add_section()
    table.add_row(
        "[bold]Total Combinations[/bold]", 
        "", 
        f"[bold]{total_combinations:,}[/bold]", 
        ""
    )
    
    return table


class ProgressTracker:
    """Track and format progress information."""
    
    def __init__(self):
        self.start_time = time.time()
        self.tests_completed = 0
        self.total_tests = 0
        self.best_score = None
        self.current_config = None
    
    def update(self, completed: int, total: int, best_score: float = None, config: Dict[str, Any] = None):
        """Update progress information."""
        self.tests_completed = completed
        self.total_tests = total
        if best_score is not None:
            self.best_score = best_score
        if config is not None:
            self.current_config = config
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since tracking started."""
        return time.time() - self.start_time
    
    def get_progress_table(self) -> Table:
        """Get current progress as a formatted table."""
        return create_progress_table(
            self.tests_completed,
            self.total_tests,
            self.best_score,
            self.current_config,
            self.get_elapsed_time()
        )
    
    def estimate_remaining_time(self) -> float:
        """Estimate remaining time based on current progress."""
        if self.tests_completed == 0:
            return 0.0
        
        elapsed = self.get_elapsed_time()
        avg_time_per_test = elapsed / self.tests_completed
        remaining_tests = self.total_tests - self.tests_completed
        
        return avg_time_per_test * remaining_tests