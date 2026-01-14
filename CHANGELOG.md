# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - Hierarchical Graph Visualization

### Added

- **Hierarchical graph display** - Shows true parent→child dependency relationships
- **Context-aware emojis and colors** - Different resource type icons:
  - 🏗️ Resource Groups (bright magenta)
  - 🔑 Role Assignments (bright yellow)
  - 📚 CosmosDB/Databases (bright cyan)
  - 💾 Storage Accounts (bright blue)
  - 📨 Service Bus (blue)
  - ⚡ Function Apps (yellow)
  - 📊 Monitoring/Insights (magenta)
- **Dependency hierarchy explanation** in README with visual examples

### Changed

- **Graph structure reversed** - Parents now shown at top with children nested below
- Renamed from `AsciiRenderer` to `TerminalRenderer` throughout codebase
- Replaced "ASCII" terminology with "terminal output" in documentation

### Fixed

- Removed duplicate tree rendering at end of output
- Removed unused plain text diagram generation method

_Released: 2026-01-13_

## [0.2.0] - Terminal-First with Rich Output

### Added

- **ASCII diagram output mode** - Terminal-friendly visualization (now the default!)
- New `AsciiRenderer` class for DOT-to-ASCII conversion
- Shows resource hierarchy with tree-style dependency arrows
- Displays modules, resources, data sources with emoji indicators
- GitHub Actions workflow for automated PyPI publishing
- PyPI trusted publishing configuration
- Comprehensive publishing documentation (PUBLISHING_SETUP.md, DEVELOPMENT.md)
- Enhanced package metadata with additional classifiers and URLs
- Improved .gitignore with comprehensive exclusions
- Examples folder with sample Terraform DOT files

### Changed

- **ASCII is now the default output** - displays diagram in terminal
- PNG generation now requires `-o` flag to specify output file
- Graphviz dependency now optional (only required for PNG output)
- Fixed `--keep-dot` to save DOT files in output directory alongside PNG/TXT
- Updated CLI help text and welcome screen to reflect ASCII-first approach
- Enhanced MANIFEST.in to include examples and documentation
- Updated pyproject.toml with maintainer information and documentation links

### Fixed

- ASCII renderer now correctly parses modern Terraform graph output
- DOT file parsing supports module subgraphs
- Module names simplified in ASCII output (removes `module.` prefix)

_Released: 2026-01-13_

## [0.1.1] - Python Compatibility Fix

### Fixed

- Update Python version requirement from ==3.13.3 to >=3.10 for broader compatibility
- Update rich dependency from ==13.7.0 to >=13.7.0
- Add Python 3.10, 3.11, 3.12 classifiers

_Released: 2026-01-13_

## [0.1.0] - Initial Release

### Added

- Initial release
- Generate PNG visualizations of Terraform infrastructure
- Support for custom Terraform executable paths
- Plan file visualization support
- Configurable node padding for graph spacing
- Rich CLI interface with progress indicators
- Automatic output directory management
- Verbose mode for detailed execution logs

_Released: 2026-01-13_
