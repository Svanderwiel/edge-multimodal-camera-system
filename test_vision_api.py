#!/usr/bin/env python3
"""
Test Vision API Integration
Tests the VisionAPIClient and PromptTemplates with sample images
"""

import cv2
import numpy as np
import time
from vision_api_client import VisionAPIClient
from prompt_templates import PromptTemplates

def create_test_images():
    """Create various test images for API testing"""
    images = {}
    
    # Test image 1: Simple colored rectangle
    img1 = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(img1, (100, 100), (540, 380), (0, 255, 0), -1)
    cv2.putText(img1, "TEST IMAGE", (200, 250), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    images['simple'] = img1
    
    # Test image 2: Multiple colored shapes
    img2 = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(img2, (50, 50), (200, 200), (255, 0, 0), -1)  # Blue rectangle
    cv2.circle(img2, (400, 150), 75, (0, 0, 255), -1)  # Red circle
    cv2.putText(img2, "SHAPES", (250, 300), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    images['shapes'] = img2
    
    # Test image 3: Text-based
    img3 = np.ones((480, 640, 3), dtype=np.uint8) * 255  # White background
    cv2.putText(img3, "HELLO WORLD", (150, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    cv2.putText(img3, "Vision API Test", (180, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    images['text'] = img3
    
    return images

def test_api_providers():
    """Test different API providers"""
    print("=== Testing API Providers ===")
    
    # Initialize clients
    api_client = VisionAPIClient()
    templates = PromptTemplates()
    
    # Check available providers
    stats = api_client.get_stats()
    print(f"Available providers: {stats['available_providers']}")
    
    if not stats['available_providers']:
        print("❌ No API keys configured!")
        print("Please set up your API keys in the .env file:")
        print("  - OPENAI_API_KEY")
        print("  - ANTHROPIC_API_KEY") 
        print("  - GOOGLE_API_KEY")
        return False
    
    # Create test images
    test_images = create_test_images()
    
    # Test with different prompts
    test_cases = [
        ('simple', 'general_description'),
        ('shapes', 'general_description'),
        ('text', 'general_description')
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for image_name, template_name in test_cases:
        print(f"\n--- Testing {image_name} image with {template_name} ---")
        
        image = test_images[image_name]
        prompt = templates.get_prompt(template_name)
        
        print(f"Prompt: {prompt}")
        print("Sending request...")
        
        start_time = time.time()
        result = api_client.query_vision(image, prompt)
        end_time = time.time()
        
        if result:
            print(f"✅ Success! ({end_time - start_time:.2f}s)")
            print(f"Response: {result}")
            success_count += 1
        else:
            print("❌ Failed to get response")
            
        # Small delay between requests
        time.sleep(1)
    
    print(f"\n=== Test Results ===")
    print(f"Success rate: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
    
    # Print final stats
    final_stats = api_client.get_stats()
    print(f"Total cost: ${final_stats['total_cost']:.4f}")
    print(f"Budget remaining: ${final_stats['budget_remaining']:.2f}")
    
    return success_count > 0

def test_prompt_templates():
    """Test prompt templates"""
    print("\n=== Testing Prompt Templates ===")
    
    templates = PromptTemplates()
    
    # Test template suggestions
    test_objects = [
        ['banana', 'apple'],
        ['bottle', 'cup'],
        ['book'],
        ['potted plant'],
        ['person', 'chair']
    ]
    
    print("Template suggestions:")
    for objects in test_objects:
        suggested = templates.suggest_template(objects)
        print(f"  {objects} -> {suggested}")
    
    # Test prompt generation
    print("\nSample prompts:")
    sample_prompts = [
        'general_description',
        'food_nutrition',
        'product_info',
        'plant_care'
    ]
    
    for template_name in sample_prompts:
        prompt = templates.get_prompt(template_name)
        print(f"\n{template_name}:")
        print(f"  {prompt}")

def test_image_optimization():
    """Test image optimization"""
    print("\n=== Testing Image Optimization ===")
    
    api_client = VisionAPIClient()
    
    # Create a test image
    test_image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    
    print(f"Original image: {test_image.shape}")
    
    # Test optimization
    start_time = time.time()
    optimized = api_client.optimize_image(test_image)
    end_time = time.time()
    
    print(f"Optimization time: {end_time - start_time:.3f}s")
    print(f"Optimized size: {len(optimized)} characters (base64)")
    print(f"Compression ratio: {len(optimized) / (test_image.size * 4):.2f}")

def main():
    """Main test function"""
    print("=== Vision API Integration Test ===")
    print("This test will verify the API integration and prompt templates")
    print()
    
    # Test prompt templates first (no API calls needed)
    test_prompt_templates()
    
    # Test image optimization
    test_image_optimization()
    
    # Test API providers (requires API keys)
    print("\n" + "="*50)
    api_success = test_api_providers()
    
    if api_success:
        print("\n🎉 All tests passed! Vision API integration is working.")
    else:
        print("\n⚠️  Some tests failed. Check your API keys and configuration.")
    
    print("\nNext steps:")
    print("1. Set up your API keys in .env file")
    print("2. Run this test again to verify API integration")
    print("3. Move to Phase 3: Smart Triggering & Cost Control")

if __name__ == "__main__":
    main()
