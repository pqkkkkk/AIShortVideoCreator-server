from .music_service import my_music_service
from .music_api import router as musicTrack_api_router


music_service = my_music_service()
music_api = musicTrack_api_router
