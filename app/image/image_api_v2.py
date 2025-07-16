from fastapi import APIRouter
from fastapi import HTTPException
from app.image.requests import GenerateImageRequest
from app.image.responses import GenerateImageResponse
from .image_service import image_service_v1

image_service = image_service_v1()
api_router = APIRouter()

@api_router.post("/image/generate", response_model=GenerateImageResponse)
async def generate_image(request: GenerateImageRequest):
    response = await image_service.get_image_from_ai_v2(request)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    
    return response