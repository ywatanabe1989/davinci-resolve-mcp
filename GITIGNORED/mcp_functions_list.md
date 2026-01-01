# DaVinci Resolve MCP Server - Complete Functions List

**Version:** 1.3.8
**Total Tools:** 130+
**Last Updated:** 2026-01-01

---

## Table of Contents
1. [System & Connection](#system--connection)
2. [Project Management](#project-management)
3. [Timeline Operations](#timeline-operations)
4. [Media Pool Operations](#media-pool-operations)
5. [Color Grading](#color-grading)
6. [Timeline Item Properties](#timeline-item-properties)
7. [Keyframe Animation](#keyframe-animation)
8. [Render & Delivery](#render--delivery)
9. [Database & Folder Navigation](#database--folder-navigation)
10. [Media Storage](#media-storage)
11. [Gallery & Stills](#gallery--stills)
12. [Markers](#markers)
13. [Screenshot Capture](#screenshot-capture)
14. [Application Control](#application-control)
15. [Layout Presets](#layout-presets)
16. [Cloud Operations](#cloud-operations)
17. [Project Properties](#project-properties)
18. [Object Inspection](#object-inspection)
19. [Missing Features (Workarounds Needed)](#missing-features-workarounds-needed)

---

## System & Connection

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://version` | Resource | Get DaVinci Resolve version information |
| `resolve://current-page` | Resource | Get current page (Edit, Color, Fusion, etc.) |
| `switch_page(page)` | Tool | Switch to a specific page (media/cut/edit/fusion/color/fairlight/deliver) |

---

## Project Management

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://projects` | Resource | List all available projects |
| `resolve://current-project` | Resource | Get current project name |
| `resolve://project-settings` | Resource | Get all project settings |
| `resolve://project-setting/{setting_name}` | Resource | Get specific project setting |
| `open_project(name)` | Tool | Open a project by name |
| `create_project(name)` | Tool | Create a new project |
| `save_project()` | Tool | Save the current project |
| `close_project()` | Tool | Close current project |
| `set_project_setting(setting_name, setting_value)` | Tool | Set a project setting |

---

## Timeline Operations

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://timelines` | Resource | List all timelines |
| `resolve://current-timeline` | Resource | Get current timeline info |
| `resolve://timeline/{name}/tracks` | Resource | Get timeline track information |
| `resolve://timeline-items` | Resource | Get all items in current timeline |
| `list_timelines_tool()` | Tool | List all timelines |
| `create_timeline(name)` | Tool | Create a new timeline |
| `create_empty_timeline(name, ...)` | Tool | Create timeline with custom settings (frame_rate, resolution, etc.) |
| `delete_timeline(name)` | Tool | Delete a timeline by name |
| `set_current_timeline(name)` | Tool | Switch to a timeline |
| `add_clip_to_timeline(clip_name, timeline_name)` | Tool | Add media pool clip to timeline |
| `duplicate_current_timeline(timeline_name, new_name)` | Tool | Duplicate a timeline |
| `create_compound_clip_from_items(clip_names, ...)` | Tool | Create compound clip |
| `create_fusion_clip_from_items(clip_names)` | Tool | Create Fusion clip |
| `insert_generator_to_timeline(generator_name)` | Tool | Insert generator |
| `insert_fusion_generator_to_timeline(generator_name)` | Tool | Insert Fusion generator |
| `insert_fusion_composition_to_timeline()` | Tool | Insert Fusion composition |
| `insert_title_to_timeline(title_name)` | Tool | Insert title |
| `insert_fusion_title_to_timeline(title_name)` | Tool | Insert Fusion title |
| `import_timeline(file_path, ...)` | Tool | Import timeline (AAF/EDL/XML/FCPXML/DRT/ADL/OTIO) |
| `export_current_timeline(file_path, export_type, export_subtype)` | Tool | Export timeline |
| `set_playhead_timecode(timecode)` | Tool | Set playhead to timecode |
| `detect_timeline_scene_cuts()` | Tool | Detect and create scene cuts |
| `create_subtitles_from_timeline_audio(language, chars_per_line)` | Tool | Create subtitles from audio |
| `export_current_frame(file_path)` | Tool | Export current frame as still |

---

## Media Pool Operations

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://media-pool-clips` | Resource | List clips in root folder |
| `resolve://media-pool-bins` | Resource | List all bins |
| `resolve://media-pool-bin/{bin_name}` | Resource | Get bin contents |
| `resolve://timeline-clips` | Resource | List clips in current timeline |
| `import_media(file_path)` | Tool | Import media file |
| `delete_media(clip_name)` | Tool | Delete media clip |
| `move_media_to_bin(clip_name, bin_name)` | Tool | Move clip to bin |
| `auto_sync_audio(clip_names, sync_method, ...)` | Tool | Sync audio between clips |
| `unlink_clips(clip_names)` | Tool | Unlink clips from media |
| `relink_clips(clip_names, media_paths, ...)` | Tool | Relink clips to media |
| `create_sub_clip(clip_name, start_frame, end_frame, ...)` | Tool | Create subclip |
| `create_bin(name)` | Tool | Create new bin |
| `link_proxy_media(clip_name, proxy_file_path)` | Tool | Link proxy media |
| `unlink_proxy_media(clip_name)` | Tool | Unlink proxy media |
| `replace_clip(clip_name, replacement_path)` | Tool | Replace clip with another |
| `transcribe_audio(clip_name, language)` | Tool | Transcribe audio |
| `clear_transcription(clip_name)` | Tool | Clear transcription |
| `export_folder(folder_name, export_path, export_type)` | Tool | Export folder to DRB |
| `transcribe_folder_audio(folder_name, language)` | Tool | Transcribe folder audio |
| `clear_folder_transcription(folder_name)` | Tool | Clear folder transcription |
| `generate_optimized_media(clip_names)` | Tool | Generate optimized media |
| `delete_optimized_media(clip_names)` | Tool | Delete optimized media |

---

## Color Grading

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://color/current-node` | Resource | Get current color node info |
| `resolve://color/wheel-params` | Resource | Get color wheel parameters |
| `resolve://color/presets` | Resource | Get all color presets |
| `resolve://lut-formats` | Resource | Get available LUT formats |
| `apply_lut(lut_path, node_index)` | Tool | Apply LUT to node |
| `set_color_wheel_param(wheel, param, value, node_index)` | Tool | Set color wheel parameter (lift/gamma/gain/offset) |
| `add_node(node_type, label)` | Tool | Add node (serial/parallel/layer) |
| `copy_grade(source_clip_name, target_clip_name, mode)` | Tool | Copy grade between clips |
| `save_color_preset(clip_name, preset_name, album_name)` | Tool | Save color preset |
| `apply_color_preset(preset_id, preset_name, clip_name, album_name)` | Tool | Apply color preset |
| `delete_color_preset(preset_id, preset_name, album_name)` | Tool | Delete color preset |
| `create_color_preset_album(album_name)` | Tool | Create preset album |
| `delete_color_preset_album(album_name)` | Tool | Delete preset album |
| `export_lut(clip_name, export_path, lut_format, lut_size)` | Tool | Export LUT from grade |
| `export_all_powergrade_luts(export_dir)` | Tool | Export all PowerGrade LUTs |

---

## Timeline Item Properties

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://timeline-item/{id}/properties` | Resource | Get timeline item properties |
| `set_timeline_item_transform(timeline_item_id, property_name, property_value)` | Tool | Set transform (Pan/Tilt/ZoomX/ZoomY/Rotation/AnchorPoint/Pitch/Yaw) |
| `set_timeline_item_crop(timeline_item_id, crop_type, crop_value)` | Tool | Set crop (Left/Right/Top/Bottom) |
| `set_timeline_item_composite(timeline_item_id, composite_mode, opacity)` | Tool | Set composite mode and opacity |
| `set_timeline_item_retime(timeline_item_id, speed, process)` | Tool | Set retime (speed, NearestFrame/FrameBlend/OpticalFlow) |
| `set_timeline_item_stabilization(timeline_item_id, enabled, method, strength)` | Tool | Set stabilization |
| `set_timeline_item_audio(timeline_item_id, volume, pan, eq_enabled)` | Tool | Set audio properties |

---

## Keyframe Animation

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://timeline-item/{id}/keyframes` | Resource | Get keyframes for timeline item |
| `add_keyframe(timeline_item_id, property_name, frame, value)` | Tool | Add keyframe |
| `modify_keyframe(timeline_item_id, property_name, frame, new_value, new_frame)` | Tool | Modify keyframe |
| `delete_keyframe(timeline_item_id, property_name, frame)` | Tool | Delete keyframe |
| `set_keyframe_interpolation(timeline_item_id, property_name, frame, interpolation_type)` | Tool | Set interpolation (Linear/Bezier/Ease-In/Ease-Out) |
| `enable_keyframes(timeline_item_id, keyframe_mode)` | Tool | Enable keyframe mode (All/Color/Sizing) |

---

## Render & Delivery

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://render-presets` | Resource | Get render presets |
| `resolve://render-queue` | Resource | Get render queue status |
| `add_to_render_queue(preset_name, timeline_name, use_in_out_range)` | Tool | Add to render queue |
| `start_render()` | Tool | Start rendering |
| `clear_render_queue()` | Tool | Clear render queue |
| `set_cache_mode(mode)` | Tool | Set cache mode (auto/on/off) |
| `set_optimized_media_mode(mode)` | Tool | Set optimized media mode |
| `set_proxy_mode(mode)` | Tool | Set proxy mode |
| `set_proxy_quality(quality)` | Tool | Set proxy quality (quarter/half/threeQuarter/full) |
| `set_cache_path(path_type, path)` | Tool | Set cache path (local/network) |

---

## Database & Folder Navigation

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://database/current` | Resource | Get current database |
| `resolve://database/list` | Resource | List all databases |
| `resolve://folder/current` | Resource | Get current folder |
| `resolve://folder/list` | Resource | List folders in current folder |
| `switch_database(db_type, db_name, ip_address)` | Tool | Switch database (Disk/PostgreSQL) |
| `navigate_to_root_folder()` | Tool | Go to root folder |
| `navigate_to_parent_folder()` | Tool | Go to parent folder |
| `navigate_to_folder(folder_name)` | Tool | Open folder |
| `create_project_folder(folder_name)` | Tool | Create folder |
| `delete_project_folder(folder_name)` | Tool | Delete folder |
| `import_project_file(file_path, project_name)` | Tool | Import .drp file |
| `export_project_file(project_name, file_path, with_stills_and_luts)` | Tool | Export project |
| `archive_project_with_media(project_name, file_path, ...)` | Tool | Archive with media |
| `restore_project_from_archive(file_path, project_name)` | Tool | Restore from archive |
| `delete_project_by_name(project_name)` | Tool | Delete project |

---

## Media Storage

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://media-storage/volumes` | Resource | Get mounted volumes |
| `get_media_storage_subfolders(folder_path)` | Tool | Get subfolders |
| `get_media_storage_files(folder_path)` | Tool | Get files |
| `reveal_path_in_media_storage(path)` | Tool | Reveal path in Media Storage |
| `add_files_to_media_pool(paths)` | Tool | Add files to Media Pool |

---

## Gallery & Stills

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://gallery/still-albums` | Resource | Get still albums |
| `resolve://gallery/powergrade-albums` | Resource | Get PowerGrade albums |
| `resolve://gallery/current-album` | Resource | Get current album |
| `create_gallery_still_album()` | Tool | Create still album |
| `create_gallery_powergrade_album()` | Tool | Create PowerGrade album |
| `rename_gallery_album(old_name, new_name)` | Tool | Rename album |
| `set_current_gallery_album(album_name)` | Tool | Set current album |
| `grab_current_still()` | Tool | Grab still from current clip |
| `grab_stills_from_all_clips(source)` | Tool | Grab stills from all clips |
| `import_stills_to_album(album_name, file_paths)` | Tool | Import stills |
| `export_stills_from_album(album_name, folder_path, file_prefix, format)` | Tool | Export stills |

---

## Markers

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://timeline/markers` | Resource | Get timeline markers |
| `resolve://clip/{clip_name}/markers` | Resource | Get clip markers |
| `add_marker(frame, color, note)` | Tool | Add marker to timeline |
| `add_marker_to_timeline(frame, color, name, note, duration, custom_data)` | Tool | Add marker with full options |
| `delete_timeline_marker(frame)` | Tool | Delete marker at frame |
| `delete_markers_by_color(color)` | Tool | Delete markers by color |
| `find_marker_by_custom_data(custom_data)` | Tool | Find marker by custom data |
| `update_marker_data(frame, custom_data)` | Tool | Update marker custom data |
| `get_marker_data(frame)` | Tool | Get marker custom data |
| `delete_marker_with_custom_data(custom_data)` | Tool | Delete marker by custom data |
| `add_marker_to_clip(clip_name, frame, color, ...)` | Tool | Add marker to media pool clip |

---

## Screenshot Capture

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://system/windows` | Resource | List all visible windows |
| `resolve://system/monitors` | Resource | Get monitor information |
| `resolve://system/resolve-window` | Resource | Find Resolve window info |
| `resolve://system/environment` | Resource | Get system environment info |
| `resolve://system/monitoring-status` | Resource | Get screenshot monitoring status |
| `take_screenshot(output_path, quality, monitor_id, capture_all, return_base64)` | Tool | Take desktop screenshot |
| `capture_resolve_ui(output_path, quality, return_base64)` | Tool | Capture Resolve window |
| `capture_window_by_handle(window_handle, output_path, quality, return_base64)` | Tool | Capture specific window |
| `start_screenshot_monitoring(output_dir, interval_sec, quality, monitor_id, capture_all)` | Tool | Start continuous monitoring |
| `stop_screenshot_monitoring()` | Tool | Stop monitoring |

---

## Application Control

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://app/state` | Resource | Get application state |
| `quit_app(force, save_project)` | Tool | Quit DaVinci Resolve |
| `restart_app(wait_seconds)` | Tool | Restart DaVinci Resolve |
| `open_settings()` | Tool | Open Project Settings dialog |
| `open_app_preferences()` | Tool | Open Preferences dialog |

---

## Layout Presets

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://layout/presets` | Resource | Get layout presets |
| `save_layout_preset_tool(preset_name)` | Tool | Save current UI layout |
| `load_layout_preset_tool(preset_name)` | Tool | Load layout preset |
| `export_layout_preset_tool(preset_name, export_path)` | Tool | Export layout preset |
| `import_layout_preset_tool(import_path, preset_name)` | Tool | Import layout preset |
| `delete_layout_preset_tool(preset_name)` | Tool | Delete layout preset |

---

## Cloud Operations

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://cloud/projects` | Resource | Get cloud projects |
| `create_cloud_project_tool(project_name, folder_path)` | Tool | Create cloud project |
| `import_cloud_project_tool(cloud_id, project_name)` | Tool | Import cloud project |
| `restore_cloud_project_tool(cloud_id, project_name)` | Tool | Restore cloud project |
| `export_project_to_cloud_tool(project_name)` | Tool | Export to cloud |
| `add_user_to_cloud_project_tool(cloud_id, user_email, permissions)` | Tool | Add user to cloud project |
| `remove_user_from_cloud_project_tool(cloud_id, user_email)` | Tool | Remove user from cloud project |

---

## Project Properties

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://project/properties` | Resource | Get all project properties |
| `resolve://project/property/{name}` | Resource | Get specific property |
| `resolve://project/timeline-format` | Resource | Get timeline format |
| `resolve://project/superscale` | Resource | Get SuperScale settings |
| `resolve://project/color-settings` | Resource | Get color settings |
| `resolve://project/metadata` | Resource | Get project metadata |
| `resolve://project/info` | Resource | Get project info |
| `set_project_property_tool(property_name, property_value)` | Tool | Set project property |
| `set_timeline_format_tool(width, height, frame_rate, interlaced)` | Tool | Set timeline format |
| `set_superscale_settings_tool(enabled, quality)` | Tool | Set SuperScale |
| `set_color_science_mode_tool(mode)` | Tool | Set color science (YRGB/ACEScct/etc.) |
| `set_color_space_tool(color_space, gamma)` | Tool | Set color space/gamma |

---

## Object Inspection

| Tool/Resource | Type | Description |
|---------------|------|-------------|
| `resolve://inspect/resolve` | Resource | Inspect Resolve object |
| `resolve://inspect/project-manager` | Resource | Inspect ProjectManager |
| `resolve://inspect/project` | Resource | Inspect current project |
| `resolve://inspect/media-pool` | Resource | Inspect MediaPool |
| `resolve://inspect/timeline` | Resource | Inspect current timeline |
| `object_help(object_type)` | Tool | Get help for Resolve object |
| `inspect_custom_object(object_path)` | Tool | Inspect custom object by path |

---

## Keyboard Simulation Tools (NEW)

The following tools use **keyboard simulation** to control DaVinci Resolve features that are NOT exposed via the scripting API. These work on Windows and WSL.

### Playback Controls
| Tool | Description | Keyboard Shortcut |
|------|-------------|-------------------|
| `play_pause()` | Toggle play/pause | Space |
| `stop_playback()` | Stop playback | K |
| `play_forward()` | Play forward (multiple presses = faster) | L |
| `play_reverse()` | Play in reverse (multiple presses = faster) | J |
| `step_frame_forward()` | Step forward one frame | Right Arrow |
| `step_frame_backward()` | Step backward one frame | Left Arrow |
| `go_to_timeline_start()` | Go to start of timeline | Home |
| `go_to_timeline_end()` | Go to end of timeline | End |
| `toggle_loop_playback()` | Toggle loop mode | Ctrl+/ |

### Edit Operations
| Tool | Description | Keyboard Shortcut |
|------|-------------|-------------------|
| `cut_at_playhead()` | Cut/Razor at playhead | Ctrl+B |
| `ripple_delete_clip()` | Ripple delete selected clip | Shift+Delete |
| `delete_clip()` | Delete selected clip (leaves gap) | Delete |
| `undo_action()` | Undo last action | Ctrl+Z |
| `redo_action()` | Redo last undone action | Ctrl+Shift+Z |
| `trim_clip_start()` | Trim start to playhead | [ |
| `trim_clip_end()` | Trim end to playhead | ] |
| `insert_clip()` | Insert clip at playhead | F9 |
| `overwrite_clip()` | Overwrite at playhead | F10 |
| `copy_clip()` | Copy selected clip | Ctrl+C |
| `paste_clip()` | Paste copied clip | Ctrl+V |

### Selection Operations
| Tool | Description | Keyboard Shortcut |
|------|-------------|-------------------|
| `select_all_clips()` | Select all clips | Ctrl+A |
| `deselect_all_clips()` | Deselect all clips | Ctrl+Shift+A |
| `select_forward_from_playhead()` | Select clips forward | Y |
| `select_backward_from_playhead()` | Select clips backward | Ctrl+Y |

### View Controls
| Tool | Description | Keyboard Shortcut |
|------|-------------|-------------------|
| `zoom_in_timeline()` | Zoom in on timeline | = |
| `zoom_out_timeline()` | Zoom out on timeline | - |
| `fit_timeline_to_view()` | Fit timeline to view | Shift+Z |
| `toggle_fullscreen_preview()` | Toggle fullscreen preview | P |

### Custom Keyboard Shortcut
| Tool | Description |
|------|-------------|
| `send_keyboard_shortcut(key, description)` | Send any keyboard shortcut to Resolve |
| `resolve://keyboard/shortcuts` | Resource: List of common shortcuts |

---

## Implementation Notes

### Workaround for Playback Controls

Since playback controls are not exposed via the scripting API, use keyboard simulation via PowerShell (for Windows/WSL):

```python
import subprocess

def send_key_to_resolve(key: str) -> bool:
    """Send keyboard input to DaVinci Resolve via PowerShell."""
    ps_script = f'''
    $resolve = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*DaVinci Resolve*' }} | Select-Object -First 1
    if ($resolve) {{
        Add-Type @'
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {{
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
        }}
'@
        [Win32]::SetForegroundWindow($resolve.MainWindowHandle)
        Start-Sleep -Milliseconds 100
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait('{key}')
        Write-Output 'Sent {key} to Resolve'
    }}
    '''
    result = subprocess.run(['powershell.exe', '-Command', ps_script], capture_output=True, text=True)
    return 'Sent' in result.stdout
```

### Keyboard Mapping for SendKeys
| Key | SendKeys Format |
|-----|-----------------|
| Space | `' '` or `{SPACE}` |
| Enter | `{ENTER}` |
| Arrow Keys | `{LEFT}`, `{RIGHT}`, `{UP}`, `{DOWN}` |
| Home/End | `{HOME}`, `{END}` |
| Ctrl+Key | `^key` (e.g., `^z` for Ctrl+Z) |
| Shift+Key | `+key` (e.g., `+{DELETE}` for Shift+Delete) |
| Alt+Key | `%key` (e.g., `%{F4}` for Alt+F4) |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| API-Based Tools | ~85 |
| Keyboard Simulation Tools | ~30 |
| Resources | ~46 |
| **Total MCP Endpoints** | **~161** |

### Coverage

| Feature Category | Status |
|------------------|--------|
| Project Management | ✅ Full API support |
| Timeline Operations | ✅ Full API support |
| Media Pool | ✅ Full API support |
| Color Grading | ✅ Full API support |
| Keyframe Animation | ✅ Full API support |
| Render & Delivery | ✅ Full API support |
| Playback Controls | ✅ Keyboard simulation |
| Edit Operations | ✅ Keyboard simulation |
| Selection | ✅ Keyboard simulation |
| View Controls | ✅ Keyboard simulation |
| Screenshot Capture | ✅ Implemented |

---

*This document provides a complete reference for all available MCP tools in the DaVinci Resolve MCP Server. Features not available via the official API are now accessible through keyboard simulation on Windows/WSL.*
