"""
Assignment Packaging & Export Script
====================================
Packages deliverables bundle into final submission ZIP.
"""

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from export_deliverables import export

if __name__ == "__main__":
    export()
