# Mixer & Device Reference

## Volume scale
| dB | Value |
|---|---|
| −∞ (silence) | 0.0 |
| −20 dB | 0.45 |
| −6 dB | 0.72 |
| **0 dB (unity)** | **0.85** |
| +3 dB | 0.93 |
| +6 dB | 1.0 |

## batch_set_mixer — full signature
```
batch_set_mixer(settings=[
  {
    "track_index": 0,
    "volume": 0.85,       # optional
    "pan": 0.0,           # optional: -1.0=L, 0.0=centre, 1.0=R
    "mute": False,        # optional
    "solo": False,        # optional
    "arm": False,         # optional
    "send_0": 0.0,        # optional: send level for return A
    "send_1": 0.0,        # optional: send level for return B
  }
])
```

## setup_send_return — one-call scaffold
Creates a return track, loads an effect, sets send levels on source tracks:
```
setup_send_return(
  return_effect_uri="…",          # URI from search_browser
  send_values={0: 0.7, 1: 0.5},  # track_index: send_level
  return_name="Reverb"
)
```

## Saving and recalling device snapshots
```
# Save current state
snapshot_device_state(track_index=0, device_index=0, name="init")

# Recall later
restore_device_snapshot(track_index=0, device_index=0, name="init")

# List all snapshots
list_snapshots()

# Morph between two snapshots
morph_between_snapshots(
  track_index=0, device_index=0,
  snapshot_a="dry", snapshot_b="wet",
  position=0.5   # 0.0=A, 1.0=B
)
```

## Automation
```
# Create clip automation for a parameter
create_clip_automation(
  track_index=0,
  clip_index=0,
  device_index=0,
  parameter_name="Dry/Wet",
  points=[
    {"beat": 0.0, "value": 0.0},
    {"beat": 4.0, "value": 1.0},
    {"beat": 8.0, "value": 0.0},
  ]
)

# Clear automation
clear_clip_automation(track_index, clip_index, device_index, parameter_name)
```

## Getting device info
```
# Full device list for a track
get_track_info(track_index=0)  # check "devices" key

# All params for device 0 on track 0
get_device_parameters(track_index=0, device_index=0)
# Returns: [{name, value, min, max, is_quantized}, ...]

# Specific device info
get_device_info(track_index=0, device_index=0)
```
