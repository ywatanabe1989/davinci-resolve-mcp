#!/usr/bin/env python3
"""Page navigation functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def page_media() -> Dict[str, Any]:
    """Switch to Media page (Shift+2)."""
    return send_key_to_resolve("+2", "Media Page (Shift+2)")


def page_cut() -> Dict[str, Any]:
    """Switch to Cut page (Shift+3)."""
    return send_key_to_resolve("+3", "Cut Page (Shift+3)")


def page_edit() -> Dict[str, Any]:
    """Switch to Edit page (Shift+4)."""
    return send_key_to_resolve("+4", "Edit Page (Shift+4)")


def page_fusion() -> Dict[str, Any]:
    """Switch to Fusion page (Shift+5)."""
    return send_key_to_resolve("+5", "Fusion Page (Shift+5)")


def page_color() -> Dict[str, Any]:
    """Switch to Color page (Shift+6)."""
    return send_key_to_resolve("+6", "Color Page (Shift+6)")


def page_fairlight() -> Dict[str, Any]:
    """Switch to Fairlight page (Shift+7)."""
    return send_key_to_resolve("+7", "Fairlight Page (Shift+7)")


def page_deliver() -> Dict[str, Any]:
    """Switch to Deliver page (Shift+8)."""
    return send_key_to_resolve("+8", "Deliver Page (Shift+8)")
