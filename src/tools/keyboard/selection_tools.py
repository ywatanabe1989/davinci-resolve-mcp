"""Selection tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_selection_tools(mcp):
    """Register selection tools with the MCP server."""
    from src.utils.keyboard import (
        select_all,
        deselect_all,
        select_clips_forward,
        select_clips_backward,
        select_nearest_edit,
    )

    @mcp.tool()
    def select_all_clips() -> Dict[str, Any]:
        """Select all clips in the timeline (Ctrl+A)."""
        return select_all()

    @mcp.tool()
    def deselect_all_clips() -> Dict[str, Any]:
        """Deselect all clips in the timeline (Ctrl+Shift+A)."""
        return deselect_all()

    @mcp.tool()
    def select_forward_from_playhead() -> Dict[str, Any]:
        """Select all clips forward from the playhead (Y)."""
        return select_clips_forward()

    @mcp.tool()
    def select_backward_from_playhead() -> Dict[str, Any]:
        """Select all clips backward from the playhead (Ctrl+Y)."""
        return select_clips_backward()

    @mcp.tool()
    def select_nearest_edit_point() -> Dict[str, Any]:
        """Select nearest edit point (V)."""
        return select_nearest_edit()
