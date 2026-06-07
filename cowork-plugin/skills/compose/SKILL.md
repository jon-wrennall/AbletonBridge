---
description: >
  Compose music in Ableton Live — create beats, melodies, chord progressions,
  bass lines, arpeggios, and drum patterns. Use when the user says "create a beat",
  "write a melody", "add chords", "compose a progression", "make a drum pattern",
  "generate a bass line", "add notes", "write some MIDI", or any request to create
  musical content in Ableton.
---

# Compose in Ableton

You have full MIDI composition capability via AbletonBridge. Use the tools below
to turn musical ideas into clips in Ableton Live.

## Core workflow

1. **Get session state first** — call `get_session_info` to confirm tempo, time
   signature, and available tracks before creating anything.
2. **Target the right track** — use `get_all_tracks_info` to find or confirm track
   indices. Create a new MIDI track with `create_midi_track` if needed.
3. **Create and fill clips** — use `create_clip_with_notes` to create a clip and add
   notes in one step, or `create_clip` then `add_notes_to_clip` for more control.
4. **Use creative generators** for speed — see references for tool details.
5. **Fire the clip** to audition — `fire_clip(track_index, clip_index)`.

## Key composition tools

| Goal | Tool |
|---|---|
| Create clip + notes in one step | `create_clip_with_notes` |
| Add notes to existing clip | `add_notes_to_clip` |
| Generate chord progression | `generate_chord_progression` |
| Generate drum pattern | `generate_drum_pattern` |
| Generate bass line | `generate_bass_line` |
| Generate arpeggio | `generate_arpeggio` |
| Euclidean rhythm | `generate_euclidean_rhythm` |
| Harmonise a melody | `harmonize_melody` |
| Quantize notes | `quantize_clip_notes` |
| Transpose notes | `transpose_clip_notes` |
| Humanise timing/velocity | `humanize_notes` |
| Randomise notes | `randomize_clip_notes` |

## Note format

Notes are dicts with: `pitch` (MIDI 0–127), `start_time` (beats), `duration` (beats),
`velocity` (1–127). Middle C = 60. One bar = 4.0 beats.

```
C4=60, D4=62, E4=64, F4=65, G4=67, A4=69, B4=71, C5=72
```

## Tips

- Always confirm the track has a MIDI instrument loaded before adding notes —
  use `get_track_info` to check. Load one with `load_instrument_or_effect` if empty.
- Set tempo before composing: `set_tempo(bpm)`.
- For drum patterns, use `create_drum_track` for a fully scaffolded drum rack + clip.
- `generate_chord_progression` returns a list of clips — fire them in sequence or
  merge notes manually.

See `references/creative-tools.md` for full argument details and examples.
