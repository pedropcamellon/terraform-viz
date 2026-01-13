"""File operations management."""

import os
from pathlib import Path

from rich.console import Console

console = Console()


class FileManager:
    """Manages file operations for visualization."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def change_directory(self, target_dir: Path) -> Path:
        """Change to target directory and return original directory."""
        original_dir = Path.cwd()

        if target_dir != Path("."):
            if not target_dir.exists():
                raise FileNotFoundError(f"Directory '{target_dir}' does not exist")

            os.chdir(target_dir)
            if self.verbose:
                console.print(
                    f"[cyan]>>>[/] Changed to directory: [white]{target_dir}[/]"
                )

        return original_dir

    def cleanup(self, file_path: Path) -> None:
        """Remove a file if it exists."""
        file_path.unlink(missing_ok=True)
        if self.verbose:
            console.print(f"[dim]>>>[/] Removed {file_path.name}")

    def get_file_size_mb(self, file_path: Path) -> float:
        """Get file size in megabytes."""
        return file_path.stat().st_size / (1024 * 1024)

    @staticmethod
    def ensure_output_dir(output_path: Path) -> None:
        """Ensure the output directory exists."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
