#!/usr/bin/env bash
set -euo pipefail

RTS_DIR="/home/user/RTSagents"
GAME_DIR="/home/user/agentdogs"

BRIDGE_LOG="$RTS_DIR/bridge.log"
TRACE_LOG="$GAME_DIR/trace_bridge.log"

# stop existing
pkill -f "$RTS_DIR/codex_cli_bridge.py" >/dev/null 2>&1 || true
pkill -f "$GAME_DIR/rtsagents_to_codex_trace.py" >/dev/null 2>&1 || true

# ensure files exist
: > "$BRIDGE_LOG"
: > "$TRACE_LOG"

nohup python3 "$RTS_DIR/codex_cli_bridge.py" --log "$RTS_DIR/events.ndjson" --follow-latest --verbose > "$BRIDGE_LOG" 2>&1 &
nohup python3 "$GAME_DIR/rtsagents_to_codex_trace.py" --in "$RTS_DIR/events.ndjson" --out "$GAME_DIR/codex-trace.json" --from-start > "$TRACE_LOG" 2>&1 &

echo "Started bridges. Logs:"
echo "- $BRIDGE_LOG"
echo "- $TRACE_LOG"
