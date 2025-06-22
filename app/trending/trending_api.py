from fastapi import APIRouter, Depends, HTTPException, Query
from .responses import GetWikipediaTrendingResponse, GetYoutubeTrendingResponse
from .trending_service import wikipedia_trending_service, youtube_trending_service

wikipedia_trending_service = wikipedia_trending_service()
youtube_trending_service = youtube_trending_service()
router = APIRouter()

@router.get("/trending/wikipedia", response_model=GetWikipediaTrendingResponse)
def get_trending_in_wikipedia(keyword: str = Query(..., description="Keyword to filter trending items"),
                    limit: int = Query(10, description="The maximum number of trending items to return")
                    ) -> GetWikipediaTrendingResponse:
    response = wikipedia_trending_service.get_trending(keyword, limit)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.message
        )
    
    return response

@router.get("/trending/youtube", response_model=GetYoutubeTrendingResponse)
def get_trending_in_youtube(keyword: str = Query(..., description="Keyword to filter trending items"),
                                   limit: int = Query(10, description="The maximum number of trending items to return")):
    try:
        response = youtube_trending_service.get_trending(keyword, limit)
        return  response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching trending items: {str(e)}"
        )