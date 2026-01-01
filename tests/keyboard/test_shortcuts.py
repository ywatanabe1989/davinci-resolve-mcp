"""Tests for keyboard shortcuts dictionary module."""


class TestGetKeyboardShortcuts:
    """Tests for get_keyboard_shortcuts function."""

    def test_returns_dictionary(self):
        """Should return a dictionary."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        result = get_keyboard_shortcuts()
        assert isinstance(result, dict)

    def test_contains_playback_shortcuts(self):
        """Should contain playback shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        assert "play_pause" in shortcuts
        assert shortcuts["play_pause"] == "Space"
        assert "stop" in shortcuts
        assert shortcuts["stop"] == "K"

    def test_contains_mark_shortcuts(self):
        """Should contain mark shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        assert "set_mark_in" in shortcuts
        assert shortcuts["set_mark_in"] == "I"
        assert "set_mark_out" in shortcuts
        assert shortcuts["set_mark_out"] == "O"

    def test_contains_page_shortcuts(self):
        """Should contain page navigation shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        assert "media_page" in shortcuts
        assert shortcuts["media_page"] == "Shift+2"
        assert "color_page" in shortcuts
        assert shortcuts["color_page"] == "Shift+6"

    def test_contains_node_shortcuts(self):
        """Should contain node shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        assert "add_serial_node" in shortcuts
        assert shortcuts["add_serial_node"] == "Alt+S"
        assert "add_parallel_node" in shortcuts
        assert shortcuts["add_parallel_node"] == "Alt+P"

    def test_contains_application_shortcuts(self):
        """Should contain application shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        assert "save_project" in shortcuts
        assert shortcuts["save_project"] == "Ctrl+S"
        assert "preferences" in shortcuts
        assert shortcuts["preferences"] == "Ctrl+,"

    def test_contains_audio_shortcuts(self):
        """Should contain audio shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        assert "volume_up_1db" in shortcuts
        assert shortcuts["volume_up_1db"] == "Ctrl+Alt+="
        assert "toggle_video_audio_separate" in shortcuts
        assert shortcuts["toggle_video_audio_separate"] == "Alt+U"

    def test_contains_color_memory_shortcuts(self):
        """Should contain color memory shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        assert "load_memory_a" in shortcuts
        assert shortcuts["load_memory_a"] == "Ctrl+1"
        assert "save_memory_a" in shortcuts
        assert shortcuts["save_memory_a"] == "Alt+1"

    def test_has_reasonable_size(self):
        """Should have a reasonable number of shortcuts."""
        from src.utils.keyboard.shortcuts import get_keyboard_shortcuts

        shortcuts = get_keyboard_shortcuts()
        # Should have at least 100 shortcuts
        assert len(shortcuts) >= 100
