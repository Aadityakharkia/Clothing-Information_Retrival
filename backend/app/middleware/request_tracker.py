"""
Request Tracker & Tokenization Middleware
=========================================
Generates unique request trace tokens, tracks execution latency,
attaches audit headers to HTTP responses, and asynchronously/safely writes
structured telemetry events to output/request_log.jsonl.
"""

import json
import os
import threading
from flask import Flask, request, g, Response
from ..models.request_token import RequestTrace

_log_lock = threading.Lock()


class RequestTrackerMiddleware:
    """Flask extension for request tracking and audit logging."""

    def __init__(self, app: Flask = None, log_file_path: str = None):
        self.log_file_path = log_file_path
        if app:
            self.init_app(app, log_file_path)

    def init_app(self, app: Flask, log_file_path: str = None):
        self.log_file_path = log_file_path or app.config.get("REQUEST_LOG_PATH", "output/request_log.jsonl")

        # Ensure directory exists
        log_dir = os.path.dirname(os.path.abspath(self.log_file_path))
        os.makedirs(log_dir, exist_ok=True)

        @app.before_request
        def before_request():
            # Honor incoming client token or generate new one
            incoming_token = request.headers.get("X-Request-Token")
            trace = RequestTrace()
            if incoming_token:
                trace.token = incoming_token
            trace.method = request.method
            trace.path = request.path
            trace.query_params = dict(request.args)
            trace.client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "127.0.0.1")
            g.request_trace = trace

        @app.after_request
        def after_request(response: Response):
            trace: RequestTrace = getattr(g, "request_trace", None)
            if trace:
                trace.finalize(response.status_code)
                # Inject trace headers
                response.headers["X-Request-Token"] = trace.token
                response.headers["X-Response-Time-Ms"] = str(trace.duration_ms)

                # Append to JSONL audit log (thread-safe)
                self._write_log(trace)

            return response

    def _write_log(self, trace: RequestTrace):
        try:
            log_line = json.dumps(trace.to_log_entry()) + "\n"
            with _log_lock:
                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    f.write(log_line)
        except Exception:
            # Telemetry logging should never crash request flow
            pass
