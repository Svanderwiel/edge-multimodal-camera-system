# Multimodal AI Camera Assistant

A real-time intelligent camera system that combines on-device object detection (YOLO) with cloud-based vision-language models (Gemini) to understand and describe the world conversationally.

## 🎯 Project Overview

This system demonstrates cutting-edge multimodal AI, edge-cloud hybrid architecture, and hardware-software integration. It detects objects locally at 30+ fps using YOLO, then selectively queries Gemini API only when interesting objects appear, displaying natural language descriptions.

### Key Features

- **Real-time Object Detection**: YOLO-based detection at 30+ fps
- **CLIP+YOLO Embeddings**: Object-specific 512-dimensional embeddings for fine-detail recognition
- **Smart Caching**: SQLite-based response caching with object-specific embeddings
- **Cost Control**: Smart triggering with cooldown logic and confidence filtering
- **Free API Usage**: Google Gemini free tier (1,500 calls/day)
- **Fine-Detail Recognition**: Can distinguish ripeness, brands, conditions, and more

## 🚀 Current Status

### ✅ Phase 1: Foundation - COMPLETED
- YOLO object detection at 30+ fps
- Camera pipeline with live video feed
- Performance testing scripts

### ✅ Phase 2: Vision API Integration - COMPLETED
- Gemini API client with image optimization
- 10 specialized prompt templates
- Rate limiting and cost control
- 75% image size reduction

### ✅ Phase 3: Smart Triggering & Cost Control - COMPLETED
- CLIP+YOLO object-specific embeddings
- SQLite response caching
- Smart triggering with cooldown logic
- Confidence threshold filtering (>0.7)
- Real Gemini API integration working

### ⏳ Phase 4: Response Display - PENDING
- Text overlay system
- Visual polish and animations
- Multiple simultaneous responses

## 🛠️ Hardware Requirements

- **NVIDIA Jetson Orin Nano Developer Kit** (or any system with camera)
- **Camera**: Raspberry Pi Camera Module 3 or USB webcam
- **Storage**: 128GB microSD card
- **Python**: 3.10+

## 📦 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd multimodal_camera
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install ultralytics opencv-python numpy pillow python-dotenv requests
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install git+https://github.com/openai/CLIP.git
```

### 4. Configure API Keys
```bash
# Edit .env file
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your Gemini API key from: https://aistudio.google.com/app/apikey

## 🎮 Usage

### Quick Tests

**Test Any Object Detection:**
```bash
source venv/bin/activate
python any_object_test.py
```

**Test Laptop Brand Detection:**
```bash
python laptop_brand_test.py
```

**Test CLIP Embeddings:**
```bash
python clip_embedding.py
```

**Test Vision API:**
```bash
python vision_api_client.py
```

### Full Demos

**Integrated Demo (Phase 3):**
```bash
python integrated_demo.py
```

**Headless Detection Test:**
```bash
python headless_detection_test.py
```

## 📊 Performance Metrics

| Component | Performance | Status |
|-----------|-------------|--------|
| YOLO Detection | 30+ fps | ✅ |
| CLIP Embedding | ~50ms/object | ✅ |
| Cache Lookup | <1ms | ✅ |
| API Response | <3s | ✅ |
| Image Optimization | 75% reduction | ✅ |
| Cost per Day | $0 (free tier) | ✅ |

## 🎯 Capabilities

### What You Can Ask

- **"Which banana is more ripe?"** - Distinguishes ripeness levels
- **"What brand is this laptop?"** - Identifies brands and models
- **"Is this food fresh?"** - Quality assessment
- **"What's in my fridge?"** - Scene analysis
- **"Compare these two objects"** - Object-specific comparison

### Prompt Templates

1. **general_description** - Basic object description
2. **food_nutrition** - Food identification and nutrition
3. **product_info** - Product details and pricing
4. **plant_care** - Plant identification and care
5. **book_info** - Book identification and details
6. **visual_qa** - Answer specific questions
7. **scene_analysis** - Comprehensive scene description
8. **kitchen_assistant** - Kitchen inventory management
9. **safety_check** - Safety assessment
10. **accessibility** - Accessibility analysis

## 🏗️ Project Structure

```
multimodal_camera/
├── PRD/                          # Product requirements and documentation
│   ├── edge_ai_camera_prd.md    # Main PRD
│   ├── ARCHITECTURE.md           # System architecture
│   ├── IMPLEMENTATION_NOTES.md   # Implementation details
│   ├── PROGRESS_TRACKING.md      # Progress tracking
│   ├── PHASE2_SUMMARY.md         # Phase 2 completion
│   └── PHASE3_SUMMARY.md         # Phase 3 completion
├── clip_embedding.py             # CLIP embedding generator
├── detection_manager.py          # Smart triggering and caching
├── vision_api_client.py          # Gemini API client
├── prompt_templates.py           # Prompt template system
├── integrated_demo.py            # Full Phase 3 demo
├── any_object_test.py            # Test with any object
├── laptop_brand_test.py          # Laptop brand detection test
├── test_detection.py             # YOLO detection test
├── vision_cache.db               # SQLite cache database
├── .env                          # Environment configuration
├── .env.example                  # Configuration template
└── .gitignore                    # Git ignore file
```

## 🔧 Configuration

Edit `.env` file to customize:

```bash
# Gemini API
GOOGLE_API_KEY=your_key_here

# API Configuration
MAX_API_CALLS_PER_MINUTE=25
API_TIMEOUT_SECONDS=15
IMAGE_QUALITY=80
IMAGE_SIZE=512

# Cost Control
MONTHLY_BUDGET_USD=0.0  # Free tier
CACHE_TTL_HOURS=24
```

## 📈 Cost Control

### Smart Triggering
- **Cooldown Logic**: 10-second cooldown per object class
- **Confidence Filtering**: Only processes detections >0.7 confidence
- **Cache-First**: Checks cache before making API calls

### Cost Savings
- **Free Tier**: 1,500 Gemini calls/day at $0 cost
- **Smart Caching**: Same object detected 10 times = 1 API call
- **99.7% Reduction**: vs naive streaming approach

## 🧪 Testing

### Run All Tests
```bash
source venv/bin/activate

# Test CLIP embeddings
python clip_embedding.py

# Test Vision API
python vision_api_client.py

# Test with real objects
python any_object_test.py
```

### Expected Results
- CLIP embeddings: 512-dimensional vectors
- API responses: Detailed object descriptions
- Cache hits: Instant responses for similar objects

## 🐛 Troubleshooting

### No API Response
- Check API key in `.env` file
- Verify internet connection
- Check API quota (1,500/day free tier)

### Low Detection Confidence
- Ensure good lighting
- Point camera directly at object
- Try different objects

### Camera Not Found
- Check camera connection
- Verify camera permissions
- Try different camera index (0, 1, 2)

## 📚 Documentation

See `PRD/` directory for detailed documentation:
- **edge_ai_camera_prd.md**: Complete project requirements
- **ARCHITECTURE.md**: System architecture details
- **IMPLEMENTATION_NOTES.md**: Implementation guidelines
- **PROGRESS_TRACKING.md**: Current progress status

## 🎓 Learning Resources

- **YOLO**: https://docs.ultralytics.com/
- **CLIP**: https://github.com/openai/CLIP
- **Gemini API**: https://ai.google.dev/gemini-api/docs
- **OpenCV**: https://docs.opencv.org/

## 🤝 Contributing

This is a personal project for demonstrating multimodal AI capabilities. Feel free to fork and adapt for your own use cases.

## 📝 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- **Ultralytics** for YOLO
- **OpenAI** for CLIP
- **Google** for Gemini API
- **NVIDIA** for Jetson platform

## 📧 Contact

For questions or feedback about this project, please refer to the documentation in the `PRD/` directory.

---

**Last Updated**: October 18, 2024  
**Current Phase**: Phase 3 Complete  
**Next Milestone**: Phase 4 - Response Display
