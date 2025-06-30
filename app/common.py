from pydantic import BaseModel

class UploadVideoInfo(BaseModel):
    video_public_id: str
    title: str
    videoUrl: str
    description: str
    keyword: str
    category: str
    privateStatus: str
    accessToken: str
    