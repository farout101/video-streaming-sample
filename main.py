import os
import shutil
import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from ffmpeg_utils import process_and_overlay_video

app = FastAPI()

UPLOAD_DIR = "uploaded_videos"
ASSETS_DIR = "assets"
PROCESSED_DIR = "processed_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.post("/upload-and-process/")
async def upload_and_process(video: UploadFile = File(...)):
    """
    Uploads a video, then processes and watermarks it in a single, 
    hardware-accelerated step.
    """
    if not video.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    if not video.content_type or not video.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a video.")

    # Ensure the overlay image exists before we start
    overlay_image_path = os.path.join(ASSETS_DIR, "overlay.jpg")
    if not os.path.exists(overlay_image_path):
        raise HTTPException(status_code=500, detail="Overlay image not found on server.")

    # Save the uploaded file temporarily
    temp_path = os.path.join(UPLOAD_DIR, video.filename)
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Failed to save temporary video file: {str(e)}"}
        )

    # Run the single, optimized processing and overlay function
    final_file_path = await asyncio.to_thread(
        process_and_overlay_video, temp_path, video.filename, overlay_image_path
    )

    # Clean up the temporary file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not final_file_path:
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to process and overlay video."}
        )

    return JSONResponse(
        status_code=201,
        content={
            "message": "Video uploaded, processed, and watermarked successfully",
            "final_filename": os.path.basename(final_file_path)
        },
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the video processing API!"}

