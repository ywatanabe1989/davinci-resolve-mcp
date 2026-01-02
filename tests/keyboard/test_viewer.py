"""Tests for keyboard viewer control module."""

from unittest.mock import patch


class TestViewerToggleSourceTimeline:
    """Tests for viewer_toggle_source_timeline function."""

    def test_sends_q_key(self):
        """Should send Q for toggle source/timeline viewer."""
        from src.utils.keyboard.viewer import viewer_toggle_source_timeline

        with patch("src.utils.keyboard.viewer.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            viewer_toggle_source_timeline()
            mock_send.assert_called_once_with("q", "Toggle Source/Timeline (Q)")


class TestViewerMatchFrame:
    """Tests for viewer_match_frame function."""

    def test_sends_f_key(self):
        """Should send F for match frame."""
        from src.utils.keyboard.viewer import viewer_match_frame

        with patch("src.utils.keyboard.viewer.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            viewer_match_frame()
            mock_send.assert_called_once_with("f", "Match Frame (F)")
