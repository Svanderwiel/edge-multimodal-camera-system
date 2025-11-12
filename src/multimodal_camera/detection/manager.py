#!/usr/bin/env python3
"""
Detection Manager for Smart Triggering & Cost Control
Implements CLIP+YOLO caching with cooldown logic
"""

import sqlite3
import time
import logging
import numpy as np
import cv2
from typing import Optional, Dict, Any, List, Tuple
from ultralytics import YOLO

from ..core.config import Config
from ..vision.embeddings import CLIPEmbeddingGenerator
from ..vision.api_client import VisionAPIClient
from ..vision.prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)

class DetectionManager:
    """Manages smart triggering logic with CLIP+YOLO caching"""

    def __init__(self, config: Optional[Config] = None):
        """Initialize DetectionManager with caching and cooldown logic"""
        self.config = config or Config()
        self.db_path = str(self.config.cache_db_path)

        # Initialize components
        logger.info(f"Loading YOLO model from {self.config.yolo_model_path}")
        self.yolo_model = YOLO(str(self.config.yolo_model_path))
        self.clip_embedding = CLIPEmbeddingGenerator()
        self.vision_api = VisionAPIClient(self.config)
        self.prompt_templates = PromptTemplates()

        # Cooldown tracking
        self.last_detection_time = {}  # {object_class: timestamp}

        # Initialize database
        self._init_database()

        logger.info("DetectionManager initialized successfully")

    def _init_database(self):
        """Initialize SQLite database for caching"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vision_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    embedding_hash TEXT UNIQUE,
                    prompt_type TEXT,
                    api_response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    hit_count INTEGER DEFAULT 0,
                    object_class TEXT,
                    confidence REAL
                )
            ''')

            # Create index for faster lookups
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_embedding_hash
                ON vision_cache(embedding_hash)
            ''')

            conn.commit()
            conn.close()

            logger.info(f"Database initialized successfully at {self.db_path}")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

    def _embedding_to_hash(self, embedding: np.ndarray) -> str:
        """Convert embedding to hash string for database storage"""
        # Convert to string representation
        embedding_str = ','.join([f"{x:.6f}" for x in embedding])
        return str(hash(embedding_str))

    def _find_similar_cached_response(self, embedding: np.ndarray, prompt_type: str,
                                    similarity_threshold: float = 0.9) -> Optional[str]:
        """Find cached response for similar embedding"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get all cached embeddings
            cursor.execute('''
                SELECT embedding_hash, api_response, hit_count
                FROM vision_cache
                WHERE prompt_type = ?
            ''', (prompt_type,))

            cached_entries = cursor.fetchall()
            conn.close()

            if not cached_entries:
                return None

            # Find most similar embedding
            best_similarity = 0.0
            best_response = None
            best_hash = None

            for embedding_hash, api_response, hit_count in cached_entries:
                # For now, we'll use a simple approach
                # In production, you'd store the actual embedding
                cached_embedding = np.random.randn(512)  # Placeholder

                similarity = self.clip_embedding.cosine_similarity(embedding, cached_embedding)

                if similarity > best_similarity and similarity > similarity_threshold:
                    best_similarity = similarity
                    best_response = api_response
                    best_hash = embedding_hash

            if best_response and best_hash:
                logger.info(f"Found cached response with similarity: {best_similarity:.3f}")
                # Update hit count
                self._update_hit_count(best_hash)

            return best_response

        except Exception as e:
            logger.error(f"Error finding cached response: {e}")
            return None

    def _update_hit_count(self, embedding_hash: str):
        """Update hit count for cached response"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE vision_cache
                SET hit_count = hit_count + 1
                WHERE embedding_hash = ?
            ''', (embedding_hash,))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Error updating hit count: {e}")

    def _cache_response(self, embedding: np.ndarray, prompt_type: str,
                       api_response: str, object_class: str, confidence: float):
        """Cache API response with embedding"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            embedding_hash = self._embedding_to_hash(embedding)

            cursor.execute('''
                INSERT OR REPLACE INTO vision_cache
                (embedding_hash, prompt_type, api_response, object_class, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (embedding_hash, prompt_type, api_response, object_class, confidence))

            conn.commit()
            conn.close()

            logger.info(f"Cached response for {object_class} with confidence {confidence:.2f}")

        except Exception as e:
            logger.error(f"Error caching response: {e}")

    def _should_trigger_api_call(self, object_class: str, confidence: float) -> bool:
        """Check if API call should be triggered based on cooldown and confidence"""
        current_time = time.time()

        # Check confidence threshold
        if confidence < self.config.confidence_threshold:
            logger.debug(f"Confidence {confidence:.2f} below threshold {self.config.confidence_threshold}")
            return False

        # Check cooldown
        if object_class in self.last_detection_time:
            time_since_last = current_time - self.last_detection_time[object_class]
            if time_since_last < self.config.cooldown_seconds:
                remaining = self.config.cooldown_seconds - time_since_last
                logger.debug(f"Cooldown active for {object_class}, {remaining:.1f}s remaining")
                return False

        # Update last detection time
        self.last_detection_time[object_class] = current_time
        return True

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """Process frame and return detection results with smart triggering"""
        results = {
            'detections': [],
            'api_responses': [],
            'cached_responses': [],
            'stats': {
                'total_detections': 0,
                'api_calls_made': 0,
                'cache_hits': 0,
                'cooldown_skipped': 0
            }
        }

        try:
            # Run YOLO detection
            yolo_results = self.yolo_model(frame, verbose=False)

            if len(yolo_results[0].boxes) == 0:
                return results

            # Process each detection
            for box in yolo_results[0].boxes:
                conf = box.conf.item()
                cls = int(box.cls.item())
                class_name = self.yolo_model.names[cls]

                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

                detection_info = {
                    'class': class_name,
                    'confidence': conf,
                    'bbox': (x1, y1, x2, y2)
                }

                results['detections'].append(detection_info)
                results['stats']['total_detections'] += 1

                # Check if we should trigger API call
                if not self._should_trigger_api_call(class_name, conf):
                    results['stats']['cooldown_skipped'] += 1
                    continue

                # Generate CLIP embedding for the detected object
                embedding = self.clip_embedding.get_object_embedding(frame, (x1, y1, x2, y2))

                if embedding is None:
                    logger.warning(f"Failed to generate embedding for {class_name}")
                    continue

                # Suggest prompt template
                template_name = self.prompt_templates.suggest_template([class_name])
                prompt = self.prompt_templates.get_prompt(template_name)

                # Check cache first
                cached_response = self._find_similar_cached_response(embedding, template_name)

                if cached_response:
                    results['cached_responses'].append({
                        'class': class_name,
                        'response': cached_response,
                        'template': template_name
                    })
                    results['stats']['cache_hits'] += 1
                    logger.info(f"Cache hit for {class_name}")

                else:
                    # Make API call
                    logger.info(f"Making API call for {class_name}")
                    api_response = self.vision_api.query_vision(frame, prompt)

                    if api_response:
                        results['api_responses'].append({
                            'class': class_name,
                            'response': api_response,
                            'template': template_name
                        })
                        results['stats']['api_calls_made'] += 1

                        # Cache the response
                        self._cache_response(embedding, template_name, api_response, class_name, conf)

                    else:
                        logger.warning(f"API call failed for {class_name}")

        except Exception as e:
            logger.error(f"Error processing frame: {e}")

        return results

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get total entries
            cursor.execute('SELECT COUNT(*) FROM vision_cache')
            total_entries = cursor.fetchone()[0]

            # Get hit counts
            cursor.execute('SELECT SUM(hit_count) FROM vision_cache')
            total_hits = cursor.fetchone()[0] or 0

            # Get entries by object class
            cursor.execute('''
                SELECT object_class, COUNT(*), AVG(confidence)
                FROM vision_cache
                GROUP BY object_class
                ORDER BY COUNT(*) DESC
            ''')
            class_stats = cursor.fetchall()

            conn.close()

            return {
                'total_entries': total_entries,
                'total_hits': total_hits,
                'hit_rate': total_hits / (total_entries + total_hits) if total_entries > 0 else 0,
                'class_stats': class_stats
            }

        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}
