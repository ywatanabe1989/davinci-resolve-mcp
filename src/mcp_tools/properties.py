#!/usr/bin/env python3
"""
DaVinci Resolve MCP Project Property Tools
Project properties, timeline format, color settings, and metadata
"""

from typing import Dict, Any

from src.utils.project_properties import (
    get_all_project_properties,
    get_project_property,
    set_project_property,
    get_timeline_format_settings,
    set_timeline_format,
    get_superscale_settings,
    set_superscale_settings,
    get_color_settings,
    set_color_science_mode,
    set_color_space,
    get_project_metadata,
    get_project_info,
)


def register_property_tools(mcp, resolve, logger):
    """Register project property MCP tools and resources."""

    @mcp.resource("resolve://project/properties")
    def get_project_properties_endpoint() -> Dict[str, Any]:
        """Get all project properties for the current project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        return get_all_project_properties(current_project)

    @mcp.resource("resolve://project/property/{property_name}")
    def get_project_property_endpoint(property_name: str) -> Dict[str, Any]:
        """Get a specific project property value.

        Args:
            property_name: Name of the property to get
        """
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        value = get_project_property(current_project, property_name)
        return {property_name: value}

    @mcp.tool()
    def set_project_property_tool(property_name: str, property_value: Any) -> str:
        """Set a project property value.

        Args:
            property_name: Name of the property to set
            property_value: Value to set for the property
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        result = set_project_property(current_project, property_name, property_value)

        if result:
            return (
                f"Successfully set project property '{property_name}' to "
                f"'{property_value}'"
            )
        else:
            return f"Failed to set project property '{property_name}'"

    @mcp.resource("resolve://project/timeline-format")
    def get_timeline_format() -> Dict[str, Any]:
        """Get timeline format settings for the current project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        return get_timeline_format_settings(current_project)

    @mcp.tool()
    def set_timeline_format_tool(
        width: int, height: int, frame_rate: float, interlaced: bool = False
    ) -> str:
        """Set timeline format (resolution and frame rate).

        Args:
            width: Timeline width in pixels
            height: Timeline height in pixels
            frame_rate: Timeline frame rate
            interlaced: Whether the timeline should use interlaced processing
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        result = set_timeline_format(
            current_project, width, height, frame_rate, interlaced
        )

        if result:
            interlace_status = "interlaced" if interlaced else "progressive"
            return (
                f"Successfully set timeline format to {width}x{height} at "
                f"{frame_rate} fps ({interlace_status})"
            )
        else:
            return "Failed to set timeline format"

    @mcp.resource("resolve://project/superscale")
    def get_superscale_settings_endpoint() -> Dict[str, Any]:
        """Get SuperScale settings for the current project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        return get_superscale_settings(current_project)

    @mcp.tool()
    def set_superscale_settings_tool(enabled: bool, quality: int = 0) -> str:
        """Set SuperScale settings for the current project.

        Args:
            enabled: Whether SuperScale is enabled
            quality: SuperScale quality (0=Auto, 1=Better Quality, 2=Smoother)
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        quality_names = {0: "Auto", 1: "Better Quality", 2: "Smoother"}

        result = set_superscale_settings(current_project, enabled, quality)

        if result:
            status = "enabled" if enabled else "disabled"
            quality_name = quality_names.get(quality, "Unknown")
            return (
                f"Successfully {status} SuperScale with quality set to {quality_name}"
            )
        else:
            return "Failed to set SuperScale settings"

    @mcp.resource("resolve://project/color-settings")
    def get_color_settings_endpoint() -> Dict[str, Any]:
        """Get color science and color space settings for the current project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        return get_color_settings(current_project)

    @mcp.tool()
    def set_color_science_mode_tool(mode: str) -> str:
        """Set color science mode for the current project.

        Args:
            mode: Color science mode ('YRGB', 'YRGB Color Managed', 'ACEScct',
                  or numeric value)
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        result = set_color_science_mode(current_project, mode)

        if result:
            return f"Successfully set color science mode to '{mode}'"
        else:
            return f"Failed to set color science mode to '{mode}'"

    @mcp.tool()
    def set_color_space_tool(color_space: str, gamma: str = None) -> str:
        """Set timeline color space and gamma.

        Args:
            color_space: Timeline color space (e.g., 'Rec.709', 'DCI-P3 D65',
                         'Rec.2020')
            gamma: Timeline gamma (e.g., 'Rec.709 Gamma', 'Gamma 2.4')
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        result = set_color_space(current_project, color_space, gamma)

        if result:
            if gamma:
                return (
                    f"Successfully set timeline color space to '{color_space}' "
                    f"with gamma '{gamma}'"
                )
            else:
                return f"Successfully set timeline color space to '{color_space}'"
        else:
            return "Failed to set timeline color space"

    @mcp.resource("resolve://project/metadata")
    def get_project_metadata_endpoint() -> Dict[str, Any]:
        """Get metadata for the current project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        return get_project_metadata(current_project)

    @mcp.resource("resolve://project/info")
    def get_project_info_endpoint() -> Dict[str, Any]:
        """Get comprehensive information about the current project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        return get_project_info(current_project)

    logger.info("Registered property tools")
