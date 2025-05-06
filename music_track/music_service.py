from typing import List, Dict
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from pydub import AudioSegment
import requests
from storage.storage_service import cloudinary_storage_service
from .dao.musicTrack_dao import  mongodb_musicTrackDao
from io import BytesIO
import tempfile
import os
from .models import CutMusic, MusicTrack
load_dotenv()

class music_service(ABC):
    @abstractmethod
    def getTrack(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def search_songs(self, keyword: str) -> List[Dict]:
        pass    
    @abstractmethod
    def cutMusicTrack(self, music: MusicTrack, startTime, endTime) -> str:
        pass

class my_music_service(music_service): 
    def __init__(self):
        self.cloud = cloudinary_storage_service(os.getenv("CLOUDINARY_CLOUD_NAME"), 
                                           os.getenv("CLOUDINARY_API_KEY"), 
                                           os.getenv("CLOUDINARY_API_SECRET"))
        
        self.dao = mongodb_musicTrackDao()
    
    async def getTrack(self) -> List[Dict]:
        return await self.dao.getAllTrack()
    
    async def search_songs(self, keyword: str) -> List[Dict]:
        return await self.dao.searchTrack(keyword)
    
    
    async def cutMusicTrack(self, musicId, startTime, endTime):
        music = await self.dao.get_music_track(musicId)
        resp = requests.get(music.musicUrl)
        if resp.status_code != 200:
            raise Exception(f"Không thể tải file từ {music.musicUrl}")
        
        audio = AudioSegment.from_file(BytesIO(resp.content), format="mp3")
        start_ms = int(startTime * 1000)
        end_ms = int(endTime * 1000)
        cut_audio = audio[start_ms: end_ms]
        
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp_file_path = tmp_file.name
        
        cut_audio.export(tmp_file_path, format="mp3")
        filename = f"cut_{startTime}_{endTime}.mp3"
        upload_result = self.cloud.upload(tmp_file_path, filename)
            
        secure_url = upload_result.get("secure_url")
        print(f"✅ Uploaded to Cloudinary: {secure_url}")
            
        cutMusic = CutMusic(musicId=id, startTime=startTime, endTime=endTime, url=secure_url)
        if(self.dao.saveMusicTrack(cutMusic)):
            os.remove(tmp_file_path)
            return True
        
        return False
        
    
