from abc import ABC, abstractmethod
from video_script.models import Voice, Script
from bson import ObjectId

class video_script_dao(ABC):
    @abstractmethod
    def GetAllVoices(gender: str):
        pass
    def GetVoiceById(self, id):
        pass
    def insertVoice(self, voice: Voice):
        pass
    def insertManyVoices(self, voices: list[Voice]):
        pass
   
class mongo_video_script_dao(video_script_dao):
    async def GetAllVoices(self, gender: str):
        try:
            results = await Voice.find_all().to_list()
            return results
        except Exception as e:
            print(f"Error: {e}")
        return []

    async def GetVoiceById(self, id):
        try:
            voice = await Voice.find_one(Voice.voiceId == id)
            if voice:
                return voice
            return None
        except Exception as e:
            print(f"Error fetching voice by id: {e}")
            return None
    
    async def insertVoice(self, voice: Voice):
        await Voice.insert_one(voice)
    async def insertManyVoices(self, voices: list[Voice]):
        await Voice.insert_many(voices)