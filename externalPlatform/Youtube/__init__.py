from .service import YouTubeService
from .youtube_api import router as youtube_api_router


search_service = YouTubeService()
youtube_api = youtube_api_router
