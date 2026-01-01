#!/usr/bin/env python3
"""
DaVinci Resolve MCP Timeline Item Transform Tools
Setting timeline item properties
"""

from .properties import find_timeline_item


def register_timeline_item_transform_tools(mcp, resolve, logger):
    """Register timeline item transform MCP tools."""

    @mcp.tool()
    def set_timeline_item_transform(
        timeline_item_id: str, property_name: str, property_value: float
    ) -> str:
        """Set a transform property for a timeline item."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return "Error: No timeline currently active"

        valid_properties = [
            "Pan",
            "Tilt",
            "ZoomX",
            "ZoomY",
            "Rotation",
            "AnchorPointX",
            "AnchorPointY",
            "Pitch",
            "Yaw",
        ]

        if property_name not in valid_properties:
            return f"Error: Invalid property. Must be one of: {', '.join(valid_properties)}"

        try:
            timeline_item, _ = find_timeline_item(
                current_timeline,
                timeline_item_id,
                search_video=True,
                search_audio=False,
            )

            if not timeline_item:
                return (
                    f"Error: Video timeline item with ID '{timeline_item_id}' not found"
                )

            if timeline_item.GetType() != "Video":
                return f"Error: Timeline item with ID '{timeline_item_id}' is not a video item"

            result = timeline_item.SetProperty(property_name, property_value)
            if result:
                return f"Successfully set {property_name} to {property_value}"
            else:
                return f"Failed to set {property_name}"
        except Exception as e:
            return f"Error setting timeline item property: {str(e)}"

    @mcp.tool()
    def set_timeline_item_crop(
        timeline_item_id: str, crop_type: str, crop_value: float
    ) -> str:
        """Set a crop property for a timeline item."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return "Error: No timeline currently active"

        valid_crop_types = ["Left", "Right", "Top", "Bottom"]

        if crop_type not in valid_crop_types:
            return f"Error: Invalid crop type. Must be one of: {', '.join(valid_crop_types)}"

        property_name = f"Crop{crop_type}"

        try:
            timeline_item, _ = find_timeline_item(
                current_timeline,
                timeline_item_id,
                search_video=True,
                search_audio=False,
            )

            if not timeline_item:
                return (
                    f"Error: Video timeline item with ID '{timeline_item_id}' not found"
                )

            if timeline_item.GetType() != "Video":
                return f"Error: Timeline item with ID '{timeline_item_id}' is not a video item"

            result = timeline_item.SetProperty(property_name, crop_value)
            if result:
                return f"Successfully set crop {crop_type.lower()} to {crop_value}"
            else:
                return f"Failed to set crop {crop_type.lower()}"
        except Exception as e:
            return f"Error setting timeline item crop: {str(e)}"

    @mcp.tool()
    def set_timeline_item_composite(
        timeline_item_id: str, composite_mode: str = None, opacity: float = None
    ) -> str:
        """Set composite properties for a timeline item."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return "Error: No timeline currently active"

        if composite_mode is None and opacity is None:
            return "Error: Must specify at least one of composite_mode or opacity"

        valid_composite_modes = [
            "Normal",
            "Add",
            "Subtract",
            "Difference",
            "Multiply",
            "Screen",
            "Overlay",
            "Hardlight",
            "Softlight",
            "Darken",
            "Lighten",
            "ColorDodge",
            "ColorBurn",
            "Exclusion",
            "Hue",
            "Saturation",
            "Color",
            "Luminosity",
        ]

        if composite_mode and composite_mode not in valid_composite_modes:
            return f"Error: Invalid composite mode"

        if opacity is not None and (opacity < 0.0 or opacity > 1.0):
            return "Error: Opacity must be between 0.0 and 1.0"

        try:
            timeline_item, _ = find_timeline_item(
                current_timeline,
                timeline_item_id,
                search_video=True,
                search_audio=False,
            )

            if not timeline_item:
                return (
                    f"Error: Video timeline item with ID '{timeline_item_id}' not found"
                )

            if timeline_item.GetType() != "Video":
                return f"Error: Timeline item with ID '{timeline_item_id}' is not a video item"

            success = True

            if composite_mode:
                if not timeline_item.SetProperty("CompositeMode", composite_mode):
                    success = False

            if opacity is not None:
                if not timeline_item.SetProperty("Opacity", opacity):
                    success = False

            if success:
                changes = []
                if composite_mode:
                    changes.append(f"composite mode to '{composite_mode}'")
                if opacity is not None:
                    changes.append(f"opacity to {opacity}")
                return f"Successfully set {' and '.join(changes)}"
            else:
                return "Failed to set some composite properties"
        except Exception as e:
            return f"Error setting composite properties: {str(e)}"

    @mcp.tool()
    def set_timeline_item_retime(
        timeline_item_id: str, speed: float = None, process: str = None
    ) -> str:
        """Set retiming properties for a timeline item."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return "Error: No timeline currently active"

        if speed is None and process is None:
            return "Error: Must specify at least one of speed or process"

        if speed is not None and speed <= 0:
            return "Error: Speed must be greater than 0"

        valid_processes = ["NearestFrame", "FrameBlend", "OpticalFlow"]
        if process and process not in valid_processes:
            return f"Error: Invalid retime process"

        try:
            timeline_item, _ = find_timeline_item(
                current_timeline,
                timeline_item_id,
                search_video=True,
                search_audio=False,
            )

            if not timeline_item:
                return (
                    f"Error: Video timeline item with ID '{timeline_item_id}' not found"
                )

            success = True

            if speed is not None:
                if not timeline_item.SetProperty("Speed", speed):
                    success = False

            if process:
                if not timeline_item.SetProperty("RetimeProcess", process):
                    success = False

            if success:
                changes = []
                if speed is not None:
                    changes.append(f"speed to {speed}x")
                if process:
                    changes.append(f"retime process to '{process}'")
                return f"Successfully set {' and '.join(changes)}"
            else:
                return "Failed to set some retime properties"
        except Exception as e:
            return f"Error setting retime properties: {str(e)}"

    @mcp.tool()
    def set_timeline_item_stabilization(
        timeline_item_id: str,
        enabled: bool = None,
        method: str = None,
        strength: float = None,
    ) -> str:
        """Set stabilization properties for a timeline item."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return "Error: No timeline currently active"

        if enabled is None and method is None and strength is None:
            return "Error: Must specify at least one parameter to modify"

        valid_methods = ["Perspective", "Similarity", "Translation"]
        if method and method not in valid_methods:
            return f"Error: Invalid stabilization method"

        if strength is not None and (strength < 0.0 or strength > 1.0):
            return "Error: Strength must be between 0.0 and 1.0"

        try:
            timeline_item, _ = find_timeline_item(
                current_timeline,
                timeline_item_id,
                search_video=True,
                search_audio=False,
            )

            if not timeline_item:
                return (
                    f"Error: Video timeline item with ID '{timeline_item_id}' not found"
                )

            if timeline_item.GetType() != "Video":
                return f"Error: Timeline item with ID '{timeline_item_id}' is not a video item"

            success = True

            if enabled is not None:
                if not timeline_item.SetProperty(
                    "StabilizationEnable", 1 if enabled else 0
                ):
                    success = False

            if method:
                if not timeline_item.SetProperty("StabilizationMethod", method):
                    success = False

            if strength is not None:
                if not timeline_item.SetProperty("StabilizationStrength", strength):
                    success = False

            if success:
                changes = []
                if enabled is not None:
                    changes.append(
                        f"stabilization {'enabled' if enabled else 'disabled'}"
                    )
                if method:
                    changes.append(f"method to '{method}'")
                if strength is not None:
                    changes.append(f"strength to {strength}")
                return f"Successfully set {' and '.join(changes)}"
            else:
                return "Failed to set some stabilization properties"
        except Exception as e:
            return f"Error setting stabilization properties: {str(e)}"

    @mcp.tool()
    def set_timeline_item_audio(
        timeline_item_id: str,
        volume: float = None,
        pan: float = None,
        eq_enabled: bool = None,
    ) -> str:
        """Set audio properties for a timeline item."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return "Error: No timeline currently active"

        if volume is None and pan is None and eq_enabled is None:
            return "Error: Must specify at least one parameter to modify"

        if volume is not None and volume < 0.0:
            return "Error: Volume must be greater than or equal to 0.0"

        if pan is not None and (pan < -1.0 or pan > 1.0):
            return "Error: Pan must be between -1.0 and 1.0"

        try:
            timeline_item, item_type = find_timeline_item(
                current_timeline, timeline_item_id
            )

            if not timeline_item:
                return f"Error: Timeline item with ID '{timeline_item_id}' not found"

            if item_type != "audio" and timeline_item.GetMediaType() != "Audio":
                return f"Error: Timeline item does not have audio properties"

            success = True

            if volume is not None:
                if not timeline_item.SetProperty("Volume", volume):
                    success = False

            if pan is not None:
                if not timeline_item.SetProperty("Pan", pan):
                    success = False

            if eq_enabled is not None:
                if not timeline_item.SetProperty("EQEnable", 1 if eq_enabled else 0):
                    success = False

            if success:
                changes = []
                if volume is not None:
                    changes.append(f"volume to {volume}")
                if pan is not None:
                    changes.append(f"pan to {pan}")
                if eq_enabled is not None:
                    changes.append(f"EQ {'enabled' if eq_enabled else 'disabled'}")
                return f"Successfully set {' and '.join(changes)}"
            else:
                return "Failed to set some audio properties"
        except Exception as e:
            return f"Error setting audio properties: {str(e)}"

    logger.info("Registered timeline item transform tools")
