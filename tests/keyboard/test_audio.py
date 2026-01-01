"""Tests for keyboard audio control module."""

from unittest.mock import patch


class TestAudioVolumeUp:
    """Tests for audio_volume_up function."""

    def test_sends_ctrl_alt_equals(self):
        """Should send Ctrl+Alt+= for volume up."""
        from src.utils.keyboard.audio import audio_volume_up

        with patch("src.utils.keyboard.audio.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            audio_volume_up()
            mock_send.assert_called_once_with("^%=", "Volume Up 1dB (Ctrl+Alt+=)")


class TestAudioVolumeDown:
    """Tests for audio_volume_down function."""

    def test_sends_ctrl_alt_minus(self):
        """Should send Ctrl+Alt+- for volume down."""
        from src.utils.keyboard.audio import audio_volume_down

        with patch("src.utils.keyboard.audio.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            audio_volume_down()
            mock_send.assert_called_once_with("^%-", "Volume Down 1dB (Ctrl+Alt+-)")


class TestAudioToggleVideoAudioSeparate:
    """Tests for audio_toggle_video_audio_separate function."""

    def test_sends_alt_u(self):
        """Should send Alt+U for toggle video/audio separate."""
        from src.utils.keyboard.audio import audio_toggle_video_audio_separate

        with patch("src.utils.keyboard.audio.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            audio_toggle_video_audio_separate()
            mock_send.assert_called_once_with(
                "%u", "Toggle Video/Audio Separate (Alt+U)"
            )
