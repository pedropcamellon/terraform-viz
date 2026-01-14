#!/usr/bin/env python3
"""Command-line interface for terraform-viz."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console

from .config import TFVizConfig
from .orchestrator import TFVizOrchestrator

console = Console()


def create_config_from_args(args: argparse.Namespace) -> TFVizConfig:
    """Create configuration from parsed arguments."""
    # Determine output mode and path
    if args.output is None:
        # Default: Terminal output only
        output_path = None
        terminal_output = True
    else:
        # User specified output file - generate PNG
        output_path = (
            args.output if args.output.is_absolute() else Path.cwd() / args.output
        )
        terminal_output = False

    return TFVizConfig(
        tf_path=args.tf_path,
        tf_dir=args.tf_dir,
        output_path=output_path,
        plan_file=args.plan_file,
        node_padding=args.node_padding,
        keep_dot=args.keep_dot,
        verbose=args.verbose,
        terminal_output=terminal_output,
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tfviz",
        description="Generate visualizations of Terraform infrastructure (terminal output by default, PNG with -o)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  terraform-viz                                  # Show diagram in terminal
  terraform-viz -o my_infra.png                  # Generate PNG file
  terraform-viz --plan-file tfplan               # Visualize specific plan file
  terraform-viz --tf-path C:\\tools\\tf.exe        # Specify TF executable path
  terraform-viz --node-padding 1.5 -o out.png    # More spacing between nodes (PNG)
  terraform-viz --tf-dir ../dev                  # Use TF files from different directory
        """,
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output PNG file path (default: ASCII to terminal only)",
    )

    parser.add_argument(
        "--tf-dir",
        type=Path,
        default=Path("."),
        help="Directory containing Terraform files (default: current directory)",
    )

    parser.add_argument(
        "--tf-path",
        type=str,
        default="terraform",
        help="Path to Terraform executable or alias (default: terraform)",
    )

    parser.add_argument(
        "--keep-dot",
        action="store_true",
        help="Keep intermediate DOT file after rendering",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--node-padding",
        type=float,
        default=1.0,
        help="Spacing between nodes (default: 1.0, larger = more spaced out)",
    )

    parser.add_argument(
        "--plan-file",
        type=Path,
        default=None,
        help="Path to Terraform plan file to visualize (optional)",
    )

    return parser.parse_args()


def show_welcome():
    """Display welcome screen with MS-DOS style."""
    from rich.panel import Panel
    from rich.table import Table

    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]TERRAFORM-VIZ[/bold cyan]\n"
            "[white]Infrastructure Visualization Tool[/white]\n"
            "[dim]v0.1.1[/dim]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    console.print()
    console.print("[bold white]QUICK START[/bold white]")
    console.print(
        "[cyan]  >[/] [white]terraform-viz[/]                    [dim]# Show ASCII diagram in terminal[/]"
    )
    console.print(
        "[cyan]  >[/] [white]terraform-viz -o infra.png[/]       [dim]# Generate PNG file[/]"
    )
    console.print(
        "[cyan]  >[/] [white]terraform-viz --verbose[/]          [dim]# Show detailed progress[/]"
    )
    console.print()

    table = Table(show_header=True, header_style="bold cyan", border_style="dim")
    table.add_column("Option", style="yellow")
    table.add_column("Description", style="white")

    table.add_row("--help", "Show all available options")
    table.add_row("--tf-path PATH", "Path to terraform executable")
    table.add_row("--tf-dir DIR", "Directory with terraform files")
    table.add_row("--plan-file FILE", "Visualize specific plan file")
    table.add_row("--node-padding N", "Adjust spacing between nodes")
    table.add_row("--keep-dot", "Keep intermediate DOT file")

    console.print(table)
    console.print()
    console.print(
        "[dim]Run with [cyan]--help[/cyan] for detailed usage information[/dim]"
    )
    console.print()


def main():
    """Main CLI entry point - orchestrates the visualization process."""
    # Show welcome screen if no arguments provided
    if len(sys.argv) == 1:
        show_welcome()
        sys.exit(0)

    args = parse_arguments()

    try:
        config = create_config_from_args(args)
        orchestrator = TFVizOrchestrator(config)
        orchestrator.execute()

    except FileNotFoundError as e:
        console.print(f"[bold red][ ERROR ][/] {e}")
        if "Graphviz" in str(e):
            console.print(
                "[yellow][ INFO  ][/] Install Graphviz with: [cyan]winget install graphviz[/]"
            )
        sys.exit(1)

    except RuntimeError as e:
        console.print(f"[bold red][ ERROR ][/] {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[bold red][ ABORT ][/] Operation cancelled by user")
        sys.exit(1)

    except Exception as e:
        console.print(f"[bold red][ ERROR ][/] Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
