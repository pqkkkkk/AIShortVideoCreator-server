from pydantic import BaseModel
from .models import VideoMetadata, TextAttachment, EmojiAttachment
from enum import Enum
from typing import Literal

class OrderDirection(Enum):
    ASC = "asc"
    DESC = "desc"

class VideoFilterObject(BaseModel):
    page_size: int = 10
    current_page_number: int = 1
    user_id: str = ""
    status: str = ""
    title: str = ""
    order_by: str = "created_at"
    order_direction: Literal["asc", "desc"] = "desc" 

class TimeRangeStatistics(Enum):
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    CUSTOM = "custom"
class TimeUnit(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
class GetVideoCountStatisticsRequest(BaseModel):
    time_unit: str = TimeUnit.DAY.value  # e.g., "day", "week", "month"
    time_range: str  # e.g., "last_7_days", "last_30_days", "custom"
    start_date: str = None  # Optional for custom ranges
    end_date: str = None  # Optional for custom ranges

class CreateVideoRequest(BaseModel):
    script: str = ""
    title: str
    userId: str
    voiceId: str = "vi-VN-NamMinhNeural"
    videoMetadata: VideoMetadata

class EditVideoRequest(BaseModel):
    public_id: str
    userId: str
    text_attachments: list[TextAttachment]
    emoji_attachments: list[EmojiAttachment]

class UploadVideoToYoutubeRequest(BaseModel):
    id: int
    title: str
    videoUrl: str
    description: str
    keyword: str
    category: str
    privateStatus: str = "private"
    accessToken: str
    