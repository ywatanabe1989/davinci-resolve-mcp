"""Tests for media storage operations module."""

from unittest.mock import Mock


class TestGetMountedVolumes:
    """Tests for get_mounted_volumes function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error list when not connected."""
        from src.api.media_storage_operations import get_mounted_volumes

        result = get_mounted_volumes(None)
        assert isinstance(result, list)
        assert len(result) == 1
        assert "Error" in result[0]

    def test_returns_error_when_media_storage_fails(self):
        """Should return error list when media storage unavailable."""
        from src.api.media_storage_operations import get_mounted_volumes

        resolve = Mock()
        resolve.GetMediaStorage.return_value = None

        result = get_mounted_volumes(resolve)
        assert isinstance(result, list)
        assert "Error" in result[0]

    def test_returns_volumes_on_success(self):
        """Should return list of mounted volumes."""
        from src.api.media_storage_operations import get_mounted_volumes

        resolve = Mock()
        media_storage = Mock()
        media_storage.GetMountedVolumeList.return_value = ["C:\\", "D:\\", "E:\\"]
        resolve.GetMediaStorage.return_value = media_storage

        result = get_mounted_volumes(resolve)
        assert isinstance(result, list)
        assert len(result) == 3
        assert "C:\\" in result


class TestGetSubfolderList:
    """Tests for get_subfolder_list function."""

    def test_returns_error_for_empty_path(self):
        """Should return error list for empty folder path."""
        from src.api.media_storage_operations import get_subfolder_list

        resolve = Mock()
        media_storage = Mock()
        resolve.GetMediaStorage.return_value = media_storage

        result = get_subfolder_list(resolve, "")
        assert isinstance(result, list)
        assert "Error" in result[0]

    def test_returns_subfolders_on_success(self):
        """Should return list of subfolders."""
        from src.api.media_storage_operations import get_subfolder_list

        resolve = Mock()
        media_storage = Mock()
        media_storage.GetSubFolderList.return_value = ["Folder1", "Folder2"]
        resolve.GetMediaStorage.return_value = media_storage

        result = get_subfolder_list(resolve, "C:\\Media")
        assert isinstance(result, list)
        assert len(result) == 2
        assert "Folder1" in result


class TestGetFileList:
    """Tests for get_file_list function."""

    def test_returns_error_for_empty_path(self):
        """Should return error list for empty folder path."""
        from src.api.media_storage_operations import get_file_list

        resolve = Mock()
        media_storage = Mock()
        resolve.GetMediaStorage.return_value = media_storage

        result = get_file_list(resolve, "")
        assert isinstance(result, list)
        assert "Error" in result[0]

    def test_returns_files_on_success(self):
        """Should return list of files."""
        from src.api.media_storage_operations import get_file_list

        resolve = Mock()
        media_storage = Mock()
        media_storage.GetFileList.return_value = ["video.mp4", "audio.wav"]
        resolve.GetMediaStorage.return_value = media_storage

        result = get_file_list(resolve, "C:\\Media")
        assert isinstance(result, list)
        assert len(result) == 2
        assert "video.mp4" in result


class TestRevealInStorage:
    """Tests for reveal_in_storage function."""

    def test_returns_error_for_empty_path(self):
        """Should return error for empty path."""
        from src.api.media_storage_operations import reveal_in_storage

        resolve = Mock()
        media_storage = Mock()
        resolve.GetMediaStorage.return_value = media_storage

        result = reveal_in_storage(resolve, "")
        assert "Error" in result

    def test_reveals_path_on_success(self):
        """Should reveal path in media storage."""
        from src.api.media_storage_operations import reveal_in_storage

        resolve = Mock()
        media_storage = Mock()
        media_storage.RevealInStorage.return_value = True
        resolve.GetMediaStorage.return_value = media_storage

        result = reveal_in_storage(resolve, "C:\\Media\\video.mp4")
        assert "Revealed" in result or "error" not in result.lower()


class TestAddItemsToMediaPool:
    """Tests for add_items_to_media_pool function."""

    def test_returns_error_for_empty_paths(self):
        """Should return error for empty paths list."""
        from src.api.media_storage_operations import add_items_to_media_pool

        resolve = Mock()
        media_storage = Mock()
        resolve.GetMediaStorage.return_value = media_storage

        result = add_items_to_media_pool(resolve, [])
        assert "error" in result

    def test_adds_items_on_success(self):
        """Should add items to media pool."""
        from src.api.media_storage_operations import add_items_to_media_pool

        resolve = Mock()
        media_storage = Mock()
        mock_clips = [Mock(), Mock()]
        media_storage.AddItemListToMediaPool.return_value = mock_clips
        resolve.GetMediaStorage.return_value = media_storage

        result = add_items_to_media_pool(resolve, ["C:\\video1.mp4", "C:\\video2.mp4"])
        assert "clips_added" in result
        assert result["clips_added"] == 2
