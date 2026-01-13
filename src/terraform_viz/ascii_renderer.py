"""ASCII diagram rendering for terminal output."""

import re
from pathlib import Path

from rich.console import Console

console = Console()


class AsciiRenderer:
    """Renders DOT files as ASCII diagrams for terminal display."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def render(self, dot_file: Path, output_file: Path | None = None) -> str:
        """Render DOT file to ASCII diagram."""
        if self.verbose:
            console.print("[cyan]>>>[/] Rendering ASCII diagram...")

        dot_content = dot_file.read_text()
        nodes, edges = self._parse_dot_file(dot_content)
        ascii_diagram = self._create_ascii_diagram(nodes, edges)

        # Print to console
        console.print(ascii_diagram)

        # Optionally save to file
        if output_file:
            output_file.write_text(ascii_diagram)
            if self.verbose:
                console.print(f"[cyan]>>>[/] Saved ASCII diagram to: [white]{output_file}[/]")

        return ascii_diagram

    def _parse_dot_file(self, dot_content: str) -> tuple[list[str], list[tuple[str, str]]]:
        """Parse DOT file and extract nodes and edges."""
        nodes = []
        edges = []

        # Extract node definitions - matches: "node_name" [label="..."];
        node_pattern = r'"([^"]+)"\s*\[label\s*='
        for match in re.finditer(node_pattern, dot_content):
            node = match.group(1).strip()
            if node and node not in nodes:
                nodes.append(node)

        # Extract edges - matches: "source" -> "target";
        edge_pattern = r'"([^"]+)"\s*->\s*"([^"]+)"'
        for match in re.finditer(edge_pattern, dot_content):
            source = match.group(1).strip()
            target = match.group(2).strip()
            edges.append((source, target))

        return nodes, edges

    def _create_ascii_diagram(
        self, nodes: list[str], edges: list[tuple[str, str]]
    ) -> str:
        """Create a simple ASCII representation of the graph."""
        output = []
        output.append("=" * 80)
        output.append("Terraform Infrastructure Diagram (ASCII)")
        output.append("=" * 80)
        output.append("")

        # Group nodes by type
        resources = [
            n
            for n in nodes
            if not n.startswith(("provider", "var.", "output.", "data.", "module."))
        ]
        modules = [n for n in nodes if n.startswith("module.")]
        providers = [n for n in nodes if n.startswith("provider")]
        variables = [n for n in nodes if n.startswith("var.")]
        outputs = [n for n in nodes if n.startswith("output.")]
        data_sources = [n for n in nodes if n.startswith("data.")]

        # Display nodes by type
        if variables:
            output.append("VARIABLES:")
            for var in variables:
                output.append(f"  📥 {var}")
            output.append("")

        if providers:
            output.append("PROVIDERS:")
            for prov in providers:
                # Simplify provider name
                prov_display = prov.replace('provider["registry.terraform.io/hashicorp/', "").rstrip('"]')
                output.append(f"  💎 {prov_display}")
            output.append("")

        if data_sources:
            output.append("DATA SOURCES:")
            for data in data_sources:
                output.append(f"  🔍 {data}")
                # Show dependencies
                deps = [edge[1] for edge in edges if edge[0] == data]
                if deps:
                    for dep in deps:
                        output.append(f"     └─► {dep}")
            output.append("")

        if modules:
            output.append("MODULES:")
            for mod in modules:
                # Simplify module name
                mod_display = mod.replace("module.", "", 1)
                output.append(f"  📚 {mod_display}")
                # Show dependencies
                deps = [edge[1] for edge in edges if edge[0] == mod]
                if deps:
                    for dep in deps:
                        dep_display = dep.replace("module.", "", 1) if dep.startswith("module.") else dep
                        output.append(f"     └─► {dep_display}")
            output.append("")

        if resources:
            output.append("RESOURCES:")
            for res in resources:
                output.append(f"  📦 {res}")
                # Show dependencies
                deps = [edge[1] for edge in edges if edge[0] == res]
                if deps:
                    for dep in deps:
                        dep_display = dep.replace("module.", "", 1) if dep.startswith("module.") else dep
                        output.append(f"     └─► {dep_display}")
            output.append("")

        if outputs:
            output.append("OUTPUTS:")
            for out in outputs:
                output.append(f"  📤 {out}")
                # Show what it depends on
                deps = [edge[1] for edge in edges if edge[0] == out]
                if deps:
                    for dep in deps:
                        output.append(f"     └─► {dep}")
            output.append("")

        output.append("=" * 80)
        output.append(
            f"Total: {len(resources)} resources, {len(modules)} modules, {len(data_sources)} data sources, {len(edges)} dependencies"
        )
        output.append("=" * 80)

        return "\n".join(output)
