from pydantic import BaseModel
from beanie import Document
# Xem lại
class ExternalItem(BaseModel):
    id: str
    title: str
    description: str
    thumbnailUrl: str
    thumbnailWidth: int
    thumbnailHeight: int
    privacyStatus: str
    categoryId: str
    tags: str
    viewCount: int = 0
    likeCount: int = 0
    shareCount: int = 0



    
    