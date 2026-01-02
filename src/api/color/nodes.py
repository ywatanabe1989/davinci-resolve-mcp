#!/usr/bin/env python3
"""
DaVinci Resolve Color Node Operations
Node management in the color page
"""

import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger("davinci-resolve-mcp.color.nodes")


def ensure_clip_selected(resolve, timeline) -> Tuple[bool, Optional[Any], str]:
    """Ensures a clip is selected in the timeline, selecting the first clip if needed."""
    current_clip = timeline.GetCurrentVideoItem()
    if current_clip:
        logger.info(f"Clip already selected: {current_clip.GetName()}")
        return (
            True,
            current_clip,
            f"Using currently selected clip: {current_clip.GetName()}",
        )

    logger.info("No clip currently selected, attempting to select first clip")
    try:
        video_track_count = timeline.GetTrackCount("video")
        logger.info(f"Timeline has {video_track_count} video tracks")

        for track_index in range(1, video_track_count + 1):
            logger.info(f"Checking video track {track_index}")
            track_items = timeline.GetItemListInTrack("video", track_index)

            if not track_items or len(track_items) == 0:
                logger.info(f"No clips in track {track_index}")
                continue

            logger.info(f"Found {len(track_items)} clips in track {track_index}")
            first_clip = track_items[0]

            if first_clip:
                clip_name = first_clip.GetName()
                logger.info(f"Attempting to select clip: {clip_name}")
                timeline.SetCurrentVideoItem(first_clip)

                selected_clip = timeline.GetCurrentVideoItem()
                if selected_clip and selected_clip.GetName() == clip_name:
                    logger.info(f"Successfully selected first clip: {clip_name}")
                    return (
                        True,
                        selected_clip,
                        f"Automatically selected clip: {clip_name}",
                    )
                else:
                    logger.warning("Failed to verify clip selection")

            logger.warning(f"Could not select a clip in track {track_index}")

        logger.warning("No clips found in any video track, or could not select any")
        return False, None, "Could not find any clips in the timeline to select"

    except Exception as e:
        logger.error(f"Error attempting to select a clip: {str(e)}")
        return False, None, f"Error selecting clip: {str(e)}"


def get_current_node(resolve) -> Dict[str, Any]:
    """Get information about the current node in the color page."""
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

        current_node_index = current_grade.GetCurrentNode()
        if current_node_index < 1:
            return {"error": "No node is currently selected"}

        node_count = current_grade.GetNodeCount()

        node_info = {
            "clip_name": current_clip.GetName(),
            "node_index": current_node_index,
            "node_count": node_count,
            "is_serial": current_grade.IsSerial(current_node_index),
            "is_parallel": current_grade.IsParallel(current_node_index),
            "is_layer": current_grade.IsLayer(current_node_index),
        }

        try:
            node_name = current_grade.GetNodeName(current_node_index)
            node_info["name"] = node_name
        except Exception:
            node_info["name"] = f"Node {current_node_index}"

        try:
            properties = {}
            try:
                properties["enabled"] = current_grade.IsNodeEnabled(current_node_index)
            except Exception:
                pass
            try:
                properties["type"] = current_grade.GetNodeType(current_node_index)
            except Exception:
                pass
            if properties:
                node_info["properties"] = properties
        except Exception:
            pass

        return node_info

    except Exception as e:
        return {"error": f"Error getting current node: {str(e)}"}


def add_node(resolve, node_type: str = "serial", label: str = None) -> str:
    """Add a new node to the current grade in the color page."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    valid_node_types = ["serial", "parallel", "layer"]
    if node_type.lower() not in valid_node_types:
        return (
            f"Error: Invalid node type. Must be one of: {', '.join(valid_node_types)}"
        )

    logger.info(f"Adding {node_type} node with label: {label if label else 'None'}")

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
            logger.warning(
                "Could not get grade object, attempting direct node creation"
            )
            try:
                color_page = project_manager.GetCurrentPage()
                if color_page and hasattr(color_page, "GetNodeGraph"):
                    node_graph = color_page.GetNodeGraph()
                    if node_graph:
                        logger.info("Successfully got node graph through ColorPage")
                        if node_type.lower() == "serial":
                            result = node_graph.AddSerialNode()
                        elif node_type.lower() == "parallel":
                            result = node_graph.AddParallelNode()
                        elif node_type.lower() == "layer":
                            result = node_graph.AddLayerNode()

                        if result:
                            return f"Successfully added {node_type} node using direct NodeGraph approach"
            except Exception as e:
                logger.error(f"Error in direct node creation attempt: {str(e)}")

            return f"Error adding {node_type} node: Cannot access grade object."

        logger.info("Proceeding with node addition with valid grade object")
        result = False
        method_name = ""

        if node_type.lower() == "serial":
            method_name = "AddSerialNode"
            logger.info(f"Calling {method_name}()")
            result = current_grade.AddSerialNode()
        elif node_type.lower() == "parallel":
            method_name = "AddParallelNode"
            logger.info(f"Calling {method_name}()")
            result = current_grade.AddParallelNode()
        elif node_type.lower() == "layer":
            method_name = "AddLayerNode"
            logger.info(f"Calling {method_name}()")
            result = current_grade.AddLayerNode()

        if not result:
            logger.error(f"Failed to add {node_type} node using {method_name}()")
            return f"Failed to add {node_type} node using {method_name}()"

        new_node_count = current_grade.GetNodeCount()
        logger.info(f"New node count: {new_node_count}")

        new_node_index = current_grade.GetCurrentNode()
        logger.info(f"New node index: {new_node_index}")

        if label and new_node_index > 0:
            try:
                logger.info(f"Setting node label to '{label}'")
                current_grade.SetNodeLabel(new_node_index, label)
                node_label_info = f" with label '{label}'"
            except Exception as e:
                logger.warning(f"Failed to set node label: {str(e)}")
                node_label_info = f" (couldn't set label to '{label}')"
        else:
            node_label_info = ""

        logger.info(
            f"Successfully added {node_type} node (index {new_node_index}){node_label_info}"
        )
        return f"Successfully added {node_type} node (index {new_node_index}){node_label_info}"

    except Exception as e:
        logger.error(f"Error adding {node_type} node: {str(e)}")
        return f"Error adding {node_type} node: {str(e)}"
