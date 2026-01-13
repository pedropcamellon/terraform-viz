"""Terraform graph generation."""

import subprocess
from pathlib import Path


class GraphGenerator:
    """Generates Terraform dependency graphs."""

    def __init__(self, tf_path: str, verbose: bool = False):
        self.tf_path = tf_path
        self.verbose = verbose

    def generate(self, output_file: Path, plan_file: Path | None = None) -> None:
        """Generate Terraform dependency graph in DOT format."""
        if self.verbose:
            print("🔄 Generating TF graph...")

        with open(output_file, "w") as dot_file:
            cmd = self._build_command(plan_file)

            result = subprocess.run(
                cmd,
                stdout=dot_file,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
            )

            if result.returncode != 0:
                raise RuntimeError(f"Failed to generate TF graph: {result.stderr}")

    def _build_command(self, plan_file: Path | None) -> str:
        """Build the terraform graph command."""
        if plan_file:
            return f'{self.tf_path} graph -plan "{plan_file}"'
        return f"{self.tf_path} graph"
