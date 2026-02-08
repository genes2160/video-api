#!/bin/bash

# Video Processing API - Quick Start Script

echo "🎬 Video Processing API - Quick Start"
echo "======================================"
echo ""

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python found: $(python --version)"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg is not installed."
    echo ""
    echo "Install FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS:         brew install ffmpeg"
    echo "  Windows:       choco install ffmpeg"
    exit 1
fi
echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Create directories
mkdir -p uploads outputs
echo "✅ Directories created"

# Run the API
echo ""
echo "🚀 Starting Video Processing API..."
echo ""
echo "API will be available at:"
echo "  - API:     http://localhost:8000"
echo "  - Swagger: http://localhost:8000/docs"
echo "  - ReDoc:   http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
