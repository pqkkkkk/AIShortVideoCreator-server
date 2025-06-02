from beanie import Document
from pydantic import BaseModel
class Video(Document):
    id: str
    title: str
    #topic: str
    status: str
    video_url: str
    #created_at: str
    userId: str
    class Settings:
        collection = "video"
class Scene(BaseModel):
    scene_id: int
    start_time: float
    end_time: float
    text: str
    background_image: str
    background_music: str
class VideoMetadata(BaseModel):
    scenes: list[Scene]
