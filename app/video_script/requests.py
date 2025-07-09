from pydantic import BaseModel

class AutoGenerateScriptRequest(BaseModel):
    video_duration: int = 45
    content: str
    scene_quantity: int = -1
    model : str = "gemini"  # Default to Gemini AI model

class GetVideoMetadataRequest(BaseModel):
    script: str
    model : str = "gemini"  # Default to Gemini AI model