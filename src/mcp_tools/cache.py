#!/usr/bin/env python3
"""
DaVinci Resolve MCP Cache Tools
Cache and optimized media management
"""

import os
from typing import List, Dict, Any


def register_cache_tools(mcp, resolve, logger):
    """Register cache management MCP tools and resources."""

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

    def get_all_media_pool_folders(media_pool):
        """Get all folders from media pool recursively."""
        folders = []
        root_folder = media_pool.GetRootFolder()

        def process_folder(folder):
            folders.append(folder)
            sub_folders = folder.GetSubFolderList()
            for sub_folder in sub_folders:
                process_folder(sub_folder)

        process_folder(root_folder)
        return folders

    @mcp.resource("resolve://cache/settings")
    def get_cache_settings() -> Dict[str, Any]:
        """Get current cache settings from the project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        try:
            settings = {}
            cache_keys = [
                "CacheMode",
                "CacheClipMode",
                "OptimizedMediaMode",
                "ProxyMode",
                "ProxyQuality",
                "TimelineCacheMode",
                "LocalCachePath",
                "NetworkCachePath",
            ]

            for key in cache_keys:
                value = current_project.GetSetting(key)
                settings[key] = value

            return settings
        except Exception as e:
            return {"error": f"Failed to get cache settings: {str(e)}"}

    @mcp.tool()
    def set_cache_mode(mode: str) -> str:
        """Set cache mode for the current project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        valid_modes = ["auto", "on", "off"]
        mode = mode.lower()
        if mode not in valid_modes:
            return (
                f"Error: Invalid cache mode. Must be one of: {', '.join(valid_modes)}"
            )

        mode_map = {"auto": "0", "on": "1", "off": "2"}

        try:
            result = current_project.SetSetting("CacheMode", mode_map[mode])
            if result:
                return f"Successfully set cache mode to '{mode}'"
            else:
                return f"Failed to set cache mode to '{mode}'"
        except Exception as e:
            return f"Error setting cache mode: {str(e)}"

    @mcp.tool()
    def set_optimized_media_mode(mode: str) -> str:
        """Set optimized media mode for the current project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        valid_modes = ["auto", "on", "off"]
        mode = mode.lower()
        if mode not in valid_modes:
            return f"Error: Invalid optimized media mode. Must be one of: {', '.join(valid_modes)}"

        mode_map = {"auto": "0", "on": "1", "off": "2"}

        try:
            result = current_project.SetSetting("OptimizedMediaMode", mode_map[mode])
            if result:
                return f"Successfully set optimized media mode to '{mode}'"
            else:
                return f"Failed to set optimized media mode to '{mode}'"
        except Exception as e:
            return f"Error setting optimized media mode: {str(e)}"

    @mcp.tool()
    def set_proxy_mode(mode: str) -> str:
        """Set proxy media mode for the current project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        valid_modes = ["auto", "on", "off"]
        mode = mode.lower()
        if mode not in valid_modes:
            return (
                f"Error: Invalid proxy mode. Must be one of: {', '.join(valid_modes)}"
            )

        mode_map = {"auto": "0", "on": "1", "off": "2"}

        try:
            result = current_project.SetSetting("ProxyMode", mode_map[mode])
            if result:
                return f"Successfully set proxy mode to '{mode}'"
            else:
                return f"Failed to set proxy mode to '{mode}'"
        except Exception as e:
            return f"Error setting proxy mode: {str(e)}"

    @mcp.tool()
    def set_proxy_quality(quality: str) -> str:
        """Set proxy media quality for the current project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        valid_qualities = ["quarter", "half", "threeQuarter", "full"]
        if quality not in valid_qualities:
            return f"Error: Invalid proxy quality. Must be one of: {', '.join(valid_qualities)}"

        quality_map = {"quarter": "0", "half": "1", "threeQuarter": "2", "full": "3"}

        try:
            result = current_project.SetSetting("ProxyQuality", quality_map[quality])
            if result:
                return f"Successfully set proxy quality to '{quality}'"
            else:
                return f"Failed to set proxy quality to '{quality}'"
        except Exception as e:
            return f"Error setting proxy quality: {str(e)}"

    @mcp.tool()
    def set_cache_path(path_type: str, path: str) -> str:
        """Set cache file path for the current project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        valid_path_types = ["local", "network"]
        path_type = path_type.lower()
        if path_type not in valid_path_types:
            return f"Error: Invalid path type. Must be one of: {', '.join(valid_path_types)}"

        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist"

        setting_key = "LocalCachePath" if path_type == "local" else "NetworkCachePath"

        try:
            result = current_project.SetSetting(setting_key, path)
            if result:
                return f"Successfully set {path_type} cache path to '{path}'"
            else:
                return f"Failed to set {path_type} cache path to '{path}'"
        except Exception as e:
            return f"Error setting cache path: {str(e)}"

    @mcp.tool()
    def generate_optimized_media(clip_names: List[str] = None) -> str:
        """Generate optimized media for specified clips or all clips."""
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

        if clip_names:
            all_clips = get_all_media_pool_clips(media_pool)
            clips_to_process = []
            missing_clips = []

            for name in clip_names:
                found = False
                for clip in all_clips:
                    if clip.GetName() == name:
                        clips_to_process.append(clip)
                        found = True
                        break
                if not found:
                    missing_clips.append(name)

            if missing_clips:
                return f"Error: Could not find these clips: {', '.join(missing_clips)}"

            if not clips_to_process:
                return "Error: No valid clips found to process"
        else:
            clips_to_process = get_all_media_pool_clips(media_pool)

        try:
            media_pool.SetCurrentFolder(media_pool.GetRootFolder())
            for clip in clips_to_process:
                clip.AddFlag("Green")

            current_page = resolve.GetCurrentPage()
            if current_page != "media":
                resolve.OpenPage("media")

            media_pool.SetClipSelection([clip for clip in clips_to_process])
            result = current_project.GenerateOptimizedMedia()

            for clip in clips_to_process:
                clip.ClearFlags("Green")

            if result:
                return f"Successfully started optimized media generation for {len(clips_to_process)} clips"
            else:
                return "Failed to start optimized media generation"
        except Exception as e:
            try:
                for clip in clips_to_process:
                    clip.ClearFlags("Green")
            except Exception:
                pass
            return f"Error generating optimized media: {str(e)}"

    @mcp.tool()
    def delete_optimized_media(clip_names: List[str] = None) -> str:
        """Delete optimized media for specified clips or all clips."""
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

        if clip_names:
            all_clips = get_all_media_pool_clips(media_pool)
            clips_to_process = []
            missing_clips = []

            for name in clip_names:
                found = False
                for clip in all_clips:
                    if clip.GetName() == name:
                        clips_to_process.append(clip)
                        found = True
                        break
                if not found:
                    missing_clips.append(name)

            if missing_clips:
                return f"Error: Could not find these clips: {', '.join(missing_clips)}"

            if not clips_to_process:
                return "Error: No valid clips found to process"
        else:
            clips_to_process = get_all_media_pool_clips(media_pool)

        try:
            media_pool.SetCurrentFolder(media_pool.GetRootFolder())
            for clip in clips_to_process:
                clip.AddFlag("Green")

            current_page = resolve.GetCurrentPage()
            if current_page != "media":
                resolve.OpenPage("media")

            media_pool.SetClipSelection([clip for clip in clips_to_process])
            result = current_project.DeleteOptimizedMedia()

            for clip in clips_to_process:
                clip.ClearFlags("Green")

            if result:
                return f"Successfully deleted optimized media for {len(clips_to_process)} clips"
            else:
                return "Failed to delete optimized media"
        except Exception as e:
            try:
                for clip in clips_to_process:
                    clip.ClearFlags("Green")
            except Exception:
                pass
            return f"Error deleting optimized media: {str(e)}"

    @mcp.tool()
    def export_folder(
        folder_name: str, export_path: str, export_type: str = "DRB"
    ) -> str:
        """Export a folder to a DRB file or other format."""
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

        target_folder = None
        root_folder = media_pool.GetRootFolder()

        if folder_name.lower() == "root" or folder_name.lower() == "master":
            target_folder = root_folder
        else:
            folders = get_all_media_pool_folders(media_pool)
            for folder in folders:
                if folder.GetName() == folder_name:
                    target_folder = folder
                    break

        if not target_folder:
            return f"Error: Folder '{folder_name}' not found in Media Pool"

        export_dir = os.path.dirname(export_path)
        if not os.path.exists(export_dir) and export_dir:
            try:
                os.makedirs(export_dir)
            except Exception as e:
                return f"Error creating directory for export: {str(e)}"

        try:
            result = target_folder.Export(export_path)
            if result:
                return (
                    f"Successfully exported folder '{folder_name}' to '{export_path}'"
                )
            else:
                return f"Failed to export folder '{folder_name}'"
        except Exception as e:
            return f"Error exporting folder: {str(e)}"

    @mcp.tool()
    def transcribe_folder_audio(folder_name: str, language: str = "en-US") -> str:
        """Transcribe audio for all clips in a folder."""
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

        target_folder = None
        root_folder = media_pool.GetRootFolder()

        if folder_name.lower() == "root" or folder_name.lower() == "master":
            target_folder = root_folder
        else:
            folders = get_all_media_pool_folders(media_pool)
            for folder in folders:
                if folder.GetName() == folder_name:
                    target_folder = folder
                    break

        if not target_folder:
            return f"Error: Folder '{folder_name}' not found in Media Pool"

        try:
            result = target_folder.TranscribeAudio(language)
            if result:
                return f"Successfully started audio transcription for folder '{folder_name}' in language '{language}'"
            else:
                return f"Failed to start audio transcription for folder '{folder_name}'"
        except Exception as e:
            return f"Error during audio transcription: {str(e)}"

    @mcp.tool()
    def clear_folder_transcription(folder_name: str) -> str:
        """Clear audio transcription for all clips in a folder."""
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

        target_folder = None
        root_folder = media_pool.GetRootFolder()

        if folder_name.lower() == "root" or folder_name.lower() == "master":
            target_folder = root_folder
        else:
            folders = get_all_media_pool_folders(media_pool)
            for folder in folders:
                if folder.GetName() == folder_name:
                    target_folder = folder
                    break

        if not target_folder:
            return f"Error: Folder '{folder_name}' not found in Media Pool"

        try:
            result = target_folder.ClearTranscription()
            if result:
                return f"Successfully cleared audio transcription for folder '{folder_name}'"
            else:
                return f"Failed to clear audio transcription for folder '{folder_name}'"
        except Exception as e:
            return f"Error clearing audio transcription: {str(e)}"

    logger.info("Registered cache tools")
