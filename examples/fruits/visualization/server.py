from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from flaskwebgui import FlaskUI
from typing import Any
import os
import json
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = FastAPI()
# CORS-Einstellungen
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request) -> FileResponse:
    """
    Returns the index.html file.
    """
    return FileResponse('dist/index.html')


@app.get("/pipe_data")
async def pipe_data(request: Request) -> JSONResponse:
    """
    Returns data from viz-data.json.
    """
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Erstellen Sie den vollständigen Dateipfad zur JSON-Datei
        file_path = os.path.join(base_path, "dist", "viz-data.json")
        with open(file_path, "r") as file:
            data = json.load(file)

        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/assets/{file_path:path}")
async def assets(file_path: str) -> Any:
    """
    Returns the requested asset file from the 'dist/assets' directory.
    """
    return FileResponse(f"dist/assets/{file_path}")

if __name__ == "__main__":
    FlaskUI(app=app, server="fastapi", port=8000).run()
