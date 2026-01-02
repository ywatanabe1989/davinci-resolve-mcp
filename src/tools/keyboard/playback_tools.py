"""Playback control tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_playback_tools(mcp):
    """Register playback control tools with the MCP server."""
    from src.utils.keyboard import (
        playback_play_pause,
        playback_stop,
        playback_forward,
        playback_reverse,
        playback_step_forward,
        playback_step_backward,
        playback_go_to_start,
        playback_go_to_end,
        playback_loop_toggle,
        playback_fast_forward,
        playback_fast_reverse,
        playback_play_around,
    )

    @mcp.tool()
    def play_pause() -> Dict[str, Any]:
        """Toggle play/pause in DaVinci Resolve (Space key)."""
        return playback_play_pause()

    @mcp.tool()
    def stop_playback() -> Dict[str, Any]:
        """Stop playback in DaVinci Resolve (K key)."""
        return playback_stop()

    @mcp.tool()
    def play_forward() -> Dict[str, Any]:
        """Play forward (L key). Press multiple times for faster playback."""
        return playback_forward()

    @mcp.tool()
    def play_reverse() -> Dict[str, Any]:
        """Play in reverse (J key). Press multiple times for faster reverse."""
        return playback_reverse()

    @mcp.tool()
    def step_frame_forward() -> Dict[str, Any]:
        """Step forward one frame (Right Arrow key)."""
        return playback_step_forward()

    @mcp.tool()
    def step_frame_backward() -> Dict[str, Any]:
        """Step backward one frame (Left Arrow key)."""
        return playback_step_backward()

    @mcp.tool()
    def go_to_timeline_start() -> Dict[str, Any]:
        """Go to the start of the timeline (Home key)."""
        return playback_go_to_start()

    @mcp.tool()
    def go_to_timeline_end() -> Dict[str, Any]:
        """Go to the end of the timeline (End key)."""
        return playback_go_to_end()

    @mcp.tool()
    def toggle_loop_playback() -> Dict[str, Any]:
        """Toggle loop playback mode (Ctrl+/)."""
        return playback_loop_toggle()

    @mcp.tool()
    def fast_forward_playback() -> Dict[str, Any]:
        """Fast forward playback (Shift+L)."""
        return playback_fast_forward()

    @mcp.tool()
    def fast_reverse_playback() -> Dict[str, Any]:
        """Fast reverse playback (Shift+J)."""
        return playback_fast_reverse()

    @mcp.tool()
    def play_around_current() -> Dict[str, Any]:
        """Play around current position (/ key)."""
        return playback_play_around()
