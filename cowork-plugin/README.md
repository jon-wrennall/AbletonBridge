# AbletonBridge Cowork Plugin

Full Ableton Live control from Claude Cowork via the AbletonBridge MCP server.

## Requirements

- Ableton Live 11+ (Suite recommended for M4L tools)
- AbletonBridge installed and running:
  - Remote Script at `~/Music/Ableton/User Library/Remote Scripts/AbletonBridge`
  - MCP server at `/Users/jonwrennall/Documents/Claude/Projects/Music/AbletonBridge`
- For M4L tools: `AbletonBridge.amxd` loaded on an audio track in your session

## Skills

| Skill | Triggers |
|---|---|
| **Compose** | "create a beat", "write a melody", "add chords", "drum pattern", "bass line" |
| **Mix** | "mix", "add reverb", "EQ", "sound design", "load an effect", "set volume" |
| **Session** | "play", "stop", "set tempo", "what tracks", "fire scene", "session overview" |
| **Deep Control** | "hidden parameters", "rack chain", "M4L", "Wavetable modulation", "audio analysis" |

## MCP Server

The plugin connects to the AbletonBridge MCP server (`uv run ... MCP_Server/server.py`).
Ableton must be open with the AbletonBridge Remote Script active for tools to work.
