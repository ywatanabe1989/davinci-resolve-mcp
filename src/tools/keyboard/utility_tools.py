"""Utility tools for DaVinci Resolve MCP Server."""

from typing import Dict, Any


def register_utility_tools(mcp):
    """Register utility tools with the MCP server."""
    from src.utils.keyboard import send_custom_key, get_keyboard_shortcuts

    @mcp.tool()
    def send_keyboard_shortcut(key: str, description: str = "") -> Dict[str, Any]:
        """
        Send a custom keyboard shortcut to DaVinci Resolve.

        Args:
            key: The key in SendKeys format:
                - Regular keys: 'a', 'b', '1', etc.
                - Special keys: {ENTER}, {TAB}, {ESC}, {BACKSPACE}, {DELETE}
                - Arrow keys: {LEFT}, {RIGHT}, {UP}, {DOWN}
                - Function keys: {F1} through {F12}
                - Modifiers: ^ for Ctrl, + for Shift, % for Alt
                - Examples: '^s' (Ctrl+S), '+{F10}' (Shift+F10), '%{F4}' (Alt+F4)
            description: Optional description of the action

        Returns:
            Dict with success status and message
        """
        return send_custom_key(key, description)

    @mcp.resource("resolve://keyboard/shortcuts")
    def list_keyboard_shortcuts() -> Dict[str, str]:
        """Get a comprehensive list of DaVinci Resolve keyboard shortcuts."""
        return get_keyboard_shortcuts()
