#!/usr/bin/env python3
"""
Vision API Client for Multimodal AI Camera Assistant
Handles image processing and API calls to Google Gemini only (free tier)
"""

import base64
import json
import time
import requests
from io import BytesIO
from typing import Optional, Dict, Any
import cv2
import numpy as np
from PIL import Image
import logging

from ..core.config import Config

# Configure logging
logger = logging.getLogger(__name__)

class VisionAPIClient:
    """Client for making vision API calls to Google Gemini only"""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the vision API client with Gemini-only configuration"""
        self.config = config or Config()
        self.setup_providers()

        # Track API usage
        self.daily_calls_made = 0
        self.last_daily_reset = time.time()
        self.api_calls_this_minute = 0
        self.last_minute_reset = time.time()
        self.total_cost = 0.0  # Free tier

    def setup_providers(self):
        """Setup available API providers - Gemini only"""
        self.providers = {}

        if self.config.google_api_key and self.config.google_api_key != 'your_google_api_key_here':
            self.providers['google'] = {
                'key': self.config.google_api_key,
                'base_url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent',
                'cost_per_image': 0.0  # Free tier
            }

        logger.info(f"Available providers: {list(self.providers.keys())}")

    def optimize_image(self, image: np.ndarray) -> str:
        """
        Optimize image for API calls
        Args:
            image: OpenCV image (BGR format)
        Returns:
            Base64 encoded JPEG string
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize to target size while maintaining aspect ratio
        height, width = rgb_image.shape[:2]
        if width > height:
            new_width = self.config.image_size
            new_height = int(height * self.config.image_size / width)
        else:
            new_height = self.config.image_size
            new_width = int(width * self.config.image_size / height)

        resized = cv2.resize(rgb_image, (new_width, new_height))

        # Convert to PIL Image
        pil_image = Image.fromarray(resized)

        # Compress to JPEG
        buffer = BytesIO()
        pil_image.save(buffer, format='JPEG', quality=self.config.image_quality, optimize=True)

        # Encode to base64
        image_bytes = buffer.getvalue()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        logger.debug(f"Image optimized: {width}x{height} -> {new_width}x{new_height}, "
                   f"quality={self.config.image_quality}, size={len(image_bytes)} bytes")

        return base64_image

    def check_rate_limit(self) -> bool:
        """Check if we're within rate limits - Gemini specific"""
        current_time = time.time()

        # Reset daily counter every 24 hours
        if current_time - self.last_daily_reset >= 86400:  # 24 hours
            self.daily_calls_made = 0
            self.last_daily_reset = current_time

        # Check daily limit
        if self.daily_calls_made >= self.config.daily_free_limit:
            logger.warning(f"Daily free limit exceeded ({self.daily_calls_made}/{self.config.daily_free_limit})")
            return False

        # Reset minute counter every minute
        if current_time - self.last_minute_reset >= 60:
            self.api_calls_this_minute = 0
            self.last_minute_reset = current_time

        return self.api_calls_this_minute < self.config.max_calls_per_minute

    def call_google(self, image_base64: str, prompt: str) -> Optional[str]:
        """Call Google Gemini API using the correct format from documentation"""
        if 'google' not in self.providers:
            return None

        url = f"{self.providers['google']['base_url']}?key={self.providers['google']['key']}"

        # Use the correct API structure from documentation
        payload = {
            'contents': [{
                'parts': [
                    {
                        'inline_data': {
                            'mime_type': 'image/jpeg',
                            'data': image_base64
                        }
                    },
                    {
                        'text': prompt
                    }
                ]
            }]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.config.api_timeout
            )
            response.raise_for_status()

            result = response.json()

            # Track free tier usage
            self.daily_calls_made += 1
            self.api_calls_this_minute += 1

            # Extract response text
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        return parts[0]['text']

            logger.error(f"Unexpected API response structure: {result}")
            return None

        except Exception as e:
            logger.error(f"Google API error: {e}")
            return None

    def query_vision(self, image: np.ndarray, prompt: str) -> Optional[str]:
        """
        Query vision API with image and prompt - Gemini only
        Args:
            image: OpenCV image (BGR format)
            prompt: Text prompt for the vision model
        Returns:
            Response text or None if failed
        """
        if not self.check_rate_limit():
            logger.warning("Rate limit exceeded, skipping API call")
            return None

        # Gemini only
        if 'google' not in self.providers:
            logger.error("Google Gemini API key not configured")
            return None

        # Optimize image
        image_base64 = self.optimize_image(image)

        logger.info("Using Google Gemini API...")
        result = self.call_google(image_base64, prompt)

        if result:
            logger.info("Success with Gemini API")
            return result
        else:
            logger.error("Gemini API call failed")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """Get API usage statistics - Gemini specific"""
        return {
            'total_cost': 0.0,  # Free tier
            'calls_this_minute': self.api_calls_this_minute,
            'daily_calls_made': self.daily_calls_made,
            'daily_free_limit': self.config.daily_free_limit,
            'daily_remaining': self.config.daily_free_limit - self.daily_calls_made,
            'available_providers': list(self.providers.keys()),
            'monthly_budget': 0.0,  # Free tier
            'budget_remaining': 0.0  # Free tier
        }
