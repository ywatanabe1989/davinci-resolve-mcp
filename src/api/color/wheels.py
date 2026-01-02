#!/usr/bin/env python3
"""
DaVinci Resolve Color Wheel Operations
Color wheel parameter get/set operations
"""

import logging
from typing import Dict, Any

from .nodes import ensure_clip_selected

logger = logging.getLogger("davinci-resolve-mcp.color.wheels")


def get_color_wheels(resolve, node_index: int = None) -> Dict[str, Any]:
    """Get color wheel parameters for a specific node."""
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}

    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        return {"error": f"Not on Color page. Current page is: {current_page}"}

    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}

    try:
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return {"error": "No clip is currently selected in the timeline"}

        current_grade = current_clip.GetCurrentGrade()
        if not current_grade:
            return {"error": "Failed to get current grade"}

        target_node_index = node_index
        if target_node_index is None:
            target_node_index = current_grade.GetCurrentNode()
            if target_node_index < 1:
                return {"error": "No node is currently selected"}
        else:
            node_count = current_grade.GetNodeCount()
            if target_node_index < 1 or target_node_index > node_count:
                return {
                    "error": f"Invalid node index {target_node_index}. Valid range: 1-{node_count}"
                }

        node_name = ""
        try:
            node_name = current_grade.GetNodeName(target_node_index)
        except Exception:
            node_name = f"Node {target_node_index}"

        color_wheels = {
            "node_index": target_node_index,
            "node_name": node_name,
            "clip_name": current_clip.GetName(),
            "wheels": {},
        }

        wheels_to_get = [
            {"name": "lift", "function_prefix": "GetLift"},
            {"name": "gamma", "function_prefix": "GetGamma"},
            {"name": "gain", "function_prefix": "GetGain"},
            {"name": "offset", "function_prefix": "GetOffset"},
        ]

        for wheel in wheels_to_get:
            wheel_name = wheel["name"]
            prefix = wheel["function_prefix"]

            wheel_data = {}
            try:
                for channel, channel_name in [
                    ("R", "red"),
                    ("G", "green"),
                    ("B", "blue"),
                    ("Y", "master"),
                ]:
                    function_name = f"{prefix}{channel}"

                    if hasattr(current_grade, function_name):
                        getter_func = getattr(current_grade, function_name)
                        value = getter_func(target_node_index)
                        wheel_data[channel_name] = value

                if wheel_data:
                    color_wheels["wheels"][wheel_name] = wheel_data
            except Exception as e:
                color_wheels["wheels"][wheel_name] = {
                    "error": f"Could not get {wheel_name} wheel: {str(e)}"
                }

        try:
            additional_controls = {}

            try:
                if hasattr(current_grade, "GetContrast"):
                    additional_controls["contrast"] = current_grade.GetContrast(
                        target_node_index
                    )
            except Exception:
                pass

            try:
                if hasattr(current_grade, "GetSaturation"):
                    additional_controls["saturation"] = current_grade.GetSaturation(
                        target_node_index
                    )
            except Exception:
                pass

            try:
                if hasattr(current_grade, "GetColorTemp"):
                    additional_controls["color_temp"] = current_grade.GetColorTemp(
                        target_node_index
                    )
            except Exception:
                pass

            try:
                if hasattr(current_grade, "GetTint"):
                    additional_controls["tint"] = current_grade.GetTint(
                        target_node_index
                    )
            except Exception:
                pass

            if additional_controls:
                color_wheels["additional_controls"] = additional_controls
        except Exception:
            pass

        return color_wheels

    except Exception as e:
        return {"error": f"Error getting color wheel parameters: {str(e)}"}


def set_color_wheel_param(
    resolve, wheel: str, param: str, value: float, node_index: int = None
) -> str:
    """Set a color wheel parameter for a node."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    valid_wheels = ["lift", "gamma", "gain", "offset"]
    if wheel.lower() not in valid_wheels:
        return f"Error: Invalid wheel name. Must be one of: {', '.join(valid_wheels)}"

    valid_params = ["red", "green", "blue", "master"]
    if param.lower() not in valid_params:
        return (
            f"Error: Invalid parameter name. Must be one of: {', '.join(valid_params)}"
        )

    logger.info(f"Setting {wheel} {param} to {value}")

    param_to_channel = {"red": "R", "green": "G", "blue": "B", "master": "Y"}
    wheel_to_function_prefix = {
        "lift": "SetLift",
        "gamma": "SetGamma",
        "gain": "SetGain",
        "offset": "SetOffset",
    }

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        logger.error("Failed to get Project Manager")
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        logger.error("No project currently open")
        return "Error: No project currently open"

    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        logger.info(f"Currently on {current_page} page, switching to color page")
        result = resolve.OpenPage("color")
        if not result:
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"
        logger.info("Successfully switched to color page")

    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        logger.error("No timeline currently active")
        return "Error: No timeline currently active"

    try:
        clip_selected, current_clip, message = ensure_clip_selected(
            resolve, current_timeline
        )

        if not clip_selected or not current_clip:
            logger.error("No clip could be selected automatically")
            return (
                f"Error: {message}. Please select a clip manually in DaVinci Resolve."
            )

        logger.info(f"Working with clip: {current_clip.GetName()}")
        logger.info("Attempting to get current grade")

        try:
            current_grade = current_clip.GetCurrentGrade()
            if current_grade:
                logger.info("Successfully got current grade using GetCurrentGrade()")
            else:
                logger.warning("GetCurrentGrade() returned None")
        except Exception as e:
            logger.error(f"Error getting current grade via GetCurrentGrade(): {str(e)}")
            current_grade = None

        if not current_grade:
            logger.info("Attempting alternative methods to access grade functionality")
            try:
                logger.info("Trying to select the clip in timeline again")
                current_timeline.SetCurrentVideoItem(current_clip)
                logger.info(f"Selected clip {current_clip.GetName()} in timeline")
                current_grade = current_clip.GetCurrentGrade()
                if current_grade:
                    logger.info("Successfully got current grade after selection")
            except Exception as e:
                logger.error(f"Error in alternative selection approach: {str(e)}")

        if not current_grade:
            logger.error("Could not get grade object after multiple attempts")
            return "Error setting color wheel parameter: Cannot access grade object."

        logger.info("Proceeding with parameter setting with valid grade object")

        target_node_index = node_index
        if target_node_index is None:
            logger.info("Getting current node index")
            target_node_index = current_grade.GetCurrentNode()
            if target_node_index < 1:
                logger.error("No node is currently selected")
                return "Error: No node is currently selected"
            logger.info(f"Using current node: {target_node_index}")
        else:
            logger.info(f"Validating provided node index: {target_node_index}")
            node_count = current_grade.GetNodeCount()
            if target_node_index < 1 or target_node_index > node_count:
                return f"Error: Invalid node index {target_node_index}. Valid range: 1-{node_count}"

        node_name = ""
        try:
            logger.info(f"Getting name for node {target_node_index}")
            node_name = (
                current_grade.GetNodeName(target_node_index)
                or f"Node {target_node_index}"
            )
            logger.info(f"Node name: {node_name}")
        except Exception as e:
            logger.warning(f"Could not get node name: {str(e)}")
            node_name = f"Node {target_node_index}"

        channel = param_to_channel[param.lower()]
        function_prefix = wheel_to_function_prefix[wheel.lower()]
        function_name = f"{function_prefix}{channel}"
        logger.info(f"Function to call: {function_name}")

        if not hasattr(current_grade, function_name):
            logger.error(f"Function '{function_name}' not found in DaVinci Resolve API")
            return f"Error: Function '{function_name}' not found in DaVinci Resolve API"

        setter_func = getattr(current_grade, function_name)
        logger.info(f"Calling {function_name}({target_node_index}, {value})")
        result = setter_func(target_node_index, value)

        if result:
            logger.info(f"Successfully set {wheel} {param} to {value} for {node_name}")
            return f"Successfully set {wheel} {param} to {value} for {node_name}"
        else:
            logger.error(f"Failed to set {wheel} {param} to {value} for {node_name}")
            return f"Failed to set {wheel} {param} to {value} for {node_name}"

    except Exception as e:
        logger.error(f"Error setting color wheel parameter: {str(e)}")
        return f"Error setting color wheel parameter: {str(e)}"
