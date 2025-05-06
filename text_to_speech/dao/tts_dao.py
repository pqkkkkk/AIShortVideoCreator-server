from abc import ABC, abstractmethod
from text_to_speech.models import Voice
from bson import ObjectId
class tts_dao(ABC):
    @abstractmethod
    def getAllSampleVoice():
        pass
    def getVoice(self, id):
        pass
    def saveVoice(self, voice: Voice):
        pass


    
class mongoTTS_dao(tts_dao):
    async def getAllSampleVoice(self):
        try:
            results = await Voice.find(Voice.type == "sample").to_list()
            return results
        except Exception as e:
            print(f"Error: {e}")
        return []

    async def getVoice(self, id):
        try:
            voice = await Voice.get(ObjectId(id))
            if voice:
                return voice
            return None
        except Exception as e:
            print(f"Error fetching voice by id: {e}")
            return None
    
    async def saveVoice(self, voice: Voice):
        await voice.insert()
        