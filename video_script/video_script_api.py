from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from video_script.service import video_script_service
from .models import Voice
from typing import List
from video_script.dto.requests import AutoGenerateScriptRequest, GetVideoMetadataRequest
from video_script.dto.responses import GetVideoMetadataResponse
import markdown2
from bs4 import BeautifulSoup
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

@router.get("/video_script/voice", response_model=List[Voice])
async def GetVoices(gender: str = Query(default="")):
    return await video_script_service.getAllVoices(gender=gender)

@router.get('/video_script/voice/{id}', response_model=Voice)
async def getVoice(id):
    return await video_script_service.getVoiceById(id=id)

@router.post("/video_script")
async def AutoGenerateVideoScript(request: AutoGenerateScriptRequest, token: str = Depends(validate_token)):
    response = await video_script_service.generateTextScript(request=request)
    if response:
        html = markdown2.markdown(response)
        soup = BeautifulSoup(html, "html.parser")
        plain_text = soup.get_text()
        return {"message": "success", "data": plain_text}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate script")
    
@router.post("/video_script/video_metadata")
async def GetVideoMetadata(request: GetVideoMetadataRequest, token: str = Depends(validate_token)):
    video_metadata = await video_script_service.get_video_metadata(request.script)
    if video_metadata:
        return GetVideoMetadataResponse(message="success", data=video_metadata)
    else:
        return GetVideoMetadataResponse(message="error", data=None)
