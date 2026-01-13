"""Main orchestrator for terraform-viz."""

from pathlib import Path

from .config import TFVizConfig
from .executables import ExecutableFinder
from .file_manager import FileManager
from .graph_generator import GraphGenerator
from .renderer import ImageRenderer


class TFVizOrchestrator:
    """Orchestrates the visualization generation process."""

    def __init__(self, config: TFVizConfig):
        self.config = config
        self.file_manager = FileManager(verbose=config.verbose)

    def execute(self) -> Path:
        """Execute the full visualization pipeline."""
        # Find required executables
        if self.config.verbose:
            print("🔍 Locating required executables...")

        dot_path = ExecutableFinder.find_graphviz()

        if self.config.verbose:
            print(f"✅ Found Graphviz: {dot_path}")
            print(f"✅ Using Terraform: {self.config.tf_path}")

        # Change to target directory
        original_dir = self.file_manager.change_directory(self.config.tf_dir)

        try:
            # Ensure output directory exists
            self.file_manager.ensure_output_dir(self.config.output_path)

            # Generate graph
            graph_gen = GraphGenerator(self.config.tf_path, self.config.verbose)
            graph_gen.generate(self.config.dot_file_path, self.config.plan_file)

            # Render image
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
        print(f"✅ Successfully generated: {self.config.output_path}")

        if self.config.output_path.exists():
            size_mb = self.file_manager.get_file_size_mb(self.config.output_path)
            print(f"📊 File size: {size_mb:.2f} MB")
