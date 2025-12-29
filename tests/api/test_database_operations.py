"""Tests for database operations module."""

from unittest.mock import Mock


class TestGetCurrentDatabase:
    """Tests for get_current_database function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected to Resolve."""
        from src.api.database_operations import get_current_database

        result = get_current_database(None)
        assert "error" in result
        assert "Not connected" in result["error"]

    def test_returns_error_when_project_manager_fails(self):
        """Should return error when project manager fails."""
        from src.api.database_operations import get_current_database

        resolve = Mock()
        resolve.GetProjectManager.return_value = None

        result = get_current_database(resolve)
        assert "error" in result
        assert "Project Manager" in result["error"]

    def test_returns_database_info_on_success(self):
        """Should return database info on success."""
        from src.api.database_operations import get_current_database

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentDatabase.return_value = {
            "DbType": "Disk",
            "DbName": "Local",
        }
        resolve.GetProjectManager.return_value = project_manager

        result = get_current_database(resolve)
        # Returns the db_info dict directly
        assert "DbType" in result
        assert result["DbType"] == "Disk"


class TestGetDatabaseList:
    """Tests for get_database_list function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error list when not connected."""
        from src.api.database_operations import get_database_list

        result = get_database_list(None)
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]

    def test_returns_database_list_on_success(self):
        """Should return list of databases."""
        from src.api.database_operations import get_database_list

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetDatabaseList.return_value = [
            {"DbType": "Disk", "DbName": "Local"},
            {"DbType": "PostgreSQL", "DbName": "Remote"},
        ]
        resolve.GetProjectManager.return_value = project_manager

        result = get_database_list(resolve)
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["DbType"] == "Disk"


class TestSetCurrentDatabase:
    """Tests for set_current_database function."""

    def test_returns_error_for_invalid_db_type(self):
        """Should return error for invalid database type."""
        from src.api.database_operations import set_current_database

        resolve = Mock()
        project_manager = Mock()
        resolve.GetProjectManager.return_value = project_manager

        result = set_current_database(resolve, "InvalidType", "test")
        assert "Error" in result
        assert "Disk" in result or "PostgreSQL" in result

    def test_switches_database_on_success(self):
        """Should switch database successfully."""
        from src.api.database_operations import set_current_database

        resolve = Mock()
        project_manager = Mock()
        project_manager.SetCurrentDatabase.return_value = True
        resolve.GetProjectManager.return_value = project_manager

        result = set_current_database(resolve, "Disk", "Local")
        assert "switched" in result.lower() or "success" in result.lower()


class TestFolderNavigation:
    """Tests for folder navigation functions."""

    def test_goto_root_folder(self):
        """Should navigate to root folder."""
        from src.api.database_operations import goto_root_folder

        resolve = Mock()
        project_manager = Mock()
        project_manager.GotoRootFolder.return_value = True
        resolve.GetProjectManager.return_value = project_manager

        result = goto_root_folder(resolve)
        assert "Navigated" in result or "root" in result.lower()

    def test_goto_parent_folder(self):
        """Should navigate to parent folder."""
        from src.api.database_operations import goto_parent_folder

        resolve = Mock()
        project_manager = Mock()
        project_manager.GotoParentFolder.return_value = True
        resolve.GetProjectManager.return_value = project_manager

        result = goto_parent_folder(resolve)
        assert "Navigated" in result or "parent" in result.lower()

    def test_open_folder(self):
        """Should open specified folder."""
        from src.api.database_operations import open_folder

        resolve = Mock()
        project_manager = Mock()
        project_manager.OpenFolder.return_value = True
        resolve.GetProjectManager.return_value = project_manager

        result = open_folder(resolve, "TestFolder")
        assert "Opened" in result or "TestFolder" in result

    def test_create_folder(self):
        """Should create new folder."""
        from src.api.database_operations import create_folder

        resolve = Mock()
        project_manager = Mock()
        project_manager.CreateFolder.return_value = True
        resolve.GetProjectManager.return_value = project_manager

        result = create_folder(resolve, "NewFolder")
        assert "Created" in result or "NewFolder" in result

    def test_delete_folder(self):
        """Should delete folder."""
        from src.api.database_operations import delete_folder

        resolve = Mock()
        project_manager = Mock()
        project_manager.DeleteFolder.return_value = True
        resolve.GetProjectManager.return_value = project_manager

        result = delete_folder(resolve, "OldFolder")
        assert "Deleted" in result or "OldFolder" in result


class TestProjectImportExport:
    """Tests for project import/export functions."""

    def test_import_project_with_empty_path(self):
        """Should return error for empty file path."""
        from src.api.database_operations import import_project

        resolve = Mock()
        project_manager = Mock()
        resolve.GetProjectManager.return_value = project_manager

        result = import_project(resolve, "")
        assert "Error" in result

    def test_export_project_success(self):
        """Should export project successfully."""
        from src.api.database_operations import export_project

        resolve = Mock()
        project_manager = Mock()
        project_manager.ExportProject.return_value = True
        resolve.GetProjectManager.return_value = project_manager

        result = export_project(resolve, "MyProject", "/path/to/file.drp")
        assert "Exported" in result or "error" not in result.lower()
