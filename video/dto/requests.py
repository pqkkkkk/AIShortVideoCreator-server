from pydantic import BaseModel

class CreateVideoRequest(BaseModel):
    script: str
    title: str
    userId: str