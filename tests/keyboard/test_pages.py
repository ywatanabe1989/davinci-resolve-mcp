"""Tests for keyboard page navigation module."""

from unittest.mock import patch


class TestPageMedia:
    """Tests for page_media function."""

    def test_sends_shift_2(self):
        """Should send Shift+2 for Media page."""
        from src.utils.keyboard.pages import page_media

        with patch("src.utils.keyboard.pages.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            page_media()
            mock_send.assert_called_once_with("+2", "Media Page (Shift+2)")


class TestPageCut:
    """Tests for page_cut function."""

    def test_sends_shift_3(self):
        """Should send Shift+3 for Cut page."""
        from src.utils.keyboard.pages import page_cut

        with patch("src.utils.keyboard.pages.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            page_cut()
            mock_send.assert_called_once_with("+3", "Cut Page (Shift+3)")


class TestPageEdit:
    """Tests for page_edit function."""

    def test_sends_shift_4(self):
        """Should send Shift+4 for Edit page."""
        from src.utils.keyboard.pages import page_edit

        with patch("src.utils.keyboard.pages.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            page_edit()
            mock_send.assert_called_once_with("+4", "Edit Page (Shift+4)")


class TestPageFusion:
    """Tests for page_fusion function."""

    def test_sends_shift_5(self):
        """Should send Shift+5 for Fusion page."""
        from src.utils.keyboard.pages import page_fusion

        with patch("src.utils.keyboard.pages.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            page_fusion()
            mock_send.assert_called_once_with("+5", "Fusion Page (Shift+5)")


class TestPageColor:
    """Tests for page_color function."""

    def test_sends_shift_6(self):
        """Should send Shift+6 for Color page."""
        from src.utils.keyboard.pages import page_color

        with patch("src.utils.keyboard.pages.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            page_color()
            mock_send.assert_called_once_with("+6", "Color Page (Shift+6)")


class TestPageFairlight:
    """Tests for page_fairlight function."""

    def test_sends_shift_7(self):
        """Should send Shift+7 for Fairlight page."""
        from src.utils.keyboard.pages import page_fairlight

        with patch("src.utils.keyboard.pages.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            page_fairlight()
            mock_send.assert_called_once_with("+7", "Fairlight Page (Shift+7)")


class TestPageDeliver:
    """Tests for page_deliver function."""

    def test_sends_shift_8(self):
        """Should send Shift+8 for Deliver page."""
        from src.utils.keyboard.pages import page_deliver

        with patch("src.utils.keyboard.pages.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            page_deliver()
            mock_send.assert_called_once_with("+8", "Deliver Page (Shift+8)")
