from pydantic import BaseModel

class UploadRequest(BaseModel):
    videoId: str
    access_token: str
