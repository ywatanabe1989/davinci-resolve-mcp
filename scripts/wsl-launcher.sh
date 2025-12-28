#!/bin/bash
# DaVinci Resolve MCP Server Launcher for WSL
# Ensures DaVinci Resolve is running on Windows, then starts the MCP server
#
# This script bridges WSL and Windows to control DaVinci Resolve's MCP server.
# It automatically starts Resolve if not running and waits for API initialization.
#
# Usage:
#   1. Copy this script or adjust WIN_PROJECT path for your installation
#   2. Ensure Python venv is set up in the Windows project directory
#   3. Run from WSL: ./scripts/wsl-launcher.sh
#
# Requirements:
#   - DaVinci Resolve installed on Windows
#   - Python venv with dependencies in WIN_PROJECT
#   - External scripting enabled in Resolve preferences

# Configuration - Adjust these paths for your installation
WIN_PROJECT='C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp'
WIN_PYTHON="$WIN_PROJECT\\venv\\Scripts\\python.exe"
WIN_SCRIPT="$WIN_PROJECT\\src\\resolve_mcp_server.py"
RESOLVE_EXE='C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe'

# Check if DaVinci Resolve is running
is_resolve_running() {
    powershell.exe -NoProfile -Command "
        \$proc = Get-Process -Name 'Resolve' -ErrorAction SilentlyContinue
        if (\$proc) { exit 0 } else { exit 1 }
    " 2>/dev/null
    return $?
}

# Start DaVinci Resolve
start_resolve() {
    echo "Starting DaVinci Resolve..." >&2
    powershell.exe -NoProfile -Command "Start-Process '$RESOLVE_EXE'" 2>/dev/null
}

# Wait for Resolve to be ready
wait_for_resolve() {
    local max_wait=90
    local wait_time=0

    echo "Waiting for DaVinci Resolve to initialize..." >&2

    while [ $wait_time -lt $max_wait ]; do
        if is_resolve_running; then
            echo "DaVinci Resolve process detected. Waiting for API initialization..." >&2
            sleep 15 # Extra time for scripting API to be ready
            echo "DaVinci Resolve should be ready." >&2
            return 0
        fi
        sleep 3
        wait_time=$((wait_time + 3))
        echo "  Waiting... ($wait_time/$max_wait seconds)" >&2
    done

    echo "ERROR: Timeout waiting for DaVinci Resolve to start" >&2
    return 1
}

show_scripting_hint() {
    cat >&2 <<'EOF'

================================================================================
IMPORTANT: Enable External Scripting in DaVinci Resolve

If the MCP server fails to connect, ensure external scripting is enabled:

1. Open DaVinci Resolve
2. Go to: DaVinci Resolve → Preferences (or Ctrl+,)
3. Navigate to: System → General
4. Set "External scripting using" to "Local"
5. Click Save and restart DaVinci Resolve

================================================================================

EOF
}

# Main logic
main() {
    if ! is_resolve_running; then
        start_resolve
        if ! wait_for_resolve; then
            show_scripting_hint
            exit 1
        fi
    else
        echo "DaVinci Resolve is already running." >&2
    fi

    # Start the MCP server
    echo "Starting DaVinci Resolve MCP Server..." >&2

    # Run and capture exit code
    powershell.exe -NoProfile -Command "
        Set-Location '$WIN_PROJECT'
        \$env:PYTHONPATH = '$WIN_PROJECT'
        \$env:RESOLVE_SCRIPT_API = 'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting'
        \$env:RESOLVE_SCRIPT_LIB = 'C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll'
        & '$WIN_PYTHON' '$WIN_SCRIPT'
    "
    local exit_code=$?

    # Show hint if server failed (likely scripting not enabled)
    if [ $exit_code -ne 0 ]; then
        show_scripting_hint
    fi

    return $exit_code
}

main "$@"
