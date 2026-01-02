"""Tests for keyboard transitions module."""

from unittest.mock import patch


class TestTransitionAdd:
    """Tests for transition_add function."""

    def test_sends_ctrl_t(self):
        """Should send Ctrl+T for add default transition."""
        from src.utils.keyboard.transitions import transition_add

        with patch("src.utils.keyboard.transitions.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            transition_add()
            mock_send.assert_called_once_with("^t", "Add Transition (Ctrl+T)")


class TestTransitionAddVideo:
    """Tests for transition_add_video function."""

    def test_sends_alt_t(self):
        """Should send Alt+T for add video transition."""
        from src.utils.keyboard.transitions import transition_add_video

        with patch("src.utils.keyboard.transitions.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            transition_add_video()
            mock_send.assert_called_once_with("%t", "Add Video Transition (Alt+T)")


class TestTransitionAddAudio:
    """Tests for transition_add_audio function."""

    def test_sends_shift_t(self):
        """Should send Shift+T for add audio transition."""
        from src.utils.keyboard.transitions import transition_add_audio

        with patch("src.utils.keyboard.transitions.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            transition_add_audio()
            mock_send.assert_called_once_with("+t", "Add Audio Transition (Shift+T)")
