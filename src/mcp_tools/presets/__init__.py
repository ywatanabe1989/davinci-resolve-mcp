#!/usr/bin/env python3
"""
DaVinci Resolve MCP Preset Tools
Color preset and LUT management
"""

from .color_presets import register_color_preset_tools
from .luts import register_lut_tools


def register_preset_tools(mcp, resolve, logger):
    """Register all preset MCP tools and resources."""
    register_color_preset_tools(mcp, resolve, logger)
    register_lut_tools(mcp, resolve, logger)
    logger.info("Registered preset tools")
