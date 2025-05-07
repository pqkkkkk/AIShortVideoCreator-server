from video_script.dao import video_script_dao
from abc import ABC, abstractmethod
from video_script.models import Voice
from storage import storage_service
from fastapi import HTTPException
from text_to_speech import tts_service
from ai import ai_service
from video_script.dto.requests import AutoGenerateScriptRequest

class video_script_service(ABC):
    @abstractmethod
    def getAllSampleVoiceList(self):
        pass
    @abstractmethod
    def getVoice(self, id):
        pass
    @abstractmethod
    def generateTextScript(self, prompt):
        pass
    @abstractmethod
    def saveVoice(self, voice):
        pass

class video_script_service_v1(video_script_service):
    async def generateTextScript(self, request: AutoGenerateScriptRequest):
        try:
            text_script = await ai_service.get_response(request.prompt)
            return text_script
        except Exception as e:
            print(f"Error: {e}")
            return None
    async def getAllSampleVoiceList(self):
        try:
            results = await video_script_dao.getAllSampleVoice()
            return results
        except Exception as e:
            print(f"Error: {e}")  
        return []         
    async def getVoice(self, id):
        try:
            res = await video_script_dao.getVoice(id)
            return res
        except Exception as e:
            print(f'Error: {e}')
            return None
    async def saveVoice(self, voice: Voice):
        try:
            await video_script_dao.saveVoice(voice)
            return voice
        except Exception as e:
            print(f"Error: {e}")
            return None
