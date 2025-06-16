from beanie import Document
from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime

class UploadInfo(BaseModel):
    videoId: str
    uploadedAt: datetime

class Video(Document):
    title: str
    #topic: str
    status: str
    video_url: str
    #created_at: str
    userId: str
    uploaded: Dict[str, List[UploadInfo]] = Field(default_factory=dict)
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
