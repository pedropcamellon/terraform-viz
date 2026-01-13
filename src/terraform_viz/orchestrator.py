"""Main orchestrator for terraform-viz."""

from pathlib import Path

from rich.console import Console

from .ascii_renderer import AsciiRenderer
from .config import TFVizConfig
from .executables import ExecutableFinder
from .file_manager import FileManager
from .graph_generator import GraphGenerator
from .renderer import ImageRenderer

console = Console()


class TFVizOrchestrator:
    """Orchestrates the visualization generation process."""

    def __init__(self, config: TFVizConfig):
        self.config = config
        self.file_manager = FileManager(verbose=config.verbose)

    def execute(self) -> Path:
        """Execute the full visualization pipeline."""
        # Find required executables
        if self.config.verbose:
            console.print("[cyan]>>>[/] Locating required executables...")

        # Graphviz only needed for PNG output
        dot_path = None if self.config.ascii_output else ExecutableFinder.find_graphviz()

        if self.config.verbose:
            if dot_path:
                console.print(f"[cyan]>>>[/] Found Graphviz: [white]{dot_path}[/]")
            console.print(
                f"[cyan]>>>[/] Using Terraform: [white]{self.config.tf_path}[/]"
            )

        # Change to target directory
        original_dir = self.file_manager.change_directory(self.config.tf_dir)

        try:
            # Ensure output directory exists
            self.file_manager.ensure_output_dir(self.config.output_path)

            # Generate graph
            graph_gen = GraphGenerator(self.config.tf_path, self.config.verbose)
            graph_gen.generate(self.config.dot_file_path, self.config.plan_file)

            # Render to appropriate format
            if self.config.ascii_output:
                # Render ASCII diagram
                renderer = AsciiRenderer(self.config.verbose)
                renderer.render(
                    self.config.dot_file_path,
                    self.config.output_path if not self.config.output_path.suffix == ".png" else None,
                )
            else:
                # Render PNG image
                renderer = ImageRenderer(dot_path, self.config.verbose)
                renderer.render(
                    self.config.dot_file_path,
                    self.config.output_path,
                    self.config.node_padding,
                )

            # Cleanup
            if not self.config.keep_dot:
                self.file_manager.cleanup(self.config.dot_file_path)

            # Report success
            self._report_success()

            return self.config.output_path

        finally:
            # Return to original directory
            if Path.cwd() != original_dir:
                import os

                os.chdir(original_dir)

    def _report_success(self) -> None:
        """Report successful generation."""
        console.print(
            f"[bold green][ OK    ][/] Successfully generated: [white]{self.config.output_path}[/]"
        )

        if self.config.output_path.exists():
            size_mb = self.file_manager.get_file_size_mb(self.config.output_path)
            console.print(f"[cyan][ INFO  ][/] File size: [white]{size_mb:.2f} MB[/]")
