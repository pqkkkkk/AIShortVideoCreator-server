from pydantic import BaseModel
from .models import YoutubeTrendingItem

class GetWikipediaTrendingResponse(BaseModel):
    data: list[str]  
    message: str = "Trending items retrieved successfully"
    status_code: int
    platform: str 
    total_count: int

class GetYoutubeTrendingResponse(BaseModel):
    data: list[YoutubeTrendingItem]
    message: str = "Trending items retrieved successfully"
    status_code: int
    platform: str
    total_count: int