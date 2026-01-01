"""Tests for keyboard marker operations module."""

from unittest.mock import patch


class TestMarkerAdd:
    """Tests for marker_add function."""

    def test_sends_m_key(self):
        """Should send M for add marker."""
        from src.utils.keyboard.markers import marker_add

        with patch("src.utils.keyboard.markers.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            marker_add()
            mock_send.assert_called_once_with("m", "Add Marker (M)")


class TestMarkerAddAndModify:
    """Tests for marker_add_and_modify function."""

    def test_sends_ctrl_m(self):
        """Should send Ctrl+M for add and modify marker."""
        from src.utils.keyboard.markers import marker_add_and_modify

        with patch("src.utils.keyboard.markers.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            marker_add_and_modify()
            mock_send.assert_called_once_with("^m", "Add/Modify Marker (Ctrl+M)")


class TestMarkerModify:
    """Tests for marker_modify function."""

    def test_sends_shift_m(self):
        """Should send Shift+M for modify marker."""
        from src.utils.keyboard.markers import marker_modify

        with patch("src.utils.keyboard.markers.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            marker_modify()
            mock_send.assert_called_once_with("+m", "Modify Marker (Shift+M)")


class TestMarkerDelete:
    """Tests for marker_delete function."""

    def test_sends_alt_m(self):
        """Should send Alt+M for delete marker."""
        from src.utils.keyboard.markers import marker_delete

        with patch("src.utils.keyboard.markers.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            marker_delete()
            mock_send.assert_called_once_with("%m", "Delete Marker (Alt+M)")


class TestMarkerGoToNext:
    """Tests for marker_go_to_next function."""

    def test_sends_shift_down(self):
        """Should send Shift+Down for next marker."""
        from src.utils.keyboard.markers import marker_go_to_next

        with patch("src.utils.keyboard.markers.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            marker_go_to_next()
            mock_send.assert_called_once_with("+{DOWN}", "Next Marker (Shift+Down)")


class TestMarkerGoToPrevious:
    """Tests for marker_go_to_previous function."""

    def test_sends_shift_up(self):
        """Should send Shift+Up for previous marker."""
        from src.utils.keyboard.markers import marker_go_to_previous

        with patch("src.utils.keyboard.markers.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            marker_go_to_previous()
            mock_send.assert_called_once_with("+{UP}", "Previous Marker (Shift+Up)")
