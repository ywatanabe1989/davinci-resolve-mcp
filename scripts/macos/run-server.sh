#!/bin/bash
# Wrapper script to run the DaVinci Resolve MCP Server with the virtual environment

# Source environment variables if not already set
if [ -z "$RESOLVE_SCRIPT_API" ]; then
  source "/Users/samuelgursky/.zshrc"
fi

# Activate virtual environment and run server
"/Users/samuelgursky/davinci-resolve-mcp-20250326/scripts/venv/bin/python" "/Users/samuelgursky/davinci-resolve-mcp-20250326/scripts/src/__main__.py" "$@"
