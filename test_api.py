#!/usr/bin/env python3
"""
API Test Script
Test all endpoints of the Video Processing API
"""

import requests
import time
from pathlib import Path

API_URL = "http://localhost:8000"

def test_health_check():
    """Test API health check"""
    print("🏥 Testing health check...")
    response = requests.get(f"{API_URL}/")
    assert response.status_code == 200, "Health check failed"
    data = response.json()
    assert data["status"] == "online", "API is not online"
    print("✅ Health check passed")
    return True

def test_trim_video(video_path: str):
    """Test video trimming endpoint"""
    print(f"\n✂️ Testing video trim with: {video_path}")
    
    if not Path(video_path).exists():
        print(f"⚠️ Skipping - video file not found: {video_path}")
        return False
    
    with open(video_path, "rb") as f:
        files = {"video": f}
        data = {
            "start_time": "2.0",
            "end_time": "8.0"
        }
        
        print("  Sending request...")
        response = requests.post(f"{API_URL}/api/trim", files=files, data=data)
    
    if response.status_code != 200:
        print(f"❌ Trim failed: {response.text}")
        return False
    
    result = response.json()
    assert result["success"], "Trim endpoint returned success=False"
    print(f"✅ Video trimmed successfully")
    print(f"   File ID: {result['file_id']}")
    print(f"   Download: {API_URL}{result['download_url']}")
    
    return result

def test_subtitle_generation(video_path: str):
    """Test subtitle generation endpoint"""
    print(f"\n📝 Testing subtitle generation with: {video_path}")
    
    if not Path(video_path).exists():
        print(f"⚠️ Skipping - video file not found: {video_path}")
        return False
    
    with open(video_path, "rb") as f:
        files = {"video": f}
        data = {"language": "en"}
        
        print("  Sending request (this may take a while)...")
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/api/subtitle",
            files=files,
            data=data,
            timeout=300  # 5 minute timeout
        )
        elapsed = time.time() - start_time
    
    if response.status_code != 200:
        print(f"❌ Subtitle generation failed: {response.text}")
        return False
    
    result = response.json()
    assert result["success"], "Subtitle endpoint returned success=False"
    print(f"✅ Subtitles generated successfully in {elapsed:.1f}s")
    print(f"   File ID: {result['file_id']}")
    print(f"   Video: {API_URL}{result['video_download_url']}")
    print(f"   SRT: {API_URL}{result['srt_download_url']}")
    
    return result

def test_download(download_url: str):
    """Test file download"""
    print(f"\n⬇️ Testing download: {download_url}")
    response = requests.get(f"{API_URL}{download_url}")
    
    if response.status_code != 200:
        print(f"❌ Download failed: {response.status_code}")
        return False
    
    print(f"✅ Download successful ({len(response.content)} bytes)")
    return True

def test_cleanup(file_id: str):
    """Test cleanup endpoint"""
    print(f"\n🧹 Testing cleanup for file ID: {file_id}")
    response = requests.delete(f"{API_URL}/api/cleanup/{file_id}")
    
    if response.status_code != 200:
        print(f"❌ Cleanup failed: {response.text}")
        return False
    
    result = response.json()
    print(f"✅ Cleanup successful - deleted {len(result['deleted_files'])} files")
    return True

def main():
    print("=" * 60)
    print("Video Processing API - Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    try:
        test_health_check()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("\n⚠️ Make sure the API is running:")
        print("   python main.py")
        return
    
    # Ask for test video
    print("\n" + "=" * 60)
    print("For the following tests, you need a test video file.")
    video_path = input("Enter path to test video (or press Enter to skip): ").strip()
    
    if not video_path:
        print("\n⚠️ Skipping video tests - no video provided")
        print("✅ Basic health check passed!")
        return
    
    # Test 2: Trim video
    print("\n" + "=" * 60)
    trim_result = test_trim_video(video_path)
    if trim_result:
        test_download(trim_result["download_url"])
        test_cleanup(trim_result["file_id"])
    
    # Test 3: Generate subtitles
    print("\n" + "=" * 60)
    subtitle_result = test_subtitle_generation(video_path)
    if subtitle_result:
        test_download(subtitle_result["video_download_url"])
        test_download(subtitle_result["srt_download_url"])
        test_cleanup(subtitle_result["file_id"])
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
