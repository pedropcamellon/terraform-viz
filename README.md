# tfviz - Terraform Infrastructure Visualizer

A simple, fast CLI tool for generating PNG visualizations of your Terraform infrastructure.

## Overview

`tfviz` generates visual diagrams showing your Terraform resources, their dependencies, and relationships. Perfect for understanding complex infrastructure, documentation, and identifying potential issues.

## Features

- 🎨 **PNG output** - High-quality visualizations ready for documentation
- 🔍 **Auto-detection** - Finds Terraform and Graphviz automatically
- 📁 **Flexible paths** - Work with any Terraform directory
- 🧹 **Clean operation** - Optional intermediate file cleanup
- 💬 **Verbose mode** - Detailed progress information
- ❌ **Error handling** - Clear error messages and suggestions

## Installation

### Prerequisites

1. **Terraform** - Available in PATH
2. **Graphviz** - Install with: `winget install graphviz`
3. **Python packages** - Managed by UV in this project

### Quick Start

```bash
# Basic usage - generates terraform_graph.png
uv run python tfviz.py

# Custom output filename  
uv run python tfviz.py -o infrastructure.png

# Work with different Terraform directory
uv run python tfviz.py --terraform-dir ../production

# Verbose output with intermediate files kept
uv run python tfviz.py -v --keep-dot
```

## Command Line Options

```
usage: tfviz.py [-h] [-o OUTPUT] [--terraform-dir TERRAFORM_DIR] [--keep-dot] [--verbose]

Generate PNG visualization of Terraform infrastructure

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output PNG filename (default: terraform_graph.png)
  --terraform-dir TERRAFORM_DIR
                        Directory containing Terraform files (default: current directory)
  --keep-dot            Keep intermediate DOT file after rendering
  --verbose, -v         Enable verbose output

Examples:
  tfviz.py                          # Generate terraform_graph.png in current directory
  tfviz.py -o my_infra.png          # Generate with custom output filename
  tfviz.py --keep-dot               # Keep intermediate DOT file
  tfviz.py --terraform-dir ../dev   # Use Terraform files from different directory
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
