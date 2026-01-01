#!/usr/bin/env python3
"""Audio control functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def audio_volume_up() -> Dict[str, Any]:
    """Increase volume by 1dB (Ctrl+Alt+=)."""
    return send_key_to_resolve("^%=", "Volume Up 1dB (Ctrl+Alt+=)")


def audio_volume_down() -> Dict[str, Any]:
    """Decrease volume by 1dB (Ctrl+Alt+-)."""
    return send_key_to_resolve("^%-", "Volume Down 1dB (Ctrl+Alt+-)")


def audio_toggle_video_audio_separate() -> Dict[str, Any]:
    """Toggle video/audio separate mode (Alt+U)."""
    return send_key_to_resolve("%u", "Toggle Video/Audio Separate (Alt+U)")
