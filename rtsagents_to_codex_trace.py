#!/usr/bin/env python3
"""
Tail RTSagents events.ndjson and write codex-trace.json for agentdogs viewer.
stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import deque
from pathlib import Path


def clamp(v: float, lo: float, hi: float) -> float:
    return lo if v < lo else hi if v > hi else v


def now_s() -> float:
    return time.time()


def open_tail(path: Path, from_start: bool):
    f = path.open("r", encoding="utf-8", errors="replace")
    if not from_start:
        f.seek(0, os.SEEK_END)
    return f


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True, help="events.ndjson from RTSagents")
    p.add_argument("--out", dest="out_path", required=True, help="codex-trace.json output")
    p.add_argument("--from-start", action="store_true", help="replay from start")
    p.add_argument("--interval", type=float, default=0.15, help="poll interval seconds")
    p.add_argument("--max-events", type=int, default=800, help="max events in output trace")
    args = p.parse_args(argv)

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)

    if not in_path.exists():
        print(f"missing input: {in_path}", file=sys.stderr)
        return 2

    f = open_tail(in_path, from_start=bool(args.from_start))
    t = 0.0
    step = 0
    z = 40.0
    x = 0.0
    y = 10.0

    events = deque(maxlen=int(args.max_events))

    def write_out():
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(list(events), ensure_ascii=True), encoding="utf-8")

    try:
        while True:
            line = f.readline()
            if line:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                detail = str(obj.get("detail", ""))
                action = str(obj.get("action", "edit"))

                # map action -> motion and event
                if action == "plan":
                    dx, dy, ev = 0.0, -0.6, 20
                elif action == "read":
                    dx, dy, ev = -0.8, 0.0, 15
                elif action == "test":
                    dx, dy, ev = 0.8, -0.2, 60
                elif action == "run":
                    dx, dy, ev = 0.4, 0.2, 50
                else:
                    dx, dy, ev = 0.6, 0.2, 25

                # expand one message into multiple steps so long text animates longer
                chunk = 24
                parts = [detail[i : i + chunk] for i in range(0, max(1, len(detail)), chunk)]
                for idx, part in enumerate(parts):
                    x = clamp(x + dx, -36, 36)
                    y = clamp(y + dy, 2, 48)
                    z -= 6.0
                    t = step * 0.12
                    step += 1
                    events.append({
                        "t": round(t, 3),
                        "x": round(x, 2),
                        "y": round(y, 2),
                        "z": round(z, 2),
                        "roll": 0,
                        "stage": "CD",
                        "event": ev,
                        "enemyId": action.upper()[:6],
                        "enemyDist": 0,
                        "hp": 120,
                        "note": part,
                    })

                write_out()
                continue

            time.sleep(max(0.05, float(args.interval)))
    except KeyboardInterrupt:
        return 0
    finally:
        try:
            f.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
