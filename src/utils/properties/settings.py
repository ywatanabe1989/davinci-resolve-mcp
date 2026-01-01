#!/usr/bin/env python3
"""
DaVinci Resolve Project Properties - Settings
SuperScale, color, and metadata settings
"""

import logging
from typing import Dict, Any

from .core import (
    get_project_property,
    set_project_property,
    get_timeline_format_settings,
    get_all_project_properties,
)

logger = logging.getLogger("davinci-resolve-mcp.project_properties.settings")


def get_superscale_settings(project_obj) -> Dict[str, Any]:
    """Get SuperScale settings for the project."""
    if project_obj is None:
        return {"error": "Invalid project object"}

    try:
        settings = {}

        superscale_enabled = get_project_property(project_obj, "superScaleEnabled")
        settings["enabled"] = bool(superscale_enabled)

        quality = get_project_property(project_obj, "superScaleQuality")
        settings["quality"] = quality

        quality_names = {
            0: "Auto",
            1: "Better Quality",
            2: "Smoother",
        }

        if quality in quality_names:
            settings["qualityName"] = quality_names[quality]

        for prop in ["superScaleOverrideWidth", "superScaleOverrideHeight"]:
            value = get_project_property(project_obj, prop)
            if value is not None:
                settings[prop] = value

        return settings

    except Exception as e:
        logger.error(f"Error getting SuperScale settings: {str(e)}")
        return {"error": f"Error getting SuperScale settings: {str(e)}"}


def set_superscale_settings(project_obj, enabled: bool, quality: int = 0) -> bool:
    """Set SuperScale settings for the project."""
    if project_obj is None:
        return False

    try:
        if quality not in [0, 1, 2]:
            logger.warning(
                f"Invalid SuperScale quality value: {quality}. Using 0 (Auto)"
            )
            quality = 0

        success = True

        if not set_project_property(project_obj, "superScaleEnabled", enabled):
            success = False

        if not set_project_property(project_obj, "superScaleQuality", quality):
            success = False

        return success

    except Exception as e:
        logger.error(f"Error setting SuperScale settings: {str(e)}")
        return False


def get_color_settings(project_obj) -> Dict[str, Any]:
    """Get color science and color space settings for the project."""
    if project_obj is None:
        return {"error": "Invalid project object"}

    try:
        settings = {}
        color_properties = [
            "colorScienceMode",
            "timelineColorSpace",
            "timelineGamma",
            "inputDRT",
            "outputDRT",
        ]

        for prop in color_properties:
            value = get_project_property(project_obj, prop)
            if value is not None:
                settings[prop] = value

        if "colorScienceMode" in settings:
            mode = settings["colorScienceMode"]
            mode_names = {
                0: "DaVinci YRGB",
                1: "DaVinci YRGB Color Managed",
                2: "ACEScct",
            }

            if mode in mode_names:
                settings["colorScienceName"] = mode_names[mode]

        return settings

    except Exception as e:
        logger.error(f"Error getting color settings: {str(e)}")
        return {"error": f"Error getting color settings: {str(e)}"}


def set_color_science_mode(project_obj, mode: str) -> bool:
    """Set color science mode for the project."""
    if project_obj is None:
        return False

    try:
        mode_values = {
            "YRGB": 0,
            "DaVinci YRGB": 0,
            "YRGB Color Managed": 1,
            "DaVinci YRGB Color Managed": 1,
            "ACEScct": 2,
            "ACES": 2,
        }

        mode_value = None

        if isinstance(mode, int) and 0 <= mode <= 2:
            mode_value = mode
        elif isinstance(mode, str):
            mode_value = mode_values.get(mode)

        if mode_value is None:
            logger.error(f"Invalid color science mode: {mode}")
            return False

        return set_project_property(project_obj, "colorScienceMode", mode_value)

    except Exception as e:
        logger.error(f"Error setting color science mode: {str(e)}")
        return False


def set_color_space(project_obj, color_space: str, gamma: str = None) -> bool:
    """Set timeline color space and gamma."""
    if project_obj is None:
        return False

    try:
        success = True

        if not set_project_property(project_obj, "timelineColorSpace", color_space):
            success = False

        if gamma is not None:
            if not set_project_property(project_obj, "timelineGamma", gamma):
                success = False

        return success

    except Exception as e:
        logger.error(f"Error setting color space: {str(e)}")
        return False


def get_project_metadata(project_obj) -> Dict[str, Any]:
    """Get project metadata."""
    if project_obj is None:
        return {"error": "Invalid project object"}

    try:
        metadata = {}

        metadata["name"] = project_obj.GetName()

        if hasattr(project_obj, "GetPath"):
            metadata["path"] = project_obj.GetPath()

        current_timeline = project_obj.GetCurrentTimeline()
        if current_timeline:
            metadata["currentTimeline"] = current_timeline.GetName()
            timeline_count = project_obj.GetTimelineCount()
            metadata["timelineCount"] = timeline_count

        format_settings = get_timeline_format_settings(project_obj)
        if "error" not in format_settings:
            metadata.update(format_settings)

        color_settings = get_color_settings(project_obj)
        if "error" not in color_settings:
            metadata["colorSettings"] = color_settings

        superscale_settings = get_superscale_settings(project_obj)
        if "error" not in superscale_settings:
            metadata["superScale"] = superscale_settings

        return metadata

    except Exception as e:
        logger.error(f"Error getting project metadata: {str(e)}")
        return {"error": f"Error getting project metadata: {str(e)}"}


def get_project_info(project_obj) -> Dict[str, Any]:
    """Get comprehensive project information including settings and metadata."""
    if project_obj is None:
        return {"error": "Invalid project object"}

    try:
        project_name = project_obj.GetName()

        project_info = {
            "name": project_name,
            "metadata": get_project_metadata(project_obj),
            "settings": get_all_project_properties(project_obj),
            "timelines": [],
        }

        timeline_count = project_obj.GetTimelineCount()
        current_timeline = project_obj.GetCurrentTimeline()
        current_timeline_name = current_timeline.GetName() if current_timeline else None

        for i in range(1, timeline_count + 1):
            timeline = project_obj.GetTimelineByIndex(i)
            if timeline:
                timeline_info = {
                    "name": timeline.GetName(),
                    "isCurrent": timeline.GetName() == current_timeline_name,
                    "duration": timeline.GetEndFrame() - timeline.GetStartFrame() + 1,
                }
                project_info["timelines"].append(timeline_info)

        return project_info

    except Exception as e:
        logger.error(f"Error getting project info: {str(e)}")
        return {"error": f"Error getting project info: {str(e)}"}
