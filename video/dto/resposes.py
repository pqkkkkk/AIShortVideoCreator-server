from pydantic import BaseModel
from video.models import Video

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