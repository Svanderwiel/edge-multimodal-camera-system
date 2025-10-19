#!/usr/bin/env python3
"""
Integrated Detection Example
Combines YOLO object detection with Vision API for Phase 2 demonstration
"""

import cv2
import time
import numpy as np
from ultralytics import YOLO
from vision_api_client import VisionAPIClient
from prompt_templates import PromptTemplates

def integrated_detection_demo():
    """Demonstrate integrated YOLO + Vision API detection"""
    
    print("=== Integrated Detection Demo ===")
    print("This demo combines YOLO object detection with Vision API")
    print("Press 'q' to quit, 's' to save current frame for API analysis")
    print()
    
    # Initialize components
    print("Loading YOLO model...")
    model = YOLO('yolov8n.pt')
    
    print("Initializing Vision API client...")
    api_client = VisionAPIClient()
    templates = PromptTemplates()
    
    # Check if API keys are configured
    stats = api_client.get_stats()
    if not stats['available_providers']:
        print("⚠️  No API keys configured. YOLO detection will work, but Vision API calls will be skipped.")
        print("   Set up API keys in .env file to enable Vision API integration.")
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
    api_call_cooldown = 10  # 10 seconds between API calls
    
    try:
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame!")
                break
            
            frame_count += 1
            
            # Run YOLO detection
            results = model(frame, verbose=False)
            annotated_frame = results[0].plot()
            
            # Get detection info
            detections = []
            if len(results[0].boxes) > 0:
                for box in results[0].boxes:
                    conf = box.conf.item()
                    cls = int(box.cls.item())
                    class_name = model.names[cls]
                    detections.append((class_name, conf))
            
            # Add info overlay
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            info_text = f"FPS: {fps:.1f} | Objects: {len(detections)}"
            cv2.putText(annotated_frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show detection details
            if detections:
                y_offset = 60
                for i, (class_name, conf) in enumerate(detections[:3]):  # Show top 3
                    text = f"{class_name}: {conf:.2f}"
                    cv2.putText(annotated_frame, text, (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    y_offset += 20
            
            # Show API status
            if stats['available_providers']:
                api_status = f"API: Ready | Cost: ${stats['total_cost']:.3f}"
                cv2.putText(annotated_frame, api_status, (10, 450), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            else:
                cv2.putText(annotated_frame, "API: No keys configured", (10, 450), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            # Show frame
            cv2.imshow('Integrated Detection Demo', annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s') and stats['available_providers']:
                # Save current frame for API analysis
                current_time = time.time()
                if current_time - last_api_call >= api_call_cooldown:
                    print(f"\nAnalyzing frame with Vision API...")
                    
                    # Suggest template based on detections
                    detected_objects = [det[0] for det in detections]
                    template_name = templates.suggest_template(detected_objects)
                    prompt = templates.get_prompt(template_name)
                    
                    print(f"Using template: {template_name}")
                    print(f"Prompt: {prompt}")
                    
                    # Make API call
                    result = api_client.query_vision(frame, prompt)
                    
                    if result:
                        print(f"Vision API Response: {result}")
                        
                        # Display response on screen for 5 seconds
                        response_start = time.time()
                        while time.time() - response_start < 5:
                            display_frame = annotated_frame.copy()
                            cv2.putText(display_frame, "Vision API Response:", (10, 120), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                            
                            # Word wrap the response
                            words = result.split()
                            lines = []
                            current_line = ""
                            for word in words:
                                if len(current_line + word) < 50:
                                    current_line += word + " "
                                else:
                                    lines.append(current_line.strip())
                                    current_line = word + " "
                            if current_line:
                                lines.append(current_line.strip())
                            
                            # Display lines
                            for i, line in enumerate(lines[:4]):  # Max 4 lines
                                cv2.putText(display_frame, line, (10, 150 + i*25), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                            
                            cv2.imshow('Integrated Detection Demo', display_frame)
                            cv2.waitKey(1)
                        
                        last_api_call = current_time
                    else:
                        print("Vision API call failed")
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
        
        if stats['available_providers']:
            final_stats = api_client.get_stats()
            print(f"API calls made: {final_stats['calls_this_minute']}")
            print(f"Total cost: ${final_stats['total_cost']:.4f}")
            print(f"Budget remaining: ${final_stats['budget_remaining']:.2f}")
        
        print("=" * 50)

if __name__ == "__main__":
    integrated_detection_demo()
