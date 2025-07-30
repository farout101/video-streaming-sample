import os
import subprocess

PROCESSED_DIR = "processed_videos"
ASSETS_DIR = "assets"
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

def run_ffmpeg_command(command: list[str]) -> bool:
    try:
        # Let FFmpeg output go to the console to avoid buffer deadlocks.
        subprocess.run(
            command,
            check=True
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"An error occurred during FFmpeg processing: {e}")
        return False

def process_and_overlay_video(input_path: str, original_filename: str, overlay_image_path: str) -> str | None:
    """
    Processes a video to a standard format and adds an overlay in a single, 
    robust, software-based FFmpeg command.
    """
    processed_filename = f"final_{original_filename}"
    output_path = os.path.join(PROCESSED_DIR, processed_filename)

    # This simplified filter chain prioritizes stability to create a playable file.
    # It scales the overlay to a fixed width and applies opacity.
    filter_command = (
        "[1:v]scale=200:-1,format=rgba,colorchannelmixer=aa=0.5[ol];"
        "[0:v][ol]overlay=W-w-10:10"
    )

    command = [
        "ffmpeg", "-i", input_path, "-i", overlay_image_path,
        "-filter_complex", filter_command,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ]

    if run_ffmpeg_command(command):
        return output_path
    return None




