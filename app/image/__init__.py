from .image_service import image_service_v1
from .image_api import api_router as image_api_router
from .models import Image

public_image_service = image_service_v1()
image_api = image_api_router

Image = Image