"""
Configuration management for the multimodal camera system.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class Config:
    """Central configuration for the multimodal camera system"""

    def __init__(self):
        """Initialize configuration from environment variables"""
        # Load environment variables
        load_dotenv()

        # Get project root directory
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.models_dir = self.data_dir / "models"
        self.cache_dir = self.data_dir / "cache"

        # Ensure directories exist
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # API Configuration
        self.google_api_key = os.getenv('GOOGLE_API_KEY')

        # API Limits
        self.max_calls_per_minute = int(os.getenv('MAX_API_CALLS_PER_MINUTE', '25'))
        self.api_timeout = int(os.getenv('API_TIMEOUT_SECONDS', '15'))
        self.daily_free_limit = 1500  # Gemini free tier

        # Image Processing
        self.image_quality = int(os.getenv('IMAGE_QUALITY', '80'))
        self.image_size = int(os.getenv('IMAGE_SIZE', '512'))

        # Detection Settings
        self.confidence_threshold = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
        self.cooldown_seconds = int(os.getenv('COOLDOWN_SECONDS', '10'))

        # Cache Settings
        self.cache_ttl_hours = int(os.getenv('CACHE_TTL_HOURS', '24'))
        self.cache_db_path = self.cache_dir / "vision_cache.db"

        # Model Paths
        self.yolo_model_path = self.models_dir / "yolov8n.pt"
        self.yolo11_model_path = self.models_dir / "yolo11n.pt"

        # Budget Settings
        self.monthly_budget_usd = float(os.getenv('MONTHLY_BUDGET_USD', '0.0'))

        logger.info("Configuration loaded successfully")

    def validate(self):
        """Validate configuration"""
        warnings = []

        if not self.google_api_key or self.google_api_key == 'your_google_api_key_here':
            warnings.append("GOOGLE_API_KEY not configured - API calls will fail")

        if not self.yolo_model_path.exists():
            warnings.append(f"YOLO model not found at {self.yolo_model_path}")

        return warnings

    def __repr__(self):
        """String representation of configuration"""
        return (
            f"Config(\n"
            f"  project_root={self.project_root},\n"
            f"  models_dir={self.models_dir},\n"
            f"  cache_dir={self.cache_dir},\n"
            f"  api_configured={bool(self.google_api_key)},\n"
            f"  confidence_threshold={self.confidence_threshold},\n"
            f"  cooldown_seconds={self.cooldown_seconds}\n"
            f")"
        )
