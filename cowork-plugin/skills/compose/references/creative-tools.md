# Creative Tool Reference

## generate_chord_progression
```
generate_chord_progression(
  track_index,
  clip_index,
  root_note="C",        # C D E F G A B
  scale="major",        # major minor dorian mixolydian phrygian lydian locrian
                        # pentatonic blues whole_tone chromatic
  progression="I-IV-V-I",  # Roman numeral or list e.g. ["I","IV","V","I"]
  bars=4,
  octave=4,
  chord_type="triad"    # triad seventh ninth
)
```

## generate_drum_pattern
```
generate_drum_pattern(
  track_index,
  clip_index,
  style="basic_rock",   # basic_rock house techno hiphop jazz reggae afrobeat
  bars=2,
  swing=0.0             # 0.0–1.0
)
```

## generate_bass_line
```
generate_bass_line(
  track_index,
  clip_index,
  root_note="C",
  scale="minor",
  style="walking",      # walking simple funky
  bars=4,
  octave=2
)
```

## generate_arpeggio
```
generate_arpeggio(
  track_index,
  clip_index,
  root_note="C",
  chord_type="minor7",  # major minor maj7 minor7 dom7 dim aug sus2 sus4
  pattern="up",         # up down up_down random
  rate=0.25,            # note duration in beats
  octaves=2,
  bars=4
)
```

## generate_euclidean_rhythm
```
generate_euclidean_rhythm(
  track_index,
  clip_index,
  pulses=3,        # number of hits
  steps=8,         # total steps
  pitch=60,        # MIDI note
  bars=1,
  velocity=100
)
```

## create_drum_track
Full scaffold: creates a MIDI track, loads Drum Rack, and fills a clip.
```
create_drum_track(
  track_index=-1,       # -1 = append
  style="basic_rock",
  bars=2,
  track_name="Drums"
)
```

## harmonize_melody
```
harmonize_melody(
  track_index,
  clip_index,
  harmony_track_index,
  harmony_clip_index,
  interval=7,           # semitones (7 = perfect fifth)
  scale="major",
  root_note="C"
)
```

## create_clip_with_notes
Most efficient single-call composition:
```
create_clip_with_notes(
  track_index,
  clip_index,
  length=4.0,           # bars × 4
  notes=[
    {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
    {"pitch": 64, "start_time": 0.5, "duration": 0.5, "velocity": 90},
  ],
  name="My Clip"        # optional
)
```
