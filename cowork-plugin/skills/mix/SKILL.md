---
description: >
  Mix and do sound design in Ableton Live — set levels, panning, sends, load
  effects, control device parameters, and build effect chains. Use when the user
  says "mix", "set the volume", "add reverb", "apply compression", "EQ this track",
  "sound design", "load an effect", "build an effects chain", "set a parameter",
  "save a preset", or any request about audio processing or mixing.
---

# Mix & Sound Design in Ableton

You control every mixing and device parameter in the session via AbletonBridge.

## Core workflow

1. **Get session state** — `get_session_info` and `get_all_tracks_info` to orient.
2. **Target tracks by index** — indices are 0-based. Master track uses `get_master_track_info`.
3. **Set mixer values** — volume, pan, sends, mute, solo in one call with `batch_set_mixer`.
4. **Load and configure devices** — use the browser to find, then `load_instrument_or_effect`.
5. **Get and set parameters** — `get_device_parameters` then `set_device_parameter`.

## Mixer tools

| Goal | Tool |
|---|---|
| Set volume / pan / mute / solo | `set_mixer(track_index, volume, pan, mute, solo)` |
| Set multiple tracks at once | `batch_set_mixer(settings=[{track_index, volume, pan, ...}])` |
| Set a send level | `set_track_send(track_index, send_index, value)` |
| Set crossfader | `set_crossfader(value)` — 0.0=A, 0.5=centre, 1.0=B |
| Arm / disarm track | `set_track_arm(track_index, armed)` |
| Mute / unmute | `set_mixer(track_index, mute=True/False)` |

**Volume scale:** 0.0=−∞dB, **0.85≈0dB**, 1.0≈+6dB. Always use 0.85 for unity gain.

## Device tools

| Goal | Tool |
|---|---|
| Search for a device | `search_browser(query)` |
| Load onto a track | `load_instrument_or_effect(track_index, uri)` |
| List devices on track | `get_track_info(track_index)` — check `devices` list |
| Get all parameters | `get_device_parameters(track_index, device_index)` |
| Set one parameter | `set_device_parameter(track_index, device_index, parameter_name, value)` |
| Set multiple parameters | `set_device_parameters(track_index, device_index, params={name: value})` |
| Enable / disable device | `set_device_enabled(track_index, device_index, enabled)` |
| Save snapshot | `snapshot_device_state(track_index, device_index, name)` |
| Restore snapshot | `restore_device_snapshot(track_index, device_index, name)` |

## Effect chain tools

| Goal | Tool |
|---|---|
| Save chain as template | `save_effect_chain(track_index, name)` |
| Load saved chain | `load_effect_chain(track_index, name)` |
| Apply chain from template | `apply_effect_chain(track_index, template_name)` |
| List saved chains | `list_effect_chain_templates()` |

## Common device parameter names

- **EQ Eight**: `"1 Frequency"`, `"1 Gain"`, `"1 Q"`, `"1 Filter On"` (1–8 for each band)
- **Compressor**: `"Threshold"`, `"Ratio"`, `"Attack Time"`, `"Release Time"`, `"Gain"`, `"Knee"`, `"Lookahead"`
- **Reverb**: `"Room Size"`, `"Decay Time"`, `"Wet"`, `"Dry"`
- **Delay**: `"Delay Time"`, `"Feedback"`, `"Dry/Wet"`
- **Auto Filter**: `"Frequency"`, `"Resonance"`, `"Filter Type"`, `"Drive"`, `"Dry/Wet"`

## Tips

- Use `search_browser("eq eight")` to get the URI, then `load_instrument_or_effect` with that URI.
- Use `get_device_parameters` before setting — it shows exact parameter names and value ranges.
- Device index is 0-based per track (first device = 0).
- Use `setup_send_return(return_track_effect_uri, send_values)` to scaffold a send/return chain in one call.

See `references/mixer-and-devices.md` for parameter value ranges and advanced patterns.
