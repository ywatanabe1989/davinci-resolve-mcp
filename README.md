# DaVinci Resolve MCP Server

[![CI](https://github.com/ywatanabe1989/davinci-resolve-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ywatanabe1989/davinci-resolve-mcp/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/ywatanabe1989/davinci-resolve-mcp/releases)

Control DaVinci Resolve from AI assistants (Claude Code, Cursor, Claude Desktop) via [MCP](https://modelcontextprotocol.io/).

## Quick Start

### 1. Prerequisites

- DaVinci Resolve installed and running
- Python 3.9+
- Enable external scripting in Resolve:
  - **Preferences → System → General → External scripting using: Local**

### 2. Install

```bash
git clone https://github.com/ywatanabe1989/davinci-resolve-mcp.git
cd davinci-resolve-mcp
pip install -r requirements.txt
```

### 3. Configure Your AI Assistant

**Claude Code** (`~/.claude.json`):
```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "/full/path/to/davinci-resolve-mcp/resolve-mcp",
      "args": []
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "/full/path/to/davinci-resolve-mcp/resolve-mcp",
      "args": []
    }
  }
}
```

### 4. Run

```bash
./resolve-mcp
```

That's it. Now ask your AI assistant to control DaVinci Resolve.

---

## Platform Support

| Platform | Status | Entry Point |
|----------|--------|-------------|
| macOS | ✅ | `./resolve-mcp` |
| Windows | ✅ | `resolve-mcp.bat` |
| WSL | ✅ | `./resolve-mcp` (auto-bridges to Windows) |
| Linux | ✅ | `./resolve-mcp` |

### WSL Users

The script automatically detects WSL and bridges to Windows DaVinci Resolve. Just run `./resolve-mcp` - no extra configuration needed.

---

## What You Can Do

Ask your AI assistant things like:

- "What version of DaVinci Resolve is running?"
- "List all projects"
- "Create a new timeline called 'Edit v2'"
- "Switch to the Color page"
- "Add a marker at the current position"
- "Import media from /path/to/folder"

### Available Tools (50+)

| Category | Examples |
|----------|----------|
| **Project** | Open, create, save, close projects |
| **Timeline** | Create, switch, list timelines |
| **Media** | Import, organize, add to timeline |
| **Markers** | Add, list, delete markers |
| **Color** | Access color page, grades, stills |
| **Delivery** | Render queue, export settings |
| **Pages** | Switch between Edit, Color, Fusion, etc. |

---

## Troubleshooting

### "Not connected to DaVinci Resolve"

1. Make sure Resolve is running
2. Enable external scripting: **Preferences → System → General → External scripting using: Local**
3. Restart Resolve after enabling

### Check if it's working

```bash
./resolve-mcp --check
```

### Verbose mode

```bash
./resolve-mcp --verbose
```

---

## Development

```bash
# Run tests
python -m pytest tests/ -v

# Format code
black .

# Lint
ruff check .
```

## License

MIT

## Credits

- Blackmagic Design for DaVinci Resolve API
- [MCP Protocol](https://modelcontextprotocol.io/) by Anthropic
- Original author: Samuel Gursky
