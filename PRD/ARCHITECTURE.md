# Multimodal AI Camera Assistant - System Architecture

## Overview

This document outlines the technical architecture decisions and implementation details for the Multimodal AI Camera Assistant project. It complements the main PRD by focusing on technical implementation rather than product requirements.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Camera Input                             │
│                     (30-60 fps video stream)                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Thread 1: Camera Pipeline                    │
│  • Camera capture (OpenCV VideoCapture)                         │
│  • Frame preprocessing (resize, normalize)                     │
│  • Frame queue management (thread-safe)                        │
│  • OpenCV display rendering (60fps, never blocks)             │
└─────────────────────┬───────────────────────────────────────────┘
                      │ (frames)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Thread 2: Detection Engine                   │
│  • YOLO inference (YOLOv8-nano + TensorRT)                     │
│  • Bounding box post-processing (NMS, filtering)               │
│  • Detection event generation                                  │
│  • Performance: 60+ fps target                                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │ (detection events)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Thread 3: Smart Trigger                      │
│  • Cooldown logic (10 seconds per object class)                │
│  • Confidence threshold filtering (>0.7)                       │
│  • Detection event queuing                                      │
│  • Cache lookup (perceptual hashing + CLIP embeddings)         │
└─────────────────────┬───────────────────────────────────────────┘
                      │ (API requests)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Thread 4: API Client                         │
│  • Async HTTP requests (httpx/asyncio)                         │
│  • Image optimization (resize to 512x512, compress)            │
│  • Multi-provider support (Gemini → Claude → GPT-4V)            │
│  • Error handling & retry logic                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │ (responses)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Thread 5: Response Handler                   │
│  • Response caching (SQLite + Redis for scaling)               │
│  • Text overlay rendering                                       │
│  • Fade-out animation management                               │
│  • Cost tracking & metrics                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Thread Architecture Details

### Thread 1: Camera Pipeline
- **Purpose**: Maintain smooth video feed at 60fps
- **Responsibilities**:
  - Camera capture using OpenCV VideoCapture
  - Basic frame preprocessing (resize, color conversion)
  - Thread-safe frame queue management
  - OpenCV display rendering (never blocks)
- **Performance**: Must maintain 60fps regardless of other thread performance
- **Dependencies**: OpenCV, camera drivers

### Thread 2: Detection Engine
- **Purpose**: Real-time object detection
- **Responsibilities**:
  - YOLO inference using TensorRT optimization
  - Bounding box post-processing (NMS, confidence filtering)
  - Detection event generation and queuing
- **Performance Target**: 60+ fps on Jetson Orin Nano
- **Dependencies**: Ultralytics YOLOv8, TensorRT, CUDA

### Thread 3: Smart Trigger
- **Purpose**: Intelligent API call management
- **Responsibilities**:
  - Cooldown logic (prevent duplicate queries)
  - Confidence threshold filtering
  - Cache lookup using perceptual hashing + CLIP embeddings
  - Detection event queuing for API processing
- **Performance**: Sub-millisecond decision making
- **Dependencies**: CLIP model, perceptual hashing library

### Thread 4: API Client
- **Purpose**: Cloud vision API integration
- **Responsibilities**:
  - Async HTTP requests using httpx/asyncio
  - Image optimization (resize, compress)
  - Multi-provider API calls (Gemini → Claude → GPT-4V)
  - Error handling, retry logic, timeout management
- **Performance**: Non-blocking, handles 5-10 requests/minute
- **Dependencies**: httpx, asyncio, vision API clients

### Thread 5: Response Handler
- **Purpose**: Response processing and display
- **Responsibilities**:
  - Response caching (SQLite for MVP, Redis for scaling)
  - Text overlay rendering on video frames
  - Fade-out animation management
  - Cost tracking and metrics collection
- **Performance**: Real-time response display
- **Dependencies**: SQLite, OpenCV text rendering

## Data Flow Architecture

### Frame Processing Pipeline
```
Raw Camera Frame (1920x1080)
    ↓
Preprocessing (resize to 640x640 for YOLO)
    ↓
YOLO Inference (TensorRT optimized)
    ↓
Post-processing (NMS, confidence filtering)
    ↓
Detection Events Queue
    ↓
Smart Trigger Logic
    ↓
API Request Queue (if triggered)
    ↓
Cloud API Processing
    ↓
Response Cache Update
    ↓
Text Overlay Rendering
    ↓
Display Frame (1920x1080)
```

### Inter-Thread Communication
- **Frame Queue**: Thread-safe queue between camera and detection
- **Detection Events Queue**: Between detection and smart trigger
- **API Request Queue**: Between smart trigger and API client
- **Response Queue**: Between API client and response handler
- **Shared State**: Detection cooldowns, cache, metrics

## Caching Strategy

### Multi-Layer Caching Architecture

#### Layer 1: Perceptual Hashing Cache
- **Purpose**: Exact image matching
- **Implementation**: pHash algorithm
- **Cache Key**: `pHash(image)`
- **Hit Rate**: ~30-40% for identical images
- **Storage**: SQLite table `perceptual_cache`

#### Layer 2: Semantic Similarity Cache
- **Purpose**: Similar object recognition
- **Implementation**: CLIP embeddings + cosine similarity
- **Cache Key**: `CLIP_embedding(image)`
- **Similarity Threshold**: >0.9 cosine similarity
- **Hit Rate**: Additional 20-30% (total 50-70%)
- **Storage**: SQLite table `semantic_cache`

#### Layer 3: Object Class + Context Cache
- **Purpose**: Context-aware caching
- **Implementation**: Object class + location + time
- **Cache Key**: `f"{object_class}_{location}_{time_window}"`
- **Hit Rate**: Additional 10-20% (total 60-80%)
- **Storage**: SQLite table `context_cache`

### Cache Management
- **TTL Strategy**:
  - General descriptions: 24 hours
  - Food/nutrition: 1 hour (context changes)
  - Product info: 7 days (stable)
  - Questions: 1 hour (contextual)
- **Eviction Policy**: LRU with size limits
- **Cache Warming**: Pre-populate with common objects

## API Integration Strategy

### Provider Priority Order
1. **Gemini Pro Vision** (Primary)
   - Cost: 1,500 free requests/day, then ~$0.002/image
   - Latency: ~1-2 seconds
   - Quality: Good for general descriptions
   - Use case: Development and MVP

2. **Claude 3.5 Sonnet** (Secondary)
   - Cost: ~$0.005/image
   - Latency: ~2-3 seconds
   - Quality: Excellent for detailed analysis
   - Use case: Production quality responses

3. **GPT-4V** (Fallback)
   - Cost: ~$0.01/image
   - Latency: ~3-5 seconds
   - Quality: Best for complex reasoning
   - Use case: Comparison testing, complex queries

### API Call Optimization
- **Image Compression**: Resize to 512x512, JPEG quality 80%
- **Batch Processing**: Queue multiple objects for single API call
- **Timeout Management**: 5-second timeout with exponential backoff
- **Rate Limiting**: Respect API rate limits (50-100 req/min)

## Performance Optimization Strategy

### YOLO Optimization Pipeline
1. **Model Selection**: YOLOv8-nano (best speed/accuracy tradeoff)
2. **TensorRT Conversion**: FP16 precision for 2-3x speedup
3. **Input Optimization**: 640x640 input resolution
4. **Post-processing**: CUDA-accelerated NMS
5. **Pipeline Optimization**: Async inference (overlap with next frame)

### Memory Management
- **Frame Buffers**: Circular buffer with 3-frame lookahead
- **Model Loading**: Single model instance shared across threads
- **Cache Size Limits**: 1GB max cache size with LRU eviction
- **Garbage Collection**: Explicit cleanup in detection thread

### Latency Optimization
- **Pipeline Overlap**: Detection runs on frame N while processing frame N-1
- **Async API Calls**: Non-blocking cloud requests
- **Response Streaming**: Display partial responses as they arrive
- **Preprocessing**: Optimize image operations with NumPy vectorization

## Error Handling & Reliability

### Graceful Degradation Strategy
1. **API Failure**: Fall back to cached responses
2. **Detection Failure**: Continue with last known detections
3. **Camera Failure**: Display error message, attempt reconnection
4. **Cache Failure**: Continue without caching (higher API costs)
5. **Thread Failure**: Restart individual threads without full system restart

### Monitoring & Metrics
- **Performance Metrics**: FPS, latency, memory usage
- **API Metrics**: Success rate, latency, cost per request
- **Cache Metrics**: Hit rate, size, eviction rate
- **Error Metrics**: Failure types, recovery time
- **User Metrics**: Detection accuracy, response quality

## Scalability Considerations

### Horizontal Scaling (Multiple Cameras)
- **Centralized API Gateway**: Shared API pool across cameras
- **Distributed Caching**: Redis cluster for shared cache
- **Load Balancing**: Distribute API calls across providers
- **Per-Camera Cooldowns**: Independent trigger logic per camera

### Vertical Scaling (Single Camera Enhancement)
- **GPU Memory**: Upgrade to Jetson AGX Orin for larger models
- **Model Size**: YOLOv8-small/medium for better accuracy
- **Batch Processing**: Process multiple frames simultaneously
- **Local LLM**: LLaVA model for offline operation

## Security Considerations

### Data Privacy
- **No Persistent Storage**: Images not stored on device
- **Ephemeral Context**: API calls use temporary contexts
- **Local Processing**: Detection runs entirely on-device
- **Secure API Keys**: Environment variables, not in code

### Network Security
- **HTTPS Only**: All API communications encrypted
- **API Key Rotation**: Regular key updates
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize all user inputs

## Development & Testing Strategy

### Development Environment
- **Primary**: Jetson Orin Nano with JetPack 5.1.2
- **Secondary**: MacBook for rapid iteration (webcam + mock APIs)
- **Testing**: Automated unit tests for each thread
- **Profiling**: Continuous performance monitoring

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Thread communication testing
- **Performance Tests**: FPS, latency, memory benchmarks
- **Stress Tests**: Long-running stability tests
- **API Tests**: Mock API responses for development

## Future Enhancement Opportunities

### Phase 2 Optimizations (Post-MVP)
- **C++/CUDA Hot Path**: Optimize preprocessing and post-processing
- **Custom TensorRT Plugins**: Specialized operations for YOLO
- **Hardware Acceleration**: GStreamer pipeline for video processing
- **Edge AI Models**: Local vision-language models (LLaVA)

### Advanced Features
- **Multi-Camera Support**: Synchronized multi-view analysis
- **Real-time Streaming**: WebRTC for remote viewing
- **Mobile Integration**: Companion app for remote control
- **Voice Integration**: Wake word detection + speech synthesis

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Author**: Scott Van der Wiel
