#!/bin/bash
# Restart script for DaVinci Resolve MCP Server
# Created as part of feature updates on March 29, 2024

echo "========================================================"
echo "DaVinci Resolve MCP Server - Restart Script"
echo "========================================================"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to check if the server is running
check_server_running() {
    # Look for Python processes running the server
    pgrep -f "python.*src/__main__.py" > /dev/null
    return $?
}

# Stop the server if it's running
if check_server_running; then
    echo "Stopping existing DaVinci Resolve MCP Server..."
    
    # Find the PID of the server process
    SERVER_PID=$(pgrep -f "python.*src/__main__.py")
    
    if [ -n "$SERVER_PID" ]; then
        echo "Server process found with PID: $SERVER_PID"
        kill $SERVER_PID
        
        # Wait for the process to stop
        for i in {1..5}; do
            if ! ps -p $SERVER_PID > /dev/null; then
                echo "Server process stopped successfully."
                break
            fi
            echo "Waiting for server to stop... ($i/5)"
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $SERVER_PID > /dev/null; then
            echo "Server did not stop gracefully. Forcing termination..."
            kill -9 $SERVER_PID
            sleep 1
        fi
    else
        echo "Could not determine server PID. Server might be running in an unexpected way."
    fi
else
    echo "No running DaVinci Resolve MCP Server detected."
fi

# Make sure we have the right environment
if [ -f "./setup.sh" ]; then
    echo "Setting up environment..."
    source ./setup.sh
else
    echo "Warning: setup.sh not found. Environment may not be properly configured."
fi

# Start the server again
echo "Starting DaVinci Resolve MCP Server..."
if [ -f "$SCRIPT_DIR/../run-now.sh" ]; then
    echo "Starting server with run-now.sh..."
    "$SCRIPT_DIR/../run-now.sh" &
    
    # Wait a moment and check if it started
    sleep 2
    if check_server_running; then
        echo "DaVinci Resolve MCP Server started successfully!"
    else
        echo "Failed to start DaVinci Resolve MCP Server. Check logs for errors."
    fi
else
    echo "Error: run-now.sh not found. Cannot start the server."
    exit 1
fi

echo "========================================================"
echo "Restart operation completed."
echo "========================================================" 