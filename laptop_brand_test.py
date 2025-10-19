#!/usr/bin/env python3
"""
Laptop Brand Detection Test
Tests the complete system with real laptop detection and brand identification
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

def laptop_brand_test():
    """Test laptop detection and brand identification"""
    
    print("=== Laptop Brand Detection Test ===")
    print("This test will:")
    print("1. Run for 10 seconds looking for laptops")
    print("2. When a laptop is detected, ask Gemini for brand information")
    print("3. Show you the real API response")
    print()
    
    # Initialize components
    print("Initializing components...")
    yolo_model = YOLO('yolov8n.pt')
    detection_manager = DetectionManager()
    vision_api = VisionAPIClient()
    templates = PromptTemplates()
    
    # Check API availability
    api_stats = vision_api.get_stats()
    print(f"Gemini API available: {'google' in api_stats['available_providers']}")
    print(f"Daily calls remaining: {api_stats['daily_remaining']}")
    print()
    
    if 'google' not in api_stats['available_providers']:
        print("❌ Gemini API not configured!")
        return
    
    # Initialize camera
    print("Opening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Could not open camera!")
        return
    
    print("✅ Camera opened! Starting 10-second test...")
    print("=" * 60)
    
    start_time = time.time()
    frame_count = 0
    laptop_detected = False
    laptop_responses = []
    
    try:
        while time.time() - start_time < 10:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("❌ Could not read frame!")
                break
            
            frame_count += 1
            
            # Run YOLO detection
            yolo_results = yolo_model(frame, verbose=False)
            
            # Check for laptops
            laptop_found = False
            laptop_bbox = None
            laptop_confidence = 0
            
            if len(yolo_results[0].boxes) > 0:
                for box in yolo_results[0].boxes:
                    conf = box.conf.item()
                    cls = int(box.cls.item())
                    class_name = yolo_model.names[cls]
                    
                    if class_name == 'laptop' and conf > 0.7:
                        laptop_found = True
                        laptop_bbox = box.xyxy[0].cpu().numpy().astype(int)
                        laptop_confidence = conf
                        break
            
            # If laptop found and we haven't asked about it yet
            if laptop_found and not laptop_detected:
                laptop_detected = True
                print(f"\n🎯 LAPTOP DETECTED!")
                print(f"   Confidence: {laptop_confidence:.2f}")
                print(f"   Bounding box: {laptop_bbox}")
                print(f"   Asking Gemini for brand information...")
                
                # Crop the laptop from the frame
                x1, y1, x2, y2 = laptop_bbox
                laptop_crop = frame[y1:y2, x1:x2]
                
                # Use product info prompt template
                prompt = templates.get_prompt('product_info')
                print(f"   Prompt: {prompt}")
                
                # Make API call
                api_response = vision_api.query_vision(laptop_crop, prompt)
                
                if api_response:
                    laptop_responses.append({
                        'confidence': laptop_confidence,
                        'bbox': laptop_bbox,
                        'response': api_response
                    })
                    
                    print(f"\n✅ GEMINI RESPONSE:")
                    print(f"   {api_response}")
                    print()
                else:
                    print("❌ API call failed")
            
            # Show progress
            elapsed = time.time() - start_time
            if frame_count % 30 == 0:  # Every 30 frames
                print(f"Time: {elapsed:.1f}s | Frames: {frame_count} | Laptop detected: {laptop_detected}")
    
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    
    finally:
        cap.release()
        
        # Print final results
        total_time = time.time() - start_time
        print("\n" + "=" * 60)
        print("=== TEST RESULTS ===")
        print(f"Total time: {total_time:.1f}s")
        print(f"Total frames: {frame_count}")
        print(f"Laptop detected: {laptop_detected}")
        print(f"API responses received: {len(laptop_responses)}")
        
        if laptop_responses:
            print("\n📱 LAPTOP BRAND ANALYSIS:")
            for i, response in enumerate(laptop_responses, 1):
                print(f"\nDetection {i}:")
                print(f"  Confidence: {response['confidence']:.2f}")
                print(f"  Gemini Response: {response['response']}")
        else:
            print("\n❌ No laptop detected with confidence > 0.7")
            print("   Try pointing the camera at a laptop")
        
        # Final API stats
        final_stats = vision_api.get_stats()
        print(f"\n📊 API Usage:")
        print(f"  Calls made: {final_stats['daily_calls_made']}")
        print(f"  Remaining: {final_stats['daily_remaining']}")
        
        print("=" * 60)

if __name__ == "__main__":
    laptop_brand_test()
