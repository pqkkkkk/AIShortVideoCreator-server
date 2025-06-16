from pydantic import BaseModel

class CreateVideoResponse(BaseModel):
    public_id: str
    secure_url: str
    message: str

class EditVideoResponse(BaseModel):
    public_id: str
    secure_url: str
    message: str