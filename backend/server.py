"""
Server Entry Point for Clothing IR Engine
=========================================
Runs the Flask application server with CLI support.
"""

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Also ensure backend is in sys.path
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.app import create_app
from backend.config import get_config

cfg = get_config()
app = create_app(cfg)

if __name__ == "__main__":
    port = int(os.getenv("PORT", cfg.PORT))
    host = os.getenv("HOST", cfg.HOST)
    debug = cfg.DEBUG
    print(f"============================================================")
    print(f"Clothing Information Retrieval Engine (CSD358)")
    print(f"Server starting on http://{host}:{port}")
    print(f"Templates: {cfg.TEMPLATE_FOLDER}")
    print(f"Static:    {cfg.STATIC_FOLDER}")
    print(f"Corpus:    {cfg.CORPUS_PATH}")
    print(f"Log:       {cfg.REQUEST_LOG_PATH}")
    print(f"============================================================")
    app.run(host=host, port=port, debug=debug)
