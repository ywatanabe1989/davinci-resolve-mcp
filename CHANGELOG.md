# Changelog

## v1.4.0 - December 2025

### New Features
- **Modular API System**: 50+ new MCP tools organized into dedicated modules
- **WSL2 Support**: Run from WSL2 while controlling DaVinci Resolve on Windows
- **GitHub Actions CI**: Automated testing across Python 3.9-3.12
- **Pre-commit Hooks**: Code quality checks (syntax, formatting, linting, tests)

### New Modules
- `database_operations.py`: Database switching, folder navigation, project import/export/archive
- `media_storage_operations.py`: Volume listing, file browsing, media pool integration
- `gallery_operations.py`: Still albums, PowerGrade management, still capture/export
- `timeline_advanced.py`: Compound clips, Fusion clips, generators, titles
- `timeline_export.py`: AAF/EDL/XML import/export, timecode control, scene detection
- `marker_operations.py`: Timeline and clip markers with custom data support
- `capture.py`: WSL-to-Windows screenshot capture via PowerShell
- `capture_continuous.py`: Continuous monitoring with GIF creation

### Quality Assurance
- 113 unit tests with mocked DaVinci Resolve API
- Test coverage for all new modules
- Automated linting with ruff and formatting with black

### Documentation
- Updated README with new features and WSL instructions
- Cleaned up duplicate sections in README

## v1.3.8 - April 2025

### Improvements
- **Cursor Integration**: Added comprehensive documentation for Cursor setup process
- **Entry Point**: Standardized on `main.py` as the proper entry point (replaces direct use of `resolve_mcp_server.py`)
- **Configuration Templates**: Updated example configuration files to use correct paths
- **Documentation**: Added detailed troubleshooting for "client closed" errors in Cursor

### Fixed
- Ensured consistent documentation for environment setup

## v1.3.7 - Installation Improvements, Path Resolution Fixes, Enhanced Configuration

### Improvements
// ... existing content ... 