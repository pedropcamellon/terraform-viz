# tfviz - Terraform Infrastructure Visualizer

[![PyPI version](https://badge.fury.io/py/tfviz.svg)](https://badge.fury.io/py/tfviz)
[![Python Support](https://img.shields.io/pypi/pyversions/tfviz.svg)](https://pypi.org/project/tfviz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, fast CLI tool for generating PNG visualizations of your Terraform infrastructure.

## Overview

`tfviz` generates visual diagrams showing your Terraform resources, their dependencies, and relationships. Perfect for understanding complex infrastructure, documentation, and identifying potential issues.

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
pip install tfviz
# or
uv add tfviz
```

### From Source

```bash
git clone https://github.com/yourusername/tfviz.git
cd tfviz
uv pip install -e .
```

### Prerequisites

1. **Terraform** - Must be available in PATH or specify path with `--tf-path`
2. **Graphviz** - Install with: `winget install graphviz` (Windows) or `brew install graphviz` (macOS)

## Usage

### Quick Start

```bash
# Basic usage - generates timestamped PNG in output/
tfviz

# Custom output filename  
tfviz -o infrastructure.png

# Work with different Terraform directory
tfviz --tf-dir ../production

# Visualize a specific plan file
tfviz --plan-file tfplan

# Specify custom Terraform executable
tfviz --tf-path /path/to/terraform

# Verbose output with intermediate files kept
tfviz -v --keep-dot

# Adjust spacing between nodes
tfviz --node-padding 1.5
```

## Command Line Options

```
usage: tfviz [-h] [-o OUTPUT] [--tf-dir TF_DIR] [--tf-path TF_PATH] 
             [--keep-dot] [--verbose] [--node-padding NODE_PADDING] 
             [--plan-file PLAN_FILE]

Generate PNG visualization of Terraform infrastructure

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output PNG filename (default: auto-generated with timestamp)
  --tf-dir TF_DIR       Directory containing Terraform files (default: current directory)
  --tf-path TF_PATH     Path to Terraform executable or alias (default: terraform)
  --keep-dot            Keep intermediate DOT file after rendering
  --verbose, -v         Enable verbose output
  --node-padding NODE_PADDING
                        Spacing between nodes (default: 1.0, larger = more spaced out)
  --plan-file PLAN_FILE
                        Path to Terraform plan file to visualize (optional)
```

## How It Works

1. **Discovery** - Locates Terraform and Graphviz executables
2. **Graph Generation** - Runs `terraform graph` to create DOT format dependency graph
3. **Rendering** - Uses Graphviz to convert DOT file to PNG
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

- Install Terraform or ensure it's in your PATH

**Graphviz not found**:

- Install Graphviz with: winget install graphviz

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

## File Structure

```
tfviz/
├── tfviz.py              # Main CLI tool
├── README.md             # This documentation
├── terraform_graph.dot   # Intermediate DOT file (if --keep-dot used)
└── *.png                 # Generated visualization files
```

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

### Terraform Directory Structure

When using `--terraform-dir`, the tool works with any directory containing `.tf` files:

```
project/
├── infrastructure/
│   ├── tfviz/              # This tool location
│   ├── main.tf             # Terraform files here
│   ├── variables.tf
│   └── outputs.tf
├── dev/
│   └── *.tf                # Dev environment  
└── production/
    └── *.tf                # Production environment
```

Use: `uv run python tfviz.py --terraform-dir ../dev` to visualize dev environment

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
