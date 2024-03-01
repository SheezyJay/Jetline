from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
ui_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')

# Route to serve the index.html file
@app.get("/")
async def read_index():
    return FileResponse(ui_directory+"/index.html")


# Mounten Sie das Verzeichnis 'ui' als statische Dateien
app.mount("/ui", StaticFiles(directory=ui_directory, html=True), name="ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
