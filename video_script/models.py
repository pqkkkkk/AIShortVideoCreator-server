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
    type: str
    voiceUrl: str
    shortName: str
    publicId: str
    class Settings:
        name = "voice"
class Scene(BaseModel):
    scene_id: int
    start_time: float
    end_time: float
    text: str
    background_image: str
    background_music: str
class VideoMetadata(BaseModel):
    scenes: list[Scene]