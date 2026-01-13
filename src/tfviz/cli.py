#!/usr/bin/env python3
"""Command-line interface for tfviz."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .config import TFVizConfig
from .orchestrator import TFVizOrchestrator


def create_config_from_args(args: argparse.Namespace) -> TFVizConfig:
    """Create configuration from parsed arguments."""
    # Determine output path
    if args.output is None:
        datetime_prefix = datetime.now().strftime("%m%d%y_%H%M")
        output_filename = f"{datetime_prefix}_infra_graph.png"
        output_dir = Path.cwd() / "output"
        output_path = output_dir / output_filename
    else:
        output_path = args.output if args.output.is_absolute() else Path.cwd() / args.output

    return TFVizConfig(
        tf_path=args.tf_path,
        tf_dir=args.tf_dir,
        output_path=output_path,
        plan_file=args.plan_file,
        node_padding=args.node_padding,
        keep_dot=args.keep_dot,
        verbose=args.verbose,
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="tfviz",
        description="Generate PNG visualization of Terraform infrastructure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tfviz                                  # Generate MMDDYY_HHMM_infra_graph.png
  tfviz -o my_infra.png                  # Custom output filename  
  tfviz --plan-file tfplan               # Visualize specific plan file
  tfviz --tf-path C:\\tools\\tf.exe        # Specify TF executable path
  tfviz --node-padding 1.5               # More spacing between nodes
  tfviz --tf-dir ../dev                  # Use TF files from different directory
        """,
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output PNG filename (default: auto-generated with date prefix)",
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


def main():
    """Main CLI entry point - orchestrates the visualization process."""
    args = parse_arguments()

    try:
        config = create_config_from_args(args)
        orchestrator = TFVizOrchestrator(config)
        orchestrator.execute()

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        if "Graphviz" in str(e):
            print("💡 Install Graphviz with: winget install graphviz")
        sys.exit(1)

    except RuntimeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
