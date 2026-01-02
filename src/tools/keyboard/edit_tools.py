"""Edit operation tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_edit_tools(mcp):
    """Register edit operation tools with the MCP server."""
    from src.utils.keyboard import (
        edit_cut_at_playhead,
        edit_ripple_delete,
        edit_delete,
        edit_undo,
        edit_redo,
        edit_trim_start,
        edit_trim_end,
        edit_insert,
        edit_overwrite,
        edit_copy,
        edit_cut,
        edit_paste,
        edit_split_clip,
        edit_join_clip,
        edit_nudge_left,
        edit_nudge_right,
        edit_replace,
        edit_place_on_top,
        edit_append_to_end,
    )

    @mcp.tool()
    def cut_at_playhead() -> Dict[str, Any]:
        """Cut/Razor at the current playhead position (Ctrl+B)."""
        return edit_cut_at_playhead()

    @mcp.tool()
    def ripple_delete_clip() -> Dict[str, Any]:
        """Ripple delete selected clip - removes clip and closes gap (Delete)."""
        return edit_ripple_delete()

    @mcp.tool()
    def delete_clip() -> Dict[str, Any]:
        """Delete the selected clip, leaving gap (Backspace)."""
        return edit_delete()

    @mcp.tool()
    def undo_action() -> Dict[str, Any]:
        """Undo the last action (Ctrl+Z)."""
        return edit_undo()

    @mcp.tool()
    def redo_action() -> Dict[str, Any]:
        """Redo the last undone action (Ctrl+Shift+Z)."""
        return edit_redo()

    @mcp.tool()
    def trim_clip_start() -> Dict[str, Any]:
        """Trim the start of the clip to the playhead (Shift+[)."""
        return edit_trim_start()

    @mcp.tool()
    def trim_clip_end() -> Dict[str, Any]:
        """Trim the end of the clip to the playhead (Shift+])."""
        return edit_trim_end()

    @mcp.tool()
    def insert_clip() -> Dict[str, Any]:
        """Insert clip at playhead, pushing existing clips (F9)."""
        return edit_insert()

    @mcp.tool()
    def overwrite_clip() -> Dict[str, Any]:
        """Overwrite at playhead, replacing existing content (F10)."""
        return edit_overwrite()

    @mcp.tool()
    def copy_clip() -> Dict[str, Any]:
        """Copy the selected clip (Ctrl+C)."""
        return edit_copy()

    @mcp.tool()
    def cut_clip_to_clipboard() -> Dict[str, Any]:
        """Cut the selected clip to clipboard (Ctrl+X)."""
        return edit_cut()

    @mcp.tool()
    def paste_clip() -> Dict[str, Any]:
        """Paste the copied clip (Ctrl+V)."""
        return edit_paste()

    @mcp.tool()
    def split_clip_at_playhead() -> Dict[str, Any]:
        """Split clip at playhead (Ctrl+\\)."""
        return edit_split_clip()

    @mcp.tool()
    def join_clips() -> Dict[str, Any]:
        """Join adjacent clips (Alt+\\)."""
        return edit_join_clip()

    @mcp.tool()
    def nudge_clip_left() -> Dict[str, Any]:
        """Nudge clip left by one frame (,)."""
        return edit_nudge_left()

    @mcp.tool()
    def nudge_clip_right() -> Dict[str, Any]:
        """Nudge clip right by one frame (.)."""
        return edit_nudge_right()

    @mcp.tool()
    def replace_clip() -> Dict[str, Any]:
        """Replace clip at playhead (F11)."""
        return edit_replace()

    @mcp.tool()
    def place_clip_on_top() -> Dict[str, Any]:
        """Place clip on top of timeline (F12)."""
        return edit_place_on_top()

    @mcp.tool()
    def append_clip_to_end() -> Dict[str, Any]:
        """Append clip to end of timeline (Shift+F12)."""
        return edit_append_to_end()
