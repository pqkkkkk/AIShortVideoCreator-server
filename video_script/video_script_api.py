from fastapi import APIRouter, HTTPException
from video_script.service import video_script_service
from .models import Voice
from typing import List
from video_script.dto.requests import AutoGenerateScriptRequest, GetVideoMetadataRequest
from video_script.dto.responses import GetVideoMetadataResponse
import markdown2
from bs4 import BeautifulSoup
router = APIRouter()

@router.get("/video_script/voiceSample", response_model=List[Voice])
async def getExampleVoice():
    return await video_script_service.getAllSampleVoiceList()

@router.post("/video_script")
async def AutoGenerateVideoScript(request: AutoGenerateScriptRequest):
    response = await video_script_service.generateTextScript(request=request)
    if response:
        html = markdown2.markdown(response)
        soup = BeautifulSoup(html, "html.parser")
        plain_text = soup.get_text()
        return {"message": "success", "data": plain_text}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate script")
@router.post("/video_script/video_metadata")
async def GetVideoMetadata(request: GetVideoMetadataRequest):
    video_metadata = await video_script_service.get_video_metadata(request.script)
    if video_metadata:
        return GetVideoMetadataResponse(message="success", data=video_metadata)
    else:
        return GetVideoMetadataResponse(message="error", data=None)
@router.get('/video_script/getVoice/{id}', response_model=Voice)
async def getVoice(id):
    return await video_script_service.getVoice(id=id)