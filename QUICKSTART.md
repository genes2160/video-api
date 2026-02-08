# Quick Reference Guide

## 🚀 Getting Started

### Option 1: Quick Start (Recommended)
```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

### Option 2: Manual Start
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

### Option 3: Docker
```bash
# Build and run
docker-compose up --build

# Access at http://localhost
```

## 📡 API Endpoints

### Trim Video
```bash
curl -X POST "http://localhost:8000/api/trim" \
  -F "video=@video.mp4" \
  -F "start_time=5.0" \
  -F "end_time=30.0"
```

### Generate Subtitles
```bash
curl -X POST "http://localhost:8000/api/subtitle" \
  -F "video=@video.mp4" \
  -F "language=en"
```

### Download File
```bash
curl -O "http://localhost:8000/api/download/abc123_trimmed.mp4"
```

### Cleanup
```bash
curl -X DELETE "http://localhost:8000/api/cleanup/abc123"
```

## 🌐 Access Points

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Web UI**: Open `index.html` in browser

## 🐍 Python Example

```python
import requests

# Trim video
with open("video.mp4", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/trim",
        files={"video": f},
        data={"start_time": 5.0, "end_time": 30.0}
    )
    result = response.json()
    print(f"Download: {result['download_url']}")

# Generate subtitles
with open("video.mp4", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/subtitle",
        files={"video": f},
        data={"language": "en"}
    )
    result = response.json()
    print(f"Video: {result['video_download_url']}")
    print(f"SRT: {result['srt_download_url']}")
```

## 🔧 Configuration

### Change Whisper Model
Edit `main.py` line 31:
```python
WHISPER_MODEL = whisper.load_model("base")  # tiny, base, small, medium, large
```

### Change Directories
Edit `main.py` lines 25-26:
```python
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
```

## 🧪 Testing

```bash
# Run test suite
python test_api.py

# Manual tests via Swagger UI
# Open http://localhost:8000/docs
```

## 📋 Supported Languages

Common language codes:
- `en` - English
- `es` - Spanish  
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean

[See full list in README.md]

## ⚠️ Troubleshooting

### FFmpeg not found
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### Port already in use
```bash
# Change port in main.py (line 280)
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Out of memory
Use smaller Whisper model:
```python
WHISPER_MODEL = whisper.load_model("tiny")
```

## 📁 Project Structure

```
video-api/
├── main.py              # FastAPI app
├── requirements.txt     # Dependencies
├── README.md           # Full documentation
├── CHANGELOG.md        # Version history
├── GOALS.md            # Project goals
├── .gitignore          # Git ignore
├── Dockerfile          # Docker config
├── docker-compose.yml  # Docker Compose
├── nginx.conf          # Nginx config
├── index.html          # Web UI
├── start.sh            # Quick start (Unix)
├── start.bat           # Quick start (Windows)
├── test_api.py         # Test suite
├── uploads/            # Temp uploads (auto-created)
└── outputs/            # Processed files (auto-created)
```

## 🎯 Common Tasks

### Process a batch of videos
```python
import requests
import glob

for video_file in glob.glob("videos/*.mp4"):
    with open(video_file, "rb") as f:
        response = requests.post(
            "http://localhost:8000/api/subtitle",
            files={"video": f},
            data={"language": "en"}
        )
        print(f"Processed: {video_file}")
```

### Clean up old files
```bash
# Delete all files in outputs older than 7 days
find outputs/ -type f -mtime +7 -delete
```

### Monitor API
```bash
# Watch logs
tail -f nohup.out

# Check health
watch -n 5 'curl -s http://localhost:8000/ | jq'
```

## 📞 Support

- **GitHub Issues**: Report bugs
- **Swagger Docs**: http://localhost:8000/docs
- **README**: Full documentation
- **Test Suite**: `python test_api.py`

---

**Last Updated**: February 7, 2026  
**Version**: 1.0.0
