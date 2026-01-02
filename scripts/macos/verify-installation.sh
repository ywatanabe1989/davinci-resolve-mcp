#!/bin/bash
# verify-installation.sh
# Script to verify that the DaVinci Resolve MCP installation has been properly set up

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
VENV_DIR="$PROJECT_ROOT/venv"

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}  DaVinci Resolve MCP Installation Verification  ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Check if virtual environment exists
check_venv() {
    echo -ne "${YELLOW}Checking Python virtual environment... ${NC}"
    if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/python" ]; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}MISSING${NC}"
        echo -e "${RED}Virtual environment not found at: $VENV_DIR${NC}"
        return 1
    fi
}

# Check if MCP SDK is installed
check_mcp_sdk() {
    echo -ne "${YELLOW}Checking MCP SDK installation... ${NC}"
    if "$VENV_DIR/bin/pip" list | grep -q "mcp"; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}MISSING${NC}"
        echo -e "${RED}MCP SDK not installed in the virtual environment${NC}"
        return 1
    fi
}

# Check if Resolve MCP server script exists
check_server_script() {
    echo -ne "${YELLOW}Checking server script... ${NC}"
    if [ -f "$PROJECT_ROOT/src/src/__main__.py" ]; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}MISSING${NC}"
        echo -e "${RED}Server script not found at: $PROJECT_ROOT/src/src/__main__.py${NC}"
        return 1
    fi
}

# Check if DaVinci Resolve is running
check_resolve_running() {
    echo -ne "${YELLOW}Checking if DaVinci Resolve is running... ${NC}"
    if ps -ef | grep -i "[D]aVinci Resolve" > /dev/null; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}NOT RUNNING${NC}"
        echo -e "${RED}DaVinci Resolve is not running - please start it${NC}"
        return 1
    fi
}

# Check Cursor MCP configuration
check_cursor_config() {
    echo -ne "${YELLOW}Checking Cursor MCP configuration... ${NC}"
    CURSOR_CONFIG_FILE="$HOME/.cursor/mcp/config.json"
    if [ -f "$CURSOR_CONFIG_FILE" ]; then
        if grep -q "davinci-resolve" "$CURSOR_CONFIG_FILE"; then
            echo -e "${GREEN}OK${NC}"
            echo -e "${GREEN}Cursor MCP config found at: $CURSOR_CONFIG_FILE${NC}"
            return 0
        else
            echo -e "${RED}INVALID${NC}"
            echo -e "${RED}Cursor MCP config does not contain 'davinci-resolve' entry${NC}"
            return 1
        fi
    else
        echo -e "${RED}MISSING${NC}"
        echo -e "${RED}Cursor MCP config not found at: $CURSOR_CONFIG_FILE${NC}"
        return 1
    fi
}

# Check if all environment variables are set
check_env_vars() {
    echo -ne "${YELLOW}Checking environment variables... ${NC}"
    local missing=0
    
    if [ -z "$RESOLVE_SCRIPT_API" ]; then
        missing=1
    fi
    
    if [ -z "$RESOLVE_SCRIPT_LIB" ]; then
        missing=1
    fi
    
    if [ -z "$PYTHONPATH" ] || ! echo "$PYTHONPATH" | grep -q "Modules"; then
        missing=1
    fi
    
    if [ $missing -eq 0 ]; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}MISSING${NC}"
        echo -e "${RED}One or more required environment variables are not set${NC}"
        return 1
    fi
}

# Run all checks
run_all_checks() {
    local passed=0
    local total=0
    
    check_venv
    if [ $? -eq 0 ]; then ((passed++)); fi
    ((total++))
    
    check_mcp_sdk
    if [ $? -eq 0 ]; then ((passed++)); fi
    ((total++))
    
    check_server_script
    if [ $? -eq 0 ]; then ((passed++)); fi
    ((total++))
    
    check_resolve_running
    if [ $? -eq 0 ]; then ((passed++)); fi
    ((total++))
    
    check_cursor_config
    if [ $? -eq 0 ]; then ((passed++)); fi
    ((total++))
    
    check_env_vars
    if [ $? -eq 0 ]; then ((passed++)); fi
    ((total++))
    
    echo -e "${BLUE}=============================================${NC}"
    echo -e "${YELLOW}Results: $passed/$total checks passed${NC}"
    
    if [ $passed -eq $total ]; then
        echo -e "${GREEN}✓ Installation verification completed successfully!${NC}"
        echo -e "${GREEN}✓ You can now use the MCP server with DaVinci Resolve${NC}"
        echo -e "${YELLOW}To start the server, run:${NC}"
        echo -e "${BLUE}  ./run-now.sh${NC}"
        echo -e "${YELLOW}Or for more options:${NC}"
        echo -e "${BLUE}  ./scripts/mcp_resolve-cursor_start${NC}"
        return 0
    else
        echo -e "${RED}✗ Installation verification failed!${NC}"
        echo -e "${YELLOW}Please fix the issues above and run this script again${NC}"
        return 1
    fi
}

# Run the verification
run_all_checks
exit $? 