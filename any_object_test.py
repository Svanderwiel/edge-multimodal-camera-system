#!/usr/bin/env python3
"""
Any Object Test - Test with any detected object
Tests the complete system with any object detected by YOLO
"""

import cv2
import numpy as np
from ultralytics import YOLO
from vision_api_client import VisionAPIClient
from prompt_templates import PromptTemplates
import time

def any_object_test():
    """Test with any detected object"""
    
    print("=== Any Object Detection Test ===")
    print("This will detect ANY object and ask Gemini about it")
    print()
    
    # Initialize components
    yolo_model = YOLO('yolov8n.pt')
    vision_api = VisionAPIClient()
    templates = PromptTemplates()
    
    # Check API
    stats = vision_api.get_stats()
    if 'google' not in stats['available_providers']:
        print("❌ Gemini API not configured!")
        return
    
    print(f"✅ Gemini API ready ({stats['daily_remaining']} calls remaining)")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open camera!")
        return
    
    print("📸 Taking photo in 3 seconds...")
    print("   Point camera at any object!")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Capture frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("❌ Could not capture photo!")
        return
    
    print("📷 Photo captured! Analyzing...")
    
    # Run YOLO detection
    yolo_results = yolo_model(frame, verbose=False)
    
    best_object = None
    best_confidence = 0
    
    if len(yolo_results[0].boxes) > 0:
        print("   Detected objects:")
        for box in yolo_results[0].boxes:
            conf = box.conf.item()
            cls = int(box.cls.item())
            class_name = yolo_model.names[cls]
            
            print(f"     - {class_name} (confidence: {conf:.2f})")
            
            if conf > best_confidence and conf > 0.3:  # Lower threshold
                best_object = {
                    'class': class_name,
                    'confidence': conf,
                    'bbox': box.xyxy[0].cpu().numpy().astype(int)
                }
                best_confidence = conf
    
    if best_object:
        print(f"\n�� SELECTED OBJECT: {best_object['class'].upper()}")
        print(f"   Confidence: {best_object['confidence']:.2f}")
        
        # Crop object
        x1, y1, x2, y2 = best_object['bbox']
        object_crop = frame[y1:y2, x1:x2]
        
        # Choose appropriate prompt template
        template_name = templates.suggest_template([best_object['class']])
        prompt = templates.get_prompt(template_name)
        
        print(f"\n🤖 Asking Gemini about {best_object['class']}:")
        print(f"   Template: {template_name}")
        print(f"   Prompt: {prompt}")
        print("   Making API call...")
        
        api_response = vision_api.query_vision(object_crop, prompt)
        
        if api_response:
            print(f"\n✅ GEMINI RESPONSE:")
            print(f"   {api_response}")
            print()
            print("🎉 SUCCESS! Real API response received!")
            print("   This proves the complete system is working!")
        else:
            print("❌ API call failed")
    else:
        print("\n❌ No objects detected with confidence > 0.3")
        print("   Try pointing camera at any object and run again")
    
    # Final stats
    final_stats = vision_api.get_stats()
    print(f"\n📊 API Usage: {final_stats['daily_calls_made']} calls made, {final_stats['daily_remaining']} remaining")

if __name__ == "__main__":
    any_object_test()
