#!/usr/bin/env python3
"""
DaVinci Resolve MCP Project Tools
Project management operations
"""

from typing import List, Dict, Any


def register_project_tools(mcp, resolve, logger):
    """Register project management MCP tools and resources."""

    @mcp.resource("resolve://projects")
    def list_projects() -> List[str]:
        """List all available projects in the current database."""
        if resolve is None:
            return ["Error: Not connected to DaVinci Resolve"]

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return ["Error: Failed to get Project Manager"]

        projects = project_manager.GetProjectListInCurrentFolder()
        return [p for p in projects if p]

    @mcp.resource("resolve://current-project")
    def get_current_project_name() -> str:
        """Get the name of the currently open project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "No project currently open"

        return current_project.GetName()

    @mcp.resource("resolve://project-settings")
    def get_project_settings() -> Dict[str, Any]:
        """Get all project settings from the current project."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        try:
            return current_project.GetSetting("")
        except Exception as e:
            return {"error": f"Failed to get project settings: {str(e)}"}

    @mcp.resource("resolve://project-setting/{setting_name}")
    def get_project_setting(setting_name: str) -> Dict[str, Any]:
        """Get a specific project setting by name."""
        if resolve is None:
            return {"error": "Not connected to DaVinci Resolve"}

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return {"error": "Failed to get Project Manager"}

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return {"error": "No project currently open"}

        try:
            value = current_project.GetSetting(setting_name)
            return {setting_name: value}
        except Exception as e:
            return {
                "error": f"Failed to get project setting '{setting_name}': {str(e)}"
            }

    @mcp.tool()
    def set_project_setting_tool(setting_name: str, setting_value: Any) -> str:
        """Set a project setting to the specified value."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        try:
            if not isinstance(setting_value, str):
                setting_value = str(setting_value)

            try:
                if setting_value.isdigit() or (
                    setting_value.startswith("-") and setting_value[1:].isdigit()
                ):
                    numeric_value = int(setting_value)
                    if current_project.SetSetting(setting_name, numeric_value):
                        return f"Successfully set project setting '{setting_name}' to {numeric_value}"
                elif (
                    "." in setting_value
                    and setting_value.replace(".", "", 1).replace("-", "", 1).isdigit()
                ):
                    numeric_value = float(setting_value)
                    if current_project.SetSetting(setting_name, numeric_value):
                        return f"Successfully set project setting '{setting_name}' to {numeric_value}"
            except (ValueError, TypeError):
                pass

            result = current_project.SetSetting(setting_name, setting_value)
            if result:
                return f"Successfully set project setting '{setting_name}' to '{setting_value}'"
            else:
                return f"Failed to set project setting '{setting_name}'"
        except Exception as e:
            return f"Error setting project setting: {str(e)}"

    @mcp.tool()
    def open_project(name: str) -> str:
        """Open a project by name."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        if not name:
            return "Error: Project name cannot be empty"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        projects = project_manager.GetProjectListInCurrentFolder()
        if name not in projects:
            return f"Error: Project '{name}' not found. Available projects: {', '.join(projects)}"

        result = project_manager.LoadProject(name)
        if result:
            return f"Successfully opened project '{name}'"
        else:
            return f"Failed to open project '{name}'"

    @mcp.tool()
    def create_project(name: str) -> str:
        """Create a new project with the given name."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        if not name:
            return "Error: Project name cannot be empty"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        projects = project_manager.GetProjectListInCurrentFolder()
        if name in projects:
            return f"Error: Project '{name}' already exists"

        result = project_manager.CreateProject(name)
        if result:
            return f"Successfully created project '{name}'"
        else:
            return f"Failed to create project '{name}'"

    @mcp.tool()
    def save_project() -> str:
        """Save the current project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        project_name = current_project.GetName()
        success = False

        try:
            if hasattr(current_project, "SaveProject"):
                result = current_project.SaveProject()
                if result:
                    success = True

            if not success and hasattr(project_manager, "SaveProject"):
                result = project_manager.SaveProject()
                if result:
                    success = True

            if success:
                return f"Successfully saved project '{project_name}'"
            else:
                return f"Automatic save likely in effect for project '{project_name}'"

        except Exception as e:
            return f"Error saving project: {str(e)}"

    @mcp.tool()
    def close_project() -> str:
        """Close the current project."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        project_name = current_project.GetName()

        try:
            result = project_manager.CloseProject(current_project)
            if result:
                return f"Successfully closed project '{project_name}'"
            else:
                return f"Failed to close project '{project_name}'"
        except Exception as e:
            return f"Error closing project: {str(e)}"

    logger.info("Registered project tools")
