from fastapi import APIRouter, Depends, HTTPException
from fastapi import Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from video.dto.requests import CreateVideoRequest, EditVideoRequest
from video.dto.resposes import (CreateVideoResponse, EditVideoResponse,
    GetVideoByIdResponse, GetAllVideosResponse)
from video.service import video_service
import json
from auth import auth_service
from auth.result_status import ValidationAccessTokenResult

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")

def validate_token(token: str = Depends(oauth2_scheme)):
    validation_result = auth_service.validate_access_token(token)
    if validation_result == ValidationAccessTokenResult.VALID:
        return token
    elif validation_result == ValidationAccessTokenResult.EXPIRED:
        raise HTTPException(status_code=401, detail="Token expired")
    elif validation_result == ValidationAccessTokenResult.INVALID:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        raise HTTPException(status_code=500, detail="Error validating token")

@router.post("/video")
async def create_video(
    #token: str = Depends(validate_token),
    video_metaData_json: str = Form(...),
    background_images: list[UploadFile] = File(default=[]),
    background_musics: list[UploadFile] = File(default=[])
    ):
    try:
        video_metadata = CreateVideoRequest(**json.loads(video_metaData_json))
        response = await video_service.create_video(
            video_metadata, 
            background_images, 
            background_musics
        )
        if response.secure_url == "":
            raise HTTPException(status_code=500, detail="Error creating video")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/video/{id}",response_model=EditVideoResponse)
async def edit_video(request: EditVideoRequest,
                     #token: str = Depends(validate_token)
                     ):
    response = await video_service.edit_video(request)
    if response.secure_url == "":
        raise HTTPException(status_code=500, detail="Error editing video")
    
    return response


@router.get("/video/{id}")
async def get_video_by_id(id: str,
                          #token: str = Depends(validate_token)
                          ):
    video = await video_service.get_video_data_by_id(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/video")
async def get_all_videos(
                        #token: str = Depends(validate_token)
                        ):
    videos_data = await video_service.get_all_videos_data()
    if videos_data.status_code != 200:
        raise HTTPException(status_code=videos_data.status_code, detail=videos_data.message)
    
    return videos_data