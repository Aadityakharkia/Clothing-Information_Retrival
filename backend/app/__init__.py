"""
Application Factory for Clothing Information Retrieval Engine
=============================================================
"""

import os
from flask import Flask
from ..config import Config, get_config
from .middleware import RequestTrackerMiddleware, register_error_handlers
from .routes import page_bp, api_bp
from .services import get_ir_system


def create_app(config_object=None) -> Flask:
    """
    Creates and configures the Flask application.
    """
    cfg = config_object or get_config()

    app = Flask(
        __name__,
        template_folder=cfg.TEMPLATE_FOLDER,
        static_folder=cfg.STATIC_FOLDER,
        static_url_path="/static"
    )

    # Load configuration
    app.config.from_object(cfg)

    # Register Middlewares
    RequestTrackerMiddleware(app, log_file_path=cfg.REQUEST_LOG_PATH)
    register_error_handlers(app)

    # Register Blueprints
    app.register_blueprint(page_bp)
    app.register_blueprint(api_bp)

    # Pre-warm IR System Index if corpus exists
    corpus_file = cfg.CORPUS_PATH
    if os.path.exists(corpus_file):
        try:
            get_ir_system(corpus_file)
        except Exception as e:
            app.logger.warning(f"Failed to pre-warm IR index: {e}")

    return app
