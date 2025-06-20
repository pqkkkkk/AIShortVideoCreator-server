from pydantic import BaseModel

class YoutubeTrendingItem(BaseModel):
    id: str
    title: str
    description: str
    thumbnailUrl: str
    thumbnailWidth: int
    thumbnailHeight: int
    viewCount: int = 0
    likeCount: int = 0
    shareCount: int = 0