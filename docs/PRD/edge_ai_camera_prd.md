# Multimodal AI Camera Assistant - Product Requirements Document

## Executive Summary

Build a real-time intelligent camera system that combines on-device object detection with cloud-based vision-language models to understand and describe the world conversationally. The system detects objects locally at 30-60fps using YOLO, then selectively queries vision APIs (GPT-4V, Claude, Gemini) only when interesting objects appear, displaying natural language descriptions overlaid on the live video feed.

**Core Value**: Demonstrates cutting-edge multimodal AI, edge-cloud hybrid architecture, and hardware-software integration skills for MAG-7 company interviews.

**Timeline**: 6-8 weeks to impressive MVP

---

## Target Audience

### Primary: Hiring Managers & Engineers At
- **Google**: Pixel camera team, Google Lens, Gemini integration
- **Meta**: Reality Labs, AR glasses, Ray-Ban Meta AI features
- **Apple**: Vision Pro team, spatial computing, on-device ML
- **OpenAI/Anthropic**: Multimodal AI applications, API integrations

### Why This Project Matters to Them
- Shows understanding of edge-cloud hybrid architecture (how real products work)
- Demonstrates multimodal AI integration (hottest skill in 2025)
- Proves hardware-software co-design capabilities
- Evidence of shipping complete, working systems

---

## Key Success Indicators

### Technical Metrics
- **Performance**: 30+ fps object detection on Jetson Orin Nano
- **Latency**: <3 seconds from detection to displayed response
- **Accuracy**: >70% mAP on common object detection
- **Uptime**: System runs continuously for 1+ hour without crashes
- **Cost**: <$5/month API costs with proper caching

### Demo Quality
- 5+ "wow moment" scenarios working reliably
- Accurate, natural language responses
- Smooth, professional-looking video overlay
- 3-5 minute demo video ready for portfolio

### Code Quality
- Clean, documented codebase on GitHub
- Modular architecture (easy to extend)
- Error handling prevents crashes
- README with clear setup instructions

---

## System Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────┐
│                   Camera Input                       │
│              (30-60 fps video stream)               │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              YOLO Object Detection                   │
│                  (On-Device)                        │
│  • Runs at 30-60 fps locally                       │
│  • Detects 80 object classes                       │
│  • Draws bounding boxes                            │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            Smart Trigger Logic                       │
│  • New object detected?                             │
│  • Cooldown expired? (10 sec)                       │
│  • High confidence? (>0.7)                          │
│  • User question asked?                             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼ (Only 5-10 calls/min)
┌─────────────────────────────────────────────────────┐
│              Vision API Query                        │
│         (Cloud - GPT-4V/Claude/Gemini)              │
│  • Resize image to 512x512                          │
│  • Send with contextual prompt                      │
│  • Receive natural language response                │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            Response Cache Check                      │
│  • Check if similar query cached                    │
│  • Store new responses (10 min TTL)                 │
│  • 30-50% cache hit rate expected                   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           Display Response Overlay                   │
│  • Text overlay on video feed                       │
│  • Semi-transparent background                      │
│  • Auto-fade after 10 seconds                       │
│  • Optional: Text-to-speech output                  │
└──────────────────────────────────────────────────────┘
```

### Cost Control Architecture

```
Every Frame (Free):
├── Camera Capture
├── YOLO Detection (on-device)
└── Draw Bounding Boxes

Selective Frames (Paid):
├── Triggered by: New object + cooldown expired
├── API Call (~$0.01)
└── Cached for reuse

Result: 5-10 API calls/min instead of 1,800/min (30fps)
Cost Reduction: 99.7%
```

---

## Hardware Requirements

### Primary Development Hardware
- **NVIDIA Jetson Orin Nano Developer Kit** - $499 (already ordered ✓)
  - 40 TOPS AI performance
  - 8GB RAM
  - CUDA + TensorRT support
  - Expected YOLO performance: 60+ fps

### Required Accessories
- **MicroSD Card**: 128GB U3/A2 rated - $18
- **Camera**: Raspberry Pi Camera Module 3 (12MP) - $25
  - Alternative: USB Webcam (Logitech C920) - $50
- **Power Supply**: USB-C 5V/3A (15W) - $12
- **Cooling**: Active fan or heatsink - $10
- **HDMI Cable**: For monitor connection - $8
- **Keyboard + Mouse**: For setup - $20 (if needed)

### Optional Hardware
- **USB Speaker**: For text-to-speech output - $15
- **7" Touchscreen Display**: Portable setup - $60
- **Case**: Protective enclosure - $20

**Total Investment**: ~$575-625 (core) or ~$150-200 (accessories only, since Orin purchased)

---

## Technology Stack

### Edge Device (Jetson Orin Nano)
- **OS**: Ubuntu 20.04 (via JetPack 5.1.2+)
- **Language**: Python 3.8+
- **Object Detection**: Ultralytics YOLOv8-nano
- **Computer Vision**: OpenCV 4.5+
- **ML Optimization**: TensorRT (for 2-3x speedup)
- **Image Processing**: NumPy, Pillow

### Cloud APIs
- **Vision-Language Models**:
  - OpenAI GPT-4 Vision (~$0.01/image)
  - Anthropic Claude 3.5 Sonnet (~$0.005/image)
  - Google Gemini Pro Vision (1,500 free/day, then ~$0.002/image)
- **Speech** (Optional):
  - Google Text-to-Speech
  - OpenAI Whisper (for voice input)

### Supporting Tools
- **HTTP Client**: `requests` or `httpx` for API calls
- **Async**: `asyncio` for non-blocking API calls
- **Caching**: Local SQLite database
- **Config**: Python-dotenv for API keys
- **Logging**: Python logging module

### Development Tools
- **IDE**: Cursor AI (for AI-assisted coding)
- **Version Control**: Git + GitHub
- **Image Tools**: Base64 encoding, JPEG compression
- **Testing**: pytest (for unit tests)

---

## Project Tasks Breakdown

### Phase 1: Foundation (Week 1-2)

#### Hardware Setup
- [ ] Flash JetPack OS to microSD card
- [ ] Complete Ubuntu setup wizard on Orin Nano
- [ ] Install system dependencies (`apt` packages)
- [ ] Configure camera (Pi Camera Module 3 or USB webcam)
- [ ] Verify camera capture at 30fps

#### Basic Camera Pipeline
- [ ] Create Python script for video capture
- [ ] Display live video feed in window
- [ ] Add FPS counter overlay
- [ ] Implement clean shutdown (press 'q' to quit)
- [ ] Test stability (30+ min continuous operation)

#### Object Detection Integration
- [ ] Install Ultralytics YOLOv8: `pip install ultralytics`
- [ ] Download YOLOv8-nano model
- [ ] Integrate YOLO inference into video loop
- [ ] Draw bounding boxes on detected objects
- [ ] Display class labels and confidence scores
- [ ] Optimize inference with TensorRT (export model to `.engine`)
- [ ] Benchmark FPS (target: 60+ fps)

---

### Phase 2: Vision API Integration (Week 3-4)

#### API Setup
- [ ] Create accounts and get API keys:
  - OpenAI (GPT-4V)
  - Anthropic (Claude)
  - Google (Gemini)
- [ ] Store API keys in `.env` file (not in git)
- [ ] Set up billing limits ($10/month max)

#### Vision API Client
- [ ] Create `VisionAPIClient` class
- [ ] Implement image encoding (NumPy array → base64 JPEG)
- [ ] Image optimization: resize to 512x512, compress to 80% quality
- [ ] Implement API calls for all 3 providers
- [ ] Add error handling (timeouts, rate limits, API errors)
- [ ] Test with static images first
- [ ] Compare response quality across providers

#### Prompt Engineering
- [ ] Create `PromptTemplates` class
- [ ] Design prompts for different scenarios:
  - General object description (2-3 sentences)
  - Food items (calories, nutrition, facts)
  - Products (brand, price, features)
  - Plants (species, care instructions)
  - Books (title, author, synopsis)
  - Visual question answering
- [ ] Test prompts, iterate for concise responses
- [ ] Document best-performing prompts

---

### Phase 3: Smart Triggering & Cost Control (Week 4-5)

#### Detection Event Management
- [ ] Create `DetectionManager` class
- [ ] Implement cooldown logic (10 seconds per object class)
- [ ] Track last detection time for each object type
- [ ] Queue detection events for background processing
- [ ] Crop detected objects from frame (use bounding box)
- [ ] Add confidence threshold filter (>0.7)

#### Response Caching
- [ ] Set up SQLite database for cache
- [ ] Implement perceptual image hashing (pHash) for similarity
- [ ] Cache structure: `(image_hash, prompt) → (response, timestamp)`
- [ ] Set TTL: 24 hours for descriptions, 1 hour for questions
- [ ] Implement cache lookup before API call
- [ ] Track cache hit rate (log metrics)

#### Background Processing
- [ ] Use threading or asyncio for non-blocking API calls
- [ ] Ensure API calls don't freeze video feed
- [ ] Queue multiple detections if needed
- [ ] Add request timeout (5 seconds max)

---

### Phase 4: Response Display (Week 5-6)

#### Text Overlay System
- [ ] Create `ResponseDisplay` class
- [ ] Render text on video frame using OpenCV
- [ ] Add semi-transparent black background behind text
- [ ] Implement word wrapping (fit text to screen width)
- [ ] Position text near detected object or at bottom
- [ ] Add fade-out animation (after 10 seconds)
- [ ] Support multiple simultaneous responses

#### Visual Polish
- [ ] Choose readable font and size
- [ ] Ensure text is visible in all lighting conditions
- [ ] Add object class icon or indicator
- [ ] Display countdown timer (time until fade)
- [ ] Show loading indicator during API call
- [ ] Add system status indicators (API connected, cache hit, etc.)

---

### Phase 5: Interactive Modes (Week 6-7)

#### Mode 1: Auto-Describe
- [ ] Automatically describe detected objects
- [ ] Prioritize most confident detection
- [ ] Send to API only when cooldown expired
- [ ] Display response near object's bounding box
- [ ] Works hands-free, no user input required

#### Mode 2: Visual Question Answering
- [ ] Add keyboard input for questions
- [ ] Capture current frame when question asked
- [ ] Send frame + question to vision API
- [ ] Display answer on screen
- [ ] Support follow-up questions
- [ ] Log question history

#### Mode 3: Scene Analysis (Optional)
- [ ] "List everything you see" mode
- [ ] Capture full frame (not just detected objects)
- [ ] Get comprehensive scene description
- [ ] Format as numbered list
- [ ] Useful for "What's in my fridge?" scenarios

#### Mode Switching
- [ ] Keyboard shortcuts: '1' auto-describe, '2' QA mode, '3' scene
- [ ] Display current mode on screen
- [ ] Clear previous responses when switching modes

---

### Phase 6: Polish & Advanced Features (Week 7-8)

#### Cost Tracking
- [ ] Log every API call (provider, cost, timestamp)
- [ ] Calculate running total cost
- [ ] Display cost on screen or in terminal
- [ ] Alert if approaching monthly budget
- [ ] Generate cost report (daily/weekly/monthly)

#### Performance Optimization
- [ ] Profile code to find bottlenecks
- [ ] Optimize image preprocessing
- [ ] Reduce memory usage
- [ ] Minimize latency (detection → display)
- [ ] Test with various lighting conditions

#### Error Handling & Reliability
- [ ] Graceful degradation if API fails
- [ ] Retry logic with exponential backoff
- [ ] Fallback to cached responses if API down
- [ ] Log all errors for debugging
- [ ] System doesn't crash on errors

#### Text-to-Speech (Optional)
- [ ] Integrate Google TTS or pyttsx3
- [ ] Speak responses aloud via USB speaker
- [ ] Add voice control (wake word detection)
- [ ] Queue audio responses
- [ ] Volume controls

---

### Phase 7: Documentation & Demo (Week 8)

#### Code Documentation
- [ ] Add docstrings to all functions/classes
- [ ] Create architecture diagram
- [ ] Document system flow
- [ ] Explain cost control strategies
- [ ] Add inline comments for complex logic

#### README Creation
- [ ] Project overview and features
- [ ] Hardware requirements list
- [ ] Setup instructions (step-by-step)
- [ ] API key configuration guide
- [ ] Usage examples
- [ ] Troubleshooting section
- [ ] Performance benchmarks
- [ ] Cost analysis

#### Demo Scenarios
- [ ] **Scenario 1**: Kitchen assistant (fridge contents)
- [ ] **Scenario 2**: Product information (bottle, book, gadget)
- [ ] **Scenario 3**: Plant identification and care
- [ ] **Scenario 4**: Food nutrition estimation
- [ ] **Scenario 5**: Visual Q&A (desk organization)
- [ ] Record 30-60 second video for each
- [ ] Create compilation demo (3-5 minutes)

#### Portfolio Materials
- [ ] Write blog post explaining architecture
- [ ] Highlight cost optimization strategies
- [ ] Include performance metrics (FPS, latency, cost)
- [ ] Add before/after videos
- [ ] Create GitHub social preview image
- [ ] Update LinkedIn/resume with project

---

## Demo Scenarios (Required for MVP)

### 1. Kitchen Assistant
**User Action**: Point camera at open refrigerator  
**System Response**: "I see milk, eggs, cheese, orange juice, butter, and several vegetables. Your eggs are running low. The milk expires in 3 days."  
**Wow Factor**: Practical, immediately useful application

### 2. Product Information
**User Action**: Point at water bottle  
**System Response**: "This is a Hydro Flask 32oz insulated water bottle. Retail price around $40-45. Keeps drinks cold for 24 hours, hot for 12 hours. Popular for hiking and outdoor activities."  
**Wow Factor**: Shows contextual understanding + real-world knowledge

### 3. Plant Care Assistant
**User Action**: Point at houseplant  
**System Response**: "This appears to be a pothos plant (Epipremnum aureum). Water when the top inch of soil is dry, about once per week. Thrives in indirect sunlight. One of the easiest plants for beginners."  
**Wow Factor**: Demonstrates visual recognition + domain expertise

### 4. Food Nutrition
**User Action**: Point at prepared meal  
**System Response**: "This looks like grilled chicken breast with steamed broccoli and brown rice. Estimated 450-500 calories, 40g protein, 45g carbs, 12g fat. Well-balanced, high-protein meal."  
**Wow Factor**: Health/fitness application, shows estimation capabilities

### 5. Visual Q&A
**User Action**: Point at messy desk, ask "What's on my desk?"  
**System Response**: "I see a laptop, coffee mug, spiral notebook, two pens, phone charging cable, small succulent plant, and a stack of papers. There's also a lamp in the background."  
**Wow Factor**: Shows natural language interaction

---

## Success Criteria

### Minimum Viable Product (Week 6)
✅ YOLO detection running at 30+ fps  
✅ Integration with at least 2 vision APIs  
✅ Smart triggering with cooldown (5-10 API calls/min)  
✅ Response caching implemented  
✅ Text overlay displaying responses  
✅ Auto-describe mode working on 20+ objects  
✅ System cost <$5/month with normal usage  
✅ 3+ demo scenarios working reliably

### Interview-Ready (Week 8)
✅ All MVP criteria met  
✅ 60+ fps detection on Orin Nano  
✅ Visual QA mode functional  
✅ 5+ demo scenarios recorded  
✅ Professional video demo (3-5 min)  
✅ Comprehensive README and documentation  
✅ Blog post published explaining architecture  
✅ Clean GitHub repo with commit history  
✅ Cost analysis documented

### Stretch Goals (Week 10+)
✅ Text-to-speech output  
✅ Voice input (wake word + questions)  
✅ Web dashboard for remote viewing  
✅ Mobile app integration  
✅ Local LLM fallback (LLaVA)  
✅ Multi-language support  
✅ Continuous narration mode

---

## Risk Mitigation

### Technical Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| YOLO too slow on Orin | High | Use TensorRT optimization, nano model, target 30fps minimum |
| API costs explode | Medium | Aggressive caching, cooldown, budget alerts, use Gemini free tier |
| Vision API latency >5s | Medium | Choose fastest provider (Claude), compress images, timeout handling |
| Camera compatibility issues | Low | Test with USB webcam as backup, use well-supported Pi Camera Module |

### Project Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Scope creep delays MVP | High | Focus on 5 core demos, defer stretch goals to post-MVP |
| SD card shipping delay | Medium | Continue MacBook development, port when Orin ready |
| Losing motivation | Medium | Ship quick wins (detection by week 2), share progress publicly |
| Hardware failure | Low | MacBook as development backup, Orin for final demo only |

---

## Interview Talking Points

### System Architecture
"I built a hybrid edge-cloud system where YOLO runs locally at 60fps on Jetson Orin Nano for real-time detection, then selectively queries vision-language models in the cloud only when interesting objects appear. This reduces API costs by 99.7% compared to naive streaming—from 1,800 API calls per minute to just 5-10."

### Cost Optimization
"Implemented three-layer cost control: cooldown logic prevents duplicate queries, perceptual hashing enables response caching with 30-50% hit rate, and image optimization reduces payload size by 75%. Total operating cost under $5/month for typical personal use."

### Technical Depth
"Optimized YOLO inference using TensorRT on Orin Nano, achieving 60+ fps on YOLOv8-nano. Designed async API calls so vision queries don't block the main detection loop. Built modular prompt system supporting diverse use cases from nutrition analysis to plant identification."

### Real-World Application
"This demonstrates the exact architecture used in production systems like Google Lens and Meta's Ray-Ban smart glasses—balancing on-device performance with cloud intelligence. The project proves I can design systems that are both technically sophisticated and cost-effective."

---

## Timeline Summary

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1-2 | Foundation | Camera + YOLO detection at 60fps |
| 3-4 | API Integration | Vision API calls working, prompts optimized |
| 4-5 | Cost Control | Smart triggering + caching implemented |
| 5-6 | Display System | Text overlay, auto-describe mode functional |
| 6-7 | Interactive Modes | QA mode, multiple demo scenarios |
| 7-8 | Polish | Documentation, demo videos, blog post |

**Total: 6-8 weeks to impressive, interview-ready project**

---

## Next Immediate Steps

### This Week (While Waiting for SD Card)
1. Download JetPack 5.1.2+ image file (10-15GB)
2. Install balenaEtcher on MacBook for flashing
3. Continue MacBook development:
   - Get camera + YOLO working
   - Test one vision API (Gemini free tier)
   - Build basic text overlay
4. Order Pi Camera Module 3 (if not using USB webcam)

### When SD Card Arrives
1. Flash JetPack to SD card (15 min)
2. Boot Orin Nano, complete setup (30 min)
3. Install dependencies (1 hour)
4. Port MacBook code to Orin (30 min)
5. Test performance, optimize with TensorRT (2 hours)

### First Demo Target
By end of Week 2: Working auto-describe mode detecting and describing 10+ common objects at 60fps.

---

**Document Version**: 2.0  
**Last Updated**: October 15, 2025  
**Author**: Scott Van der Wiel