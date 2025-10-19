#!/usr/bin/env python3
"""
Integrated Demo - Phase 3 Implementation
Combines YOLO detection with CLIP+YOLO caching and Gemini API
"""

import cv2
import time
import numpy as np
from ultralytics import YOLO
from detection_manager import DetectionManager
from vision_api_client import VisionAPIClient
from prompt_templates import PromptTemplates
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def integrated_demo():
    """Demonstrate integrated YOLO + CLIP + Vision API system"""
    
    print("=== Integrated Demo - Phase 3 ===")
    print("This demo combines:")
    print("- YOLO object detection")
    print("- CLIP+YOLO embedding for object-specific caching")
    print("- Smart triggering with cooldown logic")
    print("- Gemini API integration")
    print()
    print("Press 'q' to quit, 's' to save current frame for analysis")
    print()
    
    # Initialize components
    print("Initializing components...")
    yolo_model = YOLO('yolov8n.pt')
    detection_manager = DetectionManager()
    vision_api = VisionAPIClient()
    templates = PromptTemplates()
    
    # Check API availability
    api_stats = vision_api.get_stats()
    print(f"Available API providers: {api_stats['available_providers']}")
    
    if not api_stats['available_providers']:
        print("⚠️  No API keys configured. Detection will work, but API calls will be skipped.")
        print("   Set GOOGLE_API_KEY in .env file to enable Gemini API integration.")
        print()
    
    # Initialize camera
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera!")
        return
    
    print("Camera opened! Starting detection...")
    print("=" * 50)
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    start_time = time.time()
    frame_count = 0
    last_api_call = 0
    api_call_cooldown = 5  # 5 seconds between API calls for demo
    
    try:
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame!")
                break
            
            frame_count += 1
            
            # Process frame with DetectionManager
            results = detection_manager.process_frame(frame)
            
            # Draw detections
            annotated_frame = frame.copy()
            
            # Draw bounding boxes and labels
            for detection in results['detections']:
                x1, y1, x2, y2 = detection['bbox']
                class_name = detection['class']
                confidence = detection['confidence']
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                label = f"{class_name}: {confidence:.2f}"
                cv2.putText(annotated_frame, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # Add info overlay
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            info_text = f"FPS: {fps:.1f} | Objects: {len(results['detections'])}"
            cv2.putText(annotated_frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add API status
            if api_stats['available_providers']:
                api_status = f"API: Ready | Calls: {results['stats']['api_calls_made']} | Cache: {results['stats']['cache_hits']}"
                cv2.putText(annotated_frame, api_status, (10, 450), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            else:
                cv2.putText(annotated_frame, "API: No keys configured", (10, 450), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            # Show frame
            cv2.imshow('Integrated Demo - Phase 3', annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s') and api_stats['available_providers']:
                # Save current frame for API analysis
                current_time = time.time()
                if current_time - last_api_call >= api_call_cooldown:
                    print(f"\nAnalyzing frame with DetectionManager...")
                    
                    # Process frame for analysis
                    analysis_results = detection_manager.process_frame(frame)
                    
                    print(f"Detections: {analysis_results['stats']['total_detections']}")
                    print(f"API calls made: {analysis_results['stats']['api_calls_made']}")
                    print(f"Cache hits: {analysis_results['stats']['cache_hits']}")
                    print(f"Cooldown skipped: {analysis_results['stats']['cooldown_skipped']}")
                    
                    # Print API responses
                    for response in analysis_results['api_responses']:
                        print(f"\nAPI Response for {response['class']}:")
                        print(f"  {response['response']}")
                        
                    # Print cached responses
                    for response in analysis_results['cached_responses']:
                        print(f"\nCached Response for {response['class']}:")
                        print(f"  {response['response']}")
                    
                    last_api_call = current_time
                else:
                    remaining = api_call_cooldown - (current_time - last_api_call)
                    print(f"API call cooldown: {remaining:.1f}s remaining")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        # Print final stats
        total_time = time.time() - start_time
        avg_fps = frame_count / total_time if total_time > 0 else 0
        
        print()
        print("=" * 50)
        print("=== Demo Complete ===")
        print(f"Total time: {total_time:.1f}s")
        print(f"Total frames: {frame_count}")
        print(f"Average FPS: {avg_fps:.2f}")
        
        # Get final cache stats
        cache_stats = detection_manager.get_cache_stats()
        print(f"\nCache Statistics:")
        print(f"Total entries: {cache_stats.get('total_entries', 0)}")
        print(f"Total hits: {cache_stats.get('total_hits', 0)}")
        print(f"Hit rate: {cache_stats.get('hit_rate', 0):.2%}")
        
        if api_stats['available_providers']:
            final_api_stats = vision_api.get_stats()
            print(f"\nAPI Statistics:")
            print(f"Daily calls made: {final_api_stats['daily_calls_made']}")
            print(f"Daily remaining: {final_api_stats['daily_remaining']}")
        
        print("=" * 50)

if __name__ == "__main__":
    integrated_demo()
