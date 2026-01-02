"""Edit mode tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_mode_tools(mcp):
    """Register edit mode tools with the MCP server."""
    from src.utils.keyboard import (
        mode_selection,
        mode_blade,
        mode_trim,
        mode_dynamic_trim,
        mode_slip_slide,
        toggle_snapping,
        toggle_audio_scrubbing,
    )
    from src.utils.keyboard import (
        transition_add,
        transition_add_video,
        transition_add_audio,
    )
    from src.utils.keyboard import (
        retime_controls,
        retime_freeze_frame,
    )

    @mcp.tool()
    def enter_selection_mode() -> Dict[str, Any]:
        """Enter normal selection/edit mode (A)."""
        return mode_selection()

    @mcp.tool()
    def enter_blade_mode() -> Dict[str, Any]:
        """Enter blade/razor mode for cutting clips (B)."""
        return mode_blade()

    @mcp.tool()
    def enter_trim_mode() -> Dict[str, Any]:
        """Enter trim mode (T)."""
        return mode_trim()

    @mcp.tool()
    def enter_dynamic_trim_mode() -> Dict[str, Any]:
        """Enter dynamic trim mode (W)."""
        return mode_dynamic_trim()

    @mcp.tool()
    def enter_slip_slide_mode() -> Dict[str, Any]:
        """Enter slip/slide mode (S)."""
        return mode_slip_slide()

    @mcp.tool()
    def toggle_snapping_mode() -> Dict[str, Any]:
        """Toggle snapping on/off (N)."""
        return toggle_snapping()

    @mcp.tool()
    def toggle_audio_scrubbing_mode() -> Dict[str, Any]:
        """Toggle audio scrubbing (Shift+S)."""
        return toggle_audio_scrubbing()

    @mcp.tool()
    def add_transition() -> Dict[str, Any]:
        """Add default transition at edit point (Ctrl+T)."""
        return transition_add()

    @mcp.tool()
    def add_video_transition() -> Dict[str, Any]:
        """Add video transition only (Alt+T)."""
        return transition_add_video()

    @mcp.tool()
    def add_audio_transition() -> Dict[str, Any]:
        """Add audio transition only (Shift+T)."""
        return transition_add_audio()

    @mcp.tool()
    def show_retime_controls() -> Dict[str, Any]:
        """Show retime controls (Ctrl+R)."""
        return retime_controls()

    @mcp.tool()
    def create_freeze_frame() -> Dict[str, Any]:
        """Create freeze frame at playhead (Shift+R)."""
        return retime_freeze_frame()
