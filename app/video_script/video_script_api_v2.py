from fastapi import APIRouter, HTTPException, Depends, Query
from app.video_script.service import video_script_service
from .models import Voice
from typing import List
from app.video_script.requests import AutoGenerateScriptRequest, GetVideoMetadataRequest
from app.video_script.responses import GetVideoMetadataResponse, AutoGenerateTextScriptResponse
from app.video_script.result_status import AutoGenerateTextScriptResult, ConvertToVideoMetadataResult
import markdown2
from bs4 import BeautifulSoup

router = APIRouter()


@router.post("/video_script", response_model=AutoGenerateTextScriptResponse)
async def AutoGenerateVideoScript(request: AutoGenerateScriptRequest,
                                ):
    response = await video_script_service.generateTextScript_v2(request=request)
    if response and response.result == AutoGenerateTextScriptResult.SUCCESS:
        html = markdown2.markdown(response.data)
        soup = BeautifulSoup(html, "html.parser")
        plain_text = soup.get_text()
        return AutoGenerateTextScriptResponse(
            message=AutoGenerateTextScriptResult.SUCCESS.value,
            result=AutoGenerateTextScriptResult.SUCCESS,
            data=plain_text
        )
    else:
        raise HTTPException(status_code=500,
                            detail=response.message if response else "Failed to generate video script")
    
@router.post("/video_script/video_metadata", response_model=GetVideoMetadataResponse)
async def GetVideoMetadata(request: GetVideoMetadataRequest,
                           ):
    response = await video_script_service.get_video_metadata_v2(request)
    if response and response.result == ConvertToVideoMetadataResult.SUCCESS:
        return response
    else:
        raise HTTPException(status_code=500,
                             detail=response.message if response else "Failed to convert script to video metadata")
