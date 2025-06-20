from .service import YouTubeService
from .youtube_api import router as youtube_api_router


youtube_service = YouTubeService()
youtube_api = youtube_api_router
