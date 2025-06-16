from beanie import Document
from pydantic import BaseModel
class MusicTrack(Document):
    name: str
    artist: str
    musicUrl: str
    publicId: str
    
    class Settings:
        collection="music"
    
    class Config:
        arbitrary_types_allowed = True  # Cho phép ObjectId và các loại tùy chỉnh khác
    
class CutMusicRequest(BaseModel):
    musicId: str
    startTime: float
    endTime: float
    
class CutMusic(Document):
    startTime: int
    endTime: int
    url: str
    
    class Settings: 
        name="cutMusic"

    