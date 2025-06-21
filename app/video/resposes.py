from pydantic import BaseModel
from .models import Video

class CreateVideoResponse(BaseModel):
    public_id: str
    secure_url: str
    message: str

class EditVideoResponse(BaseModel):
    public_id: str
    secure_url: str
    message: str

class GetVideoByIdResponse(BaseModel):
    video_data: Video
    message: str
    status_code: int

class GetAllVideosResponse(BaseModel):
    videos_data : list[Video]
    total_videos: int
    message: str
    status_code: int

class UploadVideoToYoutubeResponse(BaseModel):
    video_public_id: str
    title: str
    videoUrl: str
    description: str
    keyword: str
    category: str
    privateStatus: str
    message: str
    status_code: int
    youtube_video_id: str = None
    youtube_video_url: str = None