#!/usr/bin/env python3
"""
DaVinci Resolve Project Properties - Core
Fundamental property access and format settings
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("davinci-resolve-mcp.project_properties.core")

# Common project properties with their types
PROJECT_PROPERTY_TYPES = {
    # Timeline settings
    "timelineFrameRate": "float",
    "timelineResolutionWidth": "int",
    "timelineResolutionHeight": "int",
    "timelineOutputResolutionWidth": "int",
    "timelineOutputResolutionHeight": "int",
    "timelineInterlaceProcessing": "int",
    # Color settings
    "colorScienceMode": "int",
    "timelineColorSpace": "string",
    "timelineGamma": "string",
    "inputDRT": "string",
    "outputDRT": "string",
    # Image processing
    "superScaleEnabled": "bool",
    "superScaleQuality": "int",
    "noiseReductionEnabled": "bool",
    "noiseReductionMode": "int",
    "noiseReductionValue": "float",
    # Format settings
    "timelineAudioSampleRate": "int",
    "timelineAudioBitDepth": "int",
    "mediaPoolRelativePath": "bool",
    # Cache settings
    "CacheMode": "int",
    "CacheClipMode": "int",
    "OptimizedMediaMode": "int",
    "ProxyMode": "int",
    "ProxyQuality": "int",
    "TimelineCacheMode": "int",
}


def get_all_project_properties(project_obj) -> Dict[str, Any]:
    """Get all project properties and their values."""
    if project_obj is None:
        return {"error": "Invalid project object"}

    try:
        all_settings = project_obj.GetSetting("")

        if all_settings is None or not isinstance(all_settings, dict):
            logger.warning("GetSetting('') did not return expected dictionary")

            properties = {}
            for prop_name in PROJECT_PROPERTY_TYPES.keys():
                try:
                    value = project_obj.GetSetting(prop_name)
                    properties[prop_name] = value
                except Exception as e:
                    logger.debug(f"Error getting property {prop_name}: {str(e)}")

            return properties
        else:
            return all_settings

    except Exception as e:
        logger.error(f"Error getting project properties: {str(e)}")
        return {"error": f"Error getting project properties: {str(e)}"}


def get_project_property(project_obj, property_name: str) -> Any:
    """Get a specific project property value."""
    if project_obj is None:
        return {"error": "Invalid project object"}

    try:
        value = project_obj.GetSetting(property_name)

        if property_name in PROJECT_PROPERTY_TYPES:
            property_type = PROJECT_PROPERTY_TYPES[property_name]

            if property_type == "int" and not isinstance(value, int):
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    pass
            elif property_type == "float" and not isinstance(value, float):
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    pass
            elif property_type == "bool" and not isinstance(value, bool):
                if isinstance(value, str):
                    value = value.lower() in ("true", "yes", "1", "on")

        return value
    except Exception as e:
        logger.error(f"Error getting project property {property_name}: {str(e)}")
        return {"error": f"Error getting project property: {str(e)}"}


def set_project_property(project_obj, property_name: str, property_value: Any) -> bool:
    """Set a project property value."""
    if project_obj is None:
        return False

    try:
        if property_name in PROJECT_PROPERTY_TYPES:
            property_type = PROJECT_PROPERTY_TYPES[property_name]

            if property_type == "int":
                try:
                    property_value = int(property_value)
                except (ValueError, TypeError):
                    logger.warning(
                        f"Invalid integer value for property {property_name}: {property_value}"
                    )

            elif property_type == "float":
                try:
                    property_value = float(property_value)
                except (ValueError, TypeError):
                    logger.warning(
                        f"Invalid float value for property {property_name}: {property_value}"
                    )

            elif property_type == "bool":
                if isinstance(property_value, str):
                    property_value = property_value.lower() in (
                        "true",
                        "yes",
                        "1",
                        "on",
                    )
                property_value = bool(property_value)

        return project_obj.SetSetting(property_name, property_value)

    except Exception as e:
        logger.error(f"Error setting project property {property_name}: {str(e)}")
        return False


def get_timeline_format_settings(project_obj) -> Dict[str, Any]:
    """Get timeline format settings for the project."""
    if project_obj is None:
        return {"error": "Invalid project object"}

    try:
        settings = {}
        format_properties = [
            "timelineFrameRate",
            "timelineResolutionWidth",
            "timelineResolutionHeight",
            "timelineOutputResolutionWidth",
            "timelineOutputResolutionHeight",
            "timelineInterlaceProcessing",
        ]

        for prop in format_properties:
            settings[prop] = get_project_property(project_obj, prop)

        if "timelineFrameRate" in settings:
            fps = settings["timelineFrameRate"]
            is_drop_frame = False
            if isinstance(fps, (int, float)):
                is_drop_frame = abs(fps - 29.97) < 0.01 or abs(fps - 59.94) < 0.01
            settings["isDropFrame"] = is_drop_frame

        if (
            "timelineResolutionWidth" in settings
            and "timelineResolutionHeight" in settings
        ):
            width = settings["timelineResolutionWidth"]
            height = settings["timelineResolutionHeight"]

            resolution_name = None
            if width == 3840 and height == 2160:
                resolution_name = "UHD 4K"
            elif width == 1920 and height == 1080:
                resolution_name = "FHD 1080p"
            elif width == 1280 and height == 720:
                resolution_name = "HD 720p"
            elif width == 4096 and height in [2160, 2304]:
                resolution_name = "DCI 4K"
            elif width == 2048 and height in [1080, 1152]:
                resolution_name = "DCI 2K"

            if resolution_name:
                settings["resolutionName"] = resolution_name

        return settings

    except Exception as e:
        logger.error(f"Error getting timeline format settings: {str(e)}")
        return {"error": f"Error getting timeline format settings: {str(e)}"}


def set_timeline_format(
    project_obj, width: int, height: int, frame_rate: float, interlaced: bool = False
) -> bool:
    """Set timeline format (resolution and frame rate)."""
    if project_obj is None:
        return False

    try:
        success = True

        if not set_project_property(project_obj, "timelineResolutionWidth", width):
            success = False

        if not set_project_property(project_obj, "timelineResolutionHeight", height):
            success = False

        if not set_project_property(project_obj, "timelineFrameRate", frame_rate):
            success = False

        interlace_value = 1 if interlaced else 0
        if not set_project_property(
            project_obj, "timelineInterlaceProcessing", interlace_value
        ):
            success = False

        return success

    except Exception as e:
        logger.error(f"Error setting timeline format: {str(e)}")
        return False
