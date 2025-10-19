#!/usr/bin/env python3
"""
Quick Object Detection Test - 15 seconds
Tests YOLO object detection with live camera feed
"""

import cv2
import time
import numpy as np
from ultralytics import YOLO

def test_object_detection():
    """Run object detection for 15 seconds"""
    
    print("=== Object Detection Test (15 seconds) ===")
    print("Loading YOLOv8n model...")
    model = YOLO('yolov8n.pt')
    print("Model loaded successfully!")
    print()
    
    # Initialize camera
    print("Initializing camera...")
    cap = cv2.VideoCapture(0)  # Use default camera
    
    if not cap.isOpened():
        print("Error: Could not open camera!")
        return
    
    print("Camera opened successfully!")
    print("Press 'q' to quit early")
    print()
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    start_time = time.time()
    frame_count = 0
    detection_count = 0
    
    print("Starting detection...")
    print("=" * 50)
    
    try:
        while True:
            # Check if 15 seconds have passed
            elapsed_time = time.time() - start_time
            if elapsed_time >= 15.0:
                break
            
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame!")
                break
            
            frame_count += 1
            
            # Run detection
            results = model(frame, verbose=False)
            
            # Draw detections
            annotated_frame = results[0].plot()
            
            # Count detections
            if len(results[0].boxes) > 0:
                detection_count += len(results[0].boxes)
            
            # Add info overlay
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            info_text = f"Time: {elapsed_time:.1f}s | FPS: {fps:.1f} | Detections: {detection_count}"
            cv2.putText(annotated_frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow('Object Detection Test', annotated_frame)
            
            # Check for quit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Print progress every 3 seconds
            if int(elapsed_time) % 3 == 0 and elapsed_time > 0:
                print(f"Time: {elapsed_time:.1f}s | FPS: {fps:.1f} | Detections: {detection_count}")
    
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
        print("=== Test Complete ===")
        print(f"Total time: {total_time:.1f}s")
        print(f"Total frames: {frame_count}")
        print(f"Average FPS: {avg_fps:.2f}")
        print(f"Total detections: {detection_count}")
        print(f"Detections per second: {detection_count/total_time:.2f}")
        print("=" * 50)

if __name__ == "__main__":
    test_object_detection()
