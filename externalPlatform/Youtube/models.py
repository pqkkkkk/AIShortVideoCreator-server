from pydantic import BaseModel, Field
from beanie import Document
# Xem lại
class ExternalItem(BaseModel):
    id: str
    title: str
    description: str
    thumbnailUrl: str
    thumbnailWidth: int
    thumbnailHeight: int

    viewCount: int = 0
    likeCount: int = 0
    shareCount: int = 0


class uploadVideo(BaseModel):
    id: int
    title: str
    videoUrl: str
    description: str
    keyword: str
    category: str
    privateStatus: str


class StatisticInfo(BaseModel):
    id: str
    viewCount: int = 0
    likeCount: int = 0
    favoriteCount: int = 0
    commentCount: int = 0
    