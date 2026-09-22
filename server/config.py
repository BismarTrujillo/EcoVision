"""Environment configuration.

Importing this module loads server/.env (if present) and fails fast if
GEMINI_API_KEY isn't set anywhere - main.py imports this before anything
else so the process refuses to start without it, same as before.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("GEMINI_API_KEY"):
    print(
        "ERROR: GEMINI_API_KEY environment variable is not set.\n"
        "Set it before running this script, e.g.:\n"
        "    setx GEMINI_API_KEY \"your-api-key-here\"   (Windows, new shells)\n"
        "    $env:GEMINI_API_KEY = \"your-api-key-here\" (PowerShell, current shell)\n"
        "    or create server/.env with GEMINI_API_KEY=your-api-key-here"
    )
    sys.exit(1)

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
