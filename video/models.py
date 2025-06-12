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
    bg_image_public_id: str
    bg_music_public_id: str
    bg_image_file_index: int
    bg_music_file_index: int
class VideoMetadata(BaseModel):
    scenes: list[Scene]
