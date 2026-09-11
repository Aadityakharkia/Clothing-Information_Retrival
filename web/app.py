"""
Clothing Information Retrieval Engine — Web Entry Point (Compatibility Shim)
=============================================================================
Delegates to the restructured clean architecture in backend.app.create_app().
Maintains 100% backward compatibility with legacy launch commands.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.server import app, cfg

if __name__ == "__main__":
    port = cfg.PORT
    host = cfg.HOST
    print(f"Starting Clothing IR Server via web/app.py compatibility runner on http://{host}:{port}")
    app.run(host=host, port=port, debug=cfg.DEBUG)
