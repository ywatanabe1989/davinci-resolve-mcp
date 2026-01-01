#!/usr/bin/env python3
"""
DaVinci Resolve MCP Layout Preset Tools
Save, load, export, import, and delete layout presets
"""

import os
from typing import List, Dict, Any

from src.utils.layout_presets import (
    list_layout_presets,
    save_layout_preset,
    load_layout_preset,
    export_layout_preset,
    import_layout_preset,
    delete_layout_preset,
)


def register_layout_tools(mcp, resolve, logger):
    """Register layout preset MCP tools and resources."""

    @mcp.resource("resolve://layout-presets")
    def get_layout_presets() -> List[Dict[str, Any]]:
        """Get all available layout presets for DaVinci Resolve."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        return list_layout_presets(layout_type="ui")

    @mcp.tool()
    def save_layout_preset_tool(preset_name: str) -> str:
        """Save the current UI layout as a preset.

        Args:
            preset_name: Name for the saved preset
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        result = save_layout_preset(resolve, preset_name, layout_type="ui")
        if result:
            return f"Successfully saved layout preset '{preset_name}'"
        else:
            return f"Failed to save layout preset '{preset_name}'"

    @mcp.tool()
    def load_layout_preset_tool(preset_name: str) -> str:
        """Load a UI layout preset.

        Args:
            preset_name: Name of the preset to load
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        result = load_layout_preset(resolve, preset_name, layout_type="ui")
        if result:
            return f"Successfully loaded layout preset '{preset_name}'"
        else:
            return f"Failed to load layout preset '{preset_name}'"

    @mcp.tool()
    def export_layout_preset_tool(preset_name: str, export_path: str) -> str:
        """Export a layout preset to a file.

        Args:
            preset_name: Name of the preset to export
            export_path: Path to export the preset file to
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        result = export_layout_preset(preset_name, export_path, layout_type="ui")
        if result:
            return (
                f"Successfully exported layout preset '{preset_name}' to {export_path}"
            )
        else:
            return f"Failed to export layout preset '{preset_name}'"

    @mcp.tool()
    def import_layout_preset_tool(import_path: str, preset_name: str = None) -> str:
        """Import a layout preset from a file.

        Args:
            import_path: Path to the preset file to import
            preset_name: Name to save the imported preset as (uses filename if None)
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        result = import_layout_preset(import_path, preset_name, layout_type="ui")

        if preset_name is None:
            preset_name = os.path.splitext(os.path.basename(import_path))[0]

        if result:
            return f"Successfully imported layout preset as '{preset_name}'"
        else:
            return f"Failed to import layout preset from {import_path}"

    @mcp.tool()
    def delete_layout_preset_tool(preset_name: str) -> str:
        """Delete a layout preset.

        Args:
            preset_name: Name of the preset to delete
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        result = delete_layout_preset(preset_name, layout_type="ui")
        if result:
            return f"Successfully deleted layout preset '{preset_name}'"
        else:
            return f"Failed to delete layout preset '{preset_name}'"

    logger.info("Registered layout tools")
