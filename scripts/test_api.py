#!/usr/bin/env python3
"""
Test script for Vision API Client
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import cv2
import numpy as np
from multimodal_camera.vision.api_client import VisionAPIClient
from multimodal_camera.core.config import Config

def main():
    """Test Gemini API configuration"""
    print("=== Gemini API Test ===")

    # Initialize components
    config = Config()
    api_client = VisionAPIClient(config)

    # Check API availability
    stats = api_client.get_stats()
    print(f"Available providers: {stats['available_providers']}")
    print(f"Daily calls made: {stats['daily_calls_made']}/{stats['daily_free_limit']}")
    print(f"Daily remaining: {stats['daily_remaining']}")

    if 'google' not in stats['available_providers']:
        print("❌ Gemini API key not configured!")
        print("Please set GOOGLE_API_KEY in .env file")
        return False

    # Test with sample image
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(test_image, (100, 100), (540, 380), (0, 255, 0), -1)
    cv2.putText(test_image, "GEMINI TEST", (200, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

    prompt = "Describe what you see in this image in 2-3 sentences."

    print(f"Testing with prompt: '{prompt}'")
    result = api_client.query_vision(test_image, prompt)

    if result:
        print(f"✅ Success! Response: {result}")
        return True
    else:
        print("❌ Failed to get response from Gemini")
        return False

if __name__ == "__main__":
    main()
