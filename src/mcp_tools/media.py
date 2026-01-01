#!/usr/bin/env python3
"""
DaVinci Resolve MCP Media Tools
Media pool and clip operations
"""

from typing import List, Dict, Any


def register_media_tools(mcp, resolve, logger):
    """Register media pool MCP tools and resources."""

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

    @mcp.resource("resolve://media-pool-clips")
    def list_media_pool_clips() -> List[Dict[str, Any]]:
        """List all clips in the root folder of the media pool."""
        if resolve is None:
            return [{"error": "Not connected to DaVinci Resolve"}]

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return [{"error": "Failed to get Project Manager"}]

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return [{"error": "No project currently open"}]

        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return [{"error": "Failed to get Media Pool"}]

        root_folder = media_pool.GetRootFolder()
        if not root_folder:
            return [{"error": "Failed to get root folder"}]

        clips = root_folder.GetClipList()
        if not clips:
            return [{"info": "No clips found in the root folder"}]

        result = []
        for clip in clips:
            result.append(
                {
                    "name": clip.GetName(),
                    "duration": clip.GetDuration(),
                    "fps": clip.GetClipProperty("FPS"),
                }
            )

        return result

    @mcp.tool()
    def import_media(file_path: str) -> str:
        """Import media file into the current project's media pool."""
        from src.api.media_operations import import_media as import_media_func

        return import_media_func(resolve, file_path)

    @mcp.tool()
    def delete_media(clip_name: str) -> str:
        """Delete a media clip from the media pool by name."""
        from src.api.media_operations import delete_media as delete_media_func

        return delete_media_func(resolve, clip_name)

    @mcp.tool()
    def move_media_to_bin(clip_name: str, bin_name: str) -> str:
        """Move a media clip to a specific bin in the media pool."""
        from src.api.media_operations import move_media_to_bin as move_media_func

        return move_media_func(resolve, clip_name, bin_name)

    @mcp.tool()
    def auto_sync_audio(
        clip_names: List[str],
        sync_method: str = "waveform",
        append_mode: bool = False,
        target_bin: str = None,
    ) -> str:
        """Sync audio between clips with customizable settings."""
        from src.api.media_operations import auto_sync_audio as auto_sync_audio_func

        return auto_sync_audio_func(
            resolve, clip_names, sync_method, append_mode, target_bin
        )

    @mcp.tool()
    def unlink_clips(clip_names: List[str]) -> str:
        """Unlink specified clips, disconnecting them from their media files."""
        from src.api.media_operations import unlink_clips as unlink_clips_func

        return unlink_clips_func(resolve, clip_names)

    @mcp.tool()
    def relink_clips(
        clip_names: List[str],
        media_paths: List[str] = None,
        folder_path: str = None,
        recursive: bool = False,
    ) -> str:
        """Relink specified clips to their media files."""
        from src.api.media_operations import relink_clips as relink_clips_func

        return relink_clips_func(
            resolve, clip_names, media_paths, folder_path, recursive
        )

    @mcp.tool()
    def create_sub_clip(
        clip_name: str,
        start_frame: int,
        end_frame: int,
        sub_clip_name: str = None,
        bin_name: str = None,
    ) -> str:
        """Create a subclip from the specified clip using in and out points."""
        from src.api.media_operations import create_sub_clip as create_sub_clip_func

        return create_sub_clip_func(
            resolve, clip_name, start_frame, end_frame, sub_clip_name, bin_name
        )

    @mcp.tool()
    def create_bin(name: str) -> str:
        """Create a new bin/folder in the media pool."""
        from src.api.media_operations import create_bin as create_bin_func

        return create_bin_func(resolve, name)

    @mcp.resource("resolve://media-pool-bins")
    def list_media_pool_bins() -> List[Dict[str, Any]]:
        """List all bins/folders in the media pool."""
        from src.api.media_operations import list_bins as list_bins_func

        return list_bins_func(resolve)

    @mcp.resource("resolve://media-pool-bin/{bin_name}")
    def get_media_pool_bin_contents(bin_name: str) -> List[Dict[str, Any]]:
        """Get contents of a specific bin/folder in the media pool."""
        from src.api.media_operations import get_bin_contents as get_bin_contents_func

        return get_bin_contents_func(resolve, bin_name)

    @mcp.resource("resolve://timeline-clips")
    def list_timeline_clips() -> List[Dict[str, Any]]:
        """List all clips in the current timeline."""
        if resolve is None:
            return [{"error": "Not connected to DaVinci Resolve"}]

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return [{"error": "Failed to get Project Manager"}]

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return [{"error": "No project currently open"}]

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return [{"error": "No timeline currently active"}]

        try:
            video_track_count = current_timeline.GetTrackCount("video")
            audio_track_count = current_timeline.GetTrackCount("audio")

            clips = []

            for track_index in range(1, video_track_count + 1):
                track_items = current_timeline.GetItemListInTrack("video", track_index)
                if track_items:
                    for item in track_items:
                        clips.append(
                            {
                                "name": item.GetName(),
                                "type": "video",
                                "track": track_index,
                                "start_frame": item.GetStart(),
                                "end_frame": item.GetEnd(),
                                "duration": item.GetDuration(),
                            }
                        )

            for track_index in range(1, audio_track_count + 1):
                track_items = current_timeline.GetItemListInTrack("audio", track_index)
                if track_items:
                    for item in track_items:
                        clips.append(
                            {
                                "name": item.GetName(),
                                "type": "audio",
                                "track": track_index,
                                "start_frame": item.GetStart(),
                                "end_frame": item.GetEnd(),
                                "duration": item.GetDuration(),
                            }
                        )

            if not clips:
                return [{"info": "No clips found in the current timeline"}]

            return clips
        except Exception as e:
            return [{"error": f"Error listing timeline clips: {str(e)}"}]

    @mcp.tool()
    def add_clip_to_timeline(clip_name: str, timeline_name: str = None) -> str:
        """Add a media pool clip to the timeline."""
        from src.api.media_operations import add_clip_to_timeline as add_clip_func

        return add_clip_func(resolve, clip_name, timeline_name)

    logger.info("Registered media tools")
