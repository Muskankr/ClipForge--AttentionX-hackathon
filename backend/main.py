from fastapi import FastAPI, UploadFile
import shutil
from backend.video_utils import process_video

app = FastAPI()

@app.post("/upload/")
async def upload_video(file: UploadFile):
    try:
        with open(f"temp_{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        output_paths = process_video(f"temp_{file.filename}")
        return {"message": "Video processed successfully", "output": output_paths}
    except Exception as e:
        return {"error": str(e)}
