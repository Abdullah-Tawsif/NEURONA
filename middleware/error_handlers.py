import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

logger = logging.getLogger("neurona")

ERROR_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Error - Neurona</title></head>
<body style="font-family:sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#0f0f0f;color:#fff;">
  <div style="text-align:center">
    <h1>{status_code}</h1>
    <p>{message}</p>
    <a href="/" style="color:#A68B5C">Back to Home</a>
  </div>
</body>
</html>
"""


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(404)
    async def not_found(request: Request, exc):
        logger.warning("404: %s", request.url.path)
        return HTMLResponse(
            ERROR_PAGE_HTML.format(status_code=404, message="Page not found"),
            status_code=404,
        )

    @app.exception_handler(500)
    async def server_error(request: Request, exc):
        logger.error("500: %s - %s", request.url.path, exc)
        return HTMLResponse(
            ERROR_PAGE_HTML.format(status_code=500, message="Internal server error"),
            status_code=500,
        )
