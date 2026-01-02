"""Tests for keyboard view control module."""

from unittest.mock import patch


class TestViewZoomIn:
    """Tests for view_zoom_in function."""

    def test_sends_ctrl_equals(self):
        """Should send Ctrl+= for zoom in."""
        from src.utils.keyboard.view import view_zoom_in

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_zoom_in()
            mock_send.assert_called_once_with("^=", "Zoom In (Ctrl+=)")


class TestViewZoomOut:
    """Tests for view_zoom_out function."""

    def test_sends_ctrl_minus(self):
        """Should send Ctrl+- for zoom out."""
        from src.utils.keyboard.view import view_zoom_out

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_zoom_out()
            mock_send.assert_called_once_with("^-", "Zoom Out (Ctrl+-)")


class TestViewFitTimeline:
    """Tests for view_fit_timeline function."""

    def test_sends_shift_z(self):
        """Should send Shift+Z for fit timeline."""
        from src.utils.keyboard.view import view_fit_timeline

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_fit_timeline()
            mock_send.assert_called_once_with("+z", "Fit Timeline (Shift+Z)")


class TestViewFullscreenPreview:
    """Tests for view_fullscreen_preview function."""

    def test_sends_p_key(self):
        """Should send P for fullscreen preview."""
        from src.utils.keyboard.view import view_fullscreen_preview

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_fullscreen_preview()
            mock_send.assert_called_once_with("p", "Fullscreen Preview (P)")


class TestViewFullscreenViewer:
    """Tests for view_fullscreen_viewer function."""

    def test_sends_shift_f(self):
        """Should send Shift+F for fullscreen viewer."""
        from src.utils.keyboard.view import view_fullscreen_viewer

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_fullscreen_viewer()
            mock_send.assert_called_once_with("+f", "Fullscreen Viewer (Shift+F)")


class TestViewEnhancedViewer:
    """Tests for view_enhanced_viewer function."""

    def test_sends_alt_f(self):
        """Should send Alt+F for enhanced viewer."""
        from src.utils.keyboard.view import view_enhanced_viewer

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_enhanced_viewer()
            mock_send.assert_called_once_with("%f", "Enhanced Viewer (Alt+F)")


class TestViewCinemaViewer:
    """Tests for view_cinema_viewer function."""

    def test_sends_ctrl_f(self):
        """Should send Ctrl+F for cinema viewer."""
        from src.utils.keyboard.view import view_cinema_viewer

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_cinema_viewer()
            mock_send.assert_called_once_with("^f", "Cinema Viewer (Ctrl+F)")


class TestViewSplitScreen:
    """Tests for view_split_screen function."""

    def test_sends_ctrl_alt_w(self):
        """Should send Ctrl+Alt+W for split screen."""
        from src.utils.keyboard.view import view_split_screen

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_split_screen()
            mock_send.assert_called_once_with("^%w", "Split Screen (Ctrl+Alt+W)")


class TestViewVideoScopes:
    """Tests for view_video_scopes function."""

    def test_sends_ctrl_shift_w(self):
        """Should send Ctrl+Shift+W for video scopes."""
        from src.utils.keyboard.view import view_video_scopes

        with patch("src.utils.keyboard.view.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            view_video_scopes()
            mock_send.assert_called_once_with("^+w", "Video Scopes (Ctrl+Shift+W)")
