#!/usr/bin/env python3
"""
DaVinci Resolve MCP Server - Keyboard Control Module

This module provides keyboard simulation for controlling DaVinci Resolve
features that are NOT exposed via the scripting API (e.g., playback controls).

Works on Windows and WSL by using PowerShell for keyboard input.
"""

# Core functions
from .core import (
    is_wsl,
    get_platform_type,
    send_key_to_resolve,
    send_custom_key,
)

# Playback controls
from .playback import (
    playback_play_pause,
    playback_stop,
    playback_forward,
    playback_reverse,
    playback_step_forward,
    playback_step_backward,
    playback_go_to_start,
    playback_go_to_end,
    playback_loop_toggle,
    playback_fast_forward,
    playback_fast_reverse,
    playback_play_around,
)

# Edit operations
from .edit import (
    edit_cut_at_playhead,
    edit_ripple_delete,
    edit_delete,
    edit_undo,
    edit_redo,
    edit_trim_start,
    edit_trim_end,
    edit_insert,
    edit_overwrite,
    edit_copy,
    edit_cut,
    edit_paste,
    edit_split_clip,
    edit_join_clip,
    edit_nudge_left,
    edit_nudge_right,
    edit_nudge_left_multi,
    edit_nudge_right_multi,
    edit_replace,
    edit_place_on_top,
    edit_ripple_overwrite,
    edit_fit_to_fill,
    edit_append_to_end,
)

# Selection operations
from .selection import (
    select_all,
    deselect_all,
    select_clips_forward,
    select_clips_backward,
    select_nearest_edit,
)

# View controls
from .view import (
    view_zoom_in,
    view_zoom_out,
    view_zoom_in_viewer,
    view_zoom_out_viewer,
    view_fit_timeline,
    view_fullscreen_preview,
    view_fullscreen_viewer,
    view_enhanced_viewer,
    view_cinema_viewer,
    view_expand_display,
    view_split_screen,
    view_video_scopes,
    view_display_left,
    view_display_right,
    view_display_red_channel,
    view_display_z_buffer,
    view_display_full_color,
)

# Mark operations
from .marks import (
    mark_set_in,
    mark_set_out,
    mark_clip,
    mark_go_to_in,
    mark_go_to_out,
    mark_clear_in,
    mark_clear_out,
    mark_clear_both,
)

# Marker operations
from .markers import (
    marker_add,
    marker_add_and_modify,
    marker_modify,
    marker_delete,
    marker_go_to_next,
    marker_go_to_previous,
)

# Page navigation
from .pages import (
    page_media,
    page_cut,
    page_edit,
    page_fusion,
    page_color,
    page_fairlight,
    page_deliver,
)

# Node operations (Color page)
from .nodes import (
    node_add_serial,
    node_add_parallel,
    node_add_layer,
    node_add_serial_before,
    node_add_outside,
    node_add_splitter_combiner,
    node_disable_current,
    node_disable_all,
    node_bypass_grades,
    node_reset_grades,
    node_previous,
    node_next,
    node_extract_current,
)

# Timeline navigation
from .timeline import (
    timeline_previous_clip,
    timeline_next_clip,
    timeline_step_1_second_forward,
    timeline_step_1_second_backward,
    timeline_go_to_first_frame,
    timeline_go_to_last_frame,
    timeline_go_to_prev_keyframe,
    timeline_go_to_next_keyframe,
)

# Edit modes
from .modes import (
    mode_selection,
    mode_blade,
    mode_trim,
    mode_dynamic_trim,
    mode_slip_slide,
    mode_edit_point_type,
    mode_hand_tool,
    toggle_snapping,
    toggle_audio_scrubbing,
)

# Transitions
from .transitions import (
    transition_add,
    transition_add_video,
    transition_add_audio,
)

# Application controls
from .application import (
    app_save_project,
    app_import_media,
    app_export_project,
    app_new_timeline,
    app_new_bin,
    app_project_settings,
    app_preferences,
    app_keyboard_customization,
    app_quit,
)

# Audio controls
from .audio import (
    audio_volume_up,
    audio_volume_down,
    audio_toggle_video_audio_separate,
)

# Clip controls
from .clips import (
    clip_enable_disable,
    clip_create_subclip,
    clip_add_flag,
    clip_change_duration,
)

# Viewer controls
from .viewer import (
    viewer_toggle_source_timeline,
    viewer_match_frame,
)

# Color page controls
from .color import (
    color_grab_still,
    color_auto_balance,
    color_highlight,
    color_add_version,
    color_load_memory_a,
    color_save_memory_a,
    color_load_memory_b,
    color_save_memory_b,
    color_load_memory_c,
    color_save_memory_c,
    color_load_memory_d,
    color_save_memory_d,
    color_apply_grade_from_one_prior,
    color_apply_grade_from_two_prior,
)

# Retime controls
from .retime import (
    retime_controls,
    retime_freeze_frame,
)

# Shortcuts dictionary
from .shortcuts import get_keyboard_shortcuts

# Focus management
from .focus import (
    save_user_state,
    restore_user_state,
    get_saved_state,
    clear_saved_state,
    with_user_state_preserved,
    resolve_ui_operation,
    ResolveUIContext,
)

__all__ = [
    # Core
    "is_wsl",
    "get_platform_type",
    "send_key_to_resolve",
    "send_custom_key",
    # Playback
    "playback_play_pause",
    "playback_stop",
    "playback_forward",
    "playback_reverse",
    "playback_step_forward",
    "playback_step_backward",
    "playback_go_to_start",
    "playback_go_to_end",
    "playback_loop_toggle",
    "playback_fast_forward",
    "playback_fast_reverse",
    "playback_play_around",
    # Edit
    "edit_cut_at_playhead",
    "edit_ripple_delete",
    "edit_delete",
    "edit_undo",
    "edit_redo",
    "edit_trim_start",
    "edit_trim_end",
    "edit_insert",
    "edit_overwrite",
    "edit_copy",
    "edit_cut",
    "edit_paste",
    "edit_split_clip",
    "edit_join_clip",
    "edit_nudge_left",
    "edit_nudge_right",
    "edit_nudge_left_multi",
    "edit_nudge_right_multi",
    "edit_replace",
    "edit_place_on_top",
    "edit_ripple_overwrite",
    "edit_fit_to_fill",
    "edit_append_to_end",
    # Selection
    "select_all",
    "deselect_all",
    "select_clips_forward",
    "select_clips_backward",
    "select_nearest_edit",
    # View
    "view_zoom_in",
    "view_zoom_out",
    "view_zoom_in_viewer",
    "view_zoom_out_viewer",
    "view_fit_timeline",
    "view_fullscreen_preview",
    "view_fullscreen_viewer",
    "view_enhanced_viewer",
    "view_cinema_viewer",
    "view_expand_display",
    "view_split_screen",
    "view_video_scopes",
    "view_display_left",
    "view_display_right",
    "view_display_red_channel",
    "view_display_z_buffer",
    "view_display_full_color",
    # Marks
    "mark_set_in",
    "mark_set_out",
    "mark_clip",
    "mark_go_to_in",
    "mark_go_to_out",
    "mark_clear_in",
    "mark_clear_out",
    "mark_clear_both",
    # Markers
    "marker_add",
    "marker_add_and_modify",
    "marker_modify",
    "marker_delete",
    "marker_go_to_next",
    "marker_go_to_previous",
    # Pages
    "page_media",
    "page_cut",
    "page_edit",
    "page_fusion",
    "page_color",
    "page_fairlight",
    "page_deliver",
    # Nodes
    "node_add_serial",
    "node_add_parallel",
    "node_add_layer",
    "node_add_serial_before",
    "node_add_outside",
    "node_add_splitter_combiner",
    "node_disable_current",
    "node_disable_all",
    "node_bypass_grades",
    "node_reset_grades",
    "node_previous",
    "node_next",
    "node_extract_current",
    # Timeline
    "timeline_previous_clip",
    "timeline_next_clip",
    "timeline_step_1_second_forward",
    "timeline_step_1_second_backward",
    "timeline_go_to_first_frame",
    "timeline_go_to_last_frame",
    "timeline_go_to_prev_keyframe",
    "timeline_go_to_next_keyframe",
    # Modes
    "mode_selection",
    "mode_blade",
    "mode_trim",
    "mode_dynamic_trim",
    "mode_slip_slide",
    "mode_edit_point_type",
    "mode_hand_tool",
    "toggle_snapping",
    "toggle_audio_scrubbing",
    # Transitions
    "transition_add",
    "transition_add_video",
    "transition_add_audio",
    # Application
    "app_save_project",
    "app_import_media",
    "app_export_project",
    "app_new_timeline",
    "app_new_bin",
    "app_project_settings",
    "app_preferences",
    "app_keyboard_customization",
    "app_quit",
    # Audio
    "audio_volume_up",
    "audio_volume_down",
    "audio_toggle_video_audio_separate",
    # Clips
    "clip_enable_disable",
    "clip_create_subclip",
    "clip_add_flag",
    "clip_change_duration",
    # Viewer
    "viewer_toggle_source_timeline",
    "viewer_match_frame",
    # Color
    "color_grab_still",
    "color_auto_balance",
    "color_highlight",
    "color_add_version",
    "color_load_memory_a",
    "color_save_memory_a",
    "color_load_memory_b",
    "color_save_memory_b",
    "color_load_memory_c",
    "color_save_memory_c",
    "color_load_memory_d",
    "color_save_memory_d",
    "color_apply_grade_from_one_prior",
    "color_apply_grade_from_two_prior",
    # Retime
    "retime_controls",
    "retime_freeze_frame",
    # Shortcuts
    "get_keyboard_shortcuts",
    # Focus management
    "save_user_state",
    "restore_user_state",
    "get_saved_state",
    "clear_saved_state",
    "with_user_state_preserved",
    "resolve_ui_operation",
    "ResolveUIContext",
]
