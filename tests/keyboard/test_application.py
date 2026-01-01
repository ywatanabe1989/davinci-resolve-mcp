"""Tests for keyboard application control module."""

from unittest.mock import patch


class TestAppSaveProject:
    """Tests for app_save_project function."""

    def test_sends_ctrl_s(self):
        """Should send Ctrl+S for save project."""
        from src.utils.keyboard.application import app_save_project

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_save_project()
            mock_send.assert_called_once_with("^s", "Save Project (Ctrl+S)")


class TestAppImportMedia:
    """Tests for app_import_media function."""

    def test_sends_ctrl_i(self):
        """Should send Ctrl+I for import media."""
        from src.utils.keyboard.application import app_import_media

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_import_media()
            mock_send.assert_called_once_with("^i", "Import Media (Ctrl+I)")


class TestAppExportProject:
    """Tests for app_export_project function."""

    def test_sends_ctrl_e(self):
        """Should send Ctrl+E for export project."""
        from src.utils.keyboard.application import app_export_project

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_export_project()
            mock_send.assert_called_once_with("^e", "Export Project (Ctrl+E)")


class TestAppNewTimeline:
    """Tests for app_new_timeline function."""

    def test_sends_ctrl_n(self):
        """Should send Ctrl+N for new timeline."""
        from src.utils.keyboard.application import app_new_timeline

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_new_timeline()
            mock_send.assert_called_once_with("^n", "New Timeline (Ctrl+N)")


class TestAppNewBin:
    """Tests for app_new_bin function."""

    def test_sends_ctrl_shift_n(self):
        """Should send Ctrl+Shift+N for new bin."""
        from src.utils.keyboard.application import app_new_bin

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_new_bin()
            mock_send.assert_called_once_with("^+n", "New Bin (Ctrl+Shift+N)")


class TestAppProjectSettings:
    """Tests for app_project_settings function."""

    def test_sends_shift_9(self):
        """Should send Shift+9 for project settings."""
        from src.utils.keyboard.application import app_project_settings

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_project_settings()
            mock_send.assert_called_once_with("+9", "Project Settings (Shift+9)")


class TestAppPreferences:
    """Tests for app_preferences function."""

    def test_sends_ctrl_comma(self):
        """Should send Ctrl+, for preferences."""
        from src.utils.keyboard.application import app_preferences

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_preferences()
            mock_send.assert_called_once_with("^,", "Preferences (Ctrl+,)")


class TestAppKeyboardCustomization:
    """Tests for app_keyboard_customization function."""

    def test_sends_ctrl_alt_k(self):
        """Should send Ctrl+Alt+K for keyboard customization."""
        from src.utils.keyboard.application import app_keyboard_customization

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_keyboard_customization()
            mock_send.assert_called_once_with(
                "^%k", "Keyboard Customization (Ctrl+Alt+K)"
            )


class TestAppQuit:
    """Tests for app_quit function."""

    def test_sends_ctrl_q(self):
        """Should send Ctrl+Q for quit."""
        from src.utils.keyboard.application import app_quit

        with patch("src.utils.keyboard.application.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            app_quit()
            mock_send.assert_called_once_with("^q", "Quit (Ctrl+Q)")
