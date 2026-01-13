"""Configuration management for terraform-viz."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class TFVizConfig:
    """Configuration for tfviz visualization."""

    tf_path: str
    tf_dir: Path
    output_path: Path
    plan_file: Path | None
    node_padding: float
    keep_dot: bool
    verbose: bool

    @property
    def dot_file_path(self) -> Path:
        """Get the path for the temporary DOT file."""
        return Path("tf_graph.dot")
