from pydantic import BaseModel

class AutoGenerateScriptRequest(BaseModel):
    video_duration: int
    content: str
    scene_quantity: int = 3

class GetVideoMetadataRequest(BaseModel):
    script: str