from service import video_script_service
from abc import ABC, abstractmethod
from models import VideoMetadata

class public_video_script_service(ABC):
    @abstractmethod
    async def GetVideoMetadata(self, script: str) -> dict:
        """
        Retrieves video metadata based on the provided script.
        """
        pass

class public_video_script_service_v1(public_video_script_service):
    async def GetVideoMetadata(self, script: str) -> VideoMetadata:
        video_metadata = await video_script_service.get_video_metadata(script)
        return video_metadata