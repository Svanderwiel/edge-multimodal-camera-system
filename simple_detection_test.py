#!/usr/bin/env python3
"""
Simple Object Detection Test - 15 seconds
Minimal imports and error handling
"""

import cv2
import time
from ultralytics import YOLO

def main():
    print("=== Simple Object Detection Test (15 seconds) ===")
    
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
    print("Press 'q' to quit early")
    
    start_time = time.time()
    frame_count = 0
    
    try:
        while True:
            # Check time limit
            if time.time() - start_time >= 15.0:
                break
            
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Cannot read frame!")
                break
            
            frame_count += 1
            
            # Run detection
            results = model(frame, verbose=False)
            
            # Draw results
            annotated_frame = results[0].plot()
            
            # Add info
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            info = f"Time: {elapsed:.1f}s | FPS: {fps:.1f} | Frame: {frame_count}"
            cv2.putText(annotated_frame, info, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow('Detection Test', annotated_frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\nStopped by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        print(f"\nTest complete!")
        print(f"Time: {elapsed:.1f}s | Frames: {frame_count} | FPS: {fps:.1f}")

if __name__ == "__main__":
    main()
