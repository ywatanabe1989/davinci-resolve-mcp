#!/usr/bin/env python3
"""
DaVinci Resolve MCP Delivery Tools
Rendering and delivery operations
"""

import os
from typing import List, Dict, Any


def register_delivery_tools(mcp, resolve, logger):
    """Register delivery page MCP tools and resources."""

    def get_all_media_pool_clips(media_pool):
        """Get all clips from media pool recursively including subfolders."""
        clips = []
        root_folder = media_pool.GetRootFolder()

        def process_folder(folder):
            folder_clips = folder.GetClipList()
            if folder_clips:
                clips.extend(folder_clips)
            sub_folders = folder.GetSubFolderList()
            for sub_folder in sub_folders:
                process_folder(sub_folder)

        process_folder(root_folder)
        return clips

    @mcp.resource("resolve://delivery/render-presets")
    def get_render_presets() -> List[Dict[str, Any]]:
        """Get all available render presets in the current project."""
        from src.api.delivery_operations import get_render_presets as get_presets_func

        return get_presets_func(resolve)

    @mcp.tool()
    def add_to_render_queue(
        preset_name: str, timeline_name: str = None, use_in_out_range: bool = False
    ) -> Dict[str, Any]:
        """Add a timeline to the render queue with the specified preset."""
        from src.api.delivery_operations import add_to_render_queue as add_queue_func

        return add_queue_func(resolve, preset_name, timeline_name, use_in_out_range)

    @mcp.tool()
    def start_render() -> Dict[str, Any]:
        """Start rendering the jobs in the render queue."""
        from src.api.delivery_operations import start_render as start_render_func

        return start_render_func(resolve)

    @mcp.resource("resolve://delivery/render-queue/status")
    def get_render_queue_status() -> Dict[str, Any]:
        """Get the status of jobs in the render queue."""
        from src.api.delivery_operations import (
            get_render_queue_status as get_status_func,
        )

        return get_status_func(resolve)

    @mcp.tool()
    def clear_render_queue() -> Dict[str, Any]:
        """Clear all jobs from the render queue."""
        from src.api.delivery_operations import clear_render_queue as clear_queue_func

        return clear_queue_func(resolve)

    @mcp.tool()
    def link_proxy_media(clip_name: str, proxy_file_path: str) -> str:
        """Link a proxy media file to a clip."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return "Error: Failed to get Media Pool"

        clips = get_all_media_pool_clips(media_pool)
        target_clip = None

        for clip in clips:
            if clip.GetName() == clip_name:
                target_clip = clip
                break

        if not target_clip:
            return f"Error: Clip '{clip_name}' not found in Media Pool"

        if not os.path.exists(proxy_file_path):
            return f"Error: Proxy file '{proxy_file_path}' does not exist"

        try:
            result = target_clip.LinkProxyMedia(proxy_file_path)
            if result:
                return f"Successfully linked proxy media '{proxy_file_path}' to clip '{clip_name}'"
            else:
                return f"Failed to link proxy media to clip '{clip_name}'"
        except Exception as e:
            return f"Error linking proxy media: {str(e)}"

    @mcp.tool()
    def unlink_proxy_media(clip_name: str) -> str:
        """Unlink proxy media from a clip."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return "Error: Failed to get Media Pool"

        clips = get_all_media_pool_clips(media_pool)
        target_clip = None

        for clip in clips:
            if clip.GetName() == clip_name:
                target_clip = clip
                break

        if not target_clip:
            return f"Error: Clip '{clip_name}' not found in Media Pool"

        try:
            result = target_clip.UnlinkProxyMedia()
            if result:
                return f"Successfully unlinked proxy media from clip '{clip_name}'"
            else:
                return f"Failed to unlink proxy media from clip '{clip_name}'"
        except Exception as e:
            return f"Error unlinking proxy media: {str(e)}"

    @mcp.tool()
    def replace_clip(clip_name: str, replacement_path: str) -> str:
        """Replace a clip with another media file."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return "Error: Failed to get Media Pool"

        clips = get_all_media_pool_clips(media_pool)
        target_clip = None

        for clip in clips:
            if clip.GetName() == clip_name:
                target_clip = clip
                break

        if not target_clip:
            return f"Error: Clip '{clip_name}' not found in Media Pool"

        if not os.path.exists(replacement_path):
            return f"Error: Replacement file '{replacement_path}' does not exist"

        try:
            result = target_clip.ReplaceClip(replacement_path)
            if result:
                return f"Successfully replaced clip '{clip_name}' with '{replacement_path}'"
            else:
                return f"Failed to replace clip '{clip_name}'"
        except Exception as e:
            return f"Error replacing clip: {str(e)}"

    @mcp.tool()
    def transcribe_audio(clip_name: str, language: str = "en-US") -> str:
        """Transcribe audio for a clip."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return "Error: Failed to get Media Pool"

        clips = get_all_media_pool_clips(media_pool)
        target_clip = None

        for clip in clips:
            if clip.GetName() == clip_name:
                target_clip = clip
                break

        if not target_clip:
            return f"Error: Clip '{clip_name}' not found in Media Pool"

        try:
            result = target_clip.TranscribeAudio(language)
            if result:
                return f"Successfully started audio transcription for clip '{clip_name}' in language '{language}'"
            else:
                return f"Failed to start audio transcription for clip '{clip_name}'"
        except Exception as e:
            return f"Error during audio transcription: {str(e)}"

    @mcp.tool()
    def clear_transcription(clip_name: str) -> str:
        """Clear audio transcription for a clip."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return "Error: Failed to get Media Pool"

        clips = get_all_media_pool_clips(media_pool)
        target_clip = None

        for clip in clips:
            if clip.GetName() == clip_name:
                target_clip = clip
                break

        if not target_clip:
            return f"Error: Clip '{clip_name}' not found in Media Pool"

        try:
            result = target_clip.ClearTranscription()
            if result:
                return (
                    f"Successfully cleared audio transcription for clip '{clip_name}'"
                )
            else:
                return f"Failed to clear audio transcription for clip '{clip_name}'"
        except Exception as e:
            return f"Error clearing audio transcription: {str(e)}"

    logger.info("Registered delivery tools")
