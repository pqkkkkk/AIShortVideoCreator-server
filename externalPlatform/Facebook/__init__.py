from .service import FacebookService
from .fb_api import router as fb_api_router


fb_service = FacebookService()
fb_api = fb_api_router
