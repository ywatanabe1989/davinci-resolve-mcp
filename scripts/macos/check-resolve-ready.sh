#!/bin/bash
# Pre-launch Check Script for DaVinci Resolve MCP
# This script verifies that DaVinci Resolve is running and all required components are installed
# before launching Cursor

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"
CURSOR_CONFIG_FILE="$HOME/.cursor/mcp.json"
RESOLVE_MCP_SERVER="$SCRIPT_DIR/src/__main__.py"

# Required files and their permissions
REQUIRED_FILES=(
    "$SCRIPT_DIR/src/__main__.py:755"
    "$SCRIPT_DIR/run-now.sh:755"
    "$SCRIPT_DIR/setup.sh:755"
)

# Function to check if DaVinci Resolve is running
check_resolve_running() {
    # Look for the actual process name "Resolve" (not "DaVinci Resolve")
    if pgrep -x "Resolve" > /dev/null; then
        return 0 # Running
    else
        return 1 # Not running
    fi
}

# Function to check environment variables
check_resolve_env() {
    if [ -z "$RESOLVE_SCRIPT_API" ] || [ -z "$RESOLVE_SCRIPT_LIB" ]; then
        return 1 # Not set
    else
        return 0 # Set
    fi
}

# Function to check if the virtual environment exists and has MCP installed
check_venv() {
    if [ ! -d "$VENV_DIR" ] || [ ! -f "$VENV_DIR/bin/python" ]; then
        return 1 # Missing
    fi
    
    if ! "$VENV_DIR/bin/pip" list | grep -q "mcp"; then
        return 2 # Missing MCP
    fi
    
    return 0 # All good
}

# Function to check all required files and permissions
check_required_files() {
    local missing_files=()
    local wrong_permissions=()
    
    for req in "${REQUIRED_FILES[@]}"; do
        IFS=':' read -r file perm <<< "$req"
        
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        elif [ "$(stat -f '%A' "$file")" != "$perm" ]; then
            wrong_permissions+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "${RED}✗ Missing required files:${NC}"
        for file in "${missing_files[@]}"; do
            echo -e "  - $file"
        done
        return 1
    fi
    
    if [ ${#wrong_permissions[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠ Some files have incorrect permissions:${NC}"
        for file in "${wrong_permissions[@]}"; do
            echo -e "  - $file"
        done
        return 2
    fi
    
    return 0
}

# Function to check if cursor config is properly set
check_cursor_config() {
    if [ ! -f "$CURSOR_CONFIG_FILE" ]; then
        return 1 # Missing
    fi
    
    if ! grep -q "davinci-resolve" "$CURSOR_CONFIG_FILE"; then
        return 2 # Missing config
    fi
    
    return 0 # All good
}

# Print header
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  DaVinci Resolve MCP Pre-Launch Check                        ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check 0: Required files and scripts
echo -e "${YELLOW}Checking required files and scripts...${NC}"
files_status=$(check_required_files)
file_check_result=$?

if [ "$file_check_result" -eq 0 ]; then
    echo -e "${GREEN}✓ All required files are present with correct permissions${NC}"
elif [ "$file_check_result" -eq 2 ]; then
    echo -e "${YELLOW}Fixing file permissions...${NC}"
    for req in "${REQUIRED_FILES[@]}"; do
        IFS=':' read -r file perm <<< "$req"
        if [ -f "$file" ]; then
            chmod "$perm" "$file"
            echo -e "  - Fixed permissions for $file"
        fi
    done
    echo -e "${GREEN}✓ File permissions fixed${NC}"
else
    echo -e "${RED}✗ Some required files are missing${NC}"
    echo -e "${YELLOW}Attempting to retrieve or recreate missing files...${NC}"
    
    # Check if src/__main__.py is missing and create a basic version if needed
    if [ ! -f "$RESOLVE_MCP_SERVER" ]; then
        echo -e "${YELLOW}Creating basic src/__main__.py...${NC}"
        cat > "$RESOLVE_MCP_SERVER" << 'EOF'
#!/usr/bin/env python3
"""
DaVinci Resolve MCP Server
A server that connects to DaVinci Resolve via the Model Context Protocol (MCP)

Version: 1.3.8 - Basic Server
"""

import os
import sys
import logging
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("davinci-resolve-mcp")

# Log server version and platform
VERSION = "1.3.8"
logger.info(f"Starting DaVinci Resolve MCP Server v{VERSION}")

# Create MCP server instance
mcp = FastMCP("DaVinciResolveMCP")

# Initialize connection to DaVinci Resolve
def initialize_resolve():
    """Initialize connection to DaVinci Resolve application."""
    try:
        # Import the DaVinci Resolve scripting module
        import DaVinciResolveScript as dvr_script
        
        # Get the resolve object
        resolve = dvr_script.scriptapp("Resolve")
        
        if resolve is None:
            logger.error("Failed to get Resolve object. Is DaVinci Resolve running?")
            return None
        
        logger.info(f"Connected to DaVinci Resolve: {resolve.GetProductName()} {resolve.GetVersionString()}")
        return resolve
    
    except ImportError:
        logger.error("Failed to import DaVinciResolveScript. Check environment variables.")
        logger.error("RESOLVE_SCRIPT_API, RESOLVE_SCRIPT_LIB, and PYTHONPATH must be set correctly.")
        logger.error("On macOS, typically:")
        logger.error('export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"')
        logger.error('export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"')
        logger.error('export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"')
        return None
    
    except Exception as e:
        logger.error(f"Unexpected error initializing Resolve: {str(e)}")
        return None

# Initialize Resolve once at startup
resolve = initialize_resolve()

# ------------------
# MCP Tools/Resources
# ------------------

@mcp.resource("resolve://version")
def get_resolve_version() -> str:
    """Get DaVinci Resolve version information."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    return f"{resolve.GetProductName()} {resolve.GetVersionString()}"

@mcp.resource("resolve://current-page")
def get_current_page() -> str:
    """Get the current page open in DaVinci Resolve (Edit, Color, Fusion, etc.)."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    return resolve.GetCurrentPage()

@mcp.tool()
def switch_page(page: str) -> str:
    """Switch to a specific page in DaVinci Resolve.
    
    Args:
        page: The page to switch to. Options: 'media', 'cut', 'edit', 'fusion', 'color', 'fairlight', 'deliver'
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    valid_pages = ['media', 'cut', 'edit', 'fusion', 'color', 'fairlight', 'deliver']
    page = page.lower()
    
    if page not in valid_pages:
        return f"Error: Invalid page. Choose from {', '.join(valid_pages)}"
    
    resolve.OpenPage(page.capitalize())
    return f"Successfully switched to {page} page"

# Start the server
if __name__ == "__main__":
    try:
        if resolve is None:
            logger.error("Server started but not connected to DaVinci Resolve.")
            logger.error("Make sure DaVinci Resolve is running and environment variables are correctly set.")
        else:
            logger.info("Successfully connected to DaVinci Resolve.")
        
        logger.info("Starting DaVinci Resolve MCP Server")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
EOF
        chmod 755 "$RESOLVE_MCP_SERVER"
        echo -e "${GREEN}✓ Created basic src/__main__.py${NC}"
    fi
    
    # Check if run-now.sh is missing and create if needed
    if [ ! -f "$SCRIPT_DIR/run-now.sh" ]; then
        echo -e "${YELLOW}Creating run-now.sh script...${NC}"
        cat > "$SCRIPT_DIR/run-now.sh" << 'EOF'
#!/bin/bash
# Quick setup script to get DaVinci Resolve MCP Server running

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"

echo -e "${GREEN}Setting up DaVinci Resolve MCP Server with virtual environment...${NC}"

# Create and activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
fi

# Install MCP SDK in the virtual environment with CLI support
echo -e "${YELLOW}Installing MCP SDK with CLI support in virtual environment...${NC}"
"$VENV_DIR/bin/pip" install "mcp[cli]"

# Source environment variables from .zshrc if they exist
if grep -q "RESOLVE_SCRIPT_API" "$HOME/.zshrc"; then
    echo -e "${YELLOW}Sourcing environment variables from .zshrc...${NC}"
    source "$HOME/.zshrc"
else
    echo -e "${YELLOW}Setting environment variables...${NC}"
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
fi

# Make the server script executable
chmod +x "$SCRIPT_DIR/src/__main__.py"

# Run the server with the virtual environment's Python
echo -e "${GREEN}Starting DaVinci Resolve MCP Server...${NC}"
echo -e "${YELLOW}Make sure DaVinci Resolve is running!${NC}"
echo ""

"$VENV_DIR/bin/mcp" dev "$SCRIPT_DIR/src/__main__.py"
EOF
        chmod 755 "$SCRIPT_DIR/run-now.sh"
        echo -e "${GREEN}✓ Created run-now.sh script${NC}"
    fi
    
    # Check if setup.sh is missing and create if needed
    if [ ! -f "$SCRIPT_DIR/setup.sh" ]; then
        echo -e "${YELLOW}Creating setup.sh script...${NC}"
        cat > "$SCRIPT_DIR/setup.sh" << 'EOF'
#!/bin/bash
# Setup script for DaVinci Resolve MCP Server

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"

echo -e "${GREEN}Setting up DaVinci Resolve MCP Server environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    
    echo -e "${YELLOW}Installing required packages...${NC}"
    "$VENV_DIR/bin/pip" install "mcp[cli]"
else
    echo -e "${YELLOW}Virtual environment already exists. Updating packages...${NC}"
    "$VENV_DIR/bin/pip" install --upgrade "mcp[cli]"
fi

# Setup environment variables
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"

# Find shell profile
if [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [ -n "$SHELL_PROFILE" ]; then
    echo -e "${YELLOW}Adding environment variables to $SHELL_PROFILE...${NC}"
    
    # Check if variables are already in the profile
    if grep -q "RESOLVE_SCRIPT_API" "$SHELL_PROFILE"; then
        echo -e "${YELLOW}Environment variables already exist in $SHELL_PROFILE. Skipping...${NC}"
    else
        echo "" >> "$SHELL_PROFILE"
        echo "# DaVinci Resolve MCP Server environment variables" >> "$SHELL_PROFILE"
        echo "export RESOLVE_SCRIPT_API=\"$RESOLVE_SCRIPT_API\"" >> "$SHELL_PROFILE"
        echo "export RESOLVE_SCRIPT_LIB=\"$RESOLVE_SCRIPT_LIB\"" >> "$SHELL_PROFILE"
        echo "export PYTHONPATH=\"\$PYTHONPATH:\$RESOLVE_SCRIPT_API/Modules/\"" >> "$SHELL_PROFILE"
        echo -e "${GREEN}Environment variables added to $SHELL_PROFILE${NC}"
        echo -e "${YELLOW}Please restart your terminal or run 'source $SHELL_PROFILE' to apply changes${NC}"
    fi
else
    echo -e "${RED}Warning: Could not find a shell profile to update.${NC}"
    echo "Please manually add the following environment variables to your shell profile:"
    echo "export RESOLVE_SCRIPT_API=\"$RESOLVE_SCRIPT_API\""
    echo "export RESOLVE_SCRIPT_LIB=\"$RESOLVE_SCRIPT_LIB\""
    echo "export PYTHONPATH=\"\$PYTHONPATH:\$RESOLVE_SCRIPT_API/Modules/\""
fi

# Setup Cursor configuration
CURSOR_CONFIG_DIR="$HOME/.cursor"
CURSOR_MCP_CONFIG="$CURSOR_CONFIG_DIR/mcp.json"

if [ ! -d "$CURSOR_CONFIG_DIR" ]; then
    echo -e "${YELLOW}Creating Cursor config directory...${NC}"
    mkdir -p "$CURSOR_CONFIG_DIR"
fi

# Create or update Cursor MCP config
echo -e "${YELLOW}Setting up Cursor MCP configuration...${NC}"
cat > "$CURSOR_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "$VENV_DIR/bin/python",
      "args": ["$SCRIPT_DIR/../src/__main__.py"]
    }
  }
}
EOF
echo -e "${GREEN}Cursor MCP configuration created at $CURSOR_MCP_CONFIG${NC}"

# Make scripts executable
chmod +x "$SCRIPT_DIR/src/__main__.py"
chmod +x "$SCRIPT_DIR/run-now.sh"
chmod +x "$SCRIPT_DIR/check-resolve-ready.sh"

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To use DaVinci Resolve with Cursor:${NC}"
echo "1. Make sure DaVinci Resolve is running"
echo "2. Start Cursor"
echo "3. Ask the AI assistant to interact with DaVinci Resolve"
echo ""
echo -e "${YELLOW}You can also run:${NC}"
echo "  ./check-resolve-ready.sh - To verify your environment before starting"
echo "  ./run-now.sh - To directly start the MCP server for testing"
EOF
        chmod 755 "$SCRIPT_DIR/setup.sh"
        echo -e "${GREEN}✓ Created setup.sh script${NC}"
    fi
    
    # Run setup to ensure everything is properly configured
    echo -e "${YELLOW}Running setup to ensure proper configuration...${NC}"
    "$SCRIPT_DIR/setup.sh"
fi

# Check 1: Is DaVinci Resolve running?
echo -e "${YELLOW}Checking if DaVinci Resolve is running...${NC}"
if check_resolve_running; then
    echo -e "${GREEN}✓ DaVinci Resolve is running${NC}"
else
    echo -e "${RED}✗ DaVinci Resolve is NOT running${NC}"
    echo -e "${YELLOW}Please start DaVinci Resolve before launching Cursor${NC}"
    
    # Ask if user wants to start DaVinci Resolve
    read -p "Would you like to start DaVinci Resolve now? (y/n): " start_resolve
    if [[ "$start_resolve" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Starting DaVinci Resolve...${NC}"
        open -a "DaVinci Resolve"
        echo -e "${YELLOW}Waiting for DaVinci Resolve to start...${NC}"
        sleep 5
        
        # Check again
        if check_resolve_running; then
            echo -e "${GREEN}✓ DaVinci Resolve started successfully${NC}"
        else
            echo -e "${YELLOW}DaVinci Resolve is starting. Please wait until it's fully loaded before proceeding.${NC}"
        fi
    else
        echo -e "${RED}DaVinci Resolve must be running for the MCP server to function properly.${NC}"
        exit 1
    fi
fi

# Check 2: Environment variables
echo -e "${YELLOW}Checking Resolve environment variables...${NC}"
if check_resolve_env; then
    echo -e "${GREEN}✓ Resolve environment variables are set${NC}"
    echo -e "  RESOLVE_SCRIPT_API = $RESOLVE_SCRIPT_API"
    echo -e "  RESOLVE_SCRIPT_LIB = $RESOLVE_SCRIPT_LIB"
else
    echo -e "${RED}✗ Resolve environment variables are NOT set${NC}"
    echo -e "${YELLOW}Setting default environment variables...${NC}"
    
    # Set default paths for macOS
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
    
    echo -e "${GREEN}✓ Environment variables set for this session:${NC}"
    echo -e "  RESOLVE_SCRIPT_API = $RESOLVE_SCRIPT_API"
    echo -e "  RESOLVE_SCRIPT_LIB = $RESOLVE_SCRIPT_LIB"
    echo -e "${YELLOW}Note: These variables are only set for this session. For permanent setup, run ./setup.sh${NC}"
fi

# Check 3: Virtual environment
echo -e "${YELLOW}Checking Python virtual environment...${NC}"
venv_status=$(check_venv)
if [ "$venv_status" -eq 0 ]; then
    echo -e "${GREEN}✓ Virtual environment is set up correctly with MCP installed${NC}"
elif [ "$venv_status" -eq 2 ]; then
    echo -e "${RED}✗ MCP is not installed in the virtual environment${NC}"
    echo -e "${YELLOW}Installing MCP...${NC}"
    "$VENV_DIR/bin/pip" install mcp[cli]
    echo -e "${GREEN}✓ MCP installed${NC}"
else
    echo -e "${RED}✗ Virtual environment is missing or incomplete${NC}"
    echo -e "${YELLOW}Setting up virtual environment...${NC}"
    
    # Create virtual environment
    python3 -m venv "$VENV_DIR"
    
    # Install MCP
    "$VENV_DIR/bin/pip" install mcp[cli]
    
    echo -e "${GREEN}✓ Virtual environment created and MCP installed${NC}"
fi

# Check 4: Cursor configuration
echo -e "${YELLOW}Checking Cursor configuration...${NC}"
cursor_status=$(check_cursor_config)
if [ "$cursor_status" -eq 0 ]; then
    echo -e "${GREEN}✓ Cursor is configured to use the DaVinci Resolve MCP server${NC}"
elif [ "$cursor_status" -eq 1 ]; then
    echo -e "${RED}✗ Cursor configuration file is missing${NC}"
    echo -e "${YELLOW}Creating Cursor configuration...${NC}"
    
    # Create directory if it doesn't exist
    mkdir -p "$HOME/.cursor"
    
    # Create config file
    cat > "$CURSOR_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "$VENV_DIR/bin/python",
      "args": ["$SCRIPT_DIR/../src/__main__.py"]
    }
  }
}
EOF
    echo -e "${GREEN}✓ Cursor configuration created${NC}"
else
    echo -e "${RED}✗ Cursor configuration is missing DaVinci Resolve MCP settings${NC}"
    echo -e "${YELLOW}Updating Cursor configuration...${NC}"
    
    # Backup existing config
    cp "$CURSOR_CONFIG_FILE" "$CURSOR_CONFIG_FILE.bak"
    
    # Update config file - this is a simple approach that assumes the file is valid JSON
    # A more robust approach would use jq if available
    if grep -q "\"mcpServers\"" "$CURSOR_CONFIG_FILE"; then
        # mcpServers already exists, try to add our server
        sed -i '' -e 's/"mcpServers": {/"mcpServers": {\n    "davinci-resolve": {\n      "name": "DaVinci Resolve MCP",\n      "command": "'"$VENV_DIR\/bin\/python"'",\n      "args": ["'"$SCRIPT_DIR/../src/__main__.py"'"]\n    },/g' "$CURSOR_CONFIG_FILE"
    else
        # No mcpServers exists, create everything
        cat > "$CURSOR_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "$VENV_DIR/bin/python",
      "args": ["$SCRIPT_DIR/../src/__main__.py"]
    }
  }
}
EOF
    fi
    
    echo -e "${GREEN}✓ Cursor configuration updated${NC}"
fi

# Final message
echo ""
echo -e "${GREEN}All checks complete!${NC}"
echo -e "${GREEN}Your system is ready to use DaVinci Resolve with Cursor.${NC}"
echo ""

# Ask if user wants to launch Cursor
read -p "Would you like to launch Cursor now? (y/n): " launch_cursor
if [[ "$launch_cursor" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Launching Cursor...${NC}"
    open -a "Cursor"
    echo -e "${GREEN}Cursor launched. Enjoy using DaVinci Resolve with AI assistance!${NC}"
fi

exit 0 