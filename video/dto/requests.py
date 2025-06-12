from pydantic import BaseModel
from video.models import VideoMetadata
class CreateVideoRequest(BaseModel):
    script: str
    title: str
    userId: str
    voiceId: str
    videoMetadata: VideoMetadata