"""Tests for gallery operations module."""

from unittest.mock import Mock


class TestGetGalleryStillAlbums:
    """Tests for get_gallery_still_albums function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error list when not connected."""
        from src.api.gallery_operations import get_gallery_still_albums

        result = get_gallery_still_albums(None)
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]

    def test_returns_error_when_no_project_open(self):
        """Should return error list when no project is open."""
        from src.api.gallery_operations import get_gallery_still_albums

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager

        result = get_gallery_still_albums(resolve)
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]

    def test_returns_albums_on_success(self):
        """Should return list of still albums."""
        from src.api.gallery_operations import get_gallery_still_albums

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        gallery = Mock()

        album1 = Mock()
        album1.GetStills.return_value = []
        album2 = Mock()
        album2.GetStills.return_value = []

        gallery.GetGalleryStillAlbums.return_value = [album1, album2]
        gallery.GetAlbumName.side_effect = ["Album1", "Album2"]
        project.GetGallery.return_value = gallery
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = get_gallery_still_albums(resolve)
        assert isinstance(result, list)
        assert len(result) == 2


class TestGetGalleryPowerGradeAlbums:
    """Tests for get_gallery_power_grade_albums function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error list when not connected."""
        from src.api.gallery_operations import get_gallery_power_grade_albums

        result = get_gallery_power_grade_albums(None)
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]


class TestCreateStillAlbum:
    """Tests for create_still_album function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.gallery_operations import create_still_album

        result = create_still_album(None)
        assert "Error" in result

    def test_creates_album_on_success(self):
        """Should create new still album."""
        from src.api.gallery_operations import create_still_album

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        gallery = Mock()
        new_album = Mock()

        gallery.CreateGalleryStillAlbum.return_value = new_album
        gallery.GetAlbumName.return_value = "NewAlbum"
        project.GetGallery.return_value = gallery
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = create_still_album(resolve)
        assert "created" in result.lower() or "success" in result.lower()


class TestGrabStill:
    """Tests for grab_still function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.gallery_operations import grab_still

        result = grab_still(None)
        assert "Error" in result

    def test_returns_error_when_no_timeline(self):
        """Should return error when no timeline active."""
        from src.api.gallery_operations import grab_still

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project.GetCurrentTimeline.return_value = None
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = grab_still(resolve)
        assert "Error" in result


class TestImportStills:
    """Tests for import_stills function."""

    def test_returns_error_for_empty_album_name(self):
        """Should return error for empty album name."""
        from src.api.gallery_operations import import_stills

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = import_stills(resolve, "", ["/path/to/image.jpg"])
        assert "Error" in result

    def test_returns_error_for_empty_file_paths(self):
        """Should return error for empty file paths."""
        from src.api.gallery_operations import import_stills

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = import_stills(resolve, "Album1", [])
        assert "Error" in result


class TestExportStills:
    """Tests for export_stills function."""

    def test_returns_error_for_empty_album_name(self):
        """Should return error for empty album name."""
        from src.api.gallery_operations import export_stills

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = export_stills(resolve, "", "/output/path")
        assert "Error" in result

    def test_returns_error_for_empty_folder_path(self):
        """Should return error for empty folder path."""
        from src.api.gallery_operations import export_stills

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = export_stills(resolve, "Album1", "")
        assert "Error" in result
