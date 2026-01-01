"""Color page node tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_node_tools(mcp):
    """Register color page node tools with the MCP server."""
    from src.utils.keyboard import (
        node_add_serial,
        node_add_parallel,
        node_add_layer,
        node_disable_current,
        node_disable_all,
        node_bypass_grades,
        node_reset_grades,
        node_previous,
        node_next,
        node_extract_current,
    )
    from src.utils.keyboard import (
        color_grab_still,
        color_auto_balance,
        color_highlight,
        color_add_version,
    )

    @mcp.tool()
    def add_serial_node() -> Dict[str, Any]:
        """Add serial node in Color page (Alt+S)."""
        return node_add_serial()

    @mcp.tool()
    def add_parallel_node() -> Dict[str, Any]:
        """Add parallel node in Color page (Alt+P)."""
        return node_add_parallel()

    @mcp.tool()
    def add_layer_node() -> Dict[str, Any]:
        """Add layer node in Color page (Alt+L)."""
        return node_add_layer()

    @mcp.tool()
    def disable_current_node() -> Dict[str, Any]:
        """Disable/Enable current node (Ctrl+D)."""
        return node_disable_current()

    @mcp.tool()
    def disable_all_nodes() -> Dict[str, Any]:
        """Disable/Enable all nodes (Alt+D)."""
        return node_disable_all()

    @mcp.tool()
    def bypass_all_grades() -> Dict[str, Any]:
        """Bypass all color grades (Shift+D)."""
        return node_bypass_grades()

    @mcp.tool()
    def reset_all_grades() -> Dict[str, Any]:
        """Reset all grades and notes (Ctrl+Home)."""
        return node_reset_grades()

    @mcp.tool()
    def select_previous_node() -> Dict[str, Any]:
        """Select previous node (Shift+Alt+;)."""
        return node_previous()

    @mcp.tool()
    def select_next_node() -> Dict[str, Any]:
        """Select next node (Shift+Alt+')."""
        return node_next()

    @mcp.tool()
    def extract_current_node() -> Dict[str, Any]:
        """Extract current node (E)."""
        return node_extract_current()

    @mcp.tool()
    def grab_still() -> Dict[str, Any]:
        """Grab still from current frame (Ctrl+Alt+G)."""
        return color_grab_still()

    @mcp.tool()
    def auto_color_balance() -> Dict[str, Any]:
        """Auto color balance (Alt+A)."""
        return color_auto_balance()

    @mcp.tool()
    def toggle_highlight_mode() -> Dict[str, Any]:
        """Toggle highlight mode (Shift+H)."""
        return color_highlight()

    @mcp.tool()
    def add_color_version() -> Dict[str, Any]:
        """Add new color version (Ctrl+Y)."""
        return color_add_version()
