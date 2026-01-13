"""Executable finder for required tools."""

import subprocess
from pathlib import Path


class ExecutableFinder:
    """Finds required executables for visualization."""

    @staticmethod
    def find_graphviz() -> str:
        """Find Graphviz dot executable."""
        possible_paths = [
            "dot",
            "C:\\Program Files\\Graphviz\\bin\\dot.exe",
            "C:\\Program Files (x86)\\Graphviz\\bin\\dot.exe",
        ]

        for path in possible_paths:
            try:
                subprocess.run([path, "-V"], capture_output=True, check=True)
                return path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

        raise FileNotFoundError("Graphviz dot executable not found")
