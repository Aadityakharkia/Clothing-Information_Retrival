"""
Request Tracing Context Model
=============================
"""

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, Optional


@dataclass
class RequestTrace:
    """Encapsulates telemetry metadata for an individual HTTP request."""
    token: str = field(default_factory=lambda: f"REQ-{uuid.uuid4().hex[:6].upper()}")
    start_time: float = field(default_factory=time.time)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    method: str = "GET"
    path: str = "/"
    query_params: Dict[str, Any] = field(default_factory=dict)
    client_ip: str = "127.0.0.1"
    status_code: int = 200
    duration_ms: float = 0.0

    def finalize(self, status_code: int) -> "RequestTrace":
        self.status_code = status_code
        self.duration_ms = round((time.time() - self.start_time) * 1000, 2)
        return self

    def to_log_entry(self) -> Dict[str, Any]:
        return {
            "token": self.token,
            "timestamp": self.timestamp,
            "method": self.method,
            "path": self.path,
            "query": self.query_params.get("q", "") or self.query_params.get("term1", ""),
            "params": self.query_params,
            "status": self.status_code,
            "duration_ms": self.duration_ms,
            "client_ip": self.client_ip
        }
