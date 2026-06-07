---
description: >
  Deep device and parameter control in Ableton Live via the M4L Bridge — access
  hidden parameters, navigate rack chains, control Wavetable's modulation matrix,
  edit notes by ID, monitor properties in real time, and use audio analysis. Use
  when the user says "hidden parameters", "rack chain", "M4L bridge", "Wavetable
  modulation", "deep control", "monitor a parameter", "edit note in place",
  "audio analysis", "spectrum", "AB comparison", "split stereo", or any request
  that goes beyond what standard device parameters expose.
---

# Deep Control via M4L Bridge

The M4L Bridge adds 43 tools on top of the 297 Remote Script tools. It uses the
`AbletonBridge` Max for Live device (drag onto any audio track) communicating over
UDP port 9878.

## Check M4L status first

Always call `m4l_status()` before using any M4L tool. If it returns "not connected",
the device isn't loaded. Instruct the user to drag `AbletonBridge` from their User
Library onto an audio track.

## Hidden & non-automatable parameters

Standard `get_device_parameters` only returns automatable parameters. M4L exposes all:

```
discover_device_params(track_index, device_index)
# Returns ALL parameters including hidden ones, with LOM indices

get_device_hidden_parameters(track_index, device_index)
# Full detail: name, lom_index, value, min, max

set_device_hidden_parameter(track_index, device_index, param_index, value)
# Set by LOM index (not name)

batch_set_hidden_parameters(track_index, device_index, params=[
  {"index": 12, "value": 0.5},
  {"index": 17, "value": 0.8},
])
```

## Rack chain navigation

Navigate inside Instrument Racks, Audio Effect Racks, and Drum Racks:

```
discover_chains_m4l(track_index, device_index, extra_path=None)
# Returns chains with names, device lists, drum pad notes, return chains

get_chain_device_params_m4l(track_index, device_index, chain_index, chain_device_index)
# ALL parameters (including hidden) of a device inside a rack chain

set_chain_device_param_m4l(track_index, device_index, chain_index,
                            chain_device_index, param_index, value)

set_chain_mixing(track_index, device_index, chain_index,
                 properties={"volume": 0.85, "pan": 0.0, "mute": False})

get_chain_mixing(track_index, device_index, chain_index)
```

For nested racks, pass `extra_path` e.g. `"chains 0 devices 0"`.

## Wavetable modulation matrix

```
get_wavetable_info(track_index, device_index)
# Returns oscillators, filter settings, mod matrix, unison

set_wavetable_modulation(track_index, device_index,
  target_index,   # parameter to modulate (from get_wavetable_info)
  source_index,   # modulator: Env2/Env3/LFO1/LFO2
  amount          # 0.0–1.0
)
```

## Note surgery by stable ID

Edit specific notes without destructive remove+add:

```
get_clip_notes_with_ids(track_index, clip_index)
# Returns notes with stable note_ids

modify_clip_notes(track_index, clip_index, modifications=[
  {"note_id": 42, "velocity": 110, "pitch": 64},
  {"note_id": 43, "start_time": 1.5},
])

remove_clip_notes_by_id(track_index, clip_index, note_ids=[42, 43])
```

## Real-time property monitoring

```
observe_property(lom_path="live_set tracks 0", property_name="playing_slot_index")
# Starts ~10ms polling

get_property_changes()
# Returns accumulated change events since last call — call repeatedly to poll

stop_observing(lom_path, property_name)
```

## Audio analysis

```
analyze_track_audio(track_index=-1)
# LOM meter levels — any track. -1=device's track, -2=master, 0+=specific

analyze_track_spectrum()
# 8-band spectral data from the M4L device's own track

analyze_cross_track_audio(track_index, wait_ms=500)
# Real MSP analysis from any track via send routing
# M4L device must be on a return track for this
```

## Other M4L tools

| Goal | Tool |
|---|---|
| Get Ableton version | `get_ableton_version()` |
| Get automation states | `get_automation_states(track_index, device_index)` |
| Undo-clean param set | `set_parameter_clean(track_index, device_index, param_index, value)` |
| AB device comparison | `device_ab_compare(track_index, device_index, action)` — action: get_state/save/toggle |
| Scrub a clip | `clip_scrub(track_index, clip_index, action, beat_time)` |
| Split stereo panning | `get_split_stereo(track_index)` / `set_split_stereo(track_index, left, right)` |
| Rack variations | `rack_store_variation(t, d)` / `rack_recall_variation(t, d, variation_index)` |
| Get take lanes | `get_take_lanes(track_index)` |
| Insert rack chain | `rack_insert_chain(track_index, device_index, chain_index)` |
| Drum pad note | `set_drum_chain_note(track_index, device_index, chain_index, note)` |
| Arrangement clip (LOM) | `create_arrangement_midi_clip_m4l(track_index, time, length)` |
| Cue points | `get_cue_points()` / `jump_to_cue_point(cue_point_index)` |
| Groove pool | `get_groove_pool()` / `set_groove_properties(groove_index, props)` |

See `references/m4l-tools.md` for troubleshooting and OSC command details.
