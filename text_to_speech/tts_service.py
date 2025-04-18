from gtts import gTTS
import edge_tts
from abc import ABC, abstractmethod

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
    async def text_to_speech(self, text: str, voice: str, lang: str = 'en') -> None:
        communicate = edge_tts.Communicate(text, voice="vi-VN-HoaiMyNeural")
        await communicate.save("output.mp3")