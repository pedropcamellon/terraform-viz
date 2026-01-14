# terraform-viz - Terraform Infrastructure Visualizer

[![PyPI version](https://badge.fury.io/py/terraform-viz.svg)](https://badge.fury.io/py/terraform-viz)
[![Python Support](https://img.shields.io/pypi/pyversions/terraform-viz.svg)](https://pypi.org/project/terraform-viz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, fast CLI tool for generating PNG visualizations of your Terraform infrastructure.

## Overview

`terraform-viz` generates visual diagrams showing your Terraform resources, their dependencies, and relationships. Output to terminal by default for quick review, or generate PNG images for documentation.

## Features

- 📺 **Terminal output** - Rich-formatted diagrams for quick review and CI/CD (default)
- 🎨 **PNG generation** - High-quality images for documentation (with `-o` flag)
- 🔍 **Flexible paths** - Work with any Terraform directory
- 📦 **Plan support** - Visualize specific plan files
- 🧹 **Clean operation** - Optional intermediate file cleanup
- 💬 **Verbose mode** - Detailed progress information
- 🎯 **Custom spacing** - Adjustable node padding for PNG layouts

## Installation

### From PyPI (Recommended)

```bash
pip install terraform-viz
# or
uv add terraform-viz
```

### From Source

```bash
git clone https://github.com/pedropcamellon/terraform-viz.git
cd terraform-viz
uv pip install -e .
```

### Prerequisites

1. **Terraform** - Must be available in PATH or specify path with `--tf-path`
2. **Graphviz** - Only required for PNG images (with `-o` flag)
   - Install: `winget install graphviz` (Windows) or `brew install graphviz` (macOS)

## Usage

### Quick Start

```bash
# Basic usage - shows diagram in terminal
terraform-viz

# Generate PNG image for documentation
terraform-viz -o infrastructure.png

# Work with different Terraform directory
terraform-viz --tf-dir ../production

# Visualize a specific plan file
terraform-viz --plan-file tfplan

# Specify custom Terraform executable
terraform-viz --tf-path /path/to/terraform

# Verbose output with intermediate files kept
terraform-viz -v --keep-dot

# Adjust spacing between nodes (PNG only)
terraform-viz -o output.png --node-padding 1.5
```

## Command Line Options

```
usage: terraform-viz [-h] [-o OUTPUT] [--tf-dir TF_DIR] [--tf-path TF_PATH] 
             [--keep-dot] [--verbose] [--node-padding NODE_PADDING] 
             [--plan-file PLAN_FILE]

Generate visualizations of Terraform infrastructure (terminal output by default, PNG with -o)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Generate PNG image (default: terminal output only)
  --tf-dir TF_DIR       Directory containing Terraform files (default: current directory)
  --tf-path TF_PATH     Path to Terraform executable or alias (default: terraform)
  --keep-dot            Keep intermediate DOT file after rendering
  --verbose, -v         Enable verbose output
  --node-padding NODE_PADDING
                        Spacing between nodes for PNG output (default: 1.0, larger = more spaced out)
  --plan-file PLAN_FILE
                        Path to Terraform plan file to visualize (optional)
```

## How It Works

1. **Discovery** - Locates Terraform executable (and Graphviz if generating PNG)
2. **Graph Generation** - Runs `terraform graph` to create DOT format dependency graph
3. **Rendering** - Displays ASCII diagram in terminal (default) or generates PNG with `-o` flag
4. **Cleanup** - Optionally removes intermediate DOT file

## Understanding the Output

### Modules vs Resources

**Resources** are the actual infrastructure components you're creating:

- Direct resources in your root Terraform configuration
- Examples: `azurerm_storage_account.main`, `aws_instance.web`, `random_string.suffix`
- These are the "real" things that get created in your cloud provider

**Modules** are reusable packages of Terraform configurations:

- Contain multiple resources bundled together
- Prefixed with `module.` in the graph (e.g., `module.storage.azurerm_storage_account.this`)
- Help organize and reuse infrastructure patterns
- Each module creates its own set of resources

### Reading the Hierarchy

The terminal output shows a **parent → child dependency tree**:

- **Parent at top**: Resources that others depend on
- **Children nested below**: Resources that depend on the parent
- **Multiple appearances**: A resource may appear multiple times if it has dependencies on different parents

**Example:**

```
🏗️ azurerm_resource_group.mini (parent)
├── 📚 cosmos_db.azurerm_cosmosdb_account.this (child)
│   └── 📦 azurerm_linux_web_app.backend (grandchild)
```

This means:

- The web app depends on the Cosmos DB account
- The Cosmos DB account depends on the resource group
- All must be created in order: resource group → database → web app

**Example:**

```
module.storage.azurerm_storage_account.this  ← Module resource (inside "storage" module)
azurerm_resource_group.main                  ← Root resource (in your main config)
```

### ASCII Output (Default)

The ASCII diagram shows:

- **📥 Variables** - Input variables
- **💎 Providers** - Cloud/infrastructure providers
- **🔍 Data Sources** - External data being fetched
- **📚 Modules** - Terraform modules
- **📦 Resources** - Terraform resources
- **📤 Outputs** - Output values
- **└─►** - Dependencies between resources

### PNG Output (with `-o` flag)

The generated PNG shows:

- **Resources** - Terraform resources (rectangles)
- **Data Sources** - External data being fetched (diamonds)  
- **Variables** - Input variables (ovals)
- **Outputs** - Output values (house shapes)
- **Dependencies** - Arrows showing resource relationships

Both formats help you:

- Understand resource dependencies
- Identify circular dependencies
- Visualize infrastructure complexity
- Document your architecture

## Troubleshooting

### Common Issues

**Terraform not found**:

- Check if Terraform is in PATH: `where terraform` (Windows) or `which terraform` (macOS/Linux)
- Install Terraform or ensure it's in your PATH

**Graphviz not found** (only for PNG generation):

- Check if Graphviz is in PATH: `where dot` (Windows) or `which dot` (macOS/Linux)
- Install Graphviz with: `winget install graphviz` (Windows) or `brew install graphviz` (macOS)
- Note: Not needed for ASCII output (default)

**Empty visualization**:

- Check that you're in a directory with Terraform files (*.tf)
- Ensure Terraform files are valid and can be parsed

**Large file sizes**:

- Complex infrastructures generate large PNGs
- Consider splitting large configurations into modules

### Verbose Mode

Use `-v` flag to see detailed information:

- Executable paths being used
- Directory changes
- File operations
- Cleanup actions

## Advanced Usage

### Direct Graphviz Commands

You can also use the DOT file directly with Graphviz command-line tools:

```bash
# Generate different formats (run with --keep-dot first)
dot -Tsvg terraform_graph.dot -o graph.svg
dot -Tpng terraform_graph.dot -o graph.png  
dot -Tpdf terraform_graph.dot -o graph.pdf

# Generate interactive HTML
dot -Tsvg terraform_graph.dot | dot -Tcmapx > graph.map
```

Use: `uv run python terraform_viz.py --tf-dir "C:/../dev"` to visualize dev environment

## Integration

### Documentation

Perfect for including infrastructure diagrams in:

- README files
- Wiki pages  
- Architecture documents
- Presentations

### CI/CD

Perfect for CI/CD pipelines - ASCII output works great in logs and doesn't require Graphviz:

```bash
# In your CI/CD pipeline - shows diagram in logs
terraform-viz --tf-dir ./infrastructure

# Generate PNG for artifacts
terraform-viz --tf-dir ./infrastructure -o infrastructure.png
```

Can be automated in pipelines to:

- Display infrastructure changes in build logs
- Generate PNG diagrams for deployment reports
- Archive infrastructure snapshots
- Validate Terraform configurations

---

## Development

### Building & Testing

```bash
# Build package
uv build

# Test CLI (shows ASCII by default)
uv run terraform-viz --help

# Test ASCII mode (default)
uv run terraform-viz --tf-dir /path/to/terraform

# Test PNG generation
uv run terraform-viz --tf-dir /path/to/terraform -o output.png
```

### Project Structure

```
terraform-viz/
├── .github/workflows/      # CI/CD pipelines
├── examples/               # Sample DOT files
├── src/terraform_viz/      # Source code
│   ├── cli.py             # CLI entry point
│   ├── config.py          # Configuration
│   ├── orchestrator.py    # Main orchestration
│   ├── renderer.py        # PNG rendering
│   ├── ascii_renderer.py  # ASCII rendering
│   ├── graph_generator.py # Terraform graph generation
│   ├── file_manager.py    # File operations
│   └── executables.py     # Executable finding
├── output/                # Generated visualizations
└── pyproject.toml        # Package configuration
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Publishing to PyPI

### For Maintainers

**One-time setup:**

1. Configure PyPI Trusted Publishing at <https://pypi.org/manage/account/publishing/>
   - Project: `terraform-viz`
   - Owner: `pedropcamellon`
   - Repository: `terraform-viz`
   - Workflow: `publish.yml`

**To release a new version:**

```bash
# 1. Update version in pyproject.toml and CHANGELOG.md
# 2. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "Release v0.2.0"
git push

# 3. Create and push tag
git tag v0.2.0
git push origin v0.2.0

# 4. Create GitHub release (triggers automatic PyPI publish)
gh release create v0.2.0 --title "v0.2.0" --notes-file CHANGELOG.md
```

The GitHub Action will automatically build and publish to PyPI.

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- **GitHub**: <https://github.com/pedropcamellon/terraform-viz>
- **PyPI**: <https://pypi.org/project/terraform-viz/>
- **Issues**: <https://github.com/pedropcamellon/terraform-viz/issues>
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
