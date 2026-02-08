# Video Processing API

A FastAPI-based REST API for video processing tasks including trimming videos and generating/burning subtitles.

## Features

- 🎬 **Video Trimming**: Trim videos by specifying start and end times
- 📝 **Subtitle Generation**: Auto-generate subtitles using OpenAI Whisper
- 🔥 **Subtitle Burning**: Burn subtitles directly into video files
- 🌐 **RESTful API**: Clean, documented API with Swagger UI
- 🚀 **Fast Processing**: Efficient video processing with FFmpeg
- 📦 **Easy Download**: Direct download links for processed files

## Prerequisites

- Python 3.8+
- FFmpeg installed and available in PATH
- At least 4GB RAM (for Whisper model)

### Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd video-api
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Running the API

### Development Mode
```bash
python main.py
```

### Production Mode (with Uvicorn)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Health Check
```
GET /
```

Returns API status and available endpoints.

### 2. Trim Video
```
POST /api/trim
```

**Parameters:**
- `video` (file): Video file to trim
- `start_time` (float): Start time in seconds
- `end_time` (float): End time in seconds

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/api/trim" \
  -F "video=@input.mp4" \
  -F "start_time=10.5" \
  -F "end_time=45.0"
```

**Response:**
```json
{
  "success": true,
  "message": "Video trimmed successfully",
  "file_id": "abc123-def456",
  "download_url": "/api/download/abc123-def456_trimmed.mp4",
  "file_path": "outputs/abc123-def456_trimmed.mp4"
}
```

### 3. Generate Subtitles
```
POST /api/subtitle
```

**Parameters (Option 1 - Upload):**
- `video` (file): Video file
- `language` (string, optional): Language code (default: "en")

**Parameters (Option 2 - Use existing file):**
- `file_path` (string): Path to existing video file
- `language` (string, optional): Language code (default: "en")

**Example with cURL:**
```bash
# Upload video
curl -X POST "http://localhost:8000/api/subtitle" \
  -F "video=@input.mp4" \
  -F "language=en"

# Use existing file
curl -X POST "http://localhost:8000/api/subtitle" \
  -F "file_path=outputs/video.mp4" \
  -F "language=en"
```

**Response:**
```json
{
  "success": true,
  "message": "Subtitles generated successfully",
  "file_id": "xyz789-abc123",
  "video_download_url": "/api/download/xyz789-abc123_subbed.mp4",
  "srt_download_url": "/api/download/xyz789-abc123.srt",
  "video_path": "outputs/xyz789-abc123_subbed.mp4",
  "srt_path": "outputs/xyz789-abc123.srt"
}
```

### 4. Download File
```
GET /api/download/{filename}
```

Download a processed file using the filename from previous responses.

**Example:**
```bash
curl -O "http://localhost:8000/api/download/abc123_trimmed.mp4"
```

### 5. Cleanup Files
```
DELETE /api/cleanup/{file_id}
```

Delete all files associated with a processing job.

**Example:**
```bash
curl -X DELETE "http://localhost:8000/api/cleanup/abc123-def456"
```

## Usage Examples

### Python Client Example
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

### JavaScript/Fetch Example
```javascript
// Trim video
const formData = new FormData();
formData.append('video', fileInput.files[0]);
formData.append('start_time', '10.5');
formData.append('end_time', '45.0');

const response = await fetch('http://localhost:8000/api/trim', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log('Download URL:', result.download_url);
```

## Supported Languages

Whisper supports the following language codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- And 90+ more languages

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (file doesn't exist)
- `500` - Internal Server Error (processing failed)

**Error Response Format:**
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

## Configuration

### Change Whisper Model

Edit `main.py` line 31 to use different model sizes:
```python
WHISPER_MODEL = whisper.load_model("base")  # tiny, base, small, medium, large
```

**Model Trade-offs:**
- `tiny` - Fastest, least accurate
- `base` - Fast, good for most use cases (default)
- `small` - Balanced
- `medium` - Better accuracy, slower
- `large` - Best accuracy, slowest, requires more RAM

### Change Upload/Output Directories

Edit `main.py` lines 25-26:
```python
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
```

## Project Structure

```
video-api/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
├── CHANGELOG.md        # Version history
├── uploads/            # Temporary upload directory (auto-created)
└── outputs/            # Processed files directory (auto-created)
```

## Performance Tips

1. **Use faster Whisper model** for quick processing: `tiny` or `base`
2. **Increase workers** in production: `--workers 4`
3. **Regular cleanup**: Use `/api/cleanup` endpoint to remove old files
4. **Add file size limits** in production environments
5. **Use SSD storage** for faster I/O operations

## Troubleshooting

### FFmpeg not found
```
Error: ffmpeg not found. Please install ffmpeg.
```
**Solution**: Install FFmpeg and ensure it's in your system PATH.

### Out of memory during transcription
```
Error: CUDA out of memory / RuntimeError
```
**Solution**: Use a smaller Whisper model (e.g., `base` instead of `medium`)

### Subtitle burning fails
The API automatically tries an alternative method if the first fails. If both fail, check:
- FFmpeg version (should be recent)
- Video codec compatibility
- File permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:8000/docs) when running

## Roadmap

See [CHANGELOG.md](CHANGELOG.md) for version history and [TODO.md](TODO.md) for planned features.
