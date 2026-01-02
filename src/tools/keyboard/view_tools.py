"""View control tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_view_tools(mcp):
    """Register view control tools with the MCP server."""
    from src.utils.keyboard import (
        view_zoom_in,
        view_zoom_out,
        view_fit_timeline,
        view_fullscreen_preview,
        view_fullscreen_viewer,
        view_enhanced_viewer,
        view_cinema_viewer,
        view_split_screen,
        view_video_scopes,
    )

    @mcp.tool()
    def zoom_in_timeline() -> Dict[str, Any]:
        """Zoom in on the timeline (Ctrl+=)."""
        return view_zoom_in()

    @mcp.tool()
    def zoom_out_timeline() -> Dict[str, Any]:
        """Zoom out on the timeline (Ctrl+-)."""
        return view_zoom_out()

    @mcp.tool()
    def fit_timeline_to_view() -> Dict[str, Any]:
        """Fit the entire timeline to the view (Shift+Z)."""
        return view_fit_timeline()

    @mcp.tool()
    def toggle_fullscreen_preview() -> Dict[str, Any]:
        """Toggle fullscreen preview mode (P)."""
        return view_fullscreen_preview()

    @mcp.tool()
    def toggle_fullscreen_viewer() -> Dict[str, Any]:
        """Toggle fullscreen viewer (Shift+F)."""
        return view_fullscreen_viewer()

    @mcp.tool()
    def toggle_enhanced_viewer() -> Dict[str, Any]:
        """Toggle enhanced viewer (Alt+F)."""
        return view_enhanced_viewer()

    @mcp.tool()
    def toggle_cinema_viewer() -> Dict[str, Any]:
        """Toggle cinema viewer (Ctrl+F)."""
        return view_cinema_viewer()

    @mcp.tool()
    def toggle_split_screen() -> Dict[str, Any]:
        """Toggle split screen view (Ctrl+Alt+W)."""
        return view_split_screen()

    @mcp.tool()
    def toggle_video_scopes() -> Dict[str, Any]:
        """Toggle video scopes display (Ctrl+Shift+W)."""
        return view_video_scopes()
