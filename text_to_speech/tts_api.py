from fastapi import APIRouter
from .tts_service import edge_tts_service
from .models import Voice
from typing import List

router = APIRouter()

tts_service = edge_tts_service()

@router.get("/tts/voiceSample", response_model=List[Voice])
async def getExampleVoice():
    return await tts_service.getSampleVoiceList()

@router.get("/tts/textToSpeech")
async def textToSpeech(scriptId, voiceId):
    return await tts_service.text_to_speech(scriptId, voiceId)

@router.get('/tts/getVoice/{id}', response_model=Voice)
async def getVoice(id):
    return await tts_service.getVoice(id=id)

