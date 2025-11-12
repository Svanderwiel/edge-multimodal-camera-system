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
- **Modular Architecture**: Professional Python package structure following best practices

## 📊 Current Status

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

### 🚧 Phase 4: Response Display - IN PROGRESS
- Text overlay system
- Visual polish and animations
- Multiple simultaneous responses

## 🏗️ Project Structure

```
edge-multimodal-camera-system/
├── src/
│   └── multimodal_camera/           # Main package
│       ├── __init__.py
│       ├── core/                    # Core functionality
│       │   ├── __init__.py
│       │   └── config.py           # Configuration management
│       ├── detection/               # Detection components
│       │   ├── __init__.py
│       │   └── manager.py          # Smart triggering & caching
│       ├── vision/                  # Vision API components
│       │   ├── __init__.py
│       │   ├── api_client.py       # Gemini API client
│       │   ├── prompt_templates.py # Prompt templates
│       │   └── embeddings.py       # CLIP embeddings
│       ├── cache/                   # Caching system
│       │   └── __init__.py
│       └── utils/                   # Utilities
│           └── __init__.py
├── scripts/                         # Executable scripts
│   ├── __init__.py
│   ├── run_demo.py                 # Main integrated demo
│   ├── test_api.py                 # Test API connection
│   └── test_embeddings.py          # Test CLIP embeddings
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_config.py
│   └── test_prompt_templates.py
├── data/                            # Data directory
│   ├── models/                     # YOLO models
│   │   ├── yolov8n.pt
│   │   └── yolo11n.pt
│   └── cache/                      # SQLite database location
├── config/                          # Configuration
│   └── .env.example                # Environment template
├── docs/                            # Documentation
│   └── PRD/                        # Product requirements
│       ├── edge_ai_camera_prd.md
│       ├── ARCHITECTURE.md
│       └── ...
├── requirements.txt                 # Python dependencies
├── setup.py                        # Package installation
├── pyproject.toml                  # Modern Python config
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam or USB camera
- (Optional) NVIDIA GPU with CUDA for faster processing

### 1. Clone Repository

```bash
git clone https://github.com/Svanderwiel/edge-multimodal-camera-system.git
cd edge-multimodal-camera-system
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install package in development mode
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt

# Install CLIP (required for embeddings)
pip install git+https://github.com/openai/CLIP.git
```

### 4. Configure API Keys

```bash
# Copy environment template
cp config/.env.example .env

# Edit .env and add your Gemini API key
# Get your key from: https://aistudio.google.com/app/apikey
```

Your `.env` file should look like:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

## 🎮 Usage

### Run Main Demo

```bash
# From project root
python scripts/run_demo.py

# Controls:
# - Press 'q' to quit
# - Press 's' to analyze current frame
```

### Test Components

```bash
# Test API connection
python scripts/test_api.py

# Test CLIP embeddings
python scripts/test_embeddings.py
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/multimodal_camera --cov-report=html
```

### Install as Package

```bash
# Install in development mode (editable)
pip install -e .

# Then import in Python
from multimodal_camera import DetectionManager, VisionAPIClient
```

## 📈 Performance Metrics

| Component | Performance | Status |
|-----------|-------------|--------|
| YOLO Detection | 30+ fps | ✅ Working |
| CLIP Embedding | ~50ms/object | ✅ Working |
| Cache Lookup | <1ms | ✅ Working |
| API Response | <3s | ✅ Working |
| Image Optimization | 75% reduction | ✅ Working |
| Cost per Day | $0 (free tier) | ✅ Working |

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

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# API Configuration
GOOGLE_API_KEY=your_key_here
MAX_API_CALLS_PER_MINUTE=25
API_TIMEOUT_SECONDS=15

# Image Processing
IMAGE_QUALITY=80
IMAGE_SIZE=512

# Detection Settings
CONFIDENCE_THRESHOLD=0.7
COOLDOWN_SECONDS=10

# Cache Settings
CACHE_TTL_HOURS=24
```

## 💰 Cost Control

### Smart Triggering
- **Cooldown Logic**: 10-second cooldown per object class
- **Confidence Filtering**: Only processes detections >0.7 confidence
- **Cache-First**: Checks cache before making API calls

### Cost Savings
- **Free Tier**: 1,500 Gemini calls/day at $0 cost
- **Smart Caching**: Same object detected 10 times = 1 API call
- **99.7% Reduction**: vs naive streaming approach (1,800 calls/min → 5-10 calls/min)

## 🧪 Development

### Code Formatting

```bash
# Format code with black
black src/ scripts/ tests/

# Lint with flake8
flake8 src/ scripts/ tests/
```

### Adding New Features

1. Add code to appropriate module in `src/multimodal_camera/`
2. Write tests in `tests/`
3. Update documentation
4. Run tests: `pytest`

## 📚 Documentation

See `docs/PRD/` directory for detailed documentation:
- **edge_ai_camera_prd.md**: Complete project requirements
- **ARCHITECTURE.md**: System architecture details
- **IMPLEMENTATION_NOTES.md**: Implementation guidelines
- **PROGRESS_TRACKING.md**: Current progress status

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
- Try different camera index: `cv2.VideoCapture(1)` or `(2)`

### Import Errors
- Ensure package is installed: `pip install -e .`
- Check Python path includes `src/`
- Activate virtual environment

## 🤝 Contributing

This is a personal project for demonstrating multimodal AI capabilities. Feel free to fork and adapt for your own use cases.

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- **Ultralytics** for YOLO
- **OpenAI** for CLIP
- **Google** for Gemini API
- **NVIDIA** for Jetson platform

## 📧 Contact

For questions or feedback about this project, please refer to the documentation in the `docs/PRD/` directory.

---

**Last Updated**: November 2024
**Current Phase**: Phase 3 Complete, Phase 4 In Progress
**Version**: 0.1.0
