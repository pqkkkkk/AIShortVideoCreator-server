from video_script.service import video_script_service
from abc import ABC, abstractmethod
from video_script.models import VideoMetadata

class public_video_script_service(ABC):
    @abstractmethod
    async def GetVideoMetadata(self, script: str) -> dict:
        """
        Retrieves video metadata based on the provided script.
        """
        pass
    async def prepareVoice(self, lang: str = 'vi'):
        """
        Prepares the voice for the specified language.
        """
        pass

class public_video_script_service_v1(public_video_script_service):
    async def GetVideoMetadata(self, script: str) -> VideoMetadata:
        video_metadata = await video_script_service.get_video_metadata(script)
        return video_metadata
    
    
    async def prepareVoice(self, lang: str = 'vi'):
        await video_script_service.preparVoice(lang=lang)