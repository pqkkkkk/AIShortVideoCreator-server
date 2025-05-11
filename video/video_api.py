from fastapi import APIRouter, Depends, HTTPException
from video.dto.requests import CreateVideoRequest
from video.service import video_service
router = APIRouter()

@router.post("/video")
async def create_video(request: CreateVideoRequest):
    result = await video_service.create_video(request)
    
    if result == "error":
        raise HTTPException(status_code=500, detail="Error creating video")
@router.get("/video/{id}")
async def get_video_by_id(id: str):
    video = await video_service.get_video_by_id(id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video