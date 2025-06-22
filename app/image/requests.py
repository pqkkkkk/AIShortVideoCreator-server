from pydantic import BaseModel

class GenerateImageRequest(BaseModel):
    content: str
    height: int
    width: int