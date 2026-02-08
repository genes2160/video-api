# Changelog

All notable changes to the Video Processing API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-07

### Added
- Initial release of Video Processing API
- `/api/trim` endpoint for trimming videos
- `/api/subtitle` endpoint for generating and burning subtitles
- `/api/download/{filename}` endpoint for downloading processed files
- `/api/cleanup/{file_id}` endpoint for removing processed files
- Swagger UI documentation at `/docs`
- ReDoc documentation at `/redoc`
- OpenAI Whisper integration for automatic speech recognition
- FFmpeg integration for video processing
- CORS support for cross-origin requests
- Comprehensive error handling and validation
- Support for multiple video formats
- Automatic file cleanup on errors
- UUID-based file identification system

### Features
- **Video Trimming**
  - Precise trimming using start/end timestamps
  - Fast processing with stream copy (no re-encoding)
  - Support for multiple video formats

- **Subtitle Generation**
  - Automatic transcription using Whisper
  - SRT subtitle file generation
  - Subtitle burning into video
  - Multi-language support (90+ languages)
  - Fallback subtitle embedding method

- **File Management**
  - Unique file IDs for tracking
  - Separate upload and output directories
  - Manual cleanup endpoint
  - Automatic cleanup on errors

### Technical Details
- Built with FastAPI for high performance
- Asynchronous file handling
- Timeout protection (5 minutes per operation)
- Input validation with Pydantic models
- Structured error responses
- RESTful API design

### Documentation
- Complete README with setup instructions
- API usage examples (Python, JavaScript)
- Troubleshooting guide
- Performance optimization tips
- Supported language reference

## [Unreleased]

### Planned Features
- Batch processing support
- Video format conversion
- Video quality/resolution adjustment
- Custom subtitle styling options
- Progress tracking for long operations
- WebSocket support for real-time updates
- Video thumbnail generation
- Audio extraction
- Multiple subtitle tracks
- Custom Whisper model selection per request
- Rate limiting
- Authentication and API keys
- File expiration and auto-cleanup
- Database integration for job tracking
- Background task processing with Celery
- S3/Cloud storage integration
- Video metadata extraction
- Subtitle translation
- SRT ↔ VTT conversion

### Known Issues
- Large files may timeout on slow connections
- Whisper model loads once at startup (can't switch without restart)
- No progress indication for long-running operations
- Limited to single file processing (no batch)

### Performance Considerations
- Whisper base model loaded at startup (~140MB RAM)
- Each transcription requires ~1-2GB RAM
- Video processing is CPU-intensive
- No concurrent request limiting yet

## Version History

### Future Versions

**v1.1.0** (Planned)
- Background task processing
- Progress tracking
- WebSocket support
- Improved error messages

**v1.2.0** (Planned)
- Authentication system
- Rate limiting
- User accounts
- Job history

**v2.0.0** (Planned)
- Complete UI overhaul
- Cloud storage support
- Microservices architecture
- Kubernetes deployment configs
