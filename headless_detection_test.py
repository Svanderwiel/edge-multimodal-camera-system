#!/usr/bin/env python3
"""
Headless Object Detection Test - 15 seconds
No display, just detection and logging
"""

import cv2
import time
from ultralytics import YOLO

def main():
    print("=== Headless Object Detection Test (15 seconds) ===")
    
    # Load model
    print("Loading YOLO model...")
    model = YOLO('yolov8n.pt')
    print("Model loaded!")
    
    # Initialize camera
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Cannot open camera!")
        return
    
    print("Camera opened! Starting detection...")
    print("Running for 15 seconds...")
    
    start_time = time.time()
    frame_count = 0
    detection_count = 0
    
    try:
        while True:
            # Check time limit
            elapsed = time.time() - start_time
            if elapsed >= 15.0:
                break
            
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Cannot read frame!")
                break
            
            frame_count += 1
            
            # Run detection
            results = model(frame, verbose=False)
            
            # Count detections
            if len(results[0].boxes) > 0:
                detection_count += len(results[0].boxes)
                # Print detection info
                for box in results[0].boxes:
                    conf = box.conf.item()
                    cls = int(box.cls.item())
                    class_name = model.names[cls]
                    print(f"Frame {frame_count}: {class_name} (confidence: {conf:.2f})")
            
            # Print progress every 3 seconds
            if int(elapsed) % 3 == 0 and elapsed > 0:
                fps = frame_count / elapsed
                print(f"Time: {elapsed:.1f}s | FPS: {fps:.1f} | Detections: {detection_count}")
    
    except KeyboardInterrupt:
        print("\nStopped by user")
    
    finally:
        cap.release()
        
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        print(f"\n=== Test Complete ===")
        print(f"Time: {elapsed:.1f}s")
        print(f"Frames processed: {frame_count}")
        print(f"Average FPS: {fps:.2f}")
        print(f"Total detections: {detection_count}")
        print(f"Detections per second: {detection_count/elapsed:.2f}")

if __name__ == "__main__":
    main()
