from abc import ABC, abstractmethod
from ..models import MusicTrack, CutMusic
from beanie import PydanticObjectId
from beanie.operators import RegEx, Or
from typing import Optional

class musicTrackDao(ABC):
    @abstractmethod
    async def get_music_track(self, track_id: str) -> Optional[MusicTrack]:
        pass
    
    def InsertMusicTrack(self ,musicTrack: CutMusic):
        pass
    
    def getAllTrack(self):
        pass

    def searchTrack(self,keyword:str):
        pass

class mongodb_musicTrackDao(musicTrackDao):
    async def get_music_track(self, track_id: str) -> Optional[MusicTrack]:
        try:
            return await MusicTrack.get(PydanticObjectId(track_id))
        except Exception as e:
            print(f"Error fetching music track: {str(e)}")
            return None
        
        
    async def InsertMusicTrack(self, musicTrack: MusicTrack):
        await MusicTrack.insert_one(musicTrack)
    
    async def getAllTrack(self):
        tracks = await MusicTrack.find_all().to_list()
        return tracks if tracks else []
        
    
    async def searchTrack(self,keyword:str):
        return await MusicTrack.find(
            Or(
                RegEx(MusicTrack.name, f".*{keyword}", options="i"),
                RegEx(MusicTrack.artist, f",*{keyword}", options="i")
            )).to_list()