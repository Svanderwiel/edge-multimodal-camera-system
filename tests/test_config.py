"""
Tests for configuration module
"""

import pytest
from pathlib import Path
from multimodal_camera.core.config import Config

def test_config_initialization():
    """Test that config initializes correctly"""
    config = Config()
    assert config.project_root.exists()
    assert config.models_dir.exists()
    assert config.cache_dir.exists()

def test_config_paths():
    """Test that paths are set correctly"""
    config = Config()
    assert config.yolo_model_path.name == "yolov8n.pt"
    assert config.cache_db_path.name == "vision_cache.db"

def test_config_defaults():
    """Test default configuration values"""
    config = Config()
    assert config.confidence_threshold == 0.7
    assert config.cooldown_seconds == 10
    assert config.image_quality == 80
    assert config.image_size == 512

def test_config_validation():
    """Test configuration validation"""
    config = Config()
    warnings = config.validate()
    assert isinstance(warnings, list)
