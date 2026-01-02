#!/bin/bash
# mcp_resolve_launcher.sh
# Interactive launcher script for DaVinci Resolve MCP servers
# Allows selecting which server(s) to start or stop

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CURSOR_SCRIPT="$SCRIPT_DIR/mcp_resolve-cursor_start"
CLAUDE_SCRIPT="$SCRIPT_DIR/mcp_resolve-claude_start"
# Get repository root directory (parent of scripts directory)
REPO_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# Display banner
echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}  DaVinci Resolve - MCP Server Launcher  ${NC}"
echo -e "${BLUE}=============================================${NC}"

# Check if DaVinci Resolve is running
check_resolve_running() {
    # Try to detect with pgrep
    if pgrep -q "Resolve"; then
        echo -e "${GREEN}✓ DaVinci Resolve is running${NC}"
        return 0
    fi
    
    # Fallback: use ps to check for Resolve process
    if ps -ef | grep -q "[R]esolve" || ps -ef | grep -q "[D]aVinci Resolve"; then
        echo -e "${GREEN}✓ DaVinci Resolve is running${NC}"
        return 0
    fi
    
    echo -e "${RED}✗ DaVinci Resolve is not running${NC}"
    echo -e "${YELLOW}Please start DaVinci Resolve before continuing${NC}"
    return 1
}

# Find server PIDs
find_server_pids() {
    # Look for cursor server (using mcp dev with src/__main__.py)
    CURSOR_PID=$(pgrep -f "mcp dev.*src/__main__.py" | head -1)
    
    # Look for Claude server (using mcp dev with src/__main__.py)
    CLAUDE_PID=$(pgrep -f "mcp dev.*src/__main__.py" | head -1)
    
    # If both are found and they're the same, set one to empty
    if [ "$CURSOR_PID" = "$CLAUDE_PID" ] && [ -n "$CURSOR_PID" ]; then
        # We need to disambiguate - look at log files
        if ps -p "$CURSOR_PID" -o command= | grep -q "cursor"; then
            CLAUDE_PID=""
        else
            # If we can't determine, just assume it's the Cursor server
            CLAUDE_PID=""
        fi
    fi
}

# Display server status
show_status() {
    find_server_pids
    
    echo -e "\n${BOLD}Current Server Status:${NC}"
    
    if [ -n "$CURSOR_PID" ]; then
        echo -e "${GREEN}● Cursor MCP Server: Running (PID: $CURSOR_PID)${NC}"
    else
        echo -e "${RED}○ Cursor MCP Server: Not running${NC}"
    fi
    
    if [ -n "$CLAUDE_PID" ]; then
        echo -e "${GREEN}● Claude Desktop MCP Server: Running (PID: $CLAUDE_PID)${NC}"
    else
        echo -e "${RED}○ Claude Desktop MCP Server: Not running${NC}"
    fi
    
    echo ""
}

# Stop server by PID
stop_server() {
    local pid=$1
    local name=$2
    
    if [ -n "$pid" ]; then
        echo -e "${YELLOW}Stopping $name MCP Server (PID: $pid)...${NC}"
        kill "$pid" 2>/dev/null
        
        # Wait for process to exit
        for i in {1..5}; do
            if ! ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${GREEN}✓ $name MCP Server stopped${NC}"
                return 0
            fi
            sleep 1
        done
        
        # Force kill if still running
        echo -e "${YELLOW}Server still running. Force killing...${NC}"
        kill -9 "$pid" 2>/dev/null
        echo -e "${GREEN}✓ $name MCP Server force stopped${NC}"
    else
        echo -e "${YELLOW}$name MCP Server is not running${NC}"
    fi
}

# Start Cursor server
start_cursor() {
    local force_flag=""
    local project_flag=""
    
    if [ "$1" = "force" ]; then
        force_flag="--force"
    fi
    
    if [ -n "$2" ]; then
        project_flag="--project \"$2\""
    fi
    
    echo -e "${YELLOW}Starting Cursor MCP Server...${NC}"
    
    # Check if script exists
    if [ ! -f "$CURSOR_SCRIPT" ]; then
        echo -e "${RED}✗ Cursor startup script not found: $CURSOR_SCRIPT${NC}"
        return 1
    fi
    
    # Execute the script
    command="$CURSOR_SCRIPT $force_flag $project_flag"
    eval "$command" &
    
    echo -e "${GREEN}✓ Cursor MCP Server starting in the background${NC}"
}

# Start Claude server
start_claude() {
    local force_flag=""
    local project_flag=""
    
    if [ "$1" = "force" ]; then
        force_flag="--force"
    fi
    
    if [ -n "$2" ]; then
        project_flag="--project \"$2\""
    fi
    
    echo -e "${YELLOW}Starting Claude Desktop MCP Server...${NC}"
    
    # Check if script exists
    if [ ! -f "$CLAUDE_SCRIPT" ]; then
        echo -e "${RED}✗ Claude Desktop startup script not found: $CLAUDE_SCRIPT${NC}"
        return 1
    fi
    
    # Execute the script
    command="$CLAUDE_SCRIPT $force_flag $project_flag"
    eval "$command" &
    
    echo -e "${GREEN}✓ Claude Desktop MCP Server starting in the background${NC}"
}

# Interactive menu
show_menu() {
    echo -e "${BOLD}DaVinci Resolve MCP Server Launcher${NC}"
    echo -e "${YELLOW}Select an option:${NC}"
    echo "1) Start Cursor MCP Server"
    echo "2) Start Claude Desktop MCP Server"
    echo "3) Start both servers"
    echo "4) Stop Cursor MCP Server"
    echo "5) Stop Claude Desktop MCP Server"
    echo "6) Stop both servers"
    echo "7) Show server status"
    echo "8) Exit"
    echo -e "${YELLOW}Enter your choice [1-8]:${NC} "
}

# Process menu selection
process_selection() {
    local choice="$1"
    local force_mode="$2"
    local project_name="$3"
    
    case "$choice" in
        1)
            find_server_pids
            if [ -n "$CURSOR_PID" ]; then
                echo -e "${YELLOW}Cursor MCP Server is already running (PID: $CURSOR_PID)${NC}"
                echo -e "${YELLOW}Stop it first before starting a new instance.${NC}"
            else
                start_cursor "$force_mode" "$project_name"
            fi
            ;;
        2)
            find_server_pids
            if [ -n "$CLAUDE_PID" ]; then
                echo -e "${YELLOW}Claude Desktop MCP Server is already running (PID: $CLAUDE_PID)${NC}"
                echo -e "${YELLOW}Stop it first before starting a new instance.${NC}"
            else
                start_claude "$force_mode" "$project_name"
            fi
            ;;
        3)
            find_server_pids
            if [ -n "$CURSOR_PID" ]; then
                echo -e "${YELLOW}Cursor MCP Server is already running (PID: $CURSOR_PID)${NC}"
            else
                start_cursor "$force_mode" "$project_name"
            fi
            
            if [ -n "$CLAUDE_PID" ]; then
                echo -e "${YELLOW}Claude Desktop MCP Server is already running (PID: $CLAUDE_PID)${NC}"
            else
                start_claude "$force_mode" "$project_name"
            fi
            ;;
        4)
            find_server_pids
            stop_server "$CURSOR_PID" "Cursor"
            ;;
        5)
            find_server_pids
            stop_server "$CLAUDE_PID" "Claude Desktop"
            ;;
        6)
            find_server_pids
            stop_server "$CURSOR_PID" "Cursor"
            stop_server "$CLAUDE_PID" "Claude Desktop"
            ;;
        7)
            show_status
            ;;
        8)
            echo -e "${GREEN}Exiting. Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac
}

# Check command line arguments
PROJECT_NAME=""
FORCE_MODE=""
MENU_OPTION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --project|-p)
            PROJECT_NAME="$2"
            echo -e "${YELLOW}Will use project: $2${NC}"
            shift 2
            ;;
        --force|-f)
            FORCE_MODE="force"
            echo -e "${YELLOW}Force mode enabled: Will skip Resolve running check${NC}"
            shift
            ;;
        --start-cursor)
            MENU_OPTION="1"
            shift
            ;;
        --start-claude)
            MENU_OPTION="2"
            shift
            ;;
        --start-both)
            MENU_OPTION="3"
            shift
            ;;
        --stop-cursor)
            MENU_OPTION="4"
            shift
            ;;
        --stop-claude)
            MENU_OPTION="5"
            shift
            ;;
        --stop-all)
            MENU_OPTION="6"
            shift
            ;;
        --status)
            MENU_OPTION="7"
            shift
            ;;
        *)
            echo -e "${YELLOW}Unknown argument: $1${NC}"
            shift
            ;;
    esac
done

# Check Resolve is running (unless we're stopping servers)
if [[ "$FORCE_MODE" != "force" && "$MENU_OPTION" != "4" && "$MENU_OPTION" != "5" && "$MENU_OPTION" != "6" && "$MENU_OPTION" != "7" ]]; then
    check_resolve_running
fi

# Non-interactive mode if an option was provided via command line
if [ -n "$MENU_OPTION" ]; then
    process_selection "$MENU_OPTION" "$FORCE_MODE" "$PROJECT_NAME"
    exit 0
fi

# Interactive mode
while true; do
    show_status
    show_menu
    read -r choice
    process_selection "$choice" "$FORCE_MODE" "$PROJECT_NAME"
    echo -e "\nPress Enter to continue..."
    read -r
    clear
done 