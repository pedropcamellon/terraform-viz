# Examples

This folder contains example Terraform DOT files for testing and demonstration.

## Files

- `sample_graph.dot` - Sample AWS infrastructure with VPC, subnet, security group, and EC2 instance

## Usage

Test the ASCII renderer with the sample:

```bash
# From the examples directory
cd examples
uv run python -c "from terraform_viz.ascii_renderer import AsciiRenderer; from pathlib import Path; r = AsciiRenderer(); r.render(Path('sample_graph.dot'))"

# Or from the root directory
uv run python -c "from terraform_viz.ascii_renderer import AsciiRenderer; from pathlib import Path; r = AsciiRenderer(); r.render(Path('examples/sample_graph.dot'))"
```
