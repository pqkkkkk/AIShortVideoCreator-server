from fastapi import HTTPException
from .responses import GetWikipediaTrendingResponse, GetYoutubeTrendingResponse
from .models import YoutubeTrendingItem
from app.external_service.external_platform.Youtube import youtube_service, youtube_service_async
import wikipedia



class youtube_trending_service():
    async def get_trending(self, keyword,  limit: int = 10) -> GetYoutubeTrendingResponse:
        try:
            items_from_youtube = await youtube_service_async.getTopTrending(keyword, limit)
            items = []
            for item in items_from_youtube:
                items.append(YoutubeTrendingItem(**item.__dict__))

            return GetYoutubeTrendingResponse(
                data=items,
                message="Trending items retrieved successfully",
                status_code=200,
                platform="youtube",
                total_count=len(items)
            )
        except Exception as e:
            return GetYoutubeTrendingResponse(
                data=[],
                message=f"An error occurred while fetching trending items: {str(e)}",
                status_code=500,
                platform="youtube",
                total_count=0
            )

class wikipedia_trending_service():
    def get_trending(self, keyword, limit: int = 10) -> GetWikipediaTrendingResponse:
        try:
            items = wikipedia.search(keyword, results=limit, suggestion=False)
    
            return GetWikipediaTrendingResponse(
                data=items,
                message="Trending items retrieved successfully",
                status_code=200,
                platform="wikipedia",
                total_count=len(items)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while fetching trending items: {str(e)}"
            )
        
