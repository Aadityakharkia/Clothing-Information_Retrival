"""Routes package initialization."""
from .page_routes import page_bp
from .api_routes import api_bp

__all__ = ["page_bp", "api_bp"]
