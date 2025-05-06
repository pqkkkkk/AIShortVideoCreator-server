from gtts import gTTS
import edge_tts
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from text_to_speech.models import Voice
from storage.storage_service import cloudinary_storage_service
from fastapi import HTTPException
import os
import tempfile
from .dao.tts_dao import mongoTTS_dao
load_dotenv()

class tts_service(ABC):
    @abstractmethod
    def text_to_speech(self, text: str, voice: str, lang: str = 'en') -> None:
        pass
    

class gtts_service(tts_service):
    def text_to_speech(self, text: str, voice : str, lang: str = 'en') -> None:
        tts = gTTS(text=text, lang=lang)
        tts.save("output.mp3")
        print(f"Audio saved as output.mp3")

class edge_tts_service(tts_service):
    def __init__(self):
        super().__init__()
        self.cloud = cloudinary_storage_service(os.getenv("CLOUDINARY_CLOUD_NAME"), 
                                           os.getenv("CLOUDINARY_API_KEY"), 
                                           os.getenv("CLOUDINARY_API_SECRET"))
        self.dao = mongoTTS_dao()

    async def text_to_speech(self, scriptId, voiceId, lang: str = 'vi') -> str :
        # script = self.scriptService.getScriptById(scriptId)
        script = "ĐÂY LÀ MỘT CÂU RẤT DÀI"
        voice = await self.dao.getVoice(id=voiceId)
        if voice is None:
            raise HTTPException(status_code=404, detail="Voice not found")
        tempFile = tempfile.NamedTemporaryFile(delete=False)

        tempPath = tempFile.name
        tempFile.close()

        file_name = os.path.basename(tempPath)
        print(file_name)
        
        # chuyển text thành voice
        communicate = edge_tts.Communicate(script, voice.shortName)
        await communicate.save(tempPath)

        # gọi cloudinary để lưu file vừa generate và trả ra url của file trên cloudinary
        result = self.cloud.upload(tempPath, file_name)
        os.remove(tempPath)
        
        # Lưu url của voice vừa tạo vào database 
        voice = Voice(type="script", voiceUrl=result, publicId=file_name, shortName=voice.shortName)
        await self.dao.saveVoice(voice)
        
        return [{
            "url" : result
            }]
    
    
    async def getSampleVoiceList(self):
        try:
            results = await self.dao.getAllSampleVoice()
            return results
        except Exception as e:
            print(f"Error: {e}")  
        return []

            
            
    async def getVoice(self, id):
        try:
            res = await self.dao.getVoice(id)
            return res
        except Exception as e:
            print(f'Error: {e}')
            return None
            
    

# Load các giọng có sẵn từ edge_tts
# trả ra định dạng để frontend hiểu được

# Người dùng chọn được giọng mong muốn, 
# chuyển văn bản thành giọng nói (save xuống file tạm mp3)
# và upload nó lên cloudinary và tạo url cho file đó
# Database sẽ lưu voice url trong model voice

