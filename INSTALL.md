# Installation Guide

## Prerequisites

- DaVinci Resolve 18.5+ (running)
- Python 3.9+

## Quick Install

```bash
# macOS/Linux
./install.sh

# Windows
install.bat
```

## Manual Install

```bash
# 1. Create venv
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (add to ~/.bashrc or ~/.zshrc)
```

**macOS:**
```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

**Windows (PowerShell):**
```powershell
$env:RESOLVE_SCRIPT_API = "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
$env:RESOLVE_SCRIPT_LIB = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
$env:PYTHONPATH = "$env:PYTHONPATH;$env:RESOLVE_SCRIPT_API\Modules\"
```

## Configuration

**Cursor/Claude Desktop** - Add to `~/.cursor/mcp.json`:
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

**Claude Code (WSL)** - Add to `~/.claude.json`:
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

## WSL Setup

1. Clone project to Windows filesystem (not WSL):
   ```powershell
   cd "C:\Users\YourName\Projects"
   git clone https://github.com/ywatanabe1989/davinci-resolve-mcp.git
   cd davinci-resolve-mcp
   python -m venv venv
   .\venv\Scripts\pip install -r requirements.txt
   ```

2. Configure Claude Code as shown above

3. If auto-detection fails, create `.env` from `.env.example`

## Verify Installation

```bash
./scripts/verify-installation.sh   # macOS/Linux
scripts\verify-installation.bat    # Windows
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Resolve not detected | Ensure DaVinci Resolve is running before starting |
| Import errors | Check environment variables are set correctly |
| Connection fails | Verify paths in MCP config match your installation |
| WSL timeout | Set `RESOLVE_WAIT_TIMEOUT=120` in `.env` |

Check `logs/` directory for detailed error messages.
