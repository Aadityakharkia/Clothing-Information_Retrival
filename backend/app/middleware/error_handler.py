"""
Global Error Handling Middleware
================================
Provides consistent, RFC 7807-compliant structured error responses for API routes
and friendly fallback handling for template views.
"""

import traceback
from flask import Flask, jsonify, request, g, render_template


def register_error_handlers(app: Flask):
    """Registers standard HTTP error handlers onto the Flask application."""

    @app.errorhandler(404)
    def handle_404(e):
        token = getattr(getattr(g, "request_trace", None), "token", "UNKNOWN")
        if request.path.startswith("/api/") or "application/json" in request.headers.get("Accept", ""):
            return jsonify({
                "success": False,
                "error": "Not Found",
                "message": f"Resource {request.path} does not exist.",
                "request_token": token,
                "status": 404
            }), 404
        return render_template("base.html"), 404

    @app.errorhandler(500)
    def handle_500(e):
        token = getattr(getattr(g, "request_trace", None), "token", "UNKNOWN")
        if request.path.startswith("/api/") or "application/json" in request.headers.get("Accept", ""):
            return jsonify({
                "success": False,
                "error": "Internal Server Error",
                "message": str(e),
                "request_token": token,
                "status": 500
            }), 500
        return f"<h1>Internal Server Error</h1><p>Trace Token: {token}</p>", 500

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        token = getattr(getattr(g, "request_trace", None), "token", "UNKNOWN")
        if request.path.startswith("/api/") or "application/json" in request.headers.get("Accept", ""):
            return jsonify({
                "success": False,
                "error": type(e).__name__,
                "message": str(e),
                "request_token": token,
                "status": 500
            }), 500
        return f"<h1>Server Error: {type(e).__name__}</h1><p>Message: {str(e)}</p><p>Trace Token: {token}</p>", 500
