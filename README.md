# AIShortVideoCreator-server - project of "Software Design" course

AIShortVideoCreator-server is a FastAPI-based backend service for generating, editing, storing, and managing short AI-powered videos. The system supports video script generation, text-to-speech, image handling, and user authentication.

## Features

- **AI Video Script Generation:** Generate video scripts using AI (Google Gemini API).
- **Text-to-Speech:** Convert scripts to audio using Edge TTS or Google TTS.
- **Video Creation:** Automatically create videos with generated scripts and audio.
- **Video Editing:** basic video editing capabilities (cutting music tracks, add text, add sticker).
- **User Authentication:** Sign up and sign in with password hashing.
- **Cloud Storage:** Store videos and images on Cloudinary.
- **MongoDB Integration:** Store metadata and user data using Beanie ODM.

## Project Structure

```
.
├── ai/                # AI integration (Gemini API)
├── image/             # Image upload, retrieval, and management
├── music_track/       # Music track management and cutting
├── storage/           # Cloudinary storage service
├── text_to_speech/    # Text-to-speech services
├── user/              # User authentication and management
├── video/             # Video creation and retrieval
├── video_script/      # Video script generation and voice management
├── test/              # Test scripts
├── db.py              # Database initialization
├── config.py          # Environment variable loading
├── main.py            # FastAPI application entry point
└── README.md
```

## Requirements

- Python 3.10+
- MongoDB instance
- Cloudinary account (for media storage)
- Google Gemini API key
- Edge TTS or Google TTS dependencies

## Setup

1. **Clone the repository:**
    ```sh
    git clone <https://github.com/pqkkkkk/AIShortVideoCreator-server.git>
    cd AIShortVideoCreator-server
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure environment variables:**

    Create a `.env` file in the root directory with the following keys:
    ```
    DATASOURCE_URL=<your-mongodb-uri>
    DATABASE_NAME=<your-db-name>
    CLOUDINARY_CLOUD_NAME=<your-cloudinary-cloud-name>
    CLOUDINARY_API_KEY=<your-cloudinary-api-key>
    CLOUDINARY_API_SECRET=<your-cloudinary-api-secret>
    GOOGLE_API_KEY=<your-google-gemini-api-key>
    ```

4. **Run the server:**
    ```sh
    py main.py
    ```

## API Endpoints
- All endpoints are prefixed with `/api/v1`.
- API documentation is available at `/docs`.

**Note:**  
- Make sure MongoDB and Cloudinary credentials are correct.
- For local development, ensure all required services are running.
