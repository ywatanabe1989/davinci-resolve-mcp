"""
Keyboard Control Tool Registration for DaVinci Resolve MCP Server.

This module re-exports the register_keyboard_tools function from the
modular keyboard tools package.
"""

from src.tools.keyboard import register_keyboard_tools

__all__ = ["register_keyboard_tools"]
