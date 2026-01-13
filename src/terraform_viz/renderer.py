"""PNG rendering using Graphviz."""

import subprocess
from pathlib import Path

from rich.console import Console

console = Console()


class ImageRenderer:
    """Renders DOT files to PNG images."""

    def __init__(self, dot_path: str, verbose: bool = False):
        self.dot_path = dot_path
        self.verbose = verbose

    def render(
        self, dot_file: Path, output_file: Path, node_padding: float = 1.0
    ) -> None:
        """Render DOT file to PNG using Graphviz."""
        with console.status(
            "[magenta]Rendering PNG visualization...[/]", spinner="dots"
        ):
            if self.verbose:
                console.print("[cyan]>>>[/] Rendering PNG visualization...")

            try:
                cmd = self._build_render_command(dot_file, output_file, node_padding)
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to render PNG: {e}")

    def _build_render_command(
        self, dot_file: Path, output_file: Path, node_padding: float
    ) -> list[str]:
        """Build the Graphviz rendering command."""
        node_sep = node_padding * 0.8
        rank_sep = node_padding * 1.2

        return [
            self.dot_path,
            "-Tpng",
            f"-Gnodesep={node_sep}",
            f"-Granksep={rank_sep}",
            "-Gmargin=0",
            "-Gdpi=150",
            str(dot_file),
            "-o",
            str(output_file),
        ]
