#!/bin/bash
# install.sh - One-step installation for DaVinci Resolve MCP Integration
# This script handles the entire installation process with improved error detection

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get the absolute path of this script's location
INSTALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$INSTALL_DIR/venv"
CURSOR_CONFIG_DIR="$HOME/.cursor/mcp"
CURSOR_CONFIG_FILE="$CURSOR_CONFIG_DIR/config.json"
PROJECT_CURSOR_DIR="$INSTALL_DIR/.cursor"
PROJECT_CONFIG_FILE="$PROJECT_CURSOR_DIR/mcp.json"
LOG_FILE="$INSTALL_DIR/install.log"

# Banner
echo -e "${BLUE}${BOLD}=================================================${NC}"
echo -e "${BLUE}${BOLD}  DaVinci Resolve MCP Integration Installer      ${NC}"
echo -e "${BLUE}${BOLD}=================================================${NC}"
echo -e "${YELLOW}Installation directory: ${INSTALL_DIR}${NC}"
echo -e "Installation log: ${LOG_FILE}"
echo ""

# Initialize log
echo "=== DaVinci Resolve MCP Installation Log ===" > "$LOG_FILE"
echo "Date: $(date)" >> "$LOG_FILE"
echo "Install directory: $INSTALL_DIR" >> "$LOG_FILE"
echo "User: $(whoami)" >> "$LOG_FILE"
echo "System: $(uname -a)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Function to log messages
log() {
    echo "[$(date +%T)] $1" >> "$LOG_FILE"
}

# Function to check if DaVinci Resolve is running
check_resolve_running() {
    log "Checking if DaVinci Resolve is running"
    echo -ne "${YELLOW}Checking if DaVinci Resolve is running... ${NC}"
    
    if ps -ef | grep -i "[D]aVinci Resolve" > /dev/null; then
        echo -e "${GREEN}OK${NC}"
        log "DaVinci Resolve is running"
        return 0
    else
        echo -e "${RED}NOT RUNNING${NC}"
        echo -e "${YELLOW}DaVinci Resolve must be running to complete the installation.${NC}"
        echo -e "${YELLOW}Please start DaVinci Resolve and try again.${NC}"
        log "DaVinci Resolve is not running - installation cannot proceed"
        return 1
    fi
}

# Function to create Python virtual environment
create_venv() {
    log "Creating/checking Python virtual environment"
    echo -ne "${YELLOW}Setting up Python virtual environment... ${NC}"
    
    if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/python" ]; then
        echo -e "${GREEN}ALREADY EXISTS${NC}"
        log "Virtual environment already exists"
    else
        echo -ne "${YELLOW}CREATING${NC}"
        python3 -m venv "$VENV_DIR" >> "$LOG_FILE" 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}OK${NC}"
            log "Virtual environment created successfully"
        else
            echo -e "${RED}FAILED${NC}"
            echo -e "${RED}Failed to create Python virtual environment.${NC}"
            echo -e "${YELLOW}Check that Python 3.9+ is installed.${NC}"
            log "Failed to create virtual environment"
            return 1
        fi
    fi
    
    return 0
}

# Function to install MCP SDK
install_mcp() {
    log "Installing MCP SDK"
    echo -ne "${YELLOW}Installing MCP SDK... ${NC}"
    
    "$VENV_DIR/bin/pip" install "mcp[cli]" >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}OK${NC}"
        log "MCP SDK installed successfully"
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        echo -e "${RED}Failed to install MCP SDK.${NC}"
        echo -e "${YELLOW}Check the log file for details: $LOG_FILE${NC}"
        log "Failed to install MCP SDK"
        return 1
    fi
}

# Function to set environment variables
setup_env_vars() {
    log "Setting up environment variables"
    echo -ne "${YELLOW}Setting up environment variables... ${NC}"
    
    # Generate environment variables file
    ENV_FILE="$INSTALL_DIR/.env"
    cat > "$ENV_FILE" << EOF
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
PYTHONPATH="\$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
EOF
    
    # Source the environment variables
    source "$ENV_FILE"
    
    # Export them for the current session
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
    
    echo -e "${GREEN}OK${NC}"
    log "Environment variables set:"
    log "RESOLVE_SCRIPT_API=$RESOLVE_SCRIPT_API"
    log "RESOLVE_SCRIPT_LIB=$RESOLVE_SCRIPT_LIB"
    
    # Suggest adding to shell profile
    echo -e "${YELLOW}Consider adding these environment variables to your shell profile:${NC}"
    echo -e "${BLUE}  echo 'export RESOLVE_SCRIPT_API=\"/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting\"' >> ~/.zshrc${NC}"
    echo -e "${BLUE}  echo 'export RESOLVE_SCRIPT_LIB=\"/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so\"' >> ~/.zshrc${NC}"
    echo -e "${BLUE}  echo 'export PYTHONPATH=\"\$PYTHONPATH:\$RESOLVE_SCRIPT_API/Modules/\"' >> ~/.zshrc${NC}"
    
    return 0
}

# Function to setup Cursor MCP configuration
setup_cursor_config() {
    log "Setting up Cursor MCP configuration"
    echo -ne "${YELLOW}Setting up Cursor MCP configuration... ${NC}"
    
    # Create system-level directory if it doesn't exist
    mkdir -p "$CURSOR_CONFIG_DIR"
    
    # Create system-level config file with the absolute paths
    cat > "$CURSOR_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "${INSTALL_DIR}/venv/bin/python",
      "args": ["${INSTALL_DIR}/src/__main__.py"]
    }
  }
}
EOF
    
    # Create project-level directory if it doesn't exist
    mkdir -p "$PROJECT_CURSOR_DIR"
    
    # Create project-level config file with absolute paths (same as system-level)
    cat > "$PROJECT_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "${INSTALL_DIR}/venv/bin/python",
      "args": ["${INSTALL_DIR}/src/__main__.py"]
    }
  }
}
EOF
    
    if [ -f "$CURSOR_CONFIG_FILE" ] && [ -f "$PROJECT_CONFIG_FILE" ]; then
        echo -e "${GREEN}OK${NC}"
        echo -e "${GREEN}Cursor MCP config created at: $CURSOR_CONFIG_FILE${NC}"
        echo -e "${GREEN}Project MCP config created at: $PROJECT_CONFIG_FILE${NC}"
        log "Cursor MCP configuration created successfully"
        log "System config file: $CURSOR_CONFIG_FILE"
        log "Project config file: $PROJECT_CONFIG_FILE"
        
        # Show the paths that were set
        echo -e "${YELLOW}Paths configured:${NC}"
        echo -e "${BLUE}  Python: ${INSTALL_DIR}/venv/bin/python${NC}"
        echo -e "${BLUE}  Script: ${INSTALL_DIR}/src/__main__.py${NC}"
        
        return 0
    else
        echo -e "${RED}FAILED${NC}"
        echo -e "${RED}Failed to create Cursor MCP configuration.${NC}"
        log "Failed to create Cursor MCP configuration"
        return 1
    fi
}

# Make server script executable
make_script_executable() {
    log "Making server script executable"
    echo -ne "${YELLOW}Making server script executable... ${NC}"
    
    chmod +x "$INSTALL_DIR/src/__main__.py"
    chmod +x "$INSTALL_DIR/scripts/mcp_resolve-cursor_start"
    chmod +x "$INSTALL_DIR/scripts/verify-installation.sh"
    
    echo -e "${GREEN}OK${NC}"
    log "Server scripts made executable"
    return 0
}

# Verify installation
verify_installation() {
    log "Verifying installation"
    echo -e "${BLUE}${BOLD}=================================================${NC}"
    echo -e "${YELLOW}${BOLD}Verifying installation...${NC}"
    
    # Run the verification script
    "$INSTALL_DIR/scripts/verify-installation.sh"
    VERIFY_RESULT=$?
    
    log "Verification completed with result: $VERIFY_RESULT"
    
    return $VERIFY_RESULT
}

# Run server if verification succeeds
run_server() {
    log "Starting server"
    echo -e "${BLUE}${BOLD}=================================================${NC}"
    echo -e "${GREEN}${BOLD}Starting DaVinci Resolve MCP Server...${NC}"
    echo ""
    
    # Run the server using the virtual environment
    "$VENV_DIR/bin/python" "$INSTALL_DIR/src/__main__.py"
    
    SERVER_EXIT=$?
    log "Server exited with code: $SERVER_EXIT"
    
    return $SERVER_EXIT
}

# Main installation process
main() {
    log "Starting installation process"
    
    # Check if DaVinci Resolve is running
    if ! check_resolve_running; then
        echo -e "${YELLOW}Waiting 10 seconds for DaVinci Resolve to start...${NC}"
        sleep 10
        if ! check_resolve_running; then
            log "Installation aborted - DaVinci Resolve not running"
            echo -e "${RED}Installation aborted.${NC}"
            exit 1
        fi
    fi
    
    # Create virtual environment
    if ! create_venv; then
        log "Installation aborted - virtual environment setup failed"
        echo -e "${RED}Installation aborted.${NC}"
        exit 1
    fi
    
    # Install MCP SDK
    if ! install_mcp; then
        log "Installation aborted - MCP SDK installation failed"
        echo -e "${RED}Installation aborted.${NC}"
        exit 1
    fi
    
    # Set up environment variables
    if ! setup_env_vars; then
        log "Installation aborted - environment variable setup failed"
        echo -e "${RED}Installation aborted.${NC}"
        exit 1
    fi
    
    # Set up Cursor configuration
    if ! setup_cursor_config; then
        log "Installation aborted - Cursor configuration failed"
        echo -e "${RED}Installation aborted.${NC}"
        exit 1
    fi
    
    # Make scripts executable
    if ! make_script_executable; then
        log "Installation aborted - failed to make scripts executable"
        echo -e "${RED}Installation aborted.${NC}"
        exit 1
    fi
    
    # Verify installation
    if ! verify_installation; then
        log "Installation completed with verification warnings"
        echo -e "${YELLOW}Installation completed with warnings.${NC}"
        echo -e "${YELLOW}Please fix any issues before starting the server.${NC}"
        echo -e "${YELLOW}You can run the verification script again:${NC}"
        echo -e "${BLUE}  ./scripts/verify-installation.sh${NC}"
        exit 1
    fi
    
    # Installation successful
    log "Installation completed successfully"
    echo -e "${GREEN}${BOLD}Installation completed successfully!${NC}"
    echo -e "${YELLOW}You can now start the server with:${NC}"
    echo -e "${BLUE}  ./run-now.sh${NC}"
    echo -e "${YELLOW}Or for more options:${NC}"
    echo -e "${BLUE}  ./scripts/mcp_resolve-cursor_start${NC}"
    
    # Ask if the user wants to start the server now
    echo ""
    read -p "Do you want to start the server now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_server
    else
        log "User chose not to start the server"
        echo -e "${YELLOW}You can start the server later with:${NC}"
        echo -e "${BLUE}  ./run-now.sh${NC}"
    fi
}

# Run the main installation process
main 