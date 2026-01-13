# terraform-viz - Terraform Infrastructure Visualizer

[![PyPI version](https://badge.fury.io/py/terraform-viz.svg)](https://badge.fury.io/py/terraform-viz)
[![Python Support](https://img.shields.io/pypi/pyversions/terraform-viz.svg)](https://pypi.org/project/terraform-viz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, fast CLI tool for generating PNG visualizations of your Terraform infrastructure.

## Overview

`terraform-viz` generates visual diagrams showing your Terraform resources, their dependencies, and relationships. Perfect for understanding complex infrastructure, documentation, and identifying potential issues.

## Features

- 🎨 **PNG output** - High-quality visualizations ready for documentation
- 🔍 **Flexible paths** - Work with any Terraform directory
- 📦 **Plan support** - Visualize specific plan files
- 🧹 **Clean operation** - Optional intermediate file cleanup
- 💬 **Verbose mode** - Detailed progress information with Rich formatting
- ❌ **Error handling** - Clear error messages and suggestions
- 🎯 **Custom spacing** - Adjustable node padding for optimal layouts

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
2. **Graphviz** - Install with: `winget install graphviz` (Windows) or `brew install graphviz` (macOS)
   - *Note: Graphviz not required when using `--ascii` mode*

## Usage

### Quick Start

```bash
# Basic usage - generates timestamped PNG in output/
terraform-viz

# Custom output filename  
terraform-viz -o infrastructure.png

# Work with different Terraform directory
terraform-viz --tf-dir ../production

# Visualize a specific plan file
terraform-viz --plan-file tfplan

# Specify custom Terraform executable
terraform-viz --tf-path /path/to/terraform

# Verbose output with intermediate files kept
terraform-viz -v --keep-dot

# Adjust spacing between nodes
terraform-viz --node-padding 1.5

# ASCII output for terminal/CI-CD (no Graphviz needed!)
terraform-viz --ascii
```

## Command Line Options

```
usage: terraform-viz [-h] [-o OUTPUT] [--tf-dir TF_DIR] [--tf-path TF_PATH] 
             [--keep-dot] [--ascii] [--verbose] [--node-padding NODE_PADDING] 
             [--plan-file PLAN_FILE]

Generate PNG visualization of Terraform infrastructure

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output PNG filename (default: auto-generated with timestamp)
  --tf-dir TF_DIR       Directory containing Terraform files (default: current directory)
  --tf-path TF_PATH     Path to Terraform executable or alias (default: terraform)
  --keep-dot            Keep intermediate DOT file after rendering
  --ascii               Output ASCII diagram to terminal instead of PNG (perfect for CI/CD)
  --verbose, -v         Enable verbose output
  --node-padding NODE_PADDING
                        Spacing between nodes (default: 1.0, larger = more spaced out)
  --plan-file PLAN_FILE
                        Path to Terraform plan file to visualize (optional)
```

## How It Works

1. **Discovery** - Locates Terraform and Graphviz executables (Graphviz skipped in ASCII mode)
2. **Graph Generation** - Runs `terraform graph` to create DOT format dependency graph
3. **Rendering** - Converts to PNG (via Graphviz) or ASCII diagram (for terminal output)
4. **Cleanup** - Optionally removes intermediate files

## Understanding the Output

The generated PNG shows:

- **Resources** - Terraform resources (rectangles)
- **Data Sources** - External data being fetched (diamonds)  
- **Variables** - Input variables (ovals)
- **Outputs** - Output values (house shapes)
- **Dependencies** - Arrows showing resource relationships

This helps you:

- Understand resource dependencies
- Identify circular dependencies
- Visualize infrastructure complexity
- Document your architecture

## Troubleshooting

### Common Issues

**Terraform not found**:

- Check if Terraform is in PATH: `where terraform` (Windows) or `which terraform` (macOS/Linux)
- Install Terraform or ensure it's in your PATH

**Graphviz not found**:

- Check if Graphviz is in PATH: `where dot` (Windows) or `which dot` (macOS/Linux)
- Install Graphviz with: `winget install graphviz` (Windows) or `brew install graphviz` (macOS)

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

Can be automated in pipelines to:

- Generate diagrams on infrastructure changes
- Include in deployment reports
- Archive infrastructure snapshots

#### ASCII Diagrams for Terminal/CI/CD

For headless environments or CI/CD pipelines, use the built-in `--ascii` flag to render diagrams directly in the terminal instead of Terraform's verbose plan output:

```bash
# Generate ASCII diagram to terminal
terraform-viz --ascii

# Save ASCII diagram to file
terraform-viz --ascii -o infrastructure.txt

# Use with different Terraform directory
terraform-viz --ascii --tf-dir ../production

# Combine with verbose mode
terraform-viz --ascii -v
```

**Benefits:**

- No Graphviz installation required
- Compact, readable diagrams in terminal output
- Better alternative to Terraform's verbose plan format
- Perfect for CI/CD logs and SSH sessions
- Shows resource hierarchy and dependencies clearly

**Example Output:**

```
================================================================================
Terraform Infrastructure Diagram (ASCII)
================================================================================

VARIABLES:
  📥 var.instance_type

RESOURCES:
  📦 aws_instance.web
     └─► aws_security_group.allow_http
     └─► aws_subnet.main
  📦 aws_vpc.main
     └─► provider[aws]

OUTPUTS:
  📤 output.instance_ip
     └─► aws_instance.web

================================================================================
Total: 4 resources, 0 data sources, 7 dependencies
================================================================================
```
