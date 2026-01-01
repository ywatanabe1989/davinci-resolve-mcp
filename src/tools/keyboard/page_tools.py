"""Page navigation tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_page_tools(mcp):
    """Register page navigation tools with the MCP server."""
    from src.utils.keyboard import (
        page_media,
        page_cut,
        page_edit,
        page_fusion,
        page_color,
        page_fairlight,
        page_deliver,
    )

    @mcp.tool()
    def switch_to_media_page() -> Dict[str, Any]:
        """Switch to Media page (Shift+2)."""
        return page_media()

    @mcp.tool()
    def switch_to_cut_page() -> Dict[str, Any]:
        """Switch to Cut page (Shift+3)."""
        return page_cut()

    @mcp.tool()
    def switch_to_edit_page() -> Dict[str, Any]:
        """Switch to Edit page (Shift+4)."""
        return page_edit()

    @mcp.tool()
    def switch_to_fusion_page() -> Dict[str, Any]:
        """Switch to Fusion page (Shift+5)."""
        return page_fusion()

    @mcp.tool()
    def switch_to_color_page() -> Dict[str, Any]:
        """Switch to Color page (Shift+6)."""
        return page_color()

    @mcp.tool()
    def switch_to_fairlight_page() -> Dict[str, Any]:
        """Switch to Fairlight page (Shift+7)."""
        return page_fairlight()

    @mcp.tool()
    def switch_to_deliver_page() -> Dict[str, Any]:
        """Switch to Deliver page (Shift+8)."""
        return page_deliver()
