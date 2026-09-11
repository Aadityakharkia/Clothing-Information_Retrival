"""
Configuration Management for Clothing Information Retrieval Engine
====================================================================
Provides centralized, environment-aware configuration for development,
testing, and production environments.
"""

import os
from pathlib import Path

# Base directories
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"


class Config:
    """Base Configuration."""
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "127.0.0.1")

    # File paths
    CORPUS_PATH = os.getenv("CORPUS_PATH", str(DATA_DIR / "corpus.txt"))
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", str(OUTPUT_DIR))
    REQUEST_LOG_PATH = os.getenv("REQUEST_LOG_PATH", str(OUTPUT_DIR / "request_log.jsonl"))

    # Frontend paths
    TEMPLATE_FOLDER = str(FRONTEND_DIR / "templates")
    STATIC_FOLDER = str(FRONTEND_DIR / "static")

    # IR Hyperparameters
    TOTAL_DOCS = 100
    DEFAULT_TOP_K = 10
    DEFAULT_PROXIMITY_K = 3
    DEFAULT_HYBRID_LAMBDA = 0.5


class DevelopmentConfig(Config):
    """Development Configuration."""
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    """Testing Configuration."""
    ENV = "testing"
    TESTING = True
    DEBUG = False


def get_config():
    """Returns the active configuration object based on FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "testing":
        return TestingConfig()
    elif env == "production":
        return Config()
    return DevelopmentConfig()
