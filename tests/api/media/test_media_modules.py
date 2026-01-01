"""Tests for media operations submodules."""

from unittest.mock import Mock


class TestMediaModuleImports:
    """Tests that all media submodules can be imported."""

    def test_import_media_init(self):
        """Should import media package with all exports."""
        from src.api.media import (
            list_media_pool_clips,
            import_media,
            create_bin,
            list_bins,
            get_bin_contents,
            list_timeline_clips,
            add_clip_to_timeline,
            delete_media,
            move_media_to_bin,
            auto_sync_audio,
            unlink_clips,
            relink_clips,
        )

        assert callable(list_media_pool_clips)
        assert callable(import_media)
        assert callable(create_bin)
        assert callable(list_bins)
        assert callable(get_bin_contents)
        assert callable(list_timeline_clips)
        assert callable(add_clip_to_timeline)
        assert callable(delete_media)
        assert callable(move_media_to_bin)
        assert callable(auto_sync_audio)
        assert callable(unlink_clips)
        assert callable(relink_clips)

    def test_import_pool_module(self):
        """Should import pool module."""
        from src.api.media.pool import list_media_pool_clips, create_bin

        assert callable(list_media_pool_clips)
        assert callable(create_bin)

    def test_import_clips_module(self):
        """Should import clips module."""
        from src.api.media.clips import add_clip_to_timeline, delete_media

        assert callable(add_clip_to_timeline)
        assert callable(delete_media)

    def test_import_sync_module(self):
        """Should import sync module."""
        from src.api.media.sync import auto_sync_audio, unlink_clips

        assert callable(auto_sync_audio)
        assert callable(unlink_clips)


class TestListMediaPoolClips:
    """Tests for list_media_pool_clips function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.pool import list_media_pool_clips

        result = list_media_pool_clips(None)
        assert isinstance(result, list)
        assert "error" in result[0]

    def test_returns_error_when_no_project(self):
        """Should return error when no project open."""
        from src.api.media.pool import list_media_pool_clips

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager

        result = list_media_pool_clips(resolve)
        assert isinstance(result, list)
        assert "error" in result[0]


class TestImportMedia:
    """Tests for import_media function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.pool import import_media

        result = import_media(None, "/path/to/file.mp4")
        assert "error" in result.lower()


class TestCreateBin:
    """Tests for create_bin function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.pool import create_bin

        result = create_bin(None, "New Bin")
        assert "error" in result.lower()

    def test_returns_error_for_empty_bin_name(self):
        """Should return error for empty bin name."""
        from src.api.media.pool import create_bin

        resolve = Mock()
        result = create_bin(resolve, "")
        assert "error" in result.lower()


class TestAddClipToTimeline:
    """Tests for add_clip_to_timeline function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.clips import add_clip_to_timeline

        result = add_clip_to_timeline(None, "clip_name")
        assert "error" in result.lower()


class TestDeleteMedia:
    """Tests for delete_media function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.clips import delete_media

        result = delete_media(None, "clip_name")
        assert "error" in result.lower()


class TestAutoSyncAudio:
    """Tests for auto_sync_audio function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.sync import auto_sync_audio

        result = auto_sync_audio(None, ["clip1"])
        assert "error" in result.lower()


class TestUnlinkClips:
    """Tests for unlink_clips function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.sync import unlink_clips

        result = unlink_clips(None, ["clip_name"])
        assert "error" in result.lower()


class TestRelinkClips:
    """Tests for relink_clips function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.media.sync import relink_clips

        result = relink_clips(None, ["clip_name"])
        assert "error" in result.lower()
