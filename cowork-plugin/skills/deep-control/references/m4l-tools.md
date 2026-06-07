# M4L Bridge Reference

## Architecture
```
Claude → MCP Server (TCP:9877 Remote Script) → Ableton Live
                   ↕ UDP:9878/9879
              M4L Bridge device (AbletonBridge.amxd on any audio track)
```

## Status check
```
m4l_status()
# "M4L bridge connected (v4.0.0)"  ← working
# "M4L bridge not connected"        ← device not loaded / wrong mode
```

## Troubleshooting

**"M4L bridge not connected"**
1. Open Ableton → User Library → Presets → Audio Effects → Max Audio Effect
2. Drag `AbletonBridge` onto any audio track
3. Ensure the patch is **locked** (not in Max edit mode)
4. Call `m4l_status()` again

**Timeout on M4L calls**
- Check the Max patch isn't in edit mode (close Max editor window)
- Try removing and re-adding the device
- Double-click `[js m4l_bridge.js]` in Max editor to reload script

**Spectrum data all zeros**
- Audio must be playing through the device's track
- Device must be an Audio Effect (not MIDI Effect)
- On MIDI tracks, device must be after an instrument

**cross_track analysis returns zeros**
- Device must be on a **return track** for cross-track MSP analysis
- Increase `wait_ms` (try 1000)
- LOM meters (`analyze_track_audio`) always work from any track

## Simpler / Sample deep access
```
get_simpler_properties(track_index, device_index)
# Returns: playback_mode, sample_path, start_marker, end_marker, loop_start,
#          loop_end, warp_mode, gain, slices

set_simpler_properties(track_index, device_index,
  start_marker=0.0,
  end_marker=1.0,
  warp_mode=0,      # 0=Beats 1=Tones 2=Texture 3=Re-Pitch 4=Complex 5=Complex Pro
  gain=1.0
)

simpler_sample_action(track_index, device_index, action, slice_time=None)
# actions: "insert_slice", "remove_slice", "move_slice", "clear_slices", "reset_slices"
```

## Groove pool
```
get_groove_pool()
# Returns all grooves with: name, base, timing, velocity, random, quantize_rate

set_groove_properties(groove_index, properties={
  "base": 0.5,        # 0.0–1.0
  "timing": 0.75,     # 0.0–1.0
  "velocity": 0.5,    # 0.0–1.0
  "random": 0.1,      # 0.0–1.0
  "quantize_rate": 4  # 4=1/4, 8=1/8, 16=1/16
})
```

## Property monitoring example
```
# Watch which clip is playing on track 0
observe_property("live_set tracks 0", "playing_slot_index")

# Poll for changes
changes = get_property_changes()
# [{"path": "live_set tracks 0", "property": "playing_slot_index", "value": 2}]

# Stop watching
stop_observing("live_set tracks 0", "playing_slot_index")
```

## Common LOM paths
```
"live_set"                          # song
"live_set tracks 0"                 # first track
"live_set tracks 0 clip_slots 0"    # first clip slot on first track
"live_set tracks 0 devices 0"       # first device on first track
"live_set master_track"             # master track
"live_set return_tracks 0"          # first return track
```
