"""Tests for capture utilities module."""

from unittest.mock import Mock, patch


class TestIsWsl:
    """Tests for is_wsl function."""

    def test_returns_true_on_wsl(self):
        """Should return True when running on WSL."""
        from src.utils.capture import is_wsl

        with patch("sys.platform", "linux"):
            with patch("os.uname") as mock_uname:
                mock_uname.return_value = Mock(release="5.10.0-microsoft-standard-WSL2")
                assert is_wsl() is True

    def test_returns_false_on_native_linux(self):
        """Should return False when running on native Linux."""
        from src.utils.capture import is_wsl

        with patch("sys.platform", "linux"):
            with patch("os.uname") as mock_uname:
                mock_uname.return_value = Mock(release="5.10.0-generic")
                assert is_wsl() is False

    def test_returns_false_on_windows(self):
        """Should return False when running on Windows."""
        from src.utils.capture import is_wsl

        with patch("sys.platform", "win32"):
            assert is_wsl() is False

    def test_returns_false_on_macos(self):
        """Should return False when running on macOS."""
        from src.utils.capture import is_wsl

        with patch("sys.platform", "darwin"):
            assert is_wsl() is False


class TestFindPowershell:
    """Tests for find_powershell function."""

    def test_returns_none_when_not_found(self):
        """Should return None when PowerShell not found."""
        from src.utils.capture import find_powershell

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Not found")
            result = find_powershell()
            assert result is None

    def test_returns_path_when_found(self):
        """Should return path when PowerShell found."""
        from src.utils.capture import find_powershell

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            result = find_powershell()
            assert result is not None


class TestCaptureScreenshot:
    """Tests for capture_screenshot function."""

    def test_returns_error_when_not_wsl(self):
        """Should return error when not running in WSL."""
        from src.utils.capture import capture_screenshot

        with patch("src.utils.capture.is_wsl", return_value=False):
            result = capture_screenshot()
            assert result["success"] is False
            assert "WSL" in result["error"]

    def test_returns_error_when_powershell_not_found(self):
        """Should return error when PowerShell not found."""
        from src.utils.capture import capture_screenshot

        with patch("src.utils.capture.is_wsl", return_value=True):
            with patch("src.utils.capture.find_powershell", return_value=None):
                result = capture_screenshot()
                assert result["success"] is False
                assert "PowerShell" in result["error"]


class TestListWindows:
    """Tests for list_windows function."""

    def test_returns_error_when_not_wsl(self):
        """Should return error when not running in WSL."""
        from src.utils.capture import list_windows

        with patch("src.utils.capture.is_wsl", return_value=False):
            result = list_windows()
            assert result["success"] is False


class TestCaptureWindow:
    """Tests for capture_window function."""

    def test_returns_error_when_not_wsl(self):
        """Should return error when not running in WSL."""
        from src.utils.capture import capture_window

        with patch("src.utils.capture.is_wsl", return_value=False):
            result = capture_window(12345)
            assert result["success"] is False


class TestFindResolveWindow:
    """Tests for find_resolve_window function."""

    def test_returns_none_when_list_windows_fails(self):
        """Should return None when list_windows fails."""
        from src.utils.capture import find_resolve_window

        with patch("src.utils.capture.list_windows") as mock_list:
            mock_list.return_value = {"success": False, "error": "Failed"}
            result = find_resolve_window()
            assert result is None

    def test_returns_none_when_resolve_not_found(self):
        """Should return None when Resolve window not found."""
        from src.utils.capture import find_resolve_window

        with patch("src.utils.capture.list_windows") as mock_list:
            mock_list.return_value = {
                "success": True,
                "windows": [
                    {"Title": "Notepad", "ProcessName": "notepad", "Handle": 1},
                    {"Title": "Chrome", "ProcessName": "chrome", "Handle": 2},
                ],
            }
            result = find_resolve_window()
            assert result is None

    def test_finds_resolve_window_by_title(self):
        """Should find Resolve window by title."""
        from src.utils.capture import find_resolve_window

        with patch("src.utils.capture.list_windows") as mock_list:
            mock_list.return_value = {
                "success": True,
                "windows": [
                    {"Title": "Notepad", "ProcessName": "notepad", "Handle": 1},
                    {
                        "Title": "DaVinci Resolve - Project",
                        "ProcessName": "Resolve",
                        "Handle": 2,
                    },
                ],
            }
            result = find_resolve_window()
            assert result is not None
            assert result["Handle"] == 2

    def test_finds_resolve_window_by_process_name(self):
        """Should find Resolve window by process name."""
        from src.utils.capture import find_resolve_window

        with patch("src.utils.capture.list_windows") as mock_list:
            mock_list.return_value = {
                "success": True,
                "windows": [
                    {"Title": "Some Window", "ProcessName": "Resolve", "Handle": 3},
                ],
            }
            result = find_resolve_window()
            assert result is not None


class TestCaptureResolveWindow:
    """Tests for capture_resolve_window function."""

    def test_returns_error_when_resolve_not_found(self):
        """Should return error when Resolve window not found."""
        from src.utils.capture import capture_resolve_window

        with patch("src.utils.capture.find_resolve_window", return_value=None):
            result = capture_resolve_window()
            assert result["success"] is False
            assert "not found" in result["error"]


class TestGetMonitorInfo:
    """Tests for get_monitor_info function."""

    def test_returns_error_when_not_wsl(self):
        """Should return error when not running in WSL."""
        from src.utils.capture import get_monitor_info

        with patch("src.utils.capture.is_wsl", return_value=False):
            result = get_monitor_info()
            assert result["success"] is False
