"""Mark and Marker tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_mark_tools(mcp):
    """Register mark and marker tools with the MCP server."""
    from src.utils.keyboard import (
        # Marks
        mark_set_in,
        mark_set_out,
        mark_clip,
        mark_go_to_in,
        mark_go_to_out,
        mark_clear_in,
        mark_clear_out,
        mark_clear_both,
        # Markers
        marker_add,
        marker_add_and_modify,
        marker_modify,
        marker_delete,
        marker_go_to_next,
        marker_go_to_previous,
    )

    # Mark operations
    @mcp.tool()
    def set_mark_in() -> Dict[str, Any]:
        """Set mark in point at playhead (I)."""
        return mark_set_in()

    @mcp.tool()
    def set_mark_out() -> Dict[str, Any]:
        """Set mark out point at playhead (O)."""
        return mark_set_out()

    @mcp.tool()
    def mark_current_clip() -> Dict[str, Any]:
        """Mark the current clip (X)."""
        return mark_clip()

    @mcp.tool()
    def go_to_mark_in() -> Dict[str, Any]:
        """Go to mark in point (Shift+I)."""
        return mark_go_to_in()

    @mcp.tool()
    def go_to_mark_out() -> Dict[str, Any]:
        """Go to mark out point (Shift+O)."""
        return mark_go_to_out()

    @mcp.tool()
    def clear_mark_in() -> Dict[str, Any]:
        """Clear mark in point (Alt+I)."""
        return mark_clear_in()

    @mcp.tool()
    def clear_mark_out() -> Dict[str, Any]:
        """Clear mark out point (Alt+O)."""
        return mark_clear_out()

    @mcp.tool()
    def clear_marks() -> Dict[str, Any]:
        """Clear both mark in and out points (Alt+X)."""
        return mark_clear_both()

    # Marker operations
    @mcp.tool()
    def add_marker() -> Dict[str, Any]:
        """Add marker at playhead (M)."""
        return marker_add()

    @mcp.tool()
    def add_and_modify_marker() -> Dict[str, Any]:
        """Add marker and open modify dialog (Ctrl+M)."""
        return marker_add_and_modify()

    @mcp.tool()
    def modify_marker() -> Dict[str, Any]:
        """Modify existing marker at playhead (Shift+M)."""
        return marker_modify()

    @mcp.tool()
    def delete_marker() -> Dict[str, Any]:
        """Delete marker at playhead (Alt+M)."""
        return marker_delete()

    @mcp.tool()
    def go_to_next_marker() -> Dict[str, Any]:
        """Go to next marker (Shift+Down)."""
        return marker_go_to_next()

    @mcp.tool()
    def go_to_previous_marker() -> Dict[str, Any]:
        """Go to previous marker (Shift+Up)."""
        return marker_go_to_previous()
