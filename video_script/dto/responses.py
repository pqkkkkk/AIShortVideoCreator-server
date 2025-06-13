from video_script.models import VideoMetadata
from pydantic import BaseModel
from video_script.result_status import AutoGenerateTextScriptResult, ConvertToVideoMetadataResult


class GetVideoMetadataResponse(BaseModel):
    message: str
    result: ConvertToVideoMetadataResult
    data: VideoMetadata | None

class AutoGenerateTextScriptResponse(BaseModel):
    message: str
    result: AutoGenerateTextScriptResult
    data: str | None