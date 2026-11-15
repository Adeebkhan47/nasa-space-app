"""Entrypoint for TerraNova FastAPI application on Vercel and local uvicorn."""

from __future__ import annotations

import sys
import traceback
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Ensure repository root is on sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from src.api.main import app  # noqa: E402
except Exception:
    tb = traceback.format_exc()
    print("STARTUP ERROR:\n" + tb, file=sys.stderr)
    error_app = FastAPI(title="TerraNova - Startup Diagnostic")

    @error_app.get("/{rest_of_path:path}", response_class=HTMLResponse)
    async def catch_all(rest_of_path: str = "") -> HTMLResponse:
        return HTMLResponse(
            f"<html><body style='background:#0d1117;color:#c9d1d9;font-family:monospace;padding:24px;'>"
            f"<h2 style='color:#f85149;'>FastAPI Startup Error</h2>"
            f"<p>The application encountered an error while starting:</p>"
            f"<pre style='background:#161b22;padding:16px;border-radius:6px;overflow-x:auto;white-space:pre-wrap;'>{tb}</pre>"
            f"</body></html>",
            status_code=500,
        )

    app = error_app

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
