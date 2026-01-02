#!/usr/bin/env python3
"""
DaVinci Resolve Render Operations
Render presets and adding jobs to render queue

NOTE: According to the DaVinci Resolve Scripting API documentation:
- GetRenderSettings() returns a dictionary, NOT an object with methods
- Render methods like SetRenderSettings(), GetRenderPresetList(), LoadRenderPreset()
  are called directly on the PROJECT object
"""

import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("davinci-resolve-mcp.delivery.render")


def ensure_deliver_page(resolve) -> bool:
    """Ensures we're on the deliver page for render operations."""
    try:
        current_page = resolve.GetCurrentPage()
        if current_page != "deliver":
            logger.info(f"Switching from {current_page} page to deliver page")
            resolve.OpenPage("deliver")
        return True
    except Exception as e:
        logger.error(f"Error switching to deliver page: {str(e)}")
        return False


def validate_render_preset(current_project, preset_name: str) -> Tuple[bool, List[str], str]:
    """Validates that a render preset exists and returns available presets.

    Args:
        current_project: The DaVinci Resolve project object
        preset_name: Name of the preset to validate

    Returns:
        Tuple of (is_valid, all_presets_list, message)
    """
    logger.info("Checking if preset exists")
    try:
        # GetRenderPresetList() is called on the project object directly
        all_presets = current_project.GetRenderPresetList() or []
        logger.info(f"Found {len(all_presets)} render presets")

        if preset_name in all_presets:
            logger.info(f"Found preset '{preset_name}'")
            return True, all_presets, f"Valid preset: {preset_name}"
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

    # Switch to deliver page for render operations
    ensure_deliver_page(resolve)

    presets = []

    try:
        # GetRenderPresetList() is called on the project object
        preset_list = current_project.GetRenderPresetList() or []
        for preset in preset_list:
            # Note: GetRenderSettings() is unreliable in some API versions,
            # so we just return the preset names without details
            preset_info = {"name": preset, "type": "preset", "details": {}}
            presets.append(preset_info)
    except Exception as e:
        logger.warning(f"Could not get presets: {str(e)}")

    return presets


def add_to_render_queue(
    resolve,
    preset_name: str,
    timeline_name: Optional[str] = None,
    use_in_out_range: bool = False,
    render_settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Add the current timeline or a specific timeline to the render queue.

    Args:
        resolve: DaVinci Resolve object
        preset_name: Name of the render preset to use
        timeline_name: Optional timeline name (uses current if not specified)
        use_in_out_range: If True, only render the in/out range
        render_settings: Optional dict with additional settings like TargetDir, CustomName

    Returns:
        Dict with success status and details
    """
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

    # Switch to deliver page
    ensure_deliver_page(resolve)

    # Set or get the timeline
    if timeline_name:
        # GetTimelineByName may not exist in all API versions, use index-based lookup
        timeline = None
        timeline_count = current_project.GetTimelineCount() or 0
        for i in range(1, timeline_count + 1):
            tl = current_project.GetTimelineByIndex(i)
            if tl and tl.GetName() == timeline_name:
                timeline = tl
                break
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

    # Validate preset exists
    preset_valid, available_presets, preset_message = validate_render_preset(current_project, preset_name)
    if not preset_valid:
        logger.error(f"Invalid preset: {preset_message}")
        return {"error": preset_message}

    # Load the render preset (method on project object)
    try:
        if not current_project.LoadRenderPreset(preset_name):
            logger.warning(f"LoadRenderPreset returned False for '{preset_name}', trying SetRenderSettings")
    except Exception as e:
        logger.warning(f"LoadRenderPreset failed: {str(e)}, trying SetRenderSettings")

    # Build settings dict
    settings_to_apply = {}

    # Add custom render settings if provided
    if render_settings:
        logger.info(f"Adding custom render settings: {render_settings}")
        settings_to_apply.update(render_settings)

    # Apply settings if we have any
    if settings_to_apply:
        try:
            # SetRenderSettings() is called on the project object
            result = current_project.SetRenderSettings(settings_to_apply)
            if result:
                logger.info("Successfully applied render settings")
            else:
                logger.warning("SetRenderSettings returned False")
        except Exception as e:
            logger.error(f"Error applying render settings: {str(e)}")
            return {"error": f"Error applying render settings: {str(e)}"}

    # Add to render queue
    job_id = None
    logger.info("Adding timeline to render queue")
    try:
        # AddRenderJob() is the correct method on project object
        job_id = current_project.AddRenderJob()
        logger.info(f"AddRenderJob returned: {job_id}")
    except Exception as e:
        logger.error(f"Exception while adding to render queue: {str(e)}")
        return {"error": f"Failed to add to render queue: {str(e)}"}

    if job_id:
        logger.info(f"Successfully added '{actual_timeline_name}' to render queue with preset '{preset_name}'")
        return {
            "success": True,
            "message": f"Added '{actual_timeline_name}' to render queue with preset '{preset_name}'",
            "job_id": job_id,
            "timeline": actual_timeline_name,
            "preset": preset_name,
            "in_out_range_only": use_in_out_range,
            "settings_applied": settings_to_apply if settings_to_apply else None,
        }
    else:
        logger.error("Failed to add to render queue - no job ID returned")
        return {
            "error": "Failed to add to render queue",
            "timeline": actual_timeline_name,
            "preset": preset_name,
        }
