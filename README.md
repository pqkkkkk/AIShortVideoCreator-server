# 🎬 AI Short Video Creator - Backend Server

> **A powerful, AI-driven video creation platform that transforms ideas into engaging short videos automatically**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb)](https://www.mongodb.com/)
[![Google AI](https://img.shields.io/badge/Google-Gemini%20AI-orange?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-Media%20CDN-blue?style=for-the-badge&logo=cloudinary)](https://cloudinary.com/)

## 🚀 Overview

**AI Short Video Creator** is a comprehensive full-stack application that leverages cutting-edge AI technologies to automatically generate, edit, and manage short-form videos. This backend service powers an intelligent video creation pipeline that transforms simple text prompts into professional-quality videos with AI-generated scripts, voiceovers, and visual content.

**🔗 Frontend Repository:** [AIShortVideoCreator-client-v2](https://github.com/pqkkkkk/AIShortVideoCreator-client-v2)

## ✨ Key Features

### 🤖 **AI-Powered Content Generation**
- **Intelligent Script Writing**: Google Gemini AI generates engaging video scripts tailored to user topics
- **Advanced Text-to-Speech**: Multi-language voice synthesis using Edge TTS and Google TTS
- **Smart Content Curation**: AI-driven trending topic suggestions and script optimization

### 🎥 **Professional Video Production**
- **Automated Video Assembly**: Seamlessly combines scripts, audio, images, and background music
- **Real-time Video Editing**: Dynamic text overlays, sticker placement, and music track management
- **Multi-format Export**: Optimized output for various social media platforms

### 🔧 **Enterprise-Grade Infrastructure**
- **Scalable Architecture**: Async FastAPI with MongoDB for high-performance data operations
- **Cloud-Native Storage**: Cloudinary integration for global CDN and media optimization
- **Secure Authentication**: JWT-based auth with bcrypt password hashing
- **RESTful API Design**: Clean, documented APIs with automatic OpenAPI generation

### 📊 **Content Management & Analytics**
- **Trending Analysis**: Real-time trending topic detection and recommendation
- **User Dashboard**: Comprehensive video library and project management
- **Version Control**: Track video iterations and editing history

## 🏗️ System Architecture

```mermaid
graph TB
    A[🖥️ Client App] --> B[⚡ FastAPI Server]
    B --> C[🗄️ MongoDB Atlas]
    B --> D[🤖 Google Gemini AI]
    B --> E[☁️ Cloudinary CDN]
    B --> F[🔊 Text-to-Speech Services]
    B --> G[🎬 Video Processing Engine]
    
    subgraph "🔧 Core Services"
        H[🔐 Auth Service]
        I[🎥 Video Service]
        J[📝 Script Generation]
        K[🖼️ Image Processing]
        L[🎵 Music Management]
    end
    
    B --> H
    B --> I
    B --> J
    B --> K
    B --> L
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#e3f2fd
```

## 🛠️ Technology Stack

### **Backend Framework**
- **FastAPI** - High-performance async web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server for production deployment

### **Database & ODM**
- **MongoDB Atlas** - Cloud-native NoSQL database
- **Beanie ODM** - Async MongoDB object document mapper
- **Motor** - Async MongoDB driver

### **AI & Machine Learning**
- **Google Gemini API** - Advanced language model for script generation
- **Hugging Face** - Hugging Face model integration

### **Media Processing**
- **MoviePy** - Video editing and manipulation
- **Pydub** - Audio processing and format conversion
- **Pillow** - Image processing and optimization
- **Edge TTS / Google TTS** - Text-to-speech synthesis

### **Cloud Services**
- **Cloudinary** - Media storage and CDN
- **Google Cloud APIs** - AI services integration

### **Security & Authentication**
- **BCrypt** - Password hashing
- **Python-JOSE** - JWT token management
- **OAuth 2.0** - Secure authentication flow

## 📁 Project Structure

```
AIShortVideoCreator-server/
├── 🔐 app/auth/              # Authentication & authorization
├── 🤖 app/external_service/  # External API integrations
│   ├── ai/                   # Google Gemini AI service
│   ├── storage/              # Cloudinary storage
│   └── text_to_speech/       # TTS services
├── 🖼️  app/image/            # Image upload & processing
├── 🎵 app/music_track/       # Audio management
├── 📈 app/trending/          # Trending analysis
├── 👤 app/user/              # User management
├── 🎬 app/video/             # Video creation & editing
├── 📝 app/video_script/      # Script generation
├── 🧪 test/                  # Comprehensive test suite
├── ⚙️  app/config.py         # Environment configuration
├── 🗄️  app/db.py             # Database initialization
└── 🚀 main.py               # Application entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB Atlas account
- Cloudinary account
- Google AI API key (Gemini)
- Hugging Face Access token
- YouTube API key (optional, for platform integration)
- Facebook App credentials (optional, for platform integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pqkkkkk/AIShortVideoCreator-server.git
   cd AIShortVideoCreator-server
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Database Configuration
   DATASOURCE_CLOUD_URL=mongodb+srv://username:password@cluster.mongodb.net
   DATABASE_CLOUD_NAME=ai_video_creator
   
   # Cloudinary Media Storage
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   
   # AI Services
   GEMINI_API_KEY=your_gemini_api_key
   HUGGINGFACE_ACCESS_TOKEN=your_huggingface_token
   
   # JWT Authentication
   JWT_SECRET_KEY=your_jwt_secret_key
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # External Platform Integration (Optional)
   YOUTUBE_API_KEY=your_youtube_api_key
   YOUTUBE_CLIENT_SECRET_JSON_FILE_PATH=./client_secrets.json
   
   # Font Configuration
   FONT_FAMILY_DIRECTORY=./app/assets/fonts/
   ```

5. **Launch the server**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `/docs`.

## 📚 API Documentation

### **Core Endpoints**

| Service | Endpoint | Description |
|---------|----------|-------------|
| 🔐 **Auth** | `/api/v1/auth/*` | User registration, login, token management |
| 🎬 **Videos** | `/api/v2/video/*` | Video creation, editing, retrieval |
| 📝 **Scripts** | `/api/v2/video_script/*` | AI script generation and management |
| 🖼️ **Images** | `/api/v2/image/*` | Image upload, processing, and storage |
| 🎵 **Music** | `/api/v1/music/*` | Background music and audio management |
| 📈 **Trending** | `/api/v1/trending/*` | Trending topics and analytics |

### **API Versioning**
- **v1**: Stable production APIs with authentication
- **v2**: Enhanced features and experimental endpoints

**Interactive API Documentation**: Visit `/docs` when the server is running for complete API exploration.

## 🚀 Deployment

### **Docker Deployment**

```bash
# Build the Docker image
docker build -t ai-video-creator-server .

# Run the container
docker run -p 8000:8000 --env-file .env ai-video-creator-server
```

## 🎯 Key Technical Achievements

- **Async Architecture**: Built with FastAPI for high-concurrency operations
- **AI Integration**: Seamless integration with Google Gemini for intelligent content generation
- **Media Pipeline**: Sophisticated video processing pipeline with MoviePy
- **Cloud-Native**: Fully cloud-integrated with MongoDB Atlas and Cloudinary
- **Security-First**: Comprehensive authentication and authorization system
- **Scalable Design**: Modular architecture supporting horizontal scaling


## 🔗 Links

- **Frontend Repository**: [AIShortVideoCreator-client-v2](https://github.com/pqkkkkk/AIShortVideoCreator-client-v2)

---

**Built with ❤️ using FastAPI, MongoDB, Hugging Face and Google AI**
