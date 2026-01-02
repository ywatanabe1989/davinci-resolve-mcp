#!/bin/bash
# Consolidated DaVinci Resolve MCP Server management script
# Usage: ./scripts/server.sh [start|stop|status|dev]

# Set current directory to project root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$PROJECT_ROOT"

# Define environment variables if not already set
if [ -z "$RESOLVE_SCRIPT_API" ]; then
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
fi

if [ -z "$RESOLVE_SCRIPT_LIB" ]; then
    export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
fi

if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
fi

# Check if DaVinci Resolve is running
check_resolve_running() {
    RESOLVE_PROCESS=$(ps -ef | grep -i "[D]aVinci Resolve")
    if [ -z "$RESOLVE_PROCESS" ]; then
        echo "⚠️  DaVinci Resolve is not running."
        echo "Please start DaVinci Resolve before starting the server."
        return 1
    else
        echo "✅ DaVinci Resolve is running."
        return 0
    fi
}

# Check if server is already running
check_server_running() {
    # Check for any process running our server script, whether via MCP or direct Python
    if ps aux | grep "resolve_mcp_server\.py" | grep -v grep > /dev/null ; then
        # Server is running
        return 0
    else
        # Server is not running
        return 1
    fi
}

# Activate virtual environment if it exists
activate_venv() {
    if [ -d "./venv" ]; then
        source ./venv/bin/activate
        echo "✅ Virtual environment activated."
    else
        echo "⚠️  No virtual environment found. Running with system Python."
    fi
}

# Start the server
start_server() {
    if check_server_running; then
        echo "⚠️  MCP Server is already running."
        return 0
    fi
    
    if ! check_resolve_running; then
        read -p "Do you want to continue anyway? (y/n) " choice
        case "$choice" in
            y|Y ) echo "Continuing without DaVinci Resolve...";;
            * ) echo "Aborting server start."; return 1;;
        esac
    fi
    
    activate_venv
    echo "🚀 Starting DaVinci Resolve MCP Server..."
    mkdir -p "$PROJECT_ROOT/logs"
    
    # Use direct Python as it's more reliable in background mode
    nohup python3 "$PROJECT_ROOT/src/__main__.py" > "$PROJECT_ROOT/logs/server.log" 2>&1 &
    
    # Give the server time to start
    echo "Waiting for server to initialize..."
    sleep 3
    
    if check_server_running; then
        echo "✅ Server started. Logs available at: $PROJECT_ROOT/logs/server.log"
        return 0
    else
        echo "❌ Server failed to start. Check logs at: $PROJECT_ROOT/logs/server.log"
        return 1
    fi
}

# Stop the server
stop_server() {
    if ! check_server_running; then
        echo "⚠️  MCP Server is not running."
        return 0
    fi
    
    echo "🛑 Stopping DaVinci Resolve MCP Server..."
    
    # Kill any processes running the server
    pkill -f "resolve_mcp_server\.py"
    sleep 1
    
    if check_server_running; then
        echo "⚠️  Failed to stop all server processes. Trying with higher force..."
        pkill -9 -f "resolve_mcp_server\.py"
        sleep 1
        
        if check_server_running; then
            echo "❌ Could not stop all server processes. Manual cleanup required."
            echo "   Try running: killall -9 node; killall -9 python"
            return 1
        fi
    fi
    
    echo "✅ Server stopped."
    return 0
}

# Start server in development mode
start_dev_mode() {
    if check_server_running; then
        echo "⚠️  An MCP Server is already running. Stopping it..."
        stop_server
    fi
    
    check_resolve_running
    activate_venv
    
    echo "🚀 Starting DaVinci Resolve MCP Server in development mode..."
    python3 "$PROJECT_ROOT/src/__main__.py"
}

# Show server status
show_status() {
    if check_server_running; then
        echo "✅ MCP Server is running."
        # Display process info in a user-friendly way
        echo -e "\nServer process details:"
        ps aux | grep "resolve_mcp_server\.py" | grep -v grep | awk '{print "PID: " $2 "  User: " $1 "  Started: " $9 "  Command: " $11 " " $12 " " $13}'
    else
        echo "❌ MCP Server is not running."
    fi
    
    check_resolve_running
}

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# Parse command line arguments
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 1
        start_server
        ;;
    status)
        show_status
        ;;
    dev)
        start_dev_mode
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|dev}"
        echo ""
        echo "  start   - Start the MCP server as a background process"
        echo "  stop    - Stop the running MCP server"
        echo "  restart - Restart the MCP server"
        echo "  status  - Check if the server is running"
        echo "  dev     - Start in development mode (foreground)"
        exit 1
        ;;
esac

exit 0 