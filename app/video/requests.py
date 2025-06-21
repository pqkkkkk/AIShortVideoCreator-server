from pydantic import BaseModel
from .models import VideoMetadata, TextAttachment, EmojiAttachment

class CreateVideoRequest(BaseModel):
    script: str
    title: str
    userId: str
    voiceId: str
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
    privateStatus: str
    accessToken: str
    