"""Terraform graph generation."""

import subprocess
from pathlib import Path

from rich.console import Console

console = Console()


class GraphGenerator:
    """Generates Terraform dependency graphs."""

    def __init__(self, tf_path: str, verbose: bool = False):
        self.tf_path = tf_path
        self.verbose = verbose

    def generate(self, output_file: Path, plan_file: Path | None = None) -> None:
        """Generate Terraform dependency graph in DOT format."""
        with console.status("[yellow]Generating TF graph...[/]", spinner="dots"):
            if self.verbose:
                console.print("[cyan]>>>[/] Generating TF graph...")

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
                    error_msg = result.stderr.strip()

                    # Check if terraform command not found
                    if (
                        "not recognized" in error_msg
                        or "command not found" in error_msg
                    ):
                        console.print(
                            f"[bold red][ ERROR ][/] Terraform executable not found: [white]{self.tf_path}[/]"
                        )
                        console.print(
                            "[yellow][ HINT  ][/] Use [cyan]--tf-path[/] to specify the full path to terraform.exe"
                        )
                        console.print(
                            "[yellow][ HINT  ][/] Example: [cyan]terraform-viz --tf-path C:\\\\tools\\\\terraform.exe[/]"
                        )
                        raise RuntimeError("Terraform executable not accessible")
                    else:
                        console.print(
                            f"[bold red][ ERROR ][/] Failed to generate TF graph"
                        )
                        console.print(f"[dim]{error_msg}[/]")
                        raise RuntimeError("Terraform graph generation failed")

    def _build_command(self, plan_file: Path | None) -> str:
        """Build the terraform graph command."""
        if plan_file:
            return f'{self.tf_path} graph -plan "{plan_file}"'
        return f"{self.tf_path} graph"
