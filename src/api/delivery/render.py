#!/usr/bin/env python3
"""
DaVinci Resolve Render Operations
Render presets and adding jobs to render queue
"""

import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("davinci-resolve-mcp.delivery.render")


def ensure_render_settings(resolve, current_project) -> Tuple[bool, Optional[Any], str]:
    """Ensures render settings interface is properly initialized."""
    logger.info("Attempting to get render settings interface")
    try:
        render_settings_interface = current_project.GetRenderSettings()
        if render_settings_interface:
            logger.info("Successfully got render settings interface")
            return (
                True,
                render_settings_interface,
                "Render settings interface successfully obtained",
            )
        else:
            logger.warning("GetRenderSettings() returned None")
    except Exception as e:
        logger.error(f"Error getting render settings interface: {str(e)}")
        render_settings_interface = None

    logger.warning(
        "Failed to get render settings interface, trying alternative approaches"
    )

    try:
        logger.info("Trying to refresh the deliver page")
        current_page = resolve.GetCurrentPage()
        if current_page != "deliver":
            resolve.OpenPage("deliver")
        else:
            resolve.OpenPage("edit")
            resolve.OpenPage("deliver")

        render_settings_interface = current_project.GetRenderSettings()
        if render_settings_interface:
            logger.info("Successfully got render settings interface after page refresh")
            return (
                True,
                render_settings_interface,
                "Render settings interface obtained after page refresh",
            )
    except Exception as e:
        logger.error(f"Error in page refresh approach: {str(e)}")

    try:
        logger.info("Trying with a small delay")
        import time

        time.sleep(1.0)

        render_settings_interface = current_project.GetRenderSettings()
        if render_settings_interface:
            logger.info("Successfully got render settings interface after delay")
            return (
                True,
                render_settings_interface,
                "Render settings interface obtained after delay",
            )
    except Exception as e:
        logger.error(f"Error in delay approach: {str(e)}")

    logger.error("Could not get render settings interface after multiple attempts")
    return (
        False,
        None,
        "Failed to access render settings. Deliver page functionality may not be fully initialized.",
    )


def validate_render_preset(
    render_settings_interface, preset_name: str
) -> Tuple[bool, List[str], str]:
    """Validates that a render preset exists and returns available presets."""
    logger.info("Checking if preset exists")
    try:
        project_presets = render_settings_interface.GetRenderPresetList() or []
        system_presets = render_settings_interface.GetSystemPresetList() or []

        all_presets = project_presets + system_presets
        logger.info(
            f"Found {len(project_presets)} project presets and {len(system_presets)} system presets"
        )

        if preset_name in project_presets:
            logger.info(f"Found '{preset_name}' in project presets")
            return True, all_presets, f"Valid project preset: {preset_name}"
        elif preset_name in system_presets:
            logger.info(f"Found '{preset_name}' in system presets")
            return True, all_presets, f"Valid system preset: {preset_name}"
        else:
            logger.error(f"Render preset '{preset_name}' not found")
            return (
                False,
                all_presets,
                f"Preset '{preset_name}' not found. Available presets: {', '.join(all_presets)}",
            )
    except Exception as e:
        logger.error(f"Error while checking presets: {str(e)}")
        return False, [], f"Error checking render presets: {str(e)}"


def get_render_presets(resolve) -> List[Dict[str, Any]]:
    """Get all available render presets in the current project."""
    if not resolve:
        logger.error("No connection to DaVinci Resolve")
        return {"error": "No connection to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        logger.error("Failed to get Project Manager")
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        logger.error("No project is currently open")
        return {"error": "No project is currently open"}

    page = resolve.GetCurrentPage()
    if page != "deliver":
        logger.info(f"Switching from {page} page to deliver page")
        resolve.OpenPage("deliver")

    render_settings = current_project.GetRenderSettings()
    if not render_settings:
        logger.error("Failed to get render settings")
        return {"error": "Failed to get render settings"}

    presets = []

    try:
        project_presets = render_settings.GetRenderPresetList()
        for preset in project_presets:
            preset_info = {"name": preset, "type": "project", "details": {}}

            try:
                if render_settings.SetRenderSettings({"SelectPreset": preset}):
                    format_info = render_settings.GetCurrentRenderFormatAndCodec()
                    if format_info:
                        preset_info["details"]["format"] = format_info["format"]
                        preset_info["details"]["codec"] = format_info["codec"]

                    resolution = render_settings.GetCurrentRenderResolution()
                    if resolution:
                        preset_info["details"]["resolution"] = resolution

                    frame_rate = render_settings.GetCurrentRenderFrameRate()
                    if frame_rate:
                        preset_info["details"]["frame_rate"] = frame_rate
            except Exception as e:
                logger.warning(
                    f"Could not get detailed information for preset {preset}: {str(e)}"
                )

            presets.append(preset_info)
    except Exception as e:
        logger.warning(f"Could not get project presets: {str(e)}")

    try:
        system_presets = render_settings.GetSystemPresetList()
        for preset in system_presets:
            preset_info = {"name": preset, "type": "system", "details": {}}
            presets.append(preset_info)
    except Exception as e:
        logger.warning(f"Could not get system presets: {str(e)}")

    return presets


def add_to_render_queue(
    resolve,
    preset_name: str,
    timeline_name: Optional[str] = None,
    use_in_out_range: bool = False,
    render_settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Add the current timeline or a specific timeline to the render queue."""
    if not resolve:
        logger.error("No connection to DaVinci Resolve")
        return {"error": "No connection to DaVinci Resolve"}

    logger.info(f"Adding timeline to render queue with preset: {preset_name}")
    if timeline_name:
        logger.info(f"Using specified timeline: {timeline_name}")
    else:
        logger.info("Using current timeline")

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        logger.error("Failed to get Project Manager")
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        logger.error("No project is currently open")
        return {"error": "No project is currently open"}

    page = resolve.GetCurrentPage()
    if page != "deliver":
        logger.info(f"Switching from {page} page to deliver page")
        resolve.OpenPage("deliver")

    if timeline_name:
        timeline = current_project.GetTimelineByName(timeline_name)
        if not timeline:
            logger.error(f"Timeline '{timeline_name}' not found")
            return {"error": f"Timeline '{timeline_name}' not found"}
        current_project.SetCurrentTimeline(timeline)
    else:
        timeline = current_project.GetCurrentTimeline()
        if not timeline:
            logger.error("No timeline is currently open")
            return {"error": "No timeline is currently open"}

    actual_timeline_name = timeline.GetName()
    logger.info(f"Using timeline: {actual_timeline_name}")

    success, render_settings_interface, message = ensure_render_settings(
        resolve, current_project
    )
    if not success or not render_settings_interface:
        logger.error(f"Failed to initialize render settings: {message}")
        return {"error": message}

    preset_valid, available_presets, preset_message = validate_render_preset(
        render_settings_interface, preset_name
    )
    if not preset_valid:
        logger.error(f"Invalid preset: {preset_message}")
        return {"error": preset_message}

    settings_to_apply = {"SelectPreset": preset_name}
    logger.info(f"Applying render preset: {preset_name}")

    if render_settings:
        logger.info(f"Adding additional render settings: {render_settings}")
        settings_to_apply.update(render_settings)

    try:
        if not render_settings_interface.SetRenderSettings(settings_to_apply):
            logger.error(f"Failed to apply render preset '{preset_name}'")
            return {"error": f"Failed to apply render preset '{preset_name}'"}
        logger.info("Successfully applied render preset")
    except Exception as e:
        logger.error(f"Error applying render preset: {str(e)}")
        return {"error": f"Error applying render preset: {str(e)}"}

    result = False
    logger.info("Adding timeline to render queue")
    try:
        if use_in_out_range:
            logger.info("Using in/out range for render")
            result = current_project.AddRenderJobToRenderQueue()
        else:
            logger.info(
                f"Adding entire timeline '{actual_timeline_name}' to render queue"
            )
            result = current_project.AddTimelineToRenderQueue(actual_timeline_name)
    except Exception as e:
        logger.error(f"Exception while adding to render queue: {str(e)}")

        try:
            logger.info("Trying alternative approach for adding to render queue")
            render_settings_interface.SetRenderSettings(settings_to_apply)

            import time

            time.sleep(0.5)

            if use_in_out_range:
                result = current_project.AddRenderJobToRenderQueue()
            else:
                result = current_project.AddTimelineToRenderQueue(actual_timeline_name)
        except Exception as nested_e:
            logger.error(f"Alternative approach also failed: {str(nested_e)}")
            return {
                "error": f"Failed to add to render queue: {str(e)}. Alternative approach also failed: {str(nested_e)}"
            }

    if result:
        logger.info(
            f"Successfully added '{actual_timeline_name}' to render queue with preset '{preset_name}'"
        )
        return {
            "success": True,
            "message": f"Added '{actual_timeline_name}' to render queue with preset '{preset_name}'",
            "timeline": actual_timeline_name,
            "preset": preset_name,
            "in_out_range_only": use_in_out_range,
        }
    else:
        logger.error("Failed to add to render queue")
        return {
            "error": "Failed to add to render queue",
            "timeline": actual_timeline_name,
            "preset": preset_name,
        }
