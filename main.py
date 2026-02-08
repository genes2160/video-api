#!/usr/bin/env python3
"""
Video Processing API
FastAPI server for video trimming and subtitle generation
"""

import os
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Optional

import whisper
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ============== CONFIG ==============

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Load Whisper model once at startup
print("Loading Whisper model...")
WHISPER_MODEL = whisper.load_model("base")
print("Whisper model loaded!")

# ============== APP ==============

app = FastAPI(
    title="Video Processing API",
    description="API for trimming videos and generating subtitles",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== MODELS ==============

class TrimResponse(BaseModel):
    success: bool
    message: str
    file_id: str
    download_url: str
    file_path: str

class SubtitleResponse(BaseModel):
    success: bool
    message: str
    file_id: str
    video_download_url: str
    srt_download_url: str
    video_path: str
    srt_path: str

class ErrorResponse(BaseModel):
    success: bool
    error: str

# ============== HELPERS ==============

def format_time_srt(seconds: float) -> str:
    """Convert seconds to SRT timestamp format"""
    ms = int(seconds * 1000)
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def check_ffmpeg():
    """Check if ffmpeg is available"""
    if not shutil.which("ffmpeg"):
        raise HTTPException(status_code=500, detail="ffmpeg not found. Please install ffmpeg.")

def run_ffmpeg(cmd: list) -> tuple[bool, str]:
    """Run ffmpeg command and return success status and error message"""
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # 5 minute timeout
        )
        if result.returncode != 0:
            return False, result.stderr
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "Operation timed out"
    except Exception as e:
        return False, str(e)

# ============== ENDPOINTS ==============

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "message": "Video Processing API",
        "version": "1.0.0",
        "endpoints": {
            "trim": "/api/trim",
            "subtitle": "/api/subtitle",
            "download": "/api/download/{file_id}"
        }
    }

@app.post("/api/trim", response_model=TrimResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def trim_video(
    video: UploadFile = File(..., description="Video file to trim"),
    start_time: float = Form(..., description="Start time in seconds", ge=0),
    end_time: float = Form(..., description="End time in seconds", gt=0),
):
    """
    Trim a video from start_time to end_time
    
    - **video**: Upload video file
    - **start_time**: Start time in seconds (e.g., 5.5 for 5.5 seconds)
    - **end_time**: End time in seconds (e.g., 30.0 for 30 seconds)
    
    Returns download URL and file location
    """
    check_ffmpeg()
    
    # Validate times
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="end_time must be greater than start_time")
    
    # Generate unique ID
    file_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_ext = Path(video.filename).suffix or ".mp4"
    input_path = UPLOAD_DIR / f"{file_id}_input{file_ext}"
    output_path = OUTPUT_DIR / f"{file_id}_trimmed{file_ext}"
    
    try:
        # Save upload
        with open(input_path, "wb") as f:
            content = await video.read()
            f.write(content)
        
        # Calculate duration
        duration = end_time - start_time
        
        # Trim video
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_time),
            "-i", str(input_path),
            "-t", str(duration),
            "-c", "copy",
            str(output_path)
        ]
        
        success, error = run_ffmpeg(cmd)
        
        if not success:
            raise HTTPException(status_code=500, detail=f"FFmpeg error: {error}")
        
        # Clean up input
        input_path.unlink()
        
        return TrimResponse(
            success=True,
            message="Video trimmed successfully",
            file_id=file_id,
            download_url=f"/api/download/{file_id}_trimmed{file_ext}",
            file_path=str(output_path)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up on error
        if input_path.exists():
            input_path.unlink()
        if output_path.exists():
            output_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/subtitle", response_model=SubtitleResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_subtitles(
    video: Optional[UploadFile] = File(None, description="Video file (if not using file_path)"),
    file_path: Optional[str] = Form(None, description="Path to existing video file"),
    language: str = Form("en", description="Language code (e.g., 'en', 'es', 'fr')"),
):
    """
    Generate subtitles for a video and burn them into the video
    
    - **video**: Upload video file OR
    - **file_path**: Specify path to existing video file
    - **language**: Language code for transcription (default: 'en')
    
    Returns download URLs for both the subtitled video and SRT file
    """
    check_ffmpeg()
    
    # Must have either video or file_path
    if not video and not file_path:
        raise HTTPException(status_code=400, detail="Must provide either 'video' file or 'file_path'")
    
    file_id = str(uuid.uuid4())
    
    try:
        # Determine input path
        if video:
            file_ext = Path(video.filename).suffix or ".mp4"
            input_path = UPLOAD_DIR / f"{file_id}_input{file_ext}"
            
            # Save upload
            with open(input_path, "wb") as f:
                content = await video.read()
                f.write(content)
        else:
            input_path = Path(file_path)
            if not input_path.exists():
                raise HTTPException(status_code=400, detail=f"File not found: {file_path}")
            file_ext = input_path.suffix
        
        # Output paths
        srt_path = OUTPUT_DIR / f"{file_id}.srt"
        output_video = OUTPUT_DIR / f"{file_id}_subbed{file_ext}"
        
        # Transcribe with Whisper
        print(f"Transcribing {input_path}...")
        result = WHISPER_MODEL.transcribe(str(input_path), language=language)
        
        # Write SRT
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(result["segments"], 1):
                f.write(f"{i}\n")
                f.write(f"{format_time_srt(seg['start'])} --> {format_time_srt(seg['end'])}\n")
                f.write(f"{seg['text'].strip()}\n\n")
        
        print(f"SRT created: {srt_path}")
        
        # Burn subtitles into video
        print("Burning subtitles...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-vf", f"subtitles={srt_path.name}",
            "-c:a", "copy",
            str(output_video)
        ]
        
        # Run in output directory to avoid path issues
        success, error = run_ffmpeg(cmd)
        
        if not success:
            # Try alternative method if subtitles filter fails
            print("Trying alternative subtitle method...")
            cmd = [
                "ffmpeg", "-y",
                "-i", str(input_path),
                "-i", str(srt_path),
                "-c", "copy",
                "-c:s", "mov_text",
                str(output_video)
            ]
            success, error = run_ffmpeg(cmd)
            
            if not success:
                raise HTTPException(status_code=500, detail=f"FFmpeg error: {error}")
        
        # Clean up input if it was uploaded
        if video and input_path.exists():
            input_path.unlink()
        
        return SubtitleResponse(
            success=True,
            message="Subtitles generated successfully",
            file_id=file_id,
            video_download_url=f"/api/download/{file_id}_subbed{file_ext}",
            srt_download_url=f"/api/download/{file_id}.srt",
            video_path=str(output_video),
            srt_path=str(srt_path)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up on error
        for p in [input_path, srt_path, output_video]:
            if p.exists() and video:  # Only clean uploaded files
                p.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Download a processed file
    
    - **filename**: The filename returned from trim or subtitle endpoints
    """
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@app.delete("/api/cleanup/{file_id}")
async def cleanup_files(file_id: str):
    """
    Clean up files associated with a file_id
    
    - **file_id**: The file ID returned from processing
    """
    deleted = []
    
    # Find and delete files with this ID
    for directory in [UPLOAD_DIR, OUTPUT_DIR]:
        for file in directory.glob(f"{file_id}*"):
            file.unlink()
            deleted.append(str(file))
    
    return {
        "success": True,
        "message": f"Deleted {len(deleted)} files",
        "deleted_files": deleted
    }

# ============== RUN ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
