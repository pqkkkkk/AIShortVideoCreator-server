from .models import VideoMetadata
from pydantic import BaseModel
from .result_status import AutoGenerateTextScriptResult, ConvertToVideoMetadataResult


class GetVideoMetadataResponse(BaseModel):
    message: str
    result: ConvertToVideoMetadataResult
    data: VideoMetadata | None

class AutoGenerateTextScriptResponse(BaseModel):
    message: str
    result: AutoGenerateTextScriptResult
    data: str | None