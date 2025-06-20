from pydantic import BaseModel

class GenerateImageResponse(BaseModel):
    image_url: str
    public_id: str
    status_code: int
    message: str