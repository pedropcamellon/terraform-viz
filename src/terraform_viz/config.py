"""Configuration management for terraform-viz."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class TFVizConfig:
    """Configuration for tfviz visualization."""

    tf_path: str
    tf_dir: Path
    output_path: Path | None
    plan_file: Path | None
    node_padding: float
    keep_dot: bool
    verbose: bool
    terminal_output: bool = False

    @property
    def dot_file_path(self) -> Path:
        """Get the path for the temporary DOT file."""
        # Save DOT file alongside output file
        if self.output_path and self.output_path.suffix:
            return self.output_path.with_suffix(".dot")
        elif self.output_path:
            return self.output_path.parent / "tf_graph.dot"
        # Fallback for ASCII mode with no output file
        return Path.cwd() / "output" / "tf_graph.dot"
