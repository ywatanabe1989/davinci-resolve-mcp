#!/usr/bin/env python3
"""Edit operation functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def edit_cut_at_playhead() -> Dict[str, Any]:
    """Cut/Razor at playhead position (Ctrl+B)."""
    return send_key_to_resolve("^b", "Cut at Playhead (Ctrl+B)")


def edit_ripple_delete() -> Dict[str, Any]:
    """Ripple delete selected clip (Delete)."""
    return send_key_to_resolve("{DELETE}", "Ripple Delete (Delete)")


def edit_delete() -> Dict[str, Any]:
    """Delete selected clip leaving gap (Backspace)."""
    return send_key_to_resolve("{BACKSPACE}", "Delete (Backspace)")


def edit_undo() -> Dict[str, Any]:
    """Undo last action (Ctrl+Z)."""
    return send_key_to_resolve("^z", "Undo (Ctrl+Z)")


def edit_redo() -> Dict[str, Any]:
    """Redo last undone action (Ctrl+Shift+Z)."""
    return send_key_to_resolve("^+z", "Redo (Ctrl+Shift+Z)")


def edit_trim_start() -> Dict[str, Any]:
    """Trim clip start to playhead (Shift+[)."""
    return send_key_to_resolve("+[", "Trim Start (Shift+[)")


def edit_trim_end() -> Dict[str, Any]:
    """Trim clip end to playhead (Shift+])."""
    return send_key_to_resolve("+]", "Trim End (Shift+])")


def edit_insert() -> Dict[str, Any]:
    """Insert clip at playhead (F9)."""
    return send_key_to_resolve("{F9}", "Insert (F9)")


def edit_overwrite() -> Dict[str, Any]:
    """Overwrite clip at playhead (F10)."""
    return send_key_to_resolve("{F10}", "Overwrite (F10)")


def edit_copy() -> Dict[str, Any]:
    """Copy selected clip (Ctrl+C)."""
    return send_key_to_resolve("^c", "Copy (Ctrl+C)")


def edit_cut() -> Dict[str, Any]:
    """Cut selected clip (Ctrl+X)."""
    return send_key_to_resolve("^x", "Cut (Ctrl+X)")


def edit_paste() -> Dict[str, Any]:
    """Paste clip (Ctrl+V)."""
    return send_key_to_resolve("^v", "Paste (Ctrl+V)")


def edit_split_clip() -> Dict[str, Any]:
    """Split clip at playhead (Ctrl+\\)."""
    return send_key_to_resolve("^\\", "Split Clip (Ctrl+\\)")


def edit_join_clip() -> Dict[str, Any]:
    """Join adjacent clips (Alt+\\)."""
    return send_key_to_resolve("%\\", "Join Clip (Alt+\\)")


def edit_nudge_left() -> Dict[str, Any]:
    """Nudge clip left by one frame (,)."""
    return send_key_to_resolve(",", "Nudge Left (,)")


def edit_nudge_right() -> Dict[str, Any]:
    """Nudge clip right by one frame (.)."""
    return send_key_to_resolve(".", "Nudge Right (.)")


def edit_nudge_left_multi() -> Dict[str, Any]:
    """Nudge clip left by multiple frames (Shift+,)."""
    return send_key_to_resolve("+,", "Nudge Left Multi (Shift+,)")


def edit_nudge_right_multi() -> Dict[str, Any]:
    """Nudge clip right by multiple frames (Shift+.)."""
    return send_key_to_resolve("+.", "Nudge Right Multi (Shift+.)")


def edit_replace() -> Dict[str, Any]:
    """Replace clip (F11)."""
    return send_key_to_resolve("{F11}", "Replace (F11)")


def edit_place_on_top() -> Dict[str, Any]:
    """Place clip on top (F12)."""
    return send_key_to_resolve("{F12}", "Place on Top (F12)")


def edit_ripple_overwrite() -> Dict[str, Any]:
    """Ripple overwrite (Shift+F10)."""
    return send_key_to_resolve("+{F10}", "Ripple Overwrite (Shift+F10)")


def edit_fit_to_fill() -> Dict[str, Any]:
    """Fit to fill (Shift+F11)."""
    return send_key_to_resolve("+{F11}", "Fit to Fill (Shift+F11)")


def edit_append_to_end() -> Dict[str, Any]:
    """Append clip to end of timeline (Shift+F12)."""
    return send_key_to_resolve("+{F12}", "Append to End (Shift+F12)")
