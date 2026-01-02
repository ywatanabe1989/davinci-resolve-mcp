#!/bin/bash
# DaVinci Resolve MCP - Status Check
# Shows all system state - the only thing admin needs to check

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=== DaVinci Resolve MCP Status ===${NC}"
echo ""

ERRORS=0
WARNINGS=0

# --- WSL Project ---
echo -e "${CYAN}[WSL Project]${NC}"
WSL_PATH="/home/ywatanabe/proj/davinci-resolve-mcp"
if [ -d "$WSL_PATH/src" ]; then
    echo -e "  ${GREEN}[OK]${NC} Project exists at $WSL_PATH"
else
    echo -e "  ${RED}[ERROR]${NC} Project not found at $WSL_PATH"
    ((ERRORS++))
fi

# Git status
if [ -d "$WSL_PATH/.git" ]; then
    cd "$WSL_PATH"
    BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    DIRTY=$(git status --porcelain 2>/dev/null | wc -l)
    if [ "$DIRTY" -gt 0 ]; then
        echo -e "  ${YELLOW}[WARN]${NC} Git: $BRANCH ($DIRTY uncommitted changes)"
        ((WARNINGS++))
    else
        echo -e "  ${GREEN}[OK]${NC} Git: $BRANCH (clean)"
    fi
fi

# --- Windows Symlink ---
echo ""
echo -e "${CYAN}[Windows Integration]${NC}"
WIN_PATH="/mnt/c/Program Files (x86)/ywatanabe/davinci-resolve-mcp"
if [ -L "$WIN_PATH" ]; then
    TARGET=$(readlink "$WIN_PATH" 2>/dev/null || echo "unknown")
    echo -e "  ${GREEN}[OK]${NC} Symlink exists: $WIN_PATH"
    echo -e "       -> $TARGET"
elif [ -d "$WIN_PATH" ]; then
    echo -e "  ${YELLOW}[WARN]${NC} Windows folder exists but is NOT a symlink"
    echo -e "       Run: make install (in Admin PowerShell)"
    ((WARNINGS++))
else
    echo -e "  ${RED}[ERROR]${NC} Windows installation not found"
    echo -e "       Run: make install (in Admin PowerShell)"
    ((ERRORS++))
fi

# Windows venv
if [ -f "$WIN_PATH/venv/Scripts/python.exe" ]; then
    echo -e "  ${GREEN}[OK]${NC} Windows venv exists"
else
    echo -e "  ${YELLOW}[WARN]${NC} Windows venv not found (will use system Python)"
    ((WARNINGS++))
fi

# --- DaVinci Resolve ---
echo ""
echo -e "${CYAN}[DaVinci Resolve]${NC}"
RESOLVE_DLL="/mnt/c/Program Files/Blackmagic Design/DaVinci Resolve/fusionscript.dll"
if [ -f "$RESOLVE_DLL" ]; then
    echo -e "  ${GREEN}[OK]${NC} DaVinci Resolve installed"
else
    echo -e "  ${RED}[ERROR]${NC} DaVinci Resolve not found"
    echo -e "       Install from: https://www.blackmagicdesign.com/products/davinciresolve"
    ((ERRORS++))
fi

# Check if Resolve is running (via Windows process)
RESOLVE_RUNNING=$(powershell.exe -Command "Get-Process 'Resolve' -ErrorAction SilentlyContinue" 2>/dev/null | grep -c "Resolve" || echo "0")
if [ "$RESOLVE_RUNNING" -gt 0 ]; then
    echo -e "  ${GREEN}[OK]${NC} DaVinci Resolve is running"
else
    echo -e "  ${YELLOW}[WARN]${NC} DaVinci Resolve is not running"
    echo -e "       Start Resolve before using MCP tools"
    ((WARNINGS++))
fi

# --- MCP Server ---
echo ""
echo -e "${CYAN}[MCP Server]${NC}"
MCP_CONFIG="$HOME/.dotfiles/.claude/mcp-configs-dynamic/mcp-config.json"
if [ -f "$MCP_CONFIG" ]; then
    if grep -q "davinci-resolve" "$MCP_CONFIG" 2>/dev/null; then
        echo -e "  ${GREEN}[OK]${NC} MCP config registered"
    else
        echo -e "  ${RED}[ERROR]${NC} davinci-resolve not in MCP config"
        ((ERRORS++))
    fi
else
    echo -e "  ${YELLOW}[WARN]${NC} MCP config not found at $MCP_CONFIG"
    ((WARNINGS++))
fi

# --- Summary ---
echo ""
echo -e "${CYAN}=== Summary ===${NC}"
if [ "$ERRORS" -gt 0 ]; then
    echo -e "  ${RED}$ERRORS error(s)${NC} - fix before using"
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "  ${YELLOW}$WARNINGS warning(s)${NC} - system may work with limitations"
else
    echo -e "  ${GREEN}All checks passed${NC}"
fi

echo ""
echo -e "${CYAN}Quick Commands:${NC}"
echo "  make install     - Setup Windows integration"
echo "  /mcp reconnect davinci-resolve  - Reconnect MCP in Claude"

exit "$ERRORS"
