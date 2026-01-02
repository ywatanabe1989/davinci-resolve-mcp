"""Tests for keyboard selection operations module."""

from unittest.mock import patch


class TestSelectAll:
    """Tests for select_all function."""

    def test_sends_ctrl_a(self):
        """Should send Ctrl+A for select all."""
        from src.utils.keyboard.selection import select_all

        with patch("src.utils.keyboard.selection.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            select_all()
            mock_send.assert_called_once_with("^a", "Select All (Ctrl+A)")


class TestDeselectAll:
    """Tests for deselect_all function."""

    def test_sends_ctrl_shift_a(self):
        """Should send Ctrl+Shift+A for deselect all."""
        from src.utils.keyboard.selection import deselect_all

        with patch("src.utils.keyboard.selection.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            deselect_all()
            mock_send.assert_called_once_with("^+a", "Deselect All (Ctrl+Shift+A)")


class TestSelectClipsForward:
    """Tests for select_clips_forward function."""

    def test_sends_y_key(self):
        """Should send Y for select clips forward."""
        from src.utils.keyboard.selection import select_clips_forward

        with patch("src.utils.keyboard.selection.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            select_clips_forward()
            mock_send.assert_called_once_with("y", "Select Clips Forward (Y)")


class TestSelectClipsBackward:
    """Tests for select_clips_backward function."""

    def test_sends_ctrl_y(self):
        """Should send Ctrl+Y for select clips backward."""
        from src.utils.keyboard.selection import select_clips_backward

        with patch("src.utils.keyboard.selection.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            select_clips_backward()
            mock_send.assert_called_once_with("^y", "Select Clips Backward (Ctrl+Y)")


class TestSelectNearestEdit:
    """Tests for select_nearest_edit function."""

    def test_sends_v_key(self):
        """Should send V for select nearest edit."""
        from src.utils.keyboard.selection import select_nearest_edit

        with patch("src.utils.keyboard.selection.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            select_nearest_edit()
            mock_send.assert_called_once_with("v", "Select Nearest Edit (V)")
