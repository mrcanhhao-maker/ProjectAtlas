from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional


class SessionRecorder:
    """
    Production JSONL recorder for virtual rowing sessions.

    This recorder stores one JSON object per line.
    It is intentionally independent from BLE, FTMS, and MyWhoosh.
    """

    def __init__(self, output_dir: str = "sessions", prefix: str = "rowing_session") -> None:
        self.output_dir = Path(output_dir)
        self.prefix = str(prefix)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._path: Optional[Path] = None
        self._file = None
        self._started_at: Optional[float] = None
        self._event_count = 0

    @property
    def path(self) -> Optional[Path]:
        return self._path

    @property
    def event_count(self) -> int:
        return self._event_count

    @property
    def is_open(self) -> bool:
        return self._file is not None

    def start(self, timestamp: Optional[float] = None) -> Path:
        if self._file is not None:
            return self._path  # type: ignore[return-value]

        now = float(timestamp if timestamp is not None else time.time())
        self._started_at = now

        safe_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(now))
        self._path = self.output_dir / f"{self.prefix}_{safe_stamp}.jsonl"
        self._file = self._path.open("a", encoding="utf-8")

        self.record_event(
            "session_start",
            {
                "started_at": now,
                "file": str(self._path),
            },
            timestamp=now,
        )
        return self._path

    def record_state(
        self,
        rower_state: Dict[str, Any],
        stroke_data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[float] = None,
    ) -> None:
        if self._file is None:
            self.start(timestamp=timestamp)

        payload = {
            "rower_state": dict(rower_state),
            "stroke_data": dict(stroke_data or {}),
        }
        self.record_event("rower_state", payload, timestamp=timestamp)

    def record_event(self, event_type: str, payload: Dict[str, Any], timestamp: Optional[float] = None) -> None:
        if self._file is None:
            self.start(timestamp=timestamp)

        now = float(timestamp if timestamp is not None else time.time())
        event = {
            "timestamp": now,
            "event_type": str(event_type),
            "payload": payload,
        }

        assert self._file is not None
        self._file.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        self._file.flush()
        self._event_count += 1

    def stop(self, timestamp: Optional[float] = None) -> Optional[Path]:
        if self._file is None:
            return self._path

        now = float(timestamp if timestamp is not None else time.time())
        self.record_event(
            "session_stop",
            {
                "started_at": self._started_at,
                "stopped_at": now,
                "event_count": self._event_count + 1,
            },
            timestamp=now,
        )

        self._file.close()
        self._file = None
        return self._path

    def __enter__(self) -> "SessionRecorder":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()
