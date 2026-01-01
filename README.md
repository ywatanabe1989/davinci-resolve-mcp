# DaVinci Resolve MCP Server

[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](https://github.com/ywatanabe1989/davinci-resolve-mcp/releases)
[![CI](https://github.com/ywatanabe1989/davinci-resolve-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ywatanabe1989/davinci-resolve-mcp/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

MCP server connecting AI assistants (Cursor, Claude Desktop, Claude Code) to DaVinci Resolve.

## Quick Start

```bash
git clone https://github.com/ywatanabe1989/davinci-resolve-mcp.git
cd davinci-resolve-mcp
make
make status  # Show configuration instructions
```

## Requirements

- DaVinci Resolve 18.5+ (running)
- Python 3.9+

## Features

| Category | Capabilities |
|----------|-------------|
| Project | List, open, create, save projects |
| Timeline | Create, switch, add markers, import/export EDL/XML/AAF |
| Media Pool | Import media, create bins, add clips to timeline |
| Color | Color wheels, nodes, LUTs, presets |
| Gallery | Still albums, PowerGrade management |
| Render | Add to queue, start render, manage jobs |
| UI | Switch pages (Edit, Color, Fusion, Fairlight, Deliver) |

See [docs/FEATURES.md](docs/FEATURES.md) for 100+ available functions.

## Troubleshooting

```bash
make status  # Check configuration and get hints
```

If connection fails:
1. Ensure DaVinci Resolve is running
2. Check `.env` configuration (copy from `.env.example`)
3. Check `logs/` directory for errors

## License

MIT

## Acknowledgments

- Blackmagic Design for DaVinci Resolve API
- Original author: Samuel Gursky ([github.com/samuelgursky](https://github.com/samuelgursky))
