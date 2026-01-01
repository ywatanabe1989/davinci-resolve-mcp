"""Tests for keyboard clip control module."""

from unittest.mock import patch


class TestClipEnableDisable:
    """Tests for clip_enable_disable function."""

    def test_sends_d_key(self):
        """Should send D for enable/disable clip."""
        from src.utils.keyboard.clips import clip_enable_disable

        with patch("src.utils.keyboard.clips.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            clip_enable_disable()
            mock_send.assert_called_once_with("d", "Enable/Disable Clip (D)")


class TestClipCreateSubclip:
    """Tests for clip_create_subclip function."""

    def test_sends_alt_b(self):
        """Should send Alt+B for create subclip."""
        from src.utils.keyboard.clips import clip_create_subclip

        with patch("src.utils.keyboard.clips.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            clip_create_subclip()
            mock_send.assert_called_once_with("%b", "Create Subclip (Alt+B)")


class TestClipAddFlag:
    """Tests for clip_add_flag function."""

    def test_sends_g_key(self):
        """Should send G for add flag."""
        from src.utils.keyboard.clips import clip_add_flag

        with patch("src.utils.keyboard.clips.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            clip_add_flag()
            mock_send.assert_called_once_with("g", "Add Flag (G)")


class TestClipChangeDuration:
    """Tests for clip_change_duration function."""

    def test_sends_ctrl_d(self):
        """Should send Ctrl+D for change clip duration."""
        from src.utils.keyboard.clips import clip_change_duration

        with patch("src.utils.keyboard.clips.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            clip_change_duration()
            mock_send.assert_called_once_with("^d", "Change Clip Duration (Ctrl+D)")
