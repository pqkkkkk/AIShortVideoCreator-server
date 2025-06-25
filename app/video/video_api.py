from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from app.common import UploadVideoInfo
from .requests import CreateVideoRequest, EditVideoRequest, VideoFilterObject
from .resposes import (CreateVideoResponse, EditVideoResponse,
                    UploadVideoToYoutubeResponse,
                    GetVideoByIdResponse, GetAllVideosResponse)
from .video_service import video_service_v2
import json
from app.auth import auth_service
from app.auth.result_status import ValidationAccessTokenResult

video_service = video_service_v2()
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

@router.post("/video", response_model=CreateVideoResponse)
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


@router.get("/video/{id}",response_model=GetVideoByIdResponse)
async def get_video_by_id(id: str,
                          #token: str = Depends(validate_token)
                          ):
    video = await video_service.get_video_data_by_id(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/video", response_model=GetAllVideosResponse)
async def get_all_videos(
                        filter_object: VideoFilterObject = Query(..., description="Filter object for pagination and user filtering"),
                        #token: str = Depends(validate_token)
                        ):
    videos_data = await video_service.get_all_videos_data_paginated(filter_object)
    if videos_data.status_code != 200:
        raise HTTPException(status_code=videos_data.status_code, detail=videos_data.message)
    
    return videos_data

@router.post("/video/upload/to-youtube", response_model=UploadVideoToYoutubeResponse)
async def upload_video_to_youtube(request: UploadVideoInfo):
    response = await video_service.upload_video_to_youtube(request)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    
    return response