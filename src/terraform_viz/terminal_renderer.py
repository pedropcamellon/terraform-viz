"""Terminal diagram rendering using Rich library."""

import re
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text

console = Console()


class TerminalRenderer:
    """Renders DOT files as Rich-formatted terminal diagrams."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def render(self, dot_file: Path, output_file: Path | None = None) -> str:
        """Render DOT file to Rich-formatted terminal diagram."""
        if self.verbose:
            console.print("[cyan]>>>[/] Rendering terminal diagram...")

        dot_content = dot_file.read_text()
        nodes, edges = self._parse_dot_file(dot_content)
        self._render_rich_diagram(nodes, edges)
        return ""  # Rich output is printed directly

    def _parse_dot_file(
        self, dot_content: str
    ) -> tuple[list[str], list[tuple[str, str]]]:
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

    def _render_rich_diagram(
        self, nodes: list[str], edges: list[tuple[str, str]]
    ) -> None:
        """Render diagram using Rich library features as a hierarchical graph."""
        console.print()

        # Header
        header = Text("TERRAFORM INFRASTRUCTURE GRAPH", style="bold cyan")
        console.print(Panel(header, border_style="cyan"))
        console.print()

        # Build parent->children map (reverse the edges)
        children_map = {}  # parent -> [children]
        for source, target in edges:
            if target not in children_map:
                children_map[target] = []
            children_map[target].append(source)

        # Find root nodes (nodes that have children but aren't children themselves)
        all_children = set()
        for children_list in children_map.values():
            all_children.update(children_list)

        root_nodes = [
            node for node in nodes if node in children_map and node not in all_children
        ]

        # If no clear roots, use nodes with most children
        if not root_nodes:
            root_nodes = sorted(
                children_map.keys(),
                key=lambda x: len(children_map.get(x, [])),
                reverse=True,
            )[:5]

        # Group nodes by type for coloring
        def get_node_style(node: str) -> tuple[str, str]:
            """Return (emoji, style) for a node."""
            if node.startswith("var."):
                return "📥", "yellow"
            elif node.startswith("provider"):
                return "💎", "magenta"
            elif node.startswith("data."):
                return "🔍", "blue"
            elif node.startswith("output."):
                return "📤", "bright_blue"
            elif node.startswith("module."):
                # Check for specific module types
                if "cosmos" in node or "cosmosdb" in node or "database" in node:
                    return "📚", "bright_cyan"
                elif "storage" in node:
                    return "💾", "cyan"
                elif "service_bus" in node or "servicebus" in node:
                    return "📨", "cyan"
                elif "function" in node:
                    return "⚡", "cyan"
                elif (
                    "monitoring" in node
                    or "application_insights" in node
                    or "log_analytics" in node
                ):
                    return "📊", "cyan"
                else:
                    return "📦", "cyan"
            # Specific resource types
            elif "resource_group" in node:
                return "🏗️", "bright_magenta"
            elif "role_assignment" in node or "role_definition" in node:
                return "🔑", "bright_yellow"
            elif "cosmosdb" in node or "cosmos_db" in node:
                return "📚", "bright_cyan"
            elif "storage_account" in node or "storage_container" in node:
                return "💾", "bright_blue"
            elif "servicebus" in node or "service_bus" in node:
                return "📨", "blue"
            elif "function_app" in node:
                return "⚡", "yellow"
            elif "application_insights" in node or "log_analytics" in node:
                return "📊", "magenta"
            else:
                return "📦", "green"

        def simplify_name(name: str) -> str:
            """Simplify node name for display."""
            name = name.replace("module.", "", 1)
            name = name.replace(
                'provider["registry.terraform.io/hashicorp/', ""
            ).rstrip('"]')
            return name

        def build_tree(node: str, visited: set, depth: int = 0) -> Tree:
            """Recursively build a Rich Tree from the graph."""
            if depth > 10:  # Prevent infinite recursion
                return None

            emoji, style = get_node_style(node)
            display = f"{emoji} [{style}]{simplify_name(node)}[/]"
            tree = Tree(display)

            if node in visited:
                tree.add("[dim](circular reference)[/]")
                return tree

            visited.add(node)
            children = children_map.get(node, [])
            for child in sorted(children):
                child_tree = build_tree(child, visited.copy(), depth + 1)
                if child_tree:
                    tree.add(child_tree)

            return tree

        # Render the graph starting from roots
        console.print("[bold cyan]Infrastructure Hierarchy[/]")
        console.print()

        visited_global = set()
        for root in root_nodes[:10]:  # Limit to top 10 roots
            if root in visited_global:
                continue
            tree = build_tree(root, set(), 0)
            console.print(tree)
            console.print()
            visited_global.add(root)

        # Show orphaned nodes (nodes with no parents or children)
        orphans = [n for n in nodes if n not in children_map and n not in all_children]
        if orphans:
            orphan_tree = Tree("[bold yellow]Standalone Resources[/]")
            for orphan in sorted(orphans)[:20]:
                emoji, style = get_node_style(orphan)
                orphan_tree.add(f"{emoji} [{style}]{simplify_name(orphan)}[/]")
            console.print(orphan_tree)
            console.print()

        # Summary
        resources = len(
            [
                n
                for n in nodes
                if not n.startswith(("provider", "var.", "output.", "data.", "module."))
            ]
        )
        modules = len([n for n in nodes if n.startswith("module.")])
        data_sources = len([n for n in nodes if n.startswith("data.")])

        summary = Text()
        summary.append(f"{resources} resources", style="bold green")
        summary.append("  •  ")
        summary.append(f"{modules} modules", style="bold cyan")
        summary.append("  •  ")
        summary.append(f"{data_sources} data sources", style="bold blue")
        summary.append("  •  ")
        summary.append(f"{len(edges)} dependencies", style="bold white")
        console.print(Panel(summary, title="Summary", border_style="cyan"))
        console.print()
