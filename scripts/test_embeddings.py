#!/usr/bin/env python3
"""
Test script for CLIP Embeddings
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import cv2
import numpy as np
import time
from multimodal_camera.vision.embeddings import CLIPEmbeddingGenerator

def main():
    """Test CLIP embedding functionality"""
    print("=== CLIP Embedding Test ===")

    # Initialize embedding generator
    embedding_gen = CLIPEmbeddingGenerator()

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
    main()
