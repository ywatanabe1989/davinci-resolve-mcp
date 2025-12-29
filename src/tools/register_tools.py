"""
Tool Registration for DaVinci Resolve MCP Server.

This module registers all new tools with the MCP server.
"""

from typing import List, Dict, Any


def register_database_tools(mcp, resolve):
    """Register database and folder navigation tools."""
    from src.api.database_operations import (
        get_current_database as db_get_current,
        get_database_list as db_get_list,
        set_current_database as db_set_current,
        get_current_folder as db_get_folder,
        get_folder_list_in_current_folder as db_get_folder_list,
        goto_root_folder as db_goto_root,
        goto_parent_folder as db_goto_parent,
        open_folder as db_open_folder,
        create_folder as db_create_folder,
        delete_folder as db_delete_folder,
        import_project as db_import_project,
        export_project as db_export_project,
        archive_project as db_archive_project,
        restore_project as db_restore_project,
        delete_project as db_delete_project,
    )

    @mcp.resource("resolve://database/current")
    def get_current_database_resource() -> Dict[str, Any]:
        """Get information about the current database connection."""
        return db_get_current(resolve)

    @mcp.resource("resolve://database/list")
    def get_database_list_resource() -> List[Dict[str, Any]]:
        """Get list of all databases added to Resolve."""
        return db_get_list(resolve)

    @mcp.tool()
    def switch_database(db_type: str, db_name: str, ip_address: str = "127.0.0.1"):
        """Switch to a different database. db_type: 'Disk' or 'PostgreSQL'."""
        return db_set_current(resolve, db_type, db_name, ip_address)

    @mcp.resource("resolve://folder/current")
    def get_current_folder_resource() -> str:
        """Get the current folder name in the project manager."""
        return db_get_folder(resolve)

    @mcp.resource("resolve://folder/list")
    def get_folder_list_resource() -> List[str]:
        """Get list of folder names in the current folder."""
        return db_get_folder_list(resolve)

    @mcp.tool()
    def navigate_to_root_folder() -> str:
        """Navigate to the root folder in the database."""
        return db_goto_root(resolve)

    @mcp.tool()
    def navigate_to_parent_folder() -> str:
        """Navigate to the parent folder."""
        return db_goto_parent(resolve)

    @mcp.tool()
    def navigate_to_folder(folder_name: str) -> str:
        """Open a folder by name."""
        return db_open_folder(resolve, folder_name)

    @mcp.tool()
    def create_project_folder(folder_name: str) -> str:
        """Create a new folder in the current location."""
        return db_create_folder(resolve, folder_name)

    @mcp.tool()
    def delete_project_folder(folder_name: str) -> str:
        """Delete a folder by name."""
        return db_delete_folder(resolve, folder_name)

    @mcp.tool()
    def import_project_file(file_path: str, project_name: str = None) -> str:
        """Import a project from file (.drp)."""
        return db_import_project(resolve, file_path, project_name)

    @mcp.tool()
    def export_project_file(
        project_name: str, file_path: str, with_stills_and_luts: bool = True
    ) -> str:
        """Export a project to file."""
        return db_export_project(resolve, project_name, file_path, with_stills_and_luts)

    @mcp.tool()
    def archive_project_with_media(
        project_name: str,
        file_path: str,
        archive_src_media: bool = True,
        archive_render_cache: bool = True,
        archive_proxy_media: bool = False,
    ) -> str:
        """Archive a project with media."""
        return db_archive_project(
            resolve,
            project_name,
            file_path,
            archive_src_media,
            archive_render_cache,
            archive_proxy_media,
        )

    @mcp.tool()
    def restore_project_from_archive(file_path: str, project_name: str = None) -> str:
        """Restore a project from archive."""
        return db_restore_project(resolve, file_path, project_name)

    @mcp.tool()
    def delete_project_by_name(project_name: str) -> str:
        """Delete a project from the current folder."""
        return db_delete_project(resolve, project_name)


def register_media_storage_tools(mcp, resolve):
    """Register MediaStorage tools."""
    from src.api.media_storage_operations import (
        get_mounted_volumes as ms_get_volumes,
        get_subfolder_list as ms_get_subfolders,
        get_file_list as ms_get_files,
        reveal_in_storage as ms_reveal,
        add_items_to_media_pool as ms_add_items,
    )

    @mcp.resource("resolve://media-storage/volumes")
    def get_media_storage_volumes() -> List[str]:
        """Get list of mounted volumes in Media Storage."""
        return ms_get_volumes(resolve)

    @mcp.tool()
    def get_media_storage_subfolders(folder_path: str) -> List[str]:
        """Get list of subfolders in a Media Storage path."""
        return ms_get_subfolders(resolve, folder_path)

    @mcp.tool()
    def get_media_storage_files(folder_path: str) -> List[str]:
        """Get list of files in a Media Storage path."""
        return ms_get_files(resolve, folder_path)

    @mcp.tool()
    def reveal_path_in_media_storage(path: str) -> str:
        """Reveal a path in Resolve's Media Storage panel."""
        return ms_reveal(resolve, path)

    @mcp.tool()
    def add_files_to_media_pool(paths: List[str]) -> Dict[str, Any]:
        """Add files/folders from Media Storage to Media Pool."""
        return ms_add_items(resolve, paths)


def register_gallery_tools(mcp, resolve):
    """Register Gallery/Still tools."""
    from src.api.gallery_operations import (
        get_gallery_still_albums as gal_get_albums,
        get_gallery_power_grade_albums as gal_get_pg_albums,
        get_current_still_album as gal_get_current,
        create_still_album as gal_create_still,
        create_power_grade_album as gal_create_pg,
        set_album_name as gal_set_name,
        set_current_still_album as gal_set_current,
        grab_still as gal_grab_still,
        grab_all_stills as gal_grab_all,
        import_stills as gal_import,
        export_stills as gal_export,
    )

    @mcp.resource("resolve://gallery/still-albums")
    def get_still_albums() -> List[Dict[str, str]]:
        """Get list of gallery still albums."""
        return gal_get_albums(resolve)

    @mcp.resource("resolve://gallery/powergrade-albums")
    def get_powergrade_albums() -> List[Dict[str, str]]:
        """Get list of gallery PowerGrade albums."""
        return gal_get_pg_albums(resolve)

    @mcp.resource("resolve://gallery/current-album")
    def get_current_album() -> Dict[str, Any]:
        """Get the current still album."""
        return gal_get_current(resolve)

    @mcp.tool()
    def create_gallery_still_album() -> str:
        """Create a new gallery still album."""
        return gal_create_still(resolve)

    @mcp.tool()
    def create_gallery_powergrade_album() -> str:
        """Create a new gallery PowerGrade album."""
        return gal_create_pg(resolve)

    @mcp.tool()
    def rename_gallery_album(old_name: str, new_name: str) -> str:
        """Rename a gallery album."""
        return gal_set_name(resolve, old_name, new_name)

    @mcp.tool()
    def set_current_gallery_album(album_name: str) -> str:
        """Set the current still album by name."""
        return gal_set_current(resolve, album_name)

    @mcp.tool()
    def grab_current_still() -> str:
        """Grab a still from the current video clip."""
        return gal_grab_still(resolve)

    @mcp.tool()
    def grab_stills_from_all_clips(source: int = 1) -> Dict[str, Any]:
        """Grab stills from all clips. source: 1=first frame, 2=middle frame."""
        return gal_grab_all(resolve, source)

    @mcp.tool()
    def import_stills_to_album(album_name: str, file_paths: List[str]) -> str:
        """Import still images into a gallery album."""
        return gal_import(resolve, album_name, file_paths)

    @mcp.tool()
    def export_stills_from_album(
        album_name: str,
        folder_path: str,
        file_prefix: str = "still",
        format: str = "dpx",
    ) -> str:
        """Export stills from an album. Formats: dpx,cin,tif,jpg,png,ppm,bmp,xpm,drx."""
        return gal_export(resolve, album_name, folder_path, file_prefix, format)


def register_timeline_advanced_tools(mcp, resolve):
    """Register advanced timeline tools."""
    from src.api.timeline_advanced import (
        duplicate_timeline as tl_duplicate,
        create_compound_clip as tl_compound,
        create_fusion_clip as tl_fusion_clip,
        insert_generator as tl_insert_gen,
        insert_fusion_generator as tl_insert_fusion_gen,
        insert_fusion_composition as tl_insert_fusion_comp,
        insert_title as tl_insert_title,
        insert_fusion_title as tl_insert_fusion_title,
    )

    @mcp.tool()
    def duplicate_current_timeline(
        timeline_name: str = None, new_name: str = None
    ) -> str:
        """Duplicate a timeline."""
        return tl_duplicate(resolve, timeline_name, new_name)

    @mcp.tool()
    def create_compound_clip_from_items(
        clip_names: List[str],
        compound_name: str = None,
        start_timecode: str = None,
    ) -> str:
        """Create a compound clip from timeline items."""
        return tl_compound(resolve, clip_names, compound_name, start_timecode)

    @mcp.tool()
    def create_fusion_clip_from_items(clip_names: List[str]) -> str:
        """Create a Fusion clip from timeline items."""
        return tl_fusion_clip(resolve, clip_names)

    @mcp.tool()
    def insert_generator_to_timeline(generator_name: str) -> str:
        """Insert a generator into the timeline."""
        return tl_insert_gen(resolve, generator_name)

    @mcp.tool()
    def insert_fusion_generator_to_timeline(generator_name: str) -> str:
        """Insert a Fusion generator into the timeline."""
        return tl_insert_fusion_gen(resolve, generator_name)

    @mcp.tool()
    def insert_fusion_composition_to_timeline() -> str:
        """Insert a Fusion composition into the timeline."""
        return tl_insert_fusion_comp(resolve)

    @mcp.tool()
    def insert_title_to_timeline(title_name: str) -> str:
        """Insert a title into the timeline."""
        return tl_insert_title(resolve, title_name)

    @mcp.tool()
    def insert_fusion_title_to_timeline(title_name: str) -> str:
        """Insert a Fusion title into the timeline."""
        return tl_insert_fusion_title(resolve, title_name)


def register_timeline_export_tools(mcp, resolve):
    """Register timeline import/export tools."""
    from src.api.timeline_export import (
        import_timeline_from_file as tl_import,
        export_timeline as tl_export,
        get_timeline_timecode as tl_get_tc,
        set_timeline_timecode as tl_set_tc,
        detect_scene_cuts as tl_detect_cuts,
        create_subtitles_from_audio as tl_subtitles,
        export_current_frame_as_still as tl_export_frame,
    )

    @mcp.tool()
    def import_timeline(
        file_path: str,
        timeline_name: str = None,
        import_source_clips: bool = True,
        source_clips_path: str = None,
    ) -> str:
        """Import timeline from file (AAF/EDL/XML/FCPXML/DRT/ADL/OTIO)."""
        return tl_import(
            resolve, file_path, timeline_name, import_source_clips, source_clips_path
        )

    @mcp.tool()
    def export_current_timeline(
        file_path: str, export_type: str, export_subtype: str = "NONE"
    ) -> str:
        """Export current timeline. Types: AAF,DRT,EDL,FCP_7_XML,FCPXML_1_8/9/10,etc."""
        return tl_export(resolve, file_path, export_type, export_subtype)

    @mcp.resource("resolve://timeline/timecode")
    def get_playhead_timecode() -> str:
        """Get the current playhead timecode."""
        return tl_get_tc(resolve)

    @mcp.tool()
    def set_playhead_timecode(timecode: str) -> str:
        """Set the playhead to a specific timecode (e.g., '01:00:00:00')."""
        return tl_set_tc(resolve, timecode)

    @mcp.tool()
    def detect_timeline_scene_cuts() -> str:
        """Detect and create scene cuts along the timeline."""
        return tl_detect_cuts(resolve)

    @mcp.tool()
    def create_subtitles_from_timeline_audio(
        language: str = None, chars_per_line: int = None
    ) -> str:
        """Create subtitles from audio. Languages: auto,english,japanese,etc."""
        return tl_subtitles(resolve, language, chars_per_line)

    @mcp.tool()
    def export_current_frame(file_path: str) -> str:
        """Export the current frame as a still image."""
        return tl_export_frame(resolve, file_path)


def register_marker_tools(mcp, resolve):
    """Register marker management tools."""
    from src.api.marker_operations import (
        get_timeline_markers as mk_get_timeline,
        add_timeline_marker as mk_add_timeline,
        delete_timeline_marker_at_frame as mk_del_at_frame,
        delete_timeline_markers_by_color as mk_del_by_color,
        get_marker_by_custom_data as mk_get_by_data,
        update_marker_custom_data as mk_update_data,
        get_marker_custom_data as mk_get_data,
        delete_marker_by_custom_data as mk_del_by_data,
        get_clip_markers as mk_get_clip,
        add_clip_marker as mk_add_clip,
    )

    @mcp.resource("resolve://timeline/markers")
    def get_all_timeline_markers() -> Dict[str, Any]:
        """Get all markers from the current timeline."""
        return mk_get_timeline(resolve)

    @mcp.tool()
    def add_marker_to_timeline(
        frame: int,
        color: str = "Blue",
        name: str = "",
        note: str = "",
        duration: int = 1,
        custom_data: str = "",
    ) -> str:
        """Add a marker to the current timeline."""
        return mk_add_timeline(resolve, frame, color, name, note, duration, custom_data)

    @mcp.tool()
    def delete_timeline_marker(frame: int) -> str:
        """Delete a marker at the specified frame."""
        return mk_del_at_frame(resolve, frame)

    @mcp.tool()
    def delete_markers_by_color(color: str) -> str:
        """Delete all markers of the specified color. Use 'All' for all markers."""
        return mk_del_by_color(resolve, color)

    @mcp.tool()
    def find_marker_by_custom_data(custom_data: str) -> Dict[str, Any]:
        """Find a marker by its custom data."""
        return mk_get_by_data(resolve, custom_data)

    @mcp.tool()
    def update_marker_data(frame: int, custom_data: str) -> str:
        """Update the custom data of a marker at the specified frame."""
        return mk_update_data(resolve, frame, custom_data)

    @mcp.tool()
    def get_marker_data(frame: int) -> str:
        """Get the custom data of a marker at the specified frame."""
        return mk_get_data(resolve, frame)

    @mcp.tool()
    def delete_marker_with_custom_data(custom_data: str) -> str:
        """Delete the first marker with the specified custom data."""
        return mk_del_by_data(resolve, custom_data)

    @mcp.resource("resolve://clip/{clip_name}/markers")
    def get_media_pool_clip_markers(clip_name: str) -> Dict[str, Any]:
        """Get all markers from a media pool clip."""
        return mk_get_clip(resolve, clip_name)

    @mcp.tool()
    def add_marker_to_clip(
        clip_name: str,
        frame: int,
        color: str = "Blue",
        name: str = "",
        note: str = "",
        duration: int = 1,
        custom_data: str = "",
    ) -> str:
        """Add a marker to a media pool clip."""
        return mk_add_clip(
            resolve, clip_name, frame, color, name, note, duration, custom_data
        )


def register_capture_tools_wrapper(mcp):
    """Register capture tools (no resolve dependency)."""
    from src.tools.capture_tools import register_capture_tools

    register_capture_tools(mcp)


def register_all_new_tools(mcp, resolve):
    """Register all new tools with the MCP server."""
    register_database_tools(mcp, resolve)
    register_media_storage_tools(mcp, resolve)
    register_gallery_tools(mcp, resolve)
    register_timeline_advanced_tools(mcp, resolve)
    register_timeline_export_tools(mcp, resolve)
    register_marker_tools(mcp, resolve)
    register_capture_tools_wrapper(mcp)
