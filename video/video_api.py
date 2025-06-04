from fastapi import APIRouter, Depends, HTTPException
from fastapi import Form, File, UploadFile
from video.dto.requests import CreateVideoRequest
from video.service import video_service
import json

router = APIRouter()

@router.post("/video")
async def create_video(
    video_metaData_json: str = Form(...),
    background_images: list[UploadFile] = File(...),
    background_musics: list[UploadFile] = File(...)
    ):
    try:
        secure_url = "error"
        video_metadata = CreateVideoRequest(**json.loads(video_metaData_json))
        secure_url, public_id = await video_service.create_video(
            video_metadata, 
            background_images, 
            background_musics
        )
        if secure_url == "error":
            raise HTTPException(status_code=500, detail="Error creating video")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/video/{id}")
async def get_video_by_id(id: str):
    video = await video_service.get_video_by_id(id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video