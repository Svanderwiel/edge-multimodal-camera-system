"""
Multimodal AI Camera Assistant

A real-time intelligent camera system combining on-device object detection (YOLO)
with cloud-based vision-language models for natural language scene understanding.
"""

__version__ = "0.1.0"
__author__ = "Scott Van der Wiel"

from .detection.manager import DetectionManager
from .vision.api_client import VisionAPIClient
from .vision.prompt_templates import PromptTemplates
from .vision.embeddings import CLIPEmbeddingGenerator

__all__ = [
    "DetectionManager",
    "VisionAPIClient",
    "PromptTemplates",
    "CLIPEmbeddingGenerator",
]
