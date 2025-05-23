from gtts import gTTS
import edge_tts
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from storage import storage_service
from fastapi import HTTPException
import os
import tempfile

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
    async def text_to_speech(self, text, voiceId, lang: str = 'vi') -> str :
        # voice = await self.dao.getVoice(id=voiceId)
        # if voice is None:
        #     raise HTTPException(status_code=404, detail="Voice not found")
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file_path = temp_file.name
        
        communicate = edge_tts.Communicate(text)
        await communicate.save(temp_file_path)
        
        print(f"✅ Audio saved to temporary file: {temp_file_path}")
        return temp_file_path
            

