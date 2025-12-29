"""Tests for continuous capture module."""

from unittest.mock import Mock, patch


class TestContinuousCapture:
    """Tests for ContinuousCapture class."""

    def test_init_creates_output_dir(self):
        """Should create output directory on init."""
        from src.utils.capture_continuous import ContinuousCapture

        with patch("pathlib.Path.mkdir") as mock_mkdir:
            _capture = ContinuousCapture(output_dir="/tmp/test_capture")  # noqa: F841
            mock_mkdir.assert_called_once()

    def test_start_sets_running_flag(self):
        """Should set running flag when started."""
        from src.utils.capture_continuous import ContinuousCapture

        with patch("pathlib.Path.mkdir"):
            capture = ContinuousCapture()

            with patch.object(capture, "_capture_loop"):
                capture.start()
                assert capture.running is True
                capture.stop()

    def test_stop_clears_running_flag(self):
        """Should clear running flag when stopped."""
        from src.utils.capture_continuous import ContinuousCapture

        with patch("pathlib.Path.mkdir"):
            capture = ContinuousCapture()
            capture.running = True
            capture.thread = None
            capture.stop()
            assert capture.running is False

    def test_get_status_returns_correct_info(self):
        """Should return correct status information."""
        from src.utils.capture_continuous import ContinuousCapture

        with patch("pathlib.Path.mkdir"):
            capture = ContinuousCapture(
                output_dir="/tmp/test",
                interval_sec=2.0,
                quality=80,
            )
            capture.running = True
            capture.session_id = "test_session"
            capture.screenshot_count = 5

            status = capture.get_status()

            assert status["running"] is True
            assert status["session_id"] == "test_session"
            assert status["screenshot_count"] == 5
            assert status["interval_sec"] == 2.0


class TestStartMonitoring:
    """Tests for start_monitoring function."""

    def test_returns_error_when_already_running(self):
        """Should return error when monitoring already running."""
        from src.utils import capture_continuous

        # Create a mock running instance
        mock_instance = Mock()
        mock_instance.running = True

        with patch.object(capture_continuous, "_capture_instance", mock_instance):
            result = capture_continuous.start_monitoring()
            assert result["success"] is False
            assert "already running" in result["error"]

    def test_starts_monitoring_successfully(self):
        """Should start monitoring successfully."""
        from src.utils import capture_continuous

        # Reset the global instance
        capture_continuous._capture_instance = None

        with patch("pathlib.Path.mkdir"):
            with patch.object(capture_continuous.ContinuousCapture, "_capture_loop"):
                result = capture_continuous.start_monitoring(interval_sec=1.0)
                assert result["success"] is True
                assert "session_id" in result

                # Clean up
                capture_continuous.stop_monitoring()


class TestStopMonitoring:
    """Tests for stop_monitoring function."""

    def test_returns_error_when_not_running(self):
        """Should return error when monitoring not running."""
        from src.utils import capture_continuous

        capture_continuous._capture_instance = None

        result = capture_continuous.stop_monitoring()
        assert result["success"] is False


class TestGetMonitoringStatus:
    """Tests for get_monitoring_status function."""

    def test_returns_not_running_when_no_instance(self):
        """Should return not running when no instance exists."""
        from src.utils import capture_continuous

        capture_continuous._capture_instance = None

        result = capture_continuous.get_monitoring_status()
        assert result["running"] is False

    def test_returns_status_when_instance_exists(self):
        """Should return status when instance exists."""
        from src.utils import capture_continuous

        mock_instance = Mock()
        mock_instance.get_status.return_value = {
            "running": True,
            "session_id": "test",
            "screenshot_count": 10,
        }

        with patch.object(capture_continuous, "_capture_instance", mock_instance):
            result = capture_continuous.get_monitoring_status()
            assert result["running"] is True
            assert result["screenshot_count"] == 10
