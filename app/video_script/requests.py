from pydantic import BaseModel

class AutoGenerateScriptRequest(BaseModel):
    video_duration: int = 45
    content: str
    scene_quantity: int = -1

class GetVideoMetadataRequest(BaseModel):
    script: str