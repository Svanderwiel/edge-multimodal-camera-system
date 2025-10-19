#!/usr/bin/env python3
"""
Quick Laptop Test - Immediate Results
Takes a photo and asks Gemini about laptop brand
"""

import cv2
import numpy as np
from ultralytics import YOLO
from vision_api_client import VisionAPIClient
from prompt_templates import PromptTemplates
import time

def quick_laptop_test():
    """Quick test with immediate laptop detection and API call"""
    
    print("=== Quick Laptop Brand Test ===")
    print("This will take a photo and ask Gemini about any laptop detected")
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
    print("   Point camera at a laptop!")
    
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
    
    laptop_found = False
    laptop_bbox = None
    laptop_confidence = 0
    
    if len(yolo_results[0].boxes) > 0:
        for box in yolo_results[0].boxes:
            conf = box.conf.item()
            cls = int(box.cls.item())
            class_name = yolo_model.names[cls]
            
            print(f"   Detected: {class_name} (confidence: {conf:.2f})")
            
            if class_name == 'laptop' and conf > 0.5:  # Lower threshold for demo
                laptop_found = True
                laptop_bbox = box.xyxy[0].cpu().numpy().astype(int)
                laptop_confidence = conf
                break
    
    if laptop_found:
        print(f"\n🎯 LAPTOP DETECTED!")
        print(f"   Confidence: {laptop_confidence:.2f}")
        
        # Crop laptop
        x1, y1, x2, y2 = laptop_bbox
        laptop_crop = frame[y1:y2, x1:x2]
        
        # Ask Gemini about the laptop
        prompt = templates.get_prompt('product_info')
        print(f"\n🤖 Asking Gemini: {prompt}")
        print("   Making API call...")
        
        api_response = vision_api.query_vision(laptop_crop, prompt)
        
        if api_response:
            print(f"\n✅ GEMINI RESPONSE:")
            print(f"   {api_response}")
            print()
            print("🎉 SUCCESS! Real API response received!")
        else:
            print("❌ API call failed")
    else:
        print("\n❌ No laptop detected")
        print("   Try pointing camera at a laptop and run again")
    
    # Final stats
    final_stats = vision_api.get_stats()
    print(f"\n📊 API Usage: {final_stats['daily_calls_made']} calls made, {final_stats['daily_remaining']} remaining")

if __name__ == "__main__":
    quick_laptop_test()
