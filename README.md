# DaVinci Resolve MCP Server

[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](https://github.com/ywatanabe1989/davinci-resolve-mcp/releases)
[![CI](https://github.com/ywatanabe1989/davinci-resolve-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ywatanabe1989/davinci-resolve-mcp/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

MCP server connecting AI assistants (Cursor, Claude Desktop, Claude Code) to DaVinci Resolve.

## Requirements

- DaVinci Resolve 18.5+ (running)
- Python 3.9+

## Installation

```bash
git clone https://github.com/ywatanabe1989/davinci-resolve-mcp.git
cd davinci-resolve-mcp

# macOS/Linux
./install.sh

# Windows
install.bat
```

## Configuration

### Cursor / Claude Desktop

Add to `~/.cursor/mcp.json` (macOS) or `%APPDATA%\Cursor\mcp.json` (Windows):

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/davinci-resolve-mcp/src/main.py"]
    }
  }
}
```

### Claude Code (WSL)

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "/path/to/davinci-resolve-mcp/scripts/wsl-launcher.sh",
      "args": []
    }
  }
}
```

Optional: Create `.env` from `.env.example` if auto-detection fails.

## Features

| Category | Capabilities |
|----------|-------------|
| Project | List, open, create, save projects |
| Timeline | Create, switch, add markers, import/export EDL/XML/AAF |
| Media Pool | Import media, create bins, add clips to timeline |
| Gallery | Still albums, PowerGrade management |
| General | Get version, switch pages (Edit, Color, Fusion, etc.) |

See [docs/FEATURES.md](docs/FEATURES.md) for full list.

## Troubleshooting

1. Ensure DaVinci Resolve is running before starting the server
2. Verify environment variables if connection fails:
   - **macOS**: `RESOLVE_SCRIPT_API`, `RESOLVE_SCRIPT_LIB`, `PYTHONPATH`
   - **Windows**: Same variables with Windows paths
3. Check logs in `logs/` directory

See [INSTALL.md](INSTALL.md) for detailed troubleshooting.

## License

MIT

## Acknowledgments

- Blackmagic Design for DaVinci Resolve API
- Original author: Samuel Gursky ([github.com/samuelgursky](https://github.com/samuelgursky))
