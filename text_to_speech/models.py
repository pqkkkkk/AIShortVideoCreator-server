from beanie import Document
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel

class Voice(Document):
    type: str
    voiceUrl: str
    shortName: str
    publicId: str
    
    class Settings:
        name = "voice"
