#!/bin/bash
# DaVinci Resolve MCP Server Launcher for WSL
# Ensures DaVinci Resolve is running on Windows, then starts the MCP server
#
# This script bridges WSL and Windows to control DaVinci Resolve's MCP server.
# It automatically detects paths and starts Resolve if not running.
#
# Usage:
#   ./scripts/wsl-launcher.sh
#
# Environment Variables (optional overrides):
#   RESOLVE_MCP_PROJECT  - Windows path to project (auto-detected from script location)
#   RESOLVE_MCP_PYTHON   - Windows path to Python executable (auto-detected in venv)
#   RESOLVE_MCP_SCRIPT   - Windows path to MCP server script (auto-detected)
#   RESOLVE_EXE          - Windows path to Resolve.exe (searched in common locations)
#   RESOLVE_SCRIPT_API   - Resolve scripting API path (auto-detected)
#   RESOLVE_SCRIPT_LIB   - Resolve fusionscript.dll path (auto-detected)
#
# Requirements:
#   - DaVinci Resolve installed on Windows
#   - Python venv with dependencies in project directory
#   - External scripting enabled in Resolve preferences

set -euo pipefail

# ============================================================================
# Path Detection Functions
# ============================================================================

# Convert WSL path to Windows path
wsl_to_win() {
    wslpath -w "$1" 2>/dev/null || echo "$1"
}

# Convert Windows path to WSL path
win_to_wsl() {
    wslpath -u "$1" 2>/dev/null || echo "$1"
}

# Get script directory (works even with symlinks)
get_script_dir() {
    local source="${BASH_SOURCE[0]}"
    local dir
    while [ -L "$source" ]; do
        dir="$(cd -P "$(dirname "$source")" && pwd)"
        source="$(readlink "$source")"
        [[ $source != /* ]] && source="$dir/$source"
    done
    cd -P "$(dirname "$source")" && pwd
}

# Detect project root from script location
detect_project_root() {
    local script_dir
    script_dir="$(get_script_dir)"
    # Script is in scripts/, so project root is parent
    local project_root
    project_root="$(dirname "$script_dir")"
    wsl_to_win "$project_root"
}

# Find DaVinci Resolve executable
find_resolve_exe() {
    local resolve_paths=(
        "/mnt/c/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe"
        "/mnt/d/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe"
        "/mnt/c/Program Files (x86)/Blackmagic Design/DaVinci Resolve/Resolve.exe"
    )

    for path in "${resolve_paths[@]}"; do
        if [ -f "$path" ]; then
            wsl_to_win "$path"
            return 0
        fi
    done

    # Try to find via PowerShell registry query
    local found
    found=$(powershell.exe -NoProfile -Command "
        \$paths = @(
            'C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe',
            'D:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe'
        )
        foreach (\$p in \$paths) {
            if (Test-Path \$p) { Write-Output \$p; exit }
        }
    " 2>/dev/null | tr -d '\r')

    if [ -n "$found" ]; then
        echo "$found"
        return 0
    fi

    # Default fallback
    echo 'C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe'
}

# Find Python in venv
find_python() {
    local project_wsl
    project_wsl="$(win_to_wsl "$WIN_PROJECT")"
    local venv_python="$project_wsl/venv/Scripts/python.exe"

    if [ -f "$venv_python" ]; then
        wsl_to_win "$venv_python"
    else
        # Fallback: check if python.exe exists in venv
        printf '%s\\venv\\Scripts\\python.exe' "$WIN_PROJECT"
    fi
}

# Find MCP server script
find_mcp_script() {
    local project_wsl
    project_wsl="$(win_to_wsl "$WIN_PROJECT")"
    local script_paths=(
        "$project_wsl/src/resolve_mcp_server.py"
        "$project_wsl/resolve_mcp_server.py"
    )

    for path in "${script_paths[@]}"; do
        if [ -f "$path" ]; then
            wsl_to_win "$path"
            return 0
        fi
    done

    # Default
    printf '%s\\src\\resolve_mcp_server.py' "$WIN_PROJECT"
}

# Find Resolve scripting API path
find_resolve_api() {
    local api_paths=(
        "/mnt/c/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
    )

    for path in "${api_paths[@]}"; do
        if [ -d "$path" ]; then
            wsl_to_win "$path"
            return 0
        fi
    done

    echo 'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting'
}

# Find Resolve scripting library
find_resolve_lib() {
    local lib_paths=(
        "/mnt/c/Program Files/Blackmagic Design/DaVinci Resolve/fusionscript.dll"
        "/mnt/d/Program Files/Blackmagic Design/DaVinci Resolve/fusionscript.dll"
    )

    for path in "${lib_paths[@]}"; do
        if [ -f "$path" ]; then
            wsl_to_win "$path"
            return 0
        fi
    done

    echo 'C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll'
}

# ============================================================================
# Configuration (with auto-detection and env var overrides)
# ============================================================================

init_config() {
    # Project path (from env or auto-detect)
    WIN_PROJECT="${RESOLVE_MCP_PROJECT:-$(detect_project_root)}"

    # Resolve executable (from env or search)
    RESOLVE_EXE="${RESOLVE_EXE:-$(find_resolve_exe)}"

    # Python executable (from env or find in venv)
    WIN_PYTHON="${RESOLVE_MCP_PYTHON:-$(find_python)}"

    # MCP server script (from env or find)
    WIN_SCRIPT="${RESOLVE_MCP_SCRIPT:-$(find_mcp_script)}"

    # Resolve API paths (from env or find)
    RESOLVE_API="${RESOLVE_SCRIPT_API:-$(find_resolve_api)}"
    RESOLVE_LIB="${RESOLVE_SCRIPT_LIB:-$(find_resolve_lib)}"
}

# ============================================================================
# DaVinci Resolve Control Functions
# ============================================================================

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
    local max_wait="${RESOLVE_WAIT_TIMEOUT:-90}"
    local wait_time=0

    echo "Waiting for DaVinci Resolve to initialize..." >&2

    while [ "$wait_time" -lt "$max_wait" ]; do
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

show_config() {
    cat >&2 <<EOF
DaVinci Resolve MCP - WSL Launcher Configuration
================================================
Project:      $WIN_PROJECT
Python:       $WIN_PYTHON
MCP Script:   $WIN_SCRIPT
Resolve:      $RESOLVE_EXE
API Path:     $RESOLVE_API
Library:      $RESOLVE_LIB
================================================
EOF
}

# ============================================================================
# Main Logic
# ============================================================================

main() {
    # Initialize configuration
    init_config

    # Show config in verbose mode
    if [ "${VERBOSE:-0}" = "1" ] || [ "${DEBUG:-0}" = "1" ]; then
        show_config
    fi

    # Ensure Resolve is running
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
        \$env:RESOLVE_SCRIPT_API = '$RESOLVE_API'
        \$env:RESOLVE_SCRIPT_LIB = '$RESOLVE_LIB'
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
