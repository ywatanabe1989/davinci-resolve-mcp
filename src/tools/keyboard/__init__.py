"""
Keyboard Control Tools for DaVinci Resolve MCP Server.

Registers keyboard simulation tools for AI agents to control DaVinci Resolve
features that are NOT exposed via the scripting API.
"""

from .playback_tools import register_playback_tools
from .edit_tools import register_edit_tools
from .mark_tools import register_mark_tools
from .selection_tools import register_selection_tools
from .view_tools import register_view_tools
from .page_tools import register_page_tools
from .node_tools import register_node_tools
from .mode_tools import register_mode_tools
from .app_tools import register_app_tools
from .utility_tools import register_utility_tools


def register_keyboard_tools(mcp):
    """Register all keyboard simulation tools with the MCP server."""
    register_playback_tools(mcp)
    register_edit_tools(mcp)
    register_mark_tools(mcp)
    register_selection_tools(mcp)
    register_view_tools(mcp)
    register_page_tools(mcp)
    register_node_tools(mcp)
    register_mode_tools(mcp)
    register_app_tools(mcp)
    register_utility_tools(mcp)


__all__ = ["register_keyboard_tools"]
