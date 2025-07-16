from pydantic import BaseModel
from .models import Video, VideoStatisticsInfo

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

class VideoCountStatisticsItem(BaseModel):
    time: str  # e.g., "2023-10-01"
    count: int  # Number of videos uploaded on that day
class GetVideoCountStatisticsResponse(BaseModel):
    timely_video_count: list[VideoCountStatisticsItem]
    time_unit: str
    time_range: str
    status_code: int
    message: str

class AllVideoStatisticsResponse(BaseModel):
    statistics_info: VideoStatisticsInfo
    total_youtube_uploaded_videos: int
    total_videos: int
    status_code: int
    message: str

class GetAllVideosResponse(BaseModel):
    items : list[Video]
    total_videos: int
    current_page_number: int = 1
    total_pages: int = 1
    page_size: int = 10
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

