---
description: >
  Control Ableton Live's transport, session, and arrangement — play, stop, record,
  set tempo, manage scenes, manage clips, navigate the browser, and get an overview
  of the current session. Use when the user says "play", "stop", "start recording",
  "set the tempo", "what tracks do I have", "show me the session", "fire scene",
  "duplicate track", "delete clip", "what's in my browser", or any request about
  transport, session state, tracks, scenes, or clips.
---

# Session & Transport Control

Use these tools to understand and control the Ableton Live session at a high level.

## Always start here

Call `get_session_info` at the start of every session to get:
- Tempo, time signature, song length
- Number of tracks, return tracks, scenes
- Transport state (playing, recording, loop)

For a full snapshot of tracks + devices + clips in one call:
`get_full_session_state()` — use this when you need a complete picture.

## Transport

| Goal | Tool |
|---|---|
| Play | `start_playback()` |
| Stop | `stop_playback()` |
| Continue from position | `continue_playing()` |
| Set tempo | `set_tempo(bpm)` |
| Tap tempo | `tap_tempo()` |
| Set playback position | `set_playback_position(position)` — in beats |
| Enable metronome | `set_metronome(enabled=True)` |
| Set loop | `set_song_loop(enabled, start, length)` |
| Undo / redo | `undo()` / `redo()` |

## Tracks

| Goal | Tool |
|---|---|
| Get all tracks | `get_all_tracks_info()` |
| Get one track | `get_track_info(track_index)` |
| Create MIDI track | `create_midi_track(index=-1)` |
| Create audio track | `create_audio_track(index=-1)` |
| Create return track | `create_return_track()` |
| Rename track | `set_track_name(track_index, name)` |
| Delete track | `delete_track(track_index)` |
| Duplicate track | `duplicate_track(track_index)` |
| Group tracks | `group_tracks(track_indices=[0,1,2])` |
| Freeze track | `freeze_track(track_index)` |

## Clips

| Goal | Tool |
|---|---|
| Get clip info | `get_clip_info(track_index, clip_index)` |
| Get clip notes | `get_clip_notes(track_index, clip_index)` |
| Fire clip | `fire_clip(track_index, clip_index)` |
| Stop clip | `stop_clip(track_index, clip_index)` |
| Stop all clips | `stop_all_clips()` |
| Duplicate clip | `duplicate_clip(track_index, clip_index)` |
| Delete clip | `delete_clip(track_index, clip_index)` |
| Rename clip | `set_clip_name(track_index, clip_index, name)` |
| Set clip loop | `set_clip_looping(track_index, clip_index, looping=True)` |
| Set loop points | `set_clip_loop_points(track_index, clip_index, start, end)` |

## Scenes

| Goal | Tool |
|---|---|
| Fire a scene | `fire_scene(scene_index)` |
| Create scene | `create_scene(index=-1)` |
| Rename scene | `set_scene_name(scene_index, name)` |
| Delete scene | `delete_scene(scene_index)` |
| Duplicate scene | `duplicate_scene(scene_index)` |

## Browser

| Goal | Tool |
|---|---|
| Search for instruments/effects | `search_browser(query, max_results=20)` |
| Browse by category | `get_browser_tree(category_type="instruments")` |
| Browse a specific path | `get_browser_items_at_path(path)` |
| Load found item | `load_instrument_or_effect(track_index, uri)` |
| Refresh cache | `refresh_browser_cache_tool()` — run after adding new packs |

## Recording

| Goal | Tool |
|---|---|
| Session record | `trigger_session_record()` |
| Arrangement record | `start_arrangement_recording()` |
| Stop arrangement record | `stop_arrangement_recording()` |
| Capture MIDI (retroactive) | `capture_midi(track_index)` |

## Tips

- Track indices are 0-based. Return tracks are separate from regular tracks.
- Clip indices correspond to scene rows (clip slot 0 = scene 0).
- `get_full_session_state()` returns everything in one call — use it to avoid multiple round trips.
- After structural changes (create/delete track), re-fetch indices — they shift.
