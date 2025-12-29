"""
Database and Folder Navigation Operations for DaVinci Resolve MCP Server.

Implements ProjectManager folder navigation and database management APIs.
"""

from typing import List, Dict, Any


def get_current_database(resolve) -> Dict[str, Any]:
    """Get information about the current database connection."""
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    try:
        db_info = project_manager.GetCurrentDatabase()
        return db_info if db_info else {"error": "Failed to get database info"}
    except Exception as e:
        return {"error": f"Error getting database info: {str(e)}"}


def get_database_list(resolve) -> List[Dict[str, Any]]:
    """Get list of all databases added to Resolve."""
    if resolve is None:
        return [{"error": "Not connected to DaVinci Resolve"}]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return [{"error": "Failed to get Project Manager"}]

    try:
        db_list = project_manager.GetDatabaseList()
        return db_list if db_list else []
    except Exception as e:
        return [{"error": f"Error getting database list: {str(e)}"}]


def set_current_database(
    resolve, db_type: str, db_name: str, ip_address: str = "127.0.0.1"
) -> str:
    """Switch to a different database.

    Args:
        db_type: 'Disk' or 'PostgreSQL'
        db_name: Database name
        ip_address: IP address for PostgreSQL (default: 127.0.0.1)
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    if db_type not in ["Disk", "PostgreSQL"]:
        return "Error: db_type must be 'Disk' or 'PostgreSQL'"

    try:
        db_info = {"DbType": db_type, "DbName": db_name}
        if db_type == "PostgreSQL":
            db_info["IpAddress"] = ip_address

        result = project_manager.SetCurrentDatabase(db_info)
        if result:
            return f"Successfully switched to database '{db_name}'"
        else:
            return f"Failed to switch to database '{db_name}'"
    except Exception as e:
        return f"Error switching database: {str(e)}"


def get_current_folder(resolve) -> str:
    """Get the current folder name in the project manager."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        folder_name = project_manager.GetCurrentFolder()
        return folder_name if folder_name else "Root"
    except Exception as e:
        return f"Error: {str(e)}"


def get_folder_list_in_current_folder(resolve) -> List[str]:
    """Get list of folder names in the current folder."""
    if resolve is None:
        return ["Error: Not connected to DaVinci Resolve"]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return ["Error: Failed to get Project Manager"]

    try:
        folders = project_manager.GetFolderListInCurrentFolder()
        return folders if folders else []
    except Exception as e:
        return [f"Error: {str(e)}"]


def goto_root_folder(resolve) -> str:
    """Navigate to the root folder in the database."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.GotoRootFolder()
        if result:
            return "Successfully navigated to root folder"
        else:
            return "Failed to navigate to root folder"
    except Exception as e:
        return f"Error: {str(e)}"


def goto_parent_folder(resolve) -> str:
    """Navigate to the parent folder of the current folder."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.GotoParentFolder()
        if result:
            return "Successfully navigated to parent folder"
        else:
            return "Failed to navigate to parent folder (may already be at root)"
    except Exception as e:
        return f"Error: {str(e)}"


def open_folder(resolve, folder_name: str) -> str:
    """Open a folder by name.

    Args:
        folder_name: Name of the folder to open
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not folder_name:
        return "Error: Folder name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.OpenFolder(folder_name)
        if result:
            return f"Successfully opened folder '{folder_name}'"
        else:
            return f"Failed to open folder '{folder_name}' (folder may not exist)"
    except Exception as e:
        return f"Error: {str(e)}"


def create_folder(resolve, folder_name: str) -> str:
    """Create a new folder in the current location.

    Args:
        folder_name: Name for the new folder
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not folder_name:
        return "Error: Folder name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.CreateFolder(folder_name)
        if result:
            return f"Successfully created folder '{folder_name}'"
        else:
            return f"Failed to create folder '{folder_name}' (name may already exist)"
    except Exception as e:
        return f"Error: {str(e)}"


def delete_folder(resolve, folder_name: str) -> str:
    """Delete a folder by name.

    Args:
        folder_name: Name of the folder to delete
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not folder_name:
        return "Error: Folder name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.DeleteFolder(folder_name)
        if result:
            return f"Successfully deleted folder '{folder_name}'"
        else:
            return f"Failed to delete folder '{folder_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def import_project(resolve, file_path: str, project_name: str = None) -> str:
    """Import a project from file.

    Args:
        file_path: Path to the project file (.drp)
        project_name: Optional name for the imported project
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not file_path:
        return "Error: File path cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        if project_name:
            result = project_manager.ImportProject(file_path, project_name)
        else:
            result = project_manager.ImportProject(file_path)

        if result:
            return f"Successfully imported project from '{file_path}'"
        else:
            return f"Failed to import project from '{file_path}'"
    except Exception as e:
        return f"Error: {str(e)}"


def export_project(
    resolve, project_name: str, file_path: str, with_stills_and_luts: bool = True
) -> str:
    """Export a project to file.

    Args:
        project_name: Name of the project to export
        file_path: Path to save the project file
        with_stills_and_luts: Include stills and LUTs (default: True)
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not project_name or not file_path:
        return "Error: Project name and file path cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.ExportProject(
            project_name, file_path, with_stills_and_luts
        )
        if result:
            return f"Successfully exported project '{project_name}' to '{file_path}'"
        else:
            return f"Failed to export project '{project_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def archive_project(
    resolve,
    project_name: str,
    file_path: str,
    archive_src_media: bool = True,
    archive_render_cache: bool = True,
    archive_proxy_media: bool = False,
) -> str:
    """Archive a project with media.

    Args:
        project_name: Name of the project to archive
        file_path: Path to save the archive
        archive_src_media: Include source media (default: True)
        archive_render_cache: Include render cache (default: True)
        archive_proxy_media: Include proxy media (default: False)
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not project_name or not file_path:
        return "Error: Project name and file path cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.ArchiveProject(
            project_name,
            file_path,
            archive_src_media,
            archive_render_cache,
            archive_proxy_media,
        )
        if result:
            return f"Successfully archived project '{project_name}' to '{file_path}'"
        else:
            return f"Failed to archive project '{project_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def restore_project(resolve, file_path: str, project_name: str = None) -> str:
    """Restore a project from archive.

    Args:
        file_path: Path to the archive file
        project_name: Optional name for the restored project
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not file_path:
        return "Error: File path cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        if project_name:
            result = project_manager.RestoreProject(file_path, project_name)
        else:
            result = project_manager.RestoreProject(file_path)

        if result:
            return f"Successfully restored project from '{file_path}'"
        else:
            return f"Failed to restore project from '{file_path}'"
    except Exception as e:
        return f"Error: {str(e)}"


def delete_project(resolve, project_name: str) -> str:
    """Delete a project from the current folder.

    Args:
        project_name: Name of the project to delete
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not project_name:
        return "Error: Project name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    try:
        result = project_manager.DeleteProject(project_name)
        if result:
            return f"Successfully deleted project '{project_name}'"
        else:
            return (
                f"Failed to delete project '{project_name}' (may be currently loaded)"
            )
    except Exception as e:
        return f"Error: {str(e)}"
