# Video Streaming Sample

This project provides a FastAPI-based backend for uploading, processing, and watermarking video files using FFmpeg. It demonstrates robust, software-based video processing suitable for web applications or automation pipelines.

## Features
- Upload video files via a REST API
- Overlay a watermark image (with opacity and scaling) onto uploaded videos
- Transcode videos to a standard, widely compatible format (H.264 video, AAC audio)
- All processing is performed using FFmpeg for reliability and performance

## Project Structure
```
assets/               # Contains overlay images (e.g., overlay.jpg)
processed_videos/     # Output directory for processed videos
uploaded_videos/      # Temporary storage for uploaded files
ffmpeg_utils.py       # Video processing and FFmpeg command logic
main.py               # FastAPI app with upload and process endpoint
requirements.txt      # Python dependencies
```

## API Endpoints
### `POST /upload-and-process/`
Uploads a video and returns the processed, watermarked video filename.
- **Request:** Multipart form with a `video` file field
- **Response:** JSON with status and output filename

### `GET /`
Returns a welcome message.

## How It Works
1. User uploads a video file via the API.
2. The server saves the file temporarily.
3. The video is processed using FFmpeg:
    - The overlay image is scaled to 200px width and given 50% opacity.
    - The overlay is placed in the top-right corner of the video.
    - The video is transcoded to H.264/AAC for compatibility.
4. The processed video is saved in `processed_videos/`.
5. The temporary upload is deleted.

## Requirements
- Python 3.10+
- FFmpeg (must be installed and available in your system PATH)
- pip packages: see `requirements.txt`

## Setup
1. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Ensure FFmpeg is installed and accessible from the command line.
3. Place your overlay image as `assets/overlay.jpg`.
4. Run the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

## Notes
- The overlay image must exist at `assets/overlay.jpg` before uploading videos.
- Processed videos are saved as `processed_videos/final_<original_filename>`.
- The code is designed for stability and compatibility, using a simplified FFmpeg filter chain.
