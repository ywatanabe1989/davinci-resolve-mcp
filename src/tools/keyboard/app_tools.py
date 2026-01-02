"""Application control tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_app_tools(mcp):
    """Register application control tools with the MCP server."""
    from src.utils.keyboard import (
        app_save_project,
        app_import_media,
        app_export_project,
        app_new_timeline,
        app_new_bin,
        app_project_settings,
        app_preferences,
        app_keyboard_customization,
    )
    from src.utils.keyboard import (
        clip_enable_disable,
        clip_create_subclip,
        clip_add_flag,
    )
    from src.utils.keyboard import (
        audio_volume_up,
        audio_volume_down,
    )
    from src.utils.keyboard import (
        viewer_toggle_source_timeline,
        viewer_match_frame,
    )

    @mcp.tool()
    def save_project() -> Dict[str, Any]:
        """Save the current project (Ctrl+S)."""
        return app_save_project()

    @mcp.tool()
    def import_media_dialog() -> Dict[str, Any]:
        """Open import media dialog (Ctrl+I)."""
        return app_import_media()

    @mcp.tool()
    def export_project_dialog() -> Dict[str, Any]:
        """Open export project dialog (Ctrl+E)."""
        return app_export_project()

    @mcp.tool()
    def new_timeline_dialog() -> Dict[str, Any]:
        """Create new timeline dialog (Ctrl+N)."""
        return app_new_timeline()

    @mcp.tool()
    def new_bin() -> Dict[str, Any]:
        """Create new bin in media pool (Ctrl+Shift+N)."""
        return app_new_bin()

    @mcp.tool()
    def open_project_settings() -> Dict[str, Any]:
        """Open project settings (Shift+9)."""
        return app_project_settings()

    @mcp.tool()
    def open_preferences() -> Dict[str, Any]:
        """Open preferences dialog (Ctrl+,)."""
        return app_preferences()

    @mcp.tool()
    def open_keyboard_customization() -> Dict[str, Any]:
        """Open keyboard customization dialog (Ctrl+Alt+K)."""
        return app_keyboard_customization()

    @mcp.tool()
    def toggle_clip_enabled() -> Dict[str, Any]:
        """Enable/Disable selected clip (D)."""
        return clip_enable_disable()

    @mcp.tool()
    def create_subclip() -> Dict[str, Any]:
        """Create subclip from selection (Alt+B)."""
        return clip_create_subclip()

    @mcp.tool()
    def add_flag_to_clip() -> Dict[str, Any]:
        """Add flag to selected clip (G)."""
        return clip_add_flag()

    @mcp.tool()
    def increase_volume() -> Dict[str, Any]:
        """Increase volume by 1dB (Ctrl+Alt+=)."""
        return audio_volume_up()

    @mcp.tool()
    def decrease_volume() -> Dict[str, Any]:
        """Decrease volume by 1dB (Ctrl+Alt+-)."""
        return audio_volume_down()

    @mcp.tool()
    def toggle_source_timeline_viewer() -> Dict[str, Any]:
        """Toggle between source and timeline viewer (Q)."""
        return viewer_toggle_source_timeline()

    @mcp.tool()
    def match_frame() -> Dict[str, Any]:
        """Match frame - find source clip (F)."""
        return viewer_match_frame()
