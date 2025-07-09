from .image_service import image_service_v1
from .image_api import api_router as image_api_router
from .image_api_v2 import api_router as image_api_v2_router
from .models import Image

public_image_service = image_service_v1()
image_api = image_api_router
image_api_v2 = image_api_v2_router

Image = Image