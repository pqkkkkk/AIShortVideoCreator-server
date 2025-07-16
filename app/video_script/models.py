from beanie import Document
from pydantic import BaseModel
class Script(Document):
    id : str
    content: str
    class Settings:
        collection = "image"
    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "content": "https://example.com/image.jpg",
            }
        }
class Voice(Document):
    gender: str
    sampleVoiceUrl: str
    voiceId: str
    publicId: str
    class Settings:
        collection = "Voice"
class Scene(BaseModel):
    scene_id: int
    start_time: float
    end_time: float
    text: str
    background_image: str
    background_image_description: str
    background_music: str
    background_music_description: str
class VideoMetadata(BaseModel):
    scenes: list[Scene]