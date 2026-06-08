# Extensions SDK Bridge (Optional)

An optional third parameter transport for AbletonBridge that uses Ableton's
officially-documented Extensions SDK (Live 12.4.5+ Suite beta).

## Why use it?

The _Framework Remote Script and M4L bridge expose parameters through
Ableton's internal Python APIs. The Extensions SDK uses async JavaScript
LiveAPI calls — more reliable for VST3/AU plugins on Apple Silicon and for
plugins with large parameter sets.

When active, `get_device_parameters` and `set_device_parameter` automatically
prefer the SDK tier. Everything falls back gracefully if it's not running.

## Three-tier routing

```
get_device_parameters / set_device_parameter
  │
  ├─ 1. Extensions SDK (HTTP :9883)   ← if running
  ├─ 2. M4L bridge (UDP :9878/9879)  ← if M4L device loaded (hidden params)
  └─ 3. _Framework (TCP :9877)        ← always available
```

## Requirements

- Ableton Live **12.4.5+ Suite beta**
- Node.js **v20+**
- Ableton [Extensions SDK](https://ableton.github.io/extensions-sdk)

## Setup

### 1. Get the Extensions SDK

Download from [Ableton's beta program](https://www.ableton.com/beta/) and
place the SDK folder alongside `AbletonParameterBridge/`.

### 2. Build the bridge

```bash
cd AbletonParameterBridge
npm install
npm run build
npx extensions-cli package .
```

This produces `Parameter-Bridge-1.0.0.ablx`.

### 3. Install in Live

1. Open **Live → Settings → Extensions**
2. Enable **Developer Mode**
3. Drag `Parameter-Bridge-1.0.0.ablx` into the drop zone
4. Restart Live when prompted

### 4. Run the bridge

```bash
cd AbletonParameterBridge
npx extensions-cli run --live "/Applications/Ableton Live 12 Beta.app" .
```

The bridge listens on **HTTP port 9883**. Keep this terminal open while using
the MCP server.

### 5. Verify

```
get_bridge_status
```

Should show `Extensions SDK bridge: ACTIVE (HTTP port 9883)`.

## Auto-start (macOS)

See the `AbletonParameterBridge/` README for LaunchAgent setup.

## Notes

- Port 9883 is used to avoid conflicts with M4L (9878/9879), dashboard (9880),
  and the singleton lock (9881).
- The bridge only helps with standard track devices (`track_type="track"`).
  Return/master tracks still use _Framework.
- `save_device_snapshot` and `recall_device_snapshot` also benefit from the SDK
  when it is active — snapshot capture is async and more accurate.
