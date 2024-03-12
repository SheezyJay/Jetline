from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json
app = FastAPI()
ui_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')

# Route to serve the index.html file
@app.get("/")
async def read_index():
    return FileResponse(ui_directory+"/app.html")

from pathlib import Path

@app.get("/get_pipe_data")
async def get_pipe_data():
    json_path = Path(ui_directory) / 'info.json'
    with open(json_path, 'r') as f:
        pipeline_data = json.load(f)
        
    return pipeline_data



# Mounten Sie das Verzeichnis 'ui' als statische Dateien
app.mount("/ui", StaticFiles(directory=ui_directory, html=True), name="ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)




