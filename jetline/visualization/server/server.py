from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from flaskwebgui import FlaskUI
from typing import Any

app: FastAPI = FastAPI()

@app.get("/")
async def index(request: Request) -> FileResponse:
    """
    Returns the index.html file.
    """
    return FileResponse('dist/index.html')

@app.get("/assets/{file_path:path}")
async def assets(file_path: str) -> Any:
    """
    Returns the requested asset file from the 'dist/assets' directory.
    """
    return FileResponse(f"dist/assets/{file_path}")

if __name__ == "__main__":
    # Run the FastAPI application using FlaskUI
    FlaskUI(app=app, server="fastapi").run()
