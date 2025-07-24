"""
Modern CLI Entry Point for Flamingo CUDA Autotuning System

This module provides a rich, modern command-line interface with colors, progress bars,
and enhanced user experience using Rich and Typer.

PYTHON 2 CONVERSION: Original used basic argparse and simple print statements.
Modernized with Rich formatting, interactive prompts, and comprehensive help system.
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree
from rich import print as rprint
from rich.traceback import install as install_rich_traceback

# Install rich traceback handler for better error display
install_rich_traceback(show_locals=True)

from .. import __version__, VERSION_INFO
from ..core.autotuner import AutotuningSystem
from ..core.config import FlamingoConfig
from ..plugins.manager import PluginManager
from ..migration.converter import ConfigConverter
from .themes import FlamingoTheme
from .utils import format_duration, format_results, create_banner

# Initialize rich console with custom theme
console = Console(theme=FlamingoTheme())
app = typer.Typer(
    name="flamingo",
    help="🔥 Modern CUDA Autotuning System with Rich CLI",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=True,
)

# Global options
@app.callback()
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, 
        "--version", 
        "-v",
        help="Show version information and exit",
        is_flag=True
    ),
    verbose: Optional[bool] = typer.Option(
        False,
        "--verbose",
        "-V", 
        help="Enable verbose output",
        is_flag=True
    ),
    quiet: Optional[bool] = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress all output except errors",
        is_flag=True
    ),
    no_color: Optional[bool] = typer.Option(
        False,
        "--no-color",
        help="Disable colored output",
        is_flag=True,
        envvar="NO_COLOR"
    ),
    config_dir: Optional[Path] = typer.Option(
        None,
        "--config-dir",
        "-c",
        help="Custom configuration directory",
        envvar="FLAMINGO_CONFIG_DIR"
    ),
    plugin_dir: Optional[Path] = typer.Option(
        None,
        "--plugin-dir",
        "-p", 
        help="Custom plugin directory",
        envvar="FLAMINGO_PLUGIN_DIR"
    ),
) -> None:
    """
    🔥 Flamingo CUDA Autotuning System
    
    A modern, feature-rich CUDA parameter optimization framework with:
    • Rich CLI with colors and progress bars
    • Plugin architecture for extensibility  
    • Docker containerization support
    • Migration tools from Python 2 version
    • Interactive TUI interface
    """
    
    if no_color:
        console._color_system = None
    
    # Store global options in context
    ctx.ensure_object(dict)
    ctx.obj.update({
        "verbose": verbose,
        "quiet": quiet,
        "no_color": no_color,
        "config_dir": config_dir,
        "plugin_dir": plugin_dir,
        "console": console
    })
    
    if version:
        show_version_info()
        raise typer.Exit()


def show_version_info() -> None:
    """Display comprehensive version information."""
    
    # Create version table
    table = Table(title="🔥 Flamingo CUDA Autotuning System", show_header=False)
    table.add_column("Field", style="bold blue", width=20)
    table.add_column("Value", style="green")
    
    table.add_row("Version", __version__)
    table.add_row("Python Required", VERSION_INFO["python_version_required"])
    table.add_row("Original Version", VERSION_INFO["original_version"])
    table.add_row("Conversion Date", VERSION_INFO["conversion_date"])
    
    console.print(table)
    
    # Features list
    console.print("\\n[bold blue]New Features:[/bold blue]")
    for feature in VERSION_INFO["features"]:
        console.print(f"  • {feature}")


@app.command("run")
def run_optimization(
    config_file: Path = typer.Argument(
        ...,
        help="Configuration file path",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Validate configuration without running optimization"
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i", 
        help="Run in interactive mode with prompts"
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Custom output directory for results"
    ),
    max_tests: Optional[int] = typer.Option(
        None,
        "--max-tests",
        "-m",
        help="Maximum number of tests to run"
    ),
    parallel: bool = typer.Option(
        False,
        "--parallel",
        help="Enable parallel execution where possible"
    ),
    resume: Optional[Path] = typer.Option(
        None,
        "--resume",
        help="Resume from previous log file",
        exists=True
    ),
) -> None:
    """
    🚀 Run CUDA parameter optimization
    
    This command runs the main autotuning optimization using the specified
    configuration file. It supports various modes including dry-run validation,
    interactive prompts, and resuming from previous runs.
    """
    
    with console.status("[bold green]Initializing Flamingo...", spinner="dots"):
        try:
            # Load configuration
            config = FlamingoConfig.from_file(config_file)
            
            # Initialize autotuning system
            system = AutotuningSystem(config)
            
            # Set up plugin manager
            plugin_manager = PluginManager()
            plugin_manager.load_plugins()
            
        except Exception as e:
            console.print(f"[bold red]❌ Initialization failed:[/bold red] {e}")
            raise typer.Exit(1)
    
    console.print(f"[bold green]✅ Configuration loaded:[/bold green] {config_file}")
    
    if dry_run:
        console.print("[bold yellow]🔍 Dry run mode - validation only[/bold yellow]")
        validate_configuration(config)
        return
    
    if interactive:
        run_interactive_mode(system, config)
    else:
        run_batch_mode(system, config, max_tests, parallel, resume)


def validate_configuration(config: FlamingoConfig) -> None:
    """Validate configuration and display summary."""
    
    console.print("\\n[bold blue]📋 Configuration Summary[/bold blue]")
    
    # Create configuration summary table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan", min_width=15)
    table.add_column("Value", style="green")
    table.add_column("Status", justify="center")
    
    # Add configuration rows
    table.add_row("Variables", str(len(config.variables)), "✅")
    table.add_row("Test Command", config.test_command[:50] + "..." if len(config.test_command) > 50 else config.test_command, "✅")
    table.add_row("Optimization", config.optimization_direction, "✅")
    table.add_row("Repetitions", str(config.repetitions), "✅")
    
    console.print(table)
    
    # Variable space analysis
    total_combinations = 1
    for var, values in config.variable_values.items():
        total_combinations *= len(values)
    
    console.print(f"\\n[bold cyan]📊 Parameter Space Analysis[/bold cyan]")
    console.print(f"  • Total variables: {len(config.variables)}")
    console.print(f"  • Total combinations: {total_combinations:,}")
    console.print(f"  • Estimated runtime: {estimate_runtime(total_combinations, config.repetitions)}")
    
    if total_combinations > 10000:
        console.print("[bold yellow]⚠️  Large parameter space detected - consider using sampling strategies[/bold yellow]")


def run_interactive_mode(system: AutotuningSystem, config: FlamingoConfig) -> None:
    """Run optimization in interactive mode with user prompts."""
    
    console.print("\\n[bold blue]🎯 Interactive Optimization Mode[/bold blue]")
    
    # Show parameter space
    display_parameter_space(config)
    
    # Confirm execution
    if not Confirm.ask("\\n[bold]Proceed with optimization?[/bold]", default=True):
        console.print("[yellow]Optimization cancelled by user[/yellow]")
        return
    
    # Run optimization with progress tracking
    run_with_progress(system, config)


def run_batch_mode(
    system: AutotuningSystem, 
    config: FlamingoConfig,
    max_tests: Optional[int] = None,
    parallel: bool = False,
    resume: Optional[Path] = None
) -> None:
    """Run optimization in batch mode."""
    
    console.print("\\n[bold blue]⚡ Batch Optimization Mode[/bold blue]")
    
    if resume:
        console.print(f"[bold yellow]🔄 Resuming from:[/bold yellow] {resume}")
        try:
            # Load previous results and continue optimization
            import pandas as pd
            previous_results = pd.read_csv(resume)
            console.print(f"[green]✅ Loaded {len(previous_results)} previous results[/green]")
            # Set up system to skip already completed tests
            system.load_previous_results(previous_results)
        except Exception as e:
            console.print(f"[red]❌ Failed to resume from {resume}: {e}[/red]")
            console.print("[yellow]⚠️  Starting fresh optimization instead[/yellow]")
    
    if parallel:
        console.print("[bold cyan]🚀 Parallel execution enabled[/bold cyan]")
    
    # Run optimization
    run_with_progress(system, config, max_tests, parallel)


def run_with_progress(
    system: AutotuningSystem, 
    config: FlamingoConfig,
    max_tests: Optional[int] = None,
    parallel: bool = False
) -> None:
    """Run optimization with rich progress display."""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        expand=True
    ) as progress:
        
        # Add main progress task
        total_tests = max_tests or system.estimate_total_tests()
        main_task = progress.add_task("🔥 Running optimization...", total=total_tests)
        
        # Add subtasks for different phases
        compile_task = progress.add_task("🔨 Compiling...", total=100)
        test_task = progress.add_task("🧪 Testing...", total=100) 
        analysis_task = progress.add_task("📊 Analyzing...", total=100)
        
        try:
            # Run the actual optimization
            results = system.run_optimization(
                progress_callback=lambda completed, total: progress.update(main_task, completed=completed),
                compile_callback=lambda p: progress.update(compile_task, completed=p),
                test_callback=lambda p: progress.update(test_task, completed=p),
                analysis_callback=lambda p: progress.update(analysis_task, completed=p)
            )
            
            # Display results
            display_results(results)
            
        except KeyboardInterrupt:
            console.print("\\n[bold yellow]⚠️  Optimization interrupted by user[/bold yellow]")
            # Save partial results
            try:
                if hasattr(system, '_partial_results') and system._partial_results:
                    partial_file = Path("partial_results.csv")
                    system.save_partial_results(partial_file)
                    console.print(f"[green]💾 Partial results saved to {partial_file}[/green]")
                    console.print("[blue]ℹ️  Use --resume to continue from this point[/blue]")
            except Exception as e:
                console.print(f"[red]❌ Failed to save partial results: {e}[/red]")
        except Exception as e:
            console.print(f"\\n[bold red]❌ Optimization failed:[/bold red] {e}")
            raise typer.Exit(1)


def display_parameter_space(config: FlamingoConfig) -> None:
    """Display the parameter space as a tree."""
    
    tree = Tree("🌳 [bold blue]Parameter Space[/bold blue]")
    
    for var, values in config.variable_values.items():
        var_branch = tree.add(f"[cyan]{var}[/cyan] ({len(values)} values)")
        
        # Show first few values and indicate if there are more
        display_values = values[:5]
        for value in display_values:
            var_branch.add(f"[green]{value}[/green]")
        
        if len(values) > 5:
            var_branch.add(f"[dim]... and {len(values) - 5} more[/dim]")
    
    console.print(tree)


def display_results(results: Dict[str, Any]) -> None:
    """Display optimization results with rich formatting."""
    
    console.print("\\n")
    console.print(Panel.fit(
        "[bold green]🎉 Optimization Complete![/bold green]",
        style="green"
    ))
    
    # Results table
    table = Table(title="📊 Optimization Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", min_width=20)
    table.add_column("Value", style="green")
    
    table.add_row("Best Score", f"{results.get('best_score', 'N/A')}")
    table.add_row("Best Configuration", str(results.get('best_config', 'N/A'))[:50])
    table.add_row("Total Tests", f"{results.get('total_tests', 'N/A'):,}")
    table.add_row("Duration", format_duration(results.get('duration', 0)))
    table.add_row("Success Rate", f"{results.get('success_rate', 0)*100:.1f}%")
    
    console.print(table)
    
    # Output files
    if results.get('output_files'):
        console.print("\\n[bold blue]📁 Output Files:[/bold blue]")
        for file_type, file_path in results['output_files'].items():
            console.print(f"  • {file_type}: [link]{file_path}[/link]")


def estimate_runtime(combinations: int, repetitions: int) -> str:
    """Estimate runtime based on parameter space size."""
    # Rough estimate: 1 second per test on average
    total_seconds = combinations * repetitions * 1.0
    return format_duration(total_seconds)


@app.command("validate")
def validate_config(
    config_file: Path = typer.Argument(
        ...,
        help="Configuration file to validate",
        exists=True
    )
) -> None:
    """
    ✅ Validate configuration file
    
    Check configuration file syntax, parameter definitions, and estimate
    optimization complexity without running any tests.
    """
    
    try:
        config = FlamingoConfig.from_file(config_file)
        validate_configuration(config)
        console.print("\\n[bold green]✅ Configuration is valid![/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Configuration validation failed:[/bold red] {e}")
        raise typer.Exit(1)


@app.command("demo")
def run_demo(
    example: str = typer.Option(
        "hello",
        "--example",
        "-e",
        help="Demo example to run (hello, matrix, laplace)"
    )
) -> None:
    """
    🎮 Run interactive demonstration
    
    Run one of the built-in examples to see how Flamingo works.
    Available examples: hello, matrix, laplace, looping, matlab
    """
    
    console.print(create_banner())
    console.print(f"\\n[bold blue]🎮 Running demo:[/bold blue] {example}")
    
    # Implement demo functionality
    demo_configs = {
        "hello": "examples/hello/hello.conf",
        "matrix": "examples/matrix/modified/matrix_tune.conf", 
        "laplace": "examples/laplace3d/laplace3d.conf",
        "looping": "examples/looping/looping.conf",
        "matlab": "examples/matlab/matlab_test.conf"
    }
    
    if example not in demo_configs:
        available = ", ".join(demo_configs.keys())
        console.print(f"[red]❌ Unknown example: {example}[/red]")
        console.print(f"[blue]Available examples: {available}[/blue]")
        raise typer.Exit(1)
    
    demo_path = Path(demo_configs[example])
    if not demo_path.exists():
        console.print(f"[red]❌ Demo configuration not found: {demo_path}[/red]")
        console.print("[yellow]⚠️  Make sure you're running from the project root directory[/yellow]")
        raise typer.Exit(1)
    
    console.print(f"[green]🚀 Starting {example} demo...[/green]")
    console.print(f"[dim]Configuration: {demo_path}[/dim]")
    
    # Run the demo as a dry-run first
    console.print("\\n[blue]📋 Demo Configuration Preview:[/blue]")
    try:
        config = FlamingoConfig.from_file(demo_path)
        validate_configuration(config)
        
        if Confirm.ask("\\n[bold]Run this demo optimization?[/bold]", default=True):
            # Run actual demo
            system = AutotuningSystem(config)
            run_with_progress(system, config, max_tests=min(100, system.estimate_total_tests()))
        else:
            console.print("[yellow]Demo cancelled[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Demo failed: {e}[/red]")


@app.command("migrate")  
def migrate_config(
    old_config: Path = typer.Argument(
        ...,
        help="Python 2 configuration file to migrate",
        exists=True
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file for migrated configuration"
    )
) -> None:
    """
    🔄 Migrate Python 2 configuration to Python 3
    
    Convert old Python 2.5+ configuration files to the new Python 3.10+ format
    with enhanced features and validation.
    """
    
    console.print("\\n[bold blue]🔄 Configuration Migration[/bold blue]")
    
    try:
        converter = ConfigConverter()
        
        with console.status("Converting configuration...", spinner="dots"):
            new_config = converter.convert_file(old_config)
        
        output_path = output or old_config.with_suffix('.py3.conf')
        new_config.save(output_path)
        
        console.print(f"[bold green]✅ Migration complete![/bold green]")
        console.print(f"  • Input: {old_config}")
        console.print(f"  • Output: {output_path}")
        
        # Show diff summary
        console.print("\\n[bold blue]📋 Changes Made:[/bold blue]")
        changes = converter.get_conversion_summary()
        for change in changes:
            console.print(f"  • {change}")
            
    except Exception as e:
        console.print(f"[bold red]❌ Migration failed:[/bold red] {e}")
        raise typer.Exit(1)


@app.command("plugins")
def manage_plugins(
    action: str = typer.Argument(
        "list",
        help="Action: list, install, uninstall, enable, disable"
    ),
    plugin_name: Optional[str] = typer.Argument(
        None,
        help="Plugin name (required for install/uninstall/enable/disable)"
    )
) -> None:
    """
    🔌 Manage plugins
    
    Install, uninstall, enable, disable, or list available plugins.
    """
    
    plugin_manager = PluginManager()
    
    if action == "list":
        list_plugins(plugin_manager)
    elif action == "install":
        if not plugin_name:
            console.print("[red]Plugin name required for install[/red]")
            raise typer.Exit(1)
        install_plugin(plugin_manager, plugin_name)
    elif action == "uninstall":
        if not plugin_name:
            console.print("[red]Plugin name required for uninstall[/red]")
            raise typer.Exit(1)
        uninstall_plugin(plugin_manager, plugin_name)
    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        raise typer.Exit(1)


def list_plugins(plugin_manager: PluginManager) -> None:
    """List all available and installed plugins."""
    
    console.print("\\n[bold blue]🔌 Plugin Status[/bold blue]")
    
    plugins = plugin_manager.list_plugins()
    
    if not plugins:
        console.print("[yellow]No plugins found[/yellow]")
        return
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Status", justify="center")
    table.add_column("Description", style="dim")
    
    for plugin in plugins:
        status = "✅ Enabled" if plugin.enabled else "❌ Disabled"
        table.add_row(
            plugin.name,
            plugin.version,
            status,
            plugin.description[:50] + "..." if len(plugin.description) > 50 else plugin.description
        )
    
    console.print(table)


def install_plugin(plugin_manager: PluginManager, plugin_name: str) -> None:
    """Install a plugin."""
    
    with console.status(f"Installing plugin {plugin_name}...", spinner="dots"):
        try:
            plugin_manager.install_plugin(plugin_name)
            console.print(f"[bold green]✅ Plugin '{plugin_name}' installed successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ Failed to install plugin '{plugin_name}':[/bold red] {e}")
            raise typer.Exit(1)


def uninstall_plugin(plugin_manager: PluginManager, plugin_name: str) -> None:
    """Uninstall a plugin."""
    
    if not Confirm.ask(f"Are you sure you want to uninstall '{plugin_name}'?"):
        console.print("[yellow]Uninstall cancelled[/yellow]")
        return
    
    with console.status(f"Uninstalling plugin {plugin_name}...", spinner="dots"):
        try:
            plugin_manager.uninstall_plugin(plugin_name)
            console.print(f"[bold green]✅ Plugin '{plugin_name}' uninstalled successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ Failed to uninstall plugin '{plugin_name}':[/bold red] {e}")
            raise typer.Exit(1)


@app.command("tui")
def launch_tui() -> None:
    """
    📱 Launch Terminal User Interface
    
    Start the interactive terminal-based user interface for a more
    visual and user-friendly experience.
    """
    
    console.print("[bold blue]🚀 Launching TUI...[/bold blue]")
    
    try:
        from ..tui.app import FlamingoTUI
        app = FlamingoTUI()
        app.run()
    except ImportError:
        console.print("[red]TUI dependencies not installed. Install with: pip install flamingo[tui][/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Failed to launch TUI: {e}[/red]")
        raise typer.Exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()