"""Tests for keyboard control core module."""

from unittest.mock import Mock, patch, mock_open


class TestIsWsl:
    """Tests for is_wsl function."""

    def test_returns_true_on_wsl(self):
        """Should return True when /proc/version contains 'microsoft'."""
        from src.utils.keyboard.core import is_wsl

        mock_content = "Linux version 5.10.0-microsoft-standard-WSL2"
        with patch("builtins.open", mock_open(read_data=mock_content)):
            assert is_wsl() is True

    def test_returns_true_on_wsl_case_insensitive(self):
        """Should return True regardless of case."""
        from src.utils.keyboard.core import is_wsl

        mock_content = "Linux version 5.10.0-MICROSOFT-standard-WSL2"
        with patch("builtins.open", mock_open(read_data=mock_content)):
            assert is_wsl() is True

    def test_returns_false_on_native_linux(self):
        """Should return False when /proc/version doesn't contain 'microsoft'."""
        from src.utils.keyboard.core import is_wsl

        mock_content = "Linux version 5.10.0-generic"
        with patch("builtins.open", mock_open(read_data=mock_content)):
            assert is_wsl() is False

    def test_returns_false_on_file_error(self):
        """Should return False when /proc/version cannot be read."""
        from src.utils.keyboard.core import is_wsl

        with patch("builtins.open", side_effect=FileNotFoundError):
            assert is_wsl() is False

    def test_returns_false_on_permission_error(self):
        """Should return False when /proc/version has no permissions."""
        from src.utils.keyboard.core import is_wsl

        with patch("builtins.open", side_effect=PermissionError):
            assert is_wsl() is False


class TestGetPlatformType:
    """Tests for get_platform_type function."""

    def test_returns_windows_on_windows(self):
        """Should return 'windows' on Windows platform."""
        from src.utils.keyboard.core import get_platform_type

        with patch("platform.system", return_value="Windows"):
            assert get_platform_type() == "windows"

    def test_returns_wsl_on_wsl(self):
        """Should return 'wsl' when running on WSL."""
        from src.utils.keyboard.core import get_platform_type

        with patch("platform.system", return_value="Linux"):
            with patch("src.utils.keyboard.core.is_wsl", return_value=True):
                assert get_platform_type() == "wsl"

    def test_returns_macos_on_darwin(self):
        """Should return 'macos' on macOS."""
        from src.utils.keyboard.core import get_platform_type

        with patch("platform.system", return_value="Darwin"):
            with patch("src.utils.keyboard.core.is_wsl", return_value=False):
                assert get_platform_type() == "macos"

    def test_returns_linux_on_native_linux(self):
        """Should return 'linux' on native Linux."""
        from src.utils.keyboard.core import get_platform_type

        with patch("platform.system", return_value="Linux"):
            with patch("src.utils.keyboard.core.is_wsl", return_value=False):
                assert get_platform_type() == "linux"

    def test_returns_unknown_for_unsupported(self):
        """Should return 'unknown' for unsupported platforms."""
        from src.utils.keyboard.core import get_platform_type

        with patch("platform.system", return_value="FreeBSD"):
            with patch("src.utils.keyboard.core.is_wsl", return_value=False):
                assert get_platform_type() == "unknown"


class TestSendKeyToResolve:
    """Tests for send_key_to_resolve function."""

    def test_returns_error_on_unsupported_platform(self):
        """Should return error when platform is not Windows/WSL."""
        from src.utils.keyboard.core import send_key_to_resolve

        with patch("src.utils.keyboard.core.get_platform_type", return_value="linux"):
            result = send_key_to_resolve(" ", "test")
            assert result["success"] is False
            assert "not supported" in result["error"]

    def test_returns_error_on_macos(self):
        """Should return error when running on macOS."""
        from src.utils.keyboard.core import send_key_to_resolve

        with patch("src.utils.keyboard.core.get_platform_type", return_value="macos"):
            result = send_key_to_resolve(" ", "test")
            assert result["success"] is False
            assert "macos" in result["error"]

    def test_calls_powershell_on_wsl(self):
        """Should call PowerShell on WSL platform."""
        from src.utils.keyboard.core import send_key_to_resolve

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout="SUCCESS: Sent key to Resolve")
                send_key_to_resolve(" ", "Play/Pause")

                mock_run.assert_called_once()
                call_args = mock_run.call_args
                assert "powershell.exe" in call_args[0][0]

    def test_returns_success_when_powershell_succeeds(self):
        """Should return success when PowerShell execution succeeds."""
        from src.utils.keyboard.core import send_key_to_resolve

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout="SUCCESS: Sent key to Resolve")
                result = send_key_to_resolve(" ", "Play/Pause")

                assert result["success"] is True
                assert "Play/Pause" in result["message"]

    def test_returns_error_when_resolve_not_found(self):
        """Should return error when Resolve window not found."""
        from src.utils.keyboard.core import send_key_to_resolve

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(
                    stdout="ERROR: DaVinci Resolve window not found"
                )
                result = send_key_to_resolve(" ", "Play/Pause")

                assert result["success"] is False
                assert "not found" in result["error"]

    def test_returns_error_on_timeout(self):
        """Should return error on PowerShell timeout."""
        from src.utils.keyboard.core import send_key_to_resolve
        import subprocess

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired("cmd", 10)
                result = send_key_to_resolve(" ", "Play/Pause")

                assert result["success"] is False
                assert "Timeout" in result["error"]

    def test_returns_error_on_exception(self):
        """Should return error on general exception."""
        from src.utils.keyboard.core import send_key_to_resolve

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = Exception("Connection failed")
                result = send_key_to_resolve(" ", "Play/Pause")

                assert result["success"] is False
                assert "Connection failed" in result["error"]

    def test_uses_key_in_description_when_not_provided(self):
        """Should use key in message when description not provided."""
        from src.utils.keyboard.core import send_key_to_resolve

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout="SUCCESS: Sent key to Resolve")
                result = send_key_to_resolve(" ")

                assert result["success"] is True
                assert "key ' '" in result["message"]


class TestSendCustomKey:
    """Tests for send_custom_key function."""

    def test_delegates_to_send_key_to_resolve(self):
        """Should delegate to send_key_to_resolve."""
        from src.utils.keyboard.core import send_custom_key

        with patch("src.utils.keyboard.core.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            result = send_custom_key("^s", "Save")

            mock_send.assert_called_once_with("^s", "Save")
            assert result["success"] is True

    def test_uses_default_description(self):
        """Should use 'custom key' as default description."""
        from src.utils.keyboard.core import send_custom_key

        with patch("src.utils.keyboard.core.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            send_custom_key("^s")

            mock_send.assert_called_once_with("^s", "custom key")


class TestIsResolveFocused:
    """Tests for is_resolve_focused function."""

    def test_returns_error_on_unsupported_platform(self):
        """Should return error on unsupported platform."""
        from src.utils.keyboard.core import is_resolve_focused

        with patch("src.utils.keyboard.core.get_platform_type", return_value="linux"):
            result = is_resolve_focused()
            assert result["focused"] is False
            assert "error" in result

    def test_returns_focused_true_when_resolve_active(self):
        """Should return focused=True when Resolve is the active window."""
        from src.utils.keyboard.core import is_resolve_focused

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout="FOCUSED:DaVinci Resolve Studio")
                result = is_resolve_focused()

                assert result["focused"] is True
                assert "DaVinci Resolve" in result["current_window"]

    def test_returns_focused_false_when_other_window_active(self):
        """Should return focused=False when another window is active."""
        from src.utils.keyboard.core import is_resolve_focused

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout="NOT_FOCUSED:Terminal")
                result = is_resolve_focused()

                assert result["focused"] is False
                assert "Terminal" in result["current_window"]

    def test_handles_exception(self):
        """Should handle exceptions gracefully."""
        from src.utils.keyboard.core import is_resolve_focused

        with patch("src.utils.keyboard.core.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = Exception("PowerShell error")
                result = is_resolve_focused()

                assert result["focused"] is False
                assert "error" in result


class TestSendKeyIfFocused:
    """Tests for send_key_if_focused function (non-intrusive mode)."""

    def test_skips_when_resolve_not_focused(self):
        """Should skip sending key when Resolve is not focused."""
        from src.utils.keyboard.core import send_key_if_focused

        with patch("src.utils.keyboard.core.is_resolve_focused") as mock_check:
            mock_check.return_value = {"focused": False, "current_window": "Terminal"}
            result = send_key_if_focused(" ", "Play/Pause")

            assert result["success"] is False
            assert result.get("skipped") is True
            assert "not focused" in result["error"]

    def test_sends_key_when_resolve_focused(self):
        """Should send key when Resolve is already focused."""
        from src.utils.keyboard.core import send_key_if_focused

        with patch("src.utils.keyboard.core.is_resolve_focused") as mock_check:
            mock_check.return_value = {
                "focused": True,
                "current_window": "DaVinci Resolve",
            }
            with patch("src.utils.keyboard.core.send_key_to_resolve") as mock_send:
                mock_send.return_value = {"success": True, "message": "OK"}
                result = send_key_if_focused(" ", "Play/Pause")

                assert result["success"] is True
                mock_send.assert_called_once()

    def test_returns_error_on_focus_check_error(self):
        """Should return error if focus check fails."""
        from src.utils.keyboard.core import send_key_if_focused

        with patch("src.utils.keyboard.core.is_resolve_focused") as mock_check:
            mock_check.return_value = {"focused": False, "error": "PowerShell failed"}
            result = send_key_if_focused(" ", "Play/Pause")

            assert result["success"] is False
            assert "PowerShell failed" in result["error"]


class TestResetResolveContext:
    """Tests for reset_resolve_context function."""

    def test_sends_multiple_escape_keys(self):
        """Should send multiple Escape keys to reset context."""
        from src.utils.keyboard.core import reset_resolve_context

        with patch("src.utils.keyboard.core.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            result = reset_resolve_context(escape_count=3)

            assert result["success"] is True
            assert mock_send.call_count == 3
            # Verify all calls were for ESC key
            for call in mock_send.call_args_list:
                assert "{ESC}" in call[0][0]

    def test_stops_on_first_failure(self):
        """Should stop and return error on first failed Escape."""
        from src.utils.keyboard.core import reset_resolve_context

        with patch("src.utils.keyboard.core.send_key_to_resolve") as mock_send:
            # First call succeeds, second fails
            mock_send.side_effect = [
                {"success": True, "message": "OK"},
                {"success": False, "error": "Focus lost"},
            ]
            result = reset_resolve_context(escape_count=3)

            assert result["success"] is False
            assert "Escape 2" in result["error"]
            assert mock_send.call_count == 2

    def test_default_escape_count_is_three(self):
        """Should default to 3 Escape presses."""
        from src.utils.keyboard.core import reset_resolve_context

        with patch("src.utils.keyboard.core.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            reset_resolve_context()

            assert mock_send.call_count == 3
