"""Web status dashboard HTTP server for AbletonBridge.

Provides a lightweight Starlette/Uvicorn HTTP server that serves the
real-time status dashboard and a JSON API endpoint.  All mutable state
is accessed via ``MCP_Server.state``.
"""

import logging
import time
import threading
import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List

import MCP_Server.state as state
from MCP_Server.dashboard.html import DASHBOARD_HTML

logger = logging.getLogger("AbletonBridge")


# ---------------------------------------------------------------------------
# Dashboard log handler
# ---------------------------------------------------------------------------

class DashboardLogHandler(logging.Handler):
    """Captures log records into the dashboard ring buffer.

    Stores lightweight tuples (created_float, level_str, message_str) to
    avoid formatting timestamps on every log message.  Timestamps are
    formatted only when the dashboard is actually viewed.
    """

    def emit(self, record):
        try:
            with state.server_log_lock:
                state.server_log_buffer.append(
                    (record.created, record.levelname, record.getMessage())
                )
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Helper: summarize tool arguments for the dashboard log
# ---------------------------------------------------------------------------

def summarize_args(args: dict) -> str:
    """Create a short summary of tool arguments for the dashboard log."""
    if not args:
        return ""
    parts = []
    for k, v in list(args.items())[:3]:
        sv = str(v)
        if len(sv) > 40:
            sv = sv[:37] + "..."
        parts.append(f"{k}={sv}")
    suffix = f" +{len(args)-3} more" if len(args) > 3 else ""
    return ", ".join(parts) + suffix


# ---------------------------------------------------------------------------
# Status data helpers
# ---------------------------------------------------------------------------

def get_server_version() -> str:
    """Get server version from package metadata, with fallback."""
    try:
        from importlib.metadata import version as _pkg_version
        return _pkg_version("ableton-bridge")
    except Exception:
        from MCP_Server import __version__
        return __version__


def get_m4l_status() -> tuple:
    """Return (sockets_ready, bridge_responding) with cached ping."""
    sockets_ready = bool(state.m4l_connection and state.m4l_connection._connected)
    if not sockets_ready:
        return False, False

    now = time.time()
    if now - state.m4l_ping_cache["timestamp"] < state.M4L_PING_CACHE_TTL:
        return sockets_ready, state.m4l_ping_cache["result"]

    try:
        result = state.m4l_connection.ping()
    except Exception as e:
        logger.debug("Dashboard M4L ping failed: %s", e)
        result = False

    state.m4l_ping_cache["result"] = result
    state.m4l_ping_cache["timestamp"] = now
    return sockets_ready, result


def get_connection_tiers() -> dict:
    """Return status of every parameter/control transport tier."""
    tiers = {}

    # --- Tier 1: Remote Script (TCP 9877) ---
    ableton_ok = False
    ableton_version = None
    if state.ableton_connection and state.ableton_connection.sock:
        try:
            state.ableton_connection.sock.getpeername()
            ableton_ok = True
        except Exception:
            pass
    # Pull Ableton version from M4L state if available (M4L is the reliable source)
    if getattr(state, 'm4l_connected', False) and getattr(state, 'm4l_ableton_version', None):
        ableton_version = state.m4l_ableton_version
    tiers["remote_script"] = {
        "label": "Remote Script (TCP 9877)",
        "ok": ableton_ok,
        "detail": f"Ableton Live {ableton_version}" if ableton_version else ("Connected" if ableton_ok else "Not connected — load AbletonBridge in Control Surfaces"),
        "tier": 1,
    }

    # --- Tier 2: M4L Bridge (UDP 9878/9879) ---
    m4l_sockets, m4l_ok = get_m4l_status()
    tiers["m4l_bridge"] = {
        "label": "M4L Bridge (UDP 9878→9879)",
        "ok": m4l_ok,
        "detail": (
            f"v{state.m4l_bridge_version} connected" if m4l_ok and state.m4l_bridge_version
            else "Device responding" if m4l_ok
            else "Sockets bound, device not responding — drag AbletonBridge.amxd onto an audio track" if m4l_sockets
            else "Not loaded — optional deep-parameter tools unavailable"
        ),
        "warn": m4l_ok and state.m4l_version_match is False,
        "optional": True,
        "tier": 2,
    }

    # --- Tier 3: Extensions SDK (HTTP 9878/health) ---
    # The Parameter Bridge extension serves HTTP on TCP 9878 (distinct from M4L UDP 9878).
    # It only starts after Live calls activate() on the extension.
    sdk_ok = False
    sdk_version = None
    sdk_detail = (
        "Not active — to start: (1) open a Live Set in Ableton 12 Beta, "
        "(2) enable Developer Mode in Preferences → Extensions, "
        "(3) run 'npm start' in the AbletonParameterBridge folder"
    )
    try:
        import urllib.request, json as _json
        with urllib.request.urlopen("http://127.0.0.1:9878/health", timeout=0.5) as r:
            if r.status == 200:
                sdk_ok = True
                try:
                    body = _json.loads(r.read().decode())
                    sdk_version = body.get("version") or body.get("live_version")
                except Exception:
                    pass
                sdk_detail = f"Connected — Live {sdk_version} SDK active" if sdk_version else "Connected — Live 12.4.5+ SDK active"
    except Exception:
        pass
    tiers["extensions_sdk"] = {
        "label": "Extensions SDK (TCP 9878/health)",
        "ok": sdk_ok,
        "detail": sdk_detail,
        "optional": True,
        "tier": 3,
    }

    # --- MIDI CC virtual port ---
    cc_ok = False
    cc_detail = "mido / python-rtmidi not installed"
    try:
        import mido
        port_names = mido.get_output_names()
        if "AbletonBridge" in port_names:
            cc_ok = True
            cc_detail = "Virtual MIDI port open — 100 plugin maps loaded"
        else:
            cc_ok = True  # mido available, port will be created on first use
            cc_detail = "Ready — virtual port will open on first CC send"
    except ImportError:
        pass
    tiers["midi_cc"] = {
        "label": "MIDI CC (virtual port)",
        "ok": cc_ok,
        "detail": cc_detail,
        "optional": True,
        "tier": None,
    }

    return tiers


def build_status_json() -> dict:
    """Collect all dashboard status data into a JSON-serializable dict."""
    connection_tiers = get_connection_tiers()
    ableton_connected = connection_tiers["remote_script"]["ok"]
    m4l_sockets_ready, m4l_connected = get_m4l_status()

    with state.tool_call_lock:
        recent = list(state.tool_call_log)
        total = sum(state.tool_call_counts.values())
        top_tools = sorted(state.tool_call_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    with state.server_log_lock:
        # Format timestamps from stored tuples (created_float, level, msg)
        server_logs = [
            {"ts": datetime.fromtimestamp(ts).strftime("%H:%M:%S"), "level": lvl, "msg": msg}
            for ts, lvl, msg in state.server_log_buffer
        ]

    # Dynamic tool count via the mcp instance stored in state
    mcp = state.mcp_instance
    tool_count = len(mcp._tool_manager._tools) if mcp and hasattr(mcp, '_tool_manager') else 331

    now = time.time()
    m4l_last_seen = None
    if state.m4l_last_success_time:
        elapsed = now - state.m4l_last_success_time
        if elapsed < 60:
            m4l_last_seen = f"{int(elapsed)}s ago"
        elif elapsed < 3600:
            m4l_last_seen = f"{int(elapsed/60)}m ago"
        else:
            m4l_last_seen = f"{int(elapsed/3600)}h ago"

    return {
        "version": get_server_version(),
        "uptime_seconds": round(now - state.server_start_time, 1) if state.server_start_time else 0,
        "ableton_connected": ableton_connected,
        "m4l_connected": m4l_connected,
        "m4l_sockets_ready": m4l_sockets_ready,
        "m4l_bridge_version": state.m4l_bridge_version or None,
        "m4l_version_match": state.m4l_version_match,
        "m4l_last_seen": m4l_last_seen,
        "store_counts": {
            "snapshots": len(state.snapshot_store),
            "macros": len(state.macro_store),
            "param_maps": len(state.param_map_store),
        },
        "total_tool_calls": total,
        "top_tools": top_tools,
        "recent_calls": recent,
        "server_logs": server_logs,
        "tool_count": tool_count,
        "connection_tiers": connection_tiers,
    }


# ---------------------------------------------------------------------------
# Dashboard HTTP server lifecycle
# ---------------------------------------------------------------------------

def start_dashboard_server():
    """Start the dashboard HTTP server on a background thread."""
    from starlette.applications import Starlette
    from starlette.responses import HTMLResponse, JSONResponse
    from starlette.routing import Route
    import uvicorn

    async def dashboard_page(request):
        return HTMLResponse(DASHBOARD_HTML)

    async def api_status(request):
        return JSONResponse(build_status_json())

    app = Starlette(routes=[
        Route("/", dashboard_page),
        Route("/api/status", api_status),
    ])

    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=state.DASHBOARD_PORT,
        log_level="warning",
        access_log=False,
    )
    state.dashboard_server = uvicorn.Server(config)

    def _run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(state.dashboard_server.serve())

    thread = threading.Thread(target=_run, daemon=True, name="dashboard-http")
    thread.start()
    logger.info("Dashboard started at http://127.0.0.1:%d", state.DASHBOARD_PORT)


def stop_dashboard_server():
    """Signal the dashboard server to shut down."""
    if state.dashboard_server:
        state.dashboard_server.should_exit = True
        state.dashboard_server = None
        logger.info("Dashboard server stopped")
