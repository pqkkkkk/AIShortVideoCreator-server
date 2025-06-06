from video_script.dao import video_script_dao
from abc import ABC, abstractmethod
from video_script.models import Voice
from storage import storage_service
from fastapi import HTTPException
from text_to_speech import tts_service
from ai import ai_service
from video_script.dto.requests import AutoGenerateScriptRequest
from models import VideoMetadata
import json

class video_script_service(ABC):
    @abstractmethod
    def getAllSampleVoiceList(self):
        pass
    @abstractmethod
    def getVoice(self, id):
        pass
    @abstractmethod
    def generateTextScript(self, prompt):
        pass
    @abstractmethod
    def saveVoice(self, voice):
        pass
    @abstractmethod
    def create_prompt_to_convert_script_to_object(scirpt: str):
        pass
    def get_json_content_from_response():
        pass
    def get_video_metadata(script: str) -> VideoMetadata:
        pass

class video_script_service_v1(video_script_service):
    async def generateTextScript(self, request: AutoGenerateScriptRequest):
        try:
            text_script = await ai_service.get_response(request.prompt)
            return text_script
        except Exception as e:
            print(f"Error: {e}")
            return None
    async def getAllSampleVoiceList(self):
        try:
            results = await video_script_dao.getAllSampleVoice()
            return results
        except Exception as e:
            print(f"Error: {e}")  
        return []         
    async def getVoice(self, id):
        try:
            res = await video_script_dao.getVoice(id)
            return res
        except Exception as e:
            print(f'Error: {e}')
            return None
    async def saveVoice(self, voice: Voice):
        try:
            await video_script_dao.saveVoice(voice)
            return voice
        except Exception as e:
            print(f"Error: {e}")
            return None
    def create_prompt_to_convert_script_to_object(self, script: str) -> str:
        prompt = f"""
            Bạn là một trợ lý AI chuyên nghiệp có khả năng chuyển đổi kịch bản video thành định dạng JSON có cấu trúc.
            Hãy chuyển đổi kịch bản video sau đây thành một đối tượng JSON.
            Cấu trúc JSON mong muốn của bạn phải tuân thủ định dạng sau:
            ```json
            {{
            "scenes": [
                {{
                "scene_id": "số thứ tự của cảnh",
                "start_time": "thời gian bắt đầu của cảnh (theo giây)",
                "end_time": "thời gian kết thúc của cảnh (theo giây)",
                "text": "Nội dung văn bản cho cảnh này",
                "background_image": "URL của hình ảnh nền cho cảnh này (nếu có)",
                "background_music": "URL của nhạc nền cho cảnh này (nếu có)",
                }}
            ]
            }}
            ```
            Hãy đảm bảo rằng tất cả các trường trong JSON đều được điền đầy đủ và chính xác.
            Nếu không có thông tin nào cho một trường, hãy để nó là chuỗi rỗng.
            đều được điền đầy đủ dựa trên kịch bản gốc.
            Kịch bản video:
            {script}
        """
        return prompt
    async def get_json_content_from_response(self, response_text: str) -> dict:
        try:
            if not response_text:
                raise ValueError("Response is empty or None")
            if "```json" in response_text:
                start_index = response_text.index("```json") + len("```json")
                end_index = response_text.index("```", start_index)
                json_content = response_text[start_index:end_index].strip()
            else:
                json_content = response_text.strip()
            
            video_metadata_json = json.loads(json_content)

            return video_metadata_json
        except Exception as e:
            print(f"Error parsing JSON content: {e}")
            return {}
    async def get_video_metadata(self, script: str) -> VideoMetadata:
        try:
            prompt = self.create_prompt_to_convert_script_to_object(script)
            response_text = await ai_service.get_response(prompt)
            
            video_metadata_json = await self.get_json_content_from_response(response_text)
            if not video_metadata_json:
                raise ValueError("Parsed video metadata is empty or invalid")
            
            video_metadata = VideoMetadata(**video_metadata_json)
            return video_metadata
        except Exception as e:
            print(f"Error getting video metadata: {e}")
            return None