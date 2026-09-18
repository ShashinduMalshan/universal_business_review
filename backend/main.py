"""
Universal Business Review Analyzer - Application Entrypoint
Forwarding import to modular backend.app.main:app
"""
import sys
from pathlib import Path

# Ensure workspace root is in python path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
