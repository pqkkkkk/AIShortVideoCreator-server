from .tts_service import edge_tts_service
from .tts_api import router

tts_service = edge_tts_service()
tts_api = router
