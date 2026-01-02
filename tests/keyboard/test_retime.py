"""Tests for keyboard retime control module."""

from unittest.mock import patch


class TestRetimeControls:
    """Tests for retime_controls function."""

    def test_sends_ctrl_r(self):
        """Should send Ctrl+R for retime controls."""
        from src.utils.keyboard.retime import retime_controls

        with patch("src.utils.keyboard.retime.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            retime_controls()
            mock_send.assert_called_once_with("^r", "Retime Controls (Ctrl+R)")


class TestRetimeFreezeFrame:
    """Tests for retime_freeze_frame function."""

    def test_sends_shift_r(self):
        """Should send Shift+R for freeze frame."""
        from src.utils.keyboard.retime import retime_freeze_frame

        with patch("src.utils.keyboard.retime.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            retime_freeze_frame()
            mock_send.assert_called_once_with("+r", "Freeze Frame (Shift+R)")
