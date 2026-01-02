#!/bin/bash
# DaVinci Resolve MCP Server Setup Script

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up DaVinci Resolve MCP Server...${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    echo "Please install Python 3 and try again."
    exit 1
fi

# Create and activate virtual environment
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"

echo -e "${YELLOW}Creating Python virtual environment at $VENV_DIR...${NC}"
python3 -m venv "$VENV_DIR"

# Activate virtual environment (source doesn't work in scripts)
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# Install MCP SDK in the virtual environment with CLI support
echo -e "${YELLOW}Installing MCP SDK with CLI support in virtual environment...${NC}"
"$VENV_PIP" install "mcp[cli]"

# Check if DaVinci Resolve is installed
if [ ! -d "/Applications/DaVinci Resolve" ]; then
    echo -e "${RED}Warning: DaVinci Resolve installation not found at the default location.${NC}"
    echo "If DaVinci Resolve is installed in a different location, you'll need to manually update the environment variables."
else
    echo -e "${GREEN}DaVinci Resolve installation found.${NC}"
fi

# Set up environment variables
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"

# Check if Scripting API directory exists
if [ ! -d "$RESOLVE_SCRIPT_API" ]; then
    echo -e "${RED}Warning: DaVinci Resolve Scripting API folder not found at the expected location.${NC}"
    echo "This might be due to a different version of DaVinci Resolve or custom installation."
else
    echo -e "${GREEN}DaVinci Resolve Scripting API found.${NC}"
fi

# Add environment variables to shell profile
SHELL_PROFILE=""
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
    fi
else
    echo -e "${RED}Warning: Could not find a shell profile to update.${NC}"
    echo "Please manually add the following environment variables to your shell profile:"
    echo "export RESOLVE_SCRIPT_API=\"$RESOLVE_SCRIPT_API\""
    echo "export RESOLVE_SCRIPT_LIB=\"$RESOLVE_SCRIPT_LIB\""
    echo "export PYTHONPATH=\"\$PYTHONPATH:\$RESOLVE_SCRIPT_API/Modules/\""
fi

# Create wrapper script to run server with the virtual environment
cat > "$SCRIPT_DIR/run-server.sh" << EOF
#!/bin/bash
# Wrapper script to run the DaVinci Resolve MCP Server with the virtual environment

# Source environment variables if not already set
if [ -z "\$RESOLVE_SCRIPT_API" ]; then
  source "$SHELL_PROFILE"
fi

# Activate virtual environment and run server
"$VENV_DIR/bin/python" "$SCRIPT_DIR/../src/__main__.py" "\$@"
EOF

chmod +x "$SCRIPT_DIR/run-server.sh"

# Set up Cursor configuration
CURSOR_CONFIG_DIR="$HOME/.cursor"
CURSOR_MCP_CONFIG="$CURSOR_CONFIG_DIR/mcp.json"

if [ ! -d "$CURSOR_CONFIG_DIR" ]; then
    echo -e "${YELLOW}Creating Cursor config directory...${NC}"
    mkdir -p "$CURSOR_CONFIG_DIR"
fi

# Get the full path to the wrapper script
SERVER_PATH="$SCRIPT_DIR/run-server.sh"

# Check if Cursor MCP config exists
if [ -f "$CURSOR_MCP_CONFIG" ]; then
    echo -e "${YELLOW}Found existing Cursor MCP config. Not modifying it.${NC}"
    echo "To manually add the DaVinci Resolve MCP server, edit $CURSOR_MCP_CONFIG and add:"
    echo "{\"mcpServers\": {\"davinci-resolve\": {\"command\": \"$SERVER_PATH\"}}}"
else
    echo -e "${YELLOW}Creating Cursor MCP config...${NC}"
    cat > "$CURSOR_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "$SERVER_PATH"
    }
  }
}
EOF
    echo -e "${GREEN}Created Cursor MCP config at $CURSOR_MCP_CONFIG${NC}"
fi

# Make the server script executable
chmod +x "$SCRIPT_DIR/src/__main__.py"

echo -e "${GREEN}Setup completed!${NC}"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "1. Make sure to restart your terminal or run 'source $SHELL_PROFILE' to apply the environment variables."
echo "2. DaVinci Resolve must be running before starting the MCP server."
echo "3. You can test the server by running: $SCRIPT_DIR/run-server.sh"
echo "   or with the MCP CLI: $VENV_DIR/bin/mcp dev $SCRIPT_DIR/src/__main__.py"
echo ""
echo -e "${GREEN}Happy editing with DaVinci Resolve and your AI assistant!${NC}" 