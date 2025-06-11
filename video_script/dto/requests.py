from pydantic import BaseModel

class AutoGenerateScriptRequest(BaseModel):
    video_duration: int
    content: str

class GetVideoMetadataRequest(BaseModel):
    script: str