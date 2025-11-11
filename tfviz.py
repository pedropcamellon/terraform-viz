#!/usr/bin/env python3
"""
tfviz - Terraform Infrastructure Visualizer

A CLI tool to generate visual representations of Terraform infrastructure.
Generates PNG diagrams showing resource dependencies and relationships.
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def find_terraform_executable() -> str:
    """Find terraform executable in PATH."""
    try:
        subprocess.run(["terraform", "--version"], capture_output=True, check=True)
        return "terraform"
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise FileNotFoundError("Terraform executable not found in PATH")


def find_graphviz_executable() -> str:
    """Find Graphviz dot executable."""
    possible_paths = [
        "dot",  # If in PATH
        "C:\\Program Files\\Graphviz\\bin\\dot.exe",  # Standard Windows installation
        "C:\\Program Files (x86)\\Graphviz\\bin\\dot.exe",  # 32-bit installation
    ]

    for path in possible_paths:
        try:
            subprocess.run([path, "-V"], capture_output=True, check=True)
            return path
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    raise FileNotFoundError("Graphviz dot executable not found")


def generate_terraform_graph(terraform_path: str, output_file: Path) -> None:
    """Generate Terraform dependency graph in DOT format."""
    print("🔄 Generating Terraform graph...")

    with open(output_file, "w") as dot_file:
        result = subprocess.run(
            [terraform_path, "graph"],
            stdout=dot_file,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Failed to generate Terraform graph: {result.stderr}")


def render_png(
    dot_path: str, dot_file: Path, output_file: Path, node_padding: float = 1.2
) -> None:
    """Render DOT file to PNG using Graphviz."""
    print("🎨 Rendering PNG visualization...")

    try:
        # Calculate spacing values based on node padding parameter
        node_sep = node_padding * 0.8  # Horizontal separation between nodes
        rank_sep = node_padding * 1.2  # Vertical separation between ranks/levels

        subprocess.run(
            [
                dot_path,
                "-Tpng",
                f"-Gnodesep={node_sep}",  # Horizontal spacing between nodes
                f"-Granksep={rank_sep}",  # Vertical spacing between ranks
                "-Gmargin=0",  # No outer margin
                "-Gdpi=150",  # Higher DPI for better quality
                str(dot_file),
                "-o",
                str(output_file),
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to render PNG: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="tfviz",
        description="Generate PNG visualization of Terraform infrastructure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tfviz                             # Generate MMDDYY_HHMM_infra_graph.png in current directory
  tfviz -o my_infra.png             # Generate with custom output filename  
  tfviz --node-padding 1.5          # Generate with more spacing between nodes
  tfviz --keep-dot                  # Keep intermediate DOT file
  tfviz --terraform-dir ../dev      # Use Terraform files from different directory
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
        "--terraform-dir",
        type=Path,
        default="../infrastructure",
        help="Directory containing Terraform files (default: current directory)",
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

    args = parser.parse_args()

    try:
        # Find required executables
        if args.verbose:
            print("🔍 Locating required executables...")

        dot_path = find_graphviz_executable()
        terraform_path = find_terraform_executable()

        if args.verbose:
            print(f"✅ Found Graphviz: {dot_path}")
            print(f"✅ Found Terraform: {terraform_path}")

        # Change to terraform directory if specified
        original_dir = Path.cwd()
        if args.terraform_dir != Path("."):
            if not args.terraform_dir.exists():
                print(
                    f"❌ Error: Terraform directory '{args.terraform_dir}' does not exist"
                )
                sys.exit(1)
            os.chdir(args.terraform_dir)
            if args.verbose:
                print(f"📁 Changed to directory: {args.terraform_dir}")

        # Generate output filename if not provided
        if args.output is None:
            datetime_prefix = datetime.now().strftime("%m%d%y_%H%M")
            output_filename = f"{datetime_prefix}_infra_graph.png"
            output_path = original_dir / output_filename
        else:
            output_path = (
                args.output if args.output.is_absolute() else original_dir / args.output
            )

        # Generate DOT file
        dot_file = Path("terraform_graph.dot")
        generate_terraform_graph(terraform_path, dot_file)

        # Render PNG
        render_png(dot_path, dot_file, output_path, getattr(args, "node_padding"))

        # Clean up DOT file unless requested to keep it
        if not args.keep_dot:
            dot_file.unlink(missing_ok=True)
            if args.verbose:
                print("🧹 Cleaned up intermediate DOT file")

        print(f"✅ Successfully generated: {output_path}")

        # Show file size
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"📊 File size: {size_mb:.2f} MB")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        if "Terraform" in str(e):
            print("💡 Install Terraform or ensure it's in your PATH")
        elif "Graphviz" in str(e):
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
