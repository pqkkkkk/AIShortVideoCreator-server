from beanie import Document
from pydantic import BaseModel


class MusicTrack(Document):
    name: str
    artist: str
    musicUrl: str
    publicId: str
    duration: int
    
    class Settings:
        name="Music"
    
    
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

    