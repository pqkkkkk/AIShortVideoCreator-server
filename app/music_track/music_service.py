from typing import List, Dict
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from pydub import AudioSegment
import requests
from app.external_service.storage import storage_service
from .dao.musicTrack_dao import  mongodb_musicTrackDao
from io import BytesIO
import tempfile
import os
from .models import CutMusic, MusicTrack
load_dotenv()

class music_service(ABC):
    @abstractmethod
    def GetTracks(self) -> List[Dict]:
        pass   
    @abstractmethod
    def search_songs(self, keyword: str) -> List[Dict]:
        pass    
    @abstractmethod
    def cutMusicTrack(self, music: MusicTrack, startTime, endTime) -> str:
        pass
    @abstractmethod
    def prepareMusicTrack(self):
        pass

class my_music_service(music_service): 
    def __init__(self):
        self.cloud = storage_service
        self.dao = mongodb_musicTrackDao()
    
    
    async def prepareMusicTrack(self):
        try:
            music_seed_path = os.getcwd() + "/music_seed"
            if not os.path.exists(music_seed_path):
                raise Exception("Thư mục music_seed không tồn tại")
            
            music_files = [f for f in os.listdir(music_seed_path) if f.endswith('.mp3')]
            if not music_files:
                raise Exception("Không tìm thấy file nhạc trong thư mục music_seed")
            
            for music_file in music_files:
                music_path = os.path.join(music_seed_path, music_file)
                if not os.path.isfile(music_path):
                    continue
                with open(music_path, 'rb') as file:
                    music_data = file.read()
                    secure_url, public_id, duration = await self.cloud.uploadVideoWithReturningDuration(music_data)
                    
                    if secure_url:
                        initial_music_name = os.path.splitext(music_file)[0]
                        music_name = initial_music_name.replace("-"," ")
                        music_track = MusicTrack(
                            name= music_name,
                            artist="Unknown Artist",
                            musicUrl=secure_url,
                            publicId=public_id,
                            duration= int(duration) 
                        )
                        await self.dao.InsertMusicTrack(music_track)
                        print(f"✅ Uploaded {music_file} to Cloudinary: {secure_url}")
                    else:
                        print(f"❌ Failed to upload {music_file} to Cloudinary")

                    print(f"✅ Saved {music_file} to database")
        except Exception as e:
            print(f"Error preparing music tracks: {e}")
            raise e
        
    async def GetTracks(self) -> List[MusicTrack]:
        return await self.dao.getAllTrack()
    async def get_music_track_by_id(self, publicId: str) -> MusicTrack:
        music = await self.dao.get_music_track_by_id(publicId)
        if music is None:
            raise Exception("Music track not found")
        return music
    

    async def search_songs(self, keyword: str) -> List[Dict]:
        return await self.dao.searchTrack(keyword)
    
    
    async def cutMusicTrack(self, musicId, startTime, endTime):
        music = await self.dao.get_music_track_by_id(musicId)
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
        if(self.dao.InsertMusicTrack(cutMusic)):
            os.remove(tmp_file_path)
            return True
        
        return False
        
    
