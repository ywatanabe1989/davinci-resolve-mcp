#!/usr/bin/env python3
"""
DaVinci Resolve MCP Server
A server that connects to DaVinci Resolve via the Model Context Protocol (MCP)

Version: 1.4.0 - Modular Architecture
"""

import os
import sys
import logging

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import platform utilities
from src.utils.platform import get_platform, get_resolve_paths

# Setup platform-specific paths and environment variables
paths = get_resolve_paths()
RESOLVE_API_PATH = paths["api_path"]
RESOLVE_LIB_PATH = paths["lib_path"]
RESOLVE_MODULES_PATH = paths["modules_path"]

os.environ["RESOLVE_SCRIPT_API"] = RESOLVE_API_PATH
os.environ["RESOLVE_SCRIPT_LIB"] = RESOLVE_LIB_PATH

# Add the module path to Python's path if it's not already there
if RESOLVE_MODULES_PATH not in sys.path:
    sys.path.append(RESOLVE_MODULES_PATH)

# Import MCP
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("davinci-resolve-mcp")

# Log server version and platform
VERSION = "1.4.0"
logger.info(f"Starting DaVinci Resolve MCP Server v{VERSION}")
logger.info(f"Detected platform: {get_platform()}")
logger.info(f"Using Resolve API path: {RESOLVE_API_PATH}")
logger.info(f"Using Resolve library path: {RESOLVE_LIB_PATH}")

# Create MCP server instance
mcp = FastMCP("DaVinciResolveMCP")

# Initialize DaVinci Resolve connection
resolve = None
try:
    import DaVinciResolveScript as dvr_script

    resolve = dvr_script.scriptapp("Resolve")
    if resolve:
        logger.info("Successfully connected to DaVinci Resolve")
    else:
        logger.warning(
            "DaVinci Resolve is not running or the scripting API is unavailable"
        )
except ImportError as e:
    logger.error(f"Failed to import DaVinciResolveScript: {e}")
except Exception as e:
    logger.error(f"Error connecting to DaVinci Resolve: {e}")

# Register all MCP tools and resources
from src.mcp_tools import register_all_tools

register_all_tools(mcp, resolve, logger)
logger.info("All MCP tools registered successfully")


# Note: This module should be imported, not run directly.
# Use src/__main__.py as the entry point.
