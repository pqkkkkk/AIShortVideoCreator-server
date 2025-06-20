from pydantic import BaseModel, Field, computed_field
from typing import Dict, List
from datetime import datetime
from beanie import Document
from .result_status import VideoStatus
class UploadInfo(BaseModel):
    videoId: str
    uploadedAt: datetime

class Video(Document):
    public_id: str
    title: str
    #topic: str
    status: str
    video_url: str
    #created_at: str
    userId: str
    duration: float
    uploaded: Dict[str, List[UploadInfo]] = Field(default_factory=dict)
    @computed_field
    def can_edit(self) -> bool:
        return self.status == VideoStatus.PROCESSING.value
    
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

class Position(BaseModel):
    x: float
    y: float

class TextAttachment(BaseModel):
    text: str
    start_time: float
    end_time: float
    font_size: int = 24
    color_hex: str = "#FFFFFF"
    position: Position

class EmojiAttachment(BaseModel):
    emoji: str
    start_time: float
    end_time: float
    codepoint: str
    position: Position
    size: int