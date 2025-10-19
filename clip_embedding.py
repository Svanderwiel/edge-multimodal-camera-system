#!/usr/bin/env python3
"""
CLIP Embedding Module for Object-Specific Caching
Generates CLIP embeddings for detected objects
"""

import torch
import numpy as np
import cv2
from PIL import Image
import logging
from typing import Optional, Tuple
import time

logger = logging.getLogger(__name__)

class CLIPEmbedding:
    """CLIP embedding generator for object-specific caching"""
    
    def __init__(self, device: str = None):
        """Initialize CLIP embedding generator"""
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        self.model = None
        self.preprocess = None
        self._load_model()
        
    def _load_model(self):
        """Load CLIP model"""
        try:
            import clip
            logger.info(f"Loading CLIP model on {self.device}...")
            self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
            logger.info("CLIP model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            self.model = None
            self.preprocess = None
            
    def get_object_embedding(self, frame: np.ndarray, detection_bbox: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        """
        Generate CLIP embedding for a detected object
        Args:
            frame: OpenCV image (BGR format)
            detection_bbox: (x1, y1, x2, y2) bounding box coordinates
        Returns:
            CLIP embedding vector or None if failed
        """
        try:
            # Crop the detected object
            x1, y1, x2, y2 = detection_bbox
            cropped_object = frame[y1:y2, x1:x2]
            
            if cropped_object.size == 0:
                logger.warning("Empty cropped object")
                return None
                
            # Convert BGR to RGB
            rgb_object = cv2.cvtColor(cropped_object, cv2.COLOR_BGR2RGB)
            
            if self.model is not None:
                # Use CLIP model
                return self._get_clip_embedding(rgb_object)
            else:
                # Fallback to simple feature extraction
                return self._get_fallback_embedding(rgb_object)
                
        except Exception as e:
            logger.error(f"Error generating object embedding: {e}")
            return None
            
    def _get_clip_embedding(self, rgb_object: np.ndarray) -> np.ndarray:
        """Generate CLIP embedding using the actual CLIP model"""
        try:
            # Convert to PIL Image
            pil_image = Image.fromarray(rgb_object)
            
            # Preprocess image
            processed_image = self.preprocess(pil_image).unsqueeze(0).to(self.device)
            
            # Generate embedding
            with torch.no_grad():
                embedding = self.model.encode_image(processed_image)
                
            return embedding.cpu().numpy().flatten()
            
        except Exception as e:
            logger.error(f"Error with CLIP embedding: {e}")
            return self._get_fallback_embedding(rgb_object)
            
    def _get_fallback_embedding(self, rgb_object: np.ndarray) -> np.ndarray:
        """Fallback embedding method using simple feature extraction"""
        try:
            # Resize to standard size
            resized = cv2.resize(rgb_object, (224, 224))
            
            # Convert to float and normalize
            normalized = resized.astype(np.float32) / 255.0
            
            # Extract simple features (color histograms, texture, etc.)
            features = []
            
            # Color histogram features
            for channel in range(3):  # RGB channels
                hist = cv2.calcHist([normalized], [channel], None, [32], [0, 256])
                features.extend(hist.flatten())
            
            # Texture features (gradient magnitude)
            gray = cv2.cvtColor(normalized, cv2.COLOR_RGB2GRAY)
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            
            # Add texture features
            features.extend([
                np.mean(gradient_magnitude),
                np.std(gradient_magnitude),
                np.percentile(gradient_magnitude, 25),
                np.percentile(gradient_magnitude, 75)
            ])
            
            # Convert to numpy array and normalize
            embedding = np.array(features, dtype=np.float32)
            embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error with fallback embedding: {e}")
            # Return a random embedding as last resort
            return np.random.randn(100).astype(np.float32)
            
    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            # Normalize embeddings
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
                
            # Calculate cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0

def test_clip_embedding():
    """Test the CLIP embedding functionality"""
    print("=== CLIP Embedding Test ===")
    
    # Initialize embedding generator
    embedding_gen = CLIPEmbedding()
    
    # Create test images
    test_image1 = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(test_image1, (100, 100), (200, 200), (0, 255, 0), -1)  # Green rectangle
    
    test_image2 = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(test_image2, (300, 300), (400, 400), (0, 255, 0), -1)  # Same green rectangle
    
    test_image3 = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(test_image3, (100, 100), (200, 200), (255, 0, 0), -1)  # Red rectangle
    
    # Test bounding boxes
    bbox1 = (100, 100, 200, 200)
    bbox2 = (300, 300, 400, 400)
    bbox3 = (100, 100, 200, 200)
    
    # Generate embeddings
    print("Generating embeddings...")
    start_time = time.time()
    
    embedding1 = embedding_gen.get_object_embedding(test_image1, bbox1)
    embedding2 = embedding_gen.get_object_embedding(test_image2, bbox2)
    embedding3 = embedding_gen.get_object_embedding(test_image3, bbox3)
    
    end_time = time.time()
    
    if embedding1 is not None and embedding2 is not None and embedding3 is not None:
        # Calculate similarities
        sim_same = embedding_gen.cosine_similarity(embedding1, embedding2)  # Same color
        sim_different = embedding_gen.cosine_similarity(embedding1, embedding3)  # Different color
        
        print(f"Embedding generation time: {end_time - start_time:.3f}s")
        print(f"Embedding dimensions: {len(embedding1)}")
        print(f"Similarity (same green rectangles): {sim_same:.3f}")
        print(f"Similarity (green vs red rectangle): {sim_different:.3f}")
        
        if sim_same > sim_different:
            print("✅ Embeddings correctly distinguish similar vs different objects")
        else:
            print("⚠️  Embeddings may not be working as expected")
    else:
        print("❌ Failed to generate embeddings")

if __name__ == "__main__":
    test_clip_embedding()
