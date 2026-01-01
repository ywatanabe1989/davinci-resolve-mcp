# DaVinci Resolve MCP Server Launcher
# Called directly by Claude Code MCP config

$ProjectPath = "C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp"

# Set environment
$env:PYTHONPATH = $ProjectPath
$env:RESOLVE_SCRIPT_API = "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
$env:RESOLVE_SCRIPT_LIB = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"

# Run MCP server (use system Python if venv not available)
$VenvPython = "$ProjectPath\venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    & $VenvPython "$ProjectPath\src\main.py"
} else {
    & python "$ProjectPath\src\main.py"
}
