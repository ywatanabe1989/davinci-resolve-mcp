#!/usr/bin/env python3
"""Application control functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def app_save_project() -> Dict[str, Any]:
    """Save project (Ctrl+S)."""
    return send_key_to_resolve("^s", "Save Project (Ctrl+S)")


def app_import_media() -> Dict[str, Any]:
    """Open import media dialog (Ctrl+I)."""
    return send_key_to_resolve("^i", "Import Media (Ctrl+I)")


def app_export_project() -> Dict[str, Any]:
    """Open export dialog (Ctrl+E)."""
    return send_key_to_resolve("^e", "Export Project (Ctrl+E)")


def app_new_timeline() -> Dict[str, Any]:
    """Create new timeline (Ctrl+N)."""
    return send_key_to_resolve("^n", "New Timeline (Ctrl+N)")


def app_new_bin() -> Dict[str, Any]:
    """Create new bin (Ctrl+Shift+N)."""
    return send_key_to_resolve("^+n", "New Bin (Ctrl+Shift+N)")


def app_project_settings() -> Dict[str, Any]:
    """Open project settings (Shift+9)."""
    return send_key_to_resolve("+9", "Project Settings (Shift+9)")


def app_preferences() -> Dict[str, Any]:
    """Open preferences (Ctrl+,)."""
    return send_key_to_resolve("^,", "Preferences (Ctrl+,)")


def app_keyboard_customization() -> Dict[str, Any]:
    """Open keyboard customization (Ctrl+Alt+K)."""
    return send_key_to_resolve("^%k", "Keyboard Customization (Ctrl+Alt+K)")


def app_quit() -> Dict[str, Any]:
    """Quit DaVinci Resolve (Ctrl+Q)."""
    return send_key_to_resolve("^q", "Quit (Ctrl+Q)")
