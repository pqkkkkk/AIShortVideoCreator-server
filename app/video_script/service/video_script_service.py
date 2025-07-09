from app.video_script.dao import video_script_dao
from abc import ABC, abstractmethod
from app.video_script.models import Voice
from app.external_service.storage import storage_service
from fastapi import HTTPException
from app.external_service.text_to_speech import tts_service
from app.external_service.ai import gemini_ai_service, ai_service_manager
from app.video_script.responses import GetVideoMetadataResponse, AutoGenerateTextScriptResponse
from app.video_script.requests import AutoGenerateScriptRequest, GetVideoMetadataRequest
from app.video_script.result_status import AutoGenerateTextScriptResult, ConvertToVideoMetadataResult
from app.video_script.models import VideoMetadata
import json
import asyncio

class video_script_service(ABC):
    @abstractmethod
    def getAllVoices(self, lang: str = 'vi'):
        pass
    @abstractmethod
    def getVoiceById(self, id):
        pass
    @abstractmethod
    def generateTextScript(self, prompt):
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
        """Generates a text script for a video based on the provided content and duration.
            Using only Gemini AI.
        """
        try:
            prompt = f"""
            Bạn là một trợ lý AI chuyên nghiệp có khả năng tạo kịch bản video dựa trên nội dung và thời gian video.
            Hãy tạo một kịch bản video cho nội dung sau:
            Nội dung: {request.content}
            Thời gian video: {request.video_duration} giây
            Số lượng cảnh trong video: {request.scene_quantity if request.scene_quantity > 0 else
                                        "tự động xác định sao cho hợp lý với nội dung và thời gian video"}
            mỗi cảnh gồm các thông tin:
            - thời điểm bắt đầu và kết thúc
            - Lời thoại
            - Mô tả về ảnh nền cho ảnh này
            - Mô tả về nhạc nền cho cảnh này
            Hãy đảm bảo rằng kịch bản video được tạo ra có cấu trúc rõ ràng và
            dễ hiểu và mỗi cảnh chỉ chứa 1 mô tả cho ảnh nền, nhạc nền và lời thoại.
            Không chia nhỏ khoảng thời gian ở mỗi cảnh nữa
            """
            
            text_script = await gemini_ai_service.get_response_async(prompt)

            return AutoGenerateTextScriptResponse(
                message = AutoGenerateTextScriptResult.SUCCESS.value,
                result= AutoGenerateTextScriptResult.SUCCESS,
                data=text_script
            )
        except Exception as e:
            print(f"Error: {e}")
            return AutoGenerateTextScriptResponse(
                message = AutoGenerateTextScriptResult.SERVER_BUSY.value,
                result= AutoGenerateTextScriptResult.SERVER_BUSY,
                data=None
            )
    async def generateTextScript_v2(self, request: AutoGenerateScriptRequest):
        """Generates a text script for a video based on the provided content and duration.
            Using multiple AI models.
        """
        try:
            prompt = f"""
            Bạn là một trợ lý AI chuyên nghiệp có khả năng tạo kịch bản video dựa trên nội dung và thời gian video.
            Hãy tạo một kịch bản video cho nội dung sau:
            Nội dung: {request.content}
            Thời gian video: {request.video_duration} giây
            Số lượng cảnh trong video: {request.scene_quantity if request.scene_quantity > 0 else
                                        "tự động xác định sao cho hợp lý với nội dung và thời gian video"}
            mỗi cảnh gồm các thông tin:
            - thời điểm bắt đầu và kết thúc
            - Lời thoại
            - Mô tả về ảnh nền cho ảnh này
            - Mô tả về nhạc nền cho cảnh này
            Hãy đảm bảo rằng kịch bản video được tạo ra có cấu trúc rõ ràng và
            dễ hiểu và mỗi cảnh chỉ chứa 1 mô tả cho ảnh nền, nhạc nền và lời thoại.
            Không chia nhỏ khoảng thời gian ở mỗi cảnh nữa
            """
            
            text_script = await ai_service_manager.get_ai_service(request.model).get_response_async(prompt)

            return AutoGenerateTextScriptResponse(
                message = AutoGenerateTextScriptResult.SUCCESS.value,
                result= AutoGenerateTextScriptResult.SUCCESS,
                data=text_script
            )
        except Exception as e:
            print(f"Error: {e}")
            return AutoGenerateTextScriptResponse(
                message = AutoGenerateTextScriptResult.SERVER_BUSY.value,
                result= AutoGenerateTextScriptResult.SERVER_BUSY,
                data=None
            )
    async def getAllVoices(self, gender: str):
        try:
            results = await video_script_dao.GetAllVoices(gender=gender)
            return results
        except Exception as e:
            print(f"Error: {e}")  
        return []
    async def preparVoice(self, lang: str = 'vi'):
        try:
            #voices = await self.getAllVoices(lang=lang)
            voices = await tts_service.list_voice(lang=lang)
            for voice in voices:
                temp_file_path = await tts_service.text_to_speech(
                    text="Xin chào, đây là một bài kiểm tra.",
                    voiceId=voice['ShortName'],
                    lang=lang
                )
                secure_url, public_id = await storage_service.uploadVideo(temp_file_path)
                voice_data = Voice(
                    voiceId=voice['ShortName'],
                    gender = voice['Gender'],
                    sampleVoiceUrl=secure_url,
                    publicId=public_id,
                )
                await video_script_dao.insertVoice(voice_data)
            
            print(f"✅ All voices prepared and saved successfully.")
            return True
        except Exception as e:
            print(f"Error preparing voice: {e}")
            print(e)
            return False

    async def getVoiceById(self, id):
        try:
            res = await video_script_dao.GetVoiceById(id)
            return res
        except Exception as e:
            print(f'Error: {e}')
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
                "background_image_description": "Mô tả về hình ảnh nền cho cảnh này (nếu có)",
                "background_music": "URL của nhạc nền cho cảnh này (nếu có)",
                "background_music_description": "Mô tả về nhạc nền cho cảnh này (nếu có)"
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
    def get_json_content_from_response(self, response_text: str) -> dict:
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
    async def get_video_metadata(self, script: str) -> GetVideoMetadataResponse:
        """Converts a video script into structured video metadata using Gemini AI."""
        try:
            prompt = self.create_prompt_to_convert_script_to_object(script)
            response_text = await gemini_ai_service.get_response_async(prompt)
            
            video_metadata_json = self.get_json_content_from_response(response_text)
            if not video_metadata_json:
                raise ValueError("Parsed video metadata is empty or invalid")
            
            video_metadata = VideoMetadata(**video_metadata_json)
            return GetVideoMetadataResponse(
                message=ConvertToVideoMetadataResult.SUCCESS.value,
                result=ConvertToVideoMetadataResult.SUCCESS,
                data=video_metadata
            )
        except Exception as e:
            print(f"Error getting video metadata: {e}")
            return GetVideoMetadataResponse(
                message=ConvertToVideoMetadataResult.SERVER_BUSY.value,
                result=ConvertToVideoMetadataResult.SERVER_BUSY,
                data=None
            )
    
    async def get_video_metadata_v2(self, request: GetVideoMetadataRequest) -> GetVideoMetadataResponse:
        """Support for multiple AI models to get video metadata from script"""
        try:
            prompt = self.create_prompt_to_convert_script_to_object(request.script)
            response_text = await ai_service_manager.get_ai_service(request.model).get_response_async(prompt)
            
            video_metadata_json = self.get_json_content_from_response(response_text)
            if not video_metadata_json:
                raise ValueError("Parsed video metadata is empty or invalid")
            
            video_metadata = VideoMetadata(**video_metadata_json)
            return GetVideoMetadataResponse(
                message=ConvertToVideoMetadataResult.SUCCESS.value,
                result=ConvertToVideoMetadataResult.SUCCESS,
                data=video_metadata
            )
        except Exception as e:
            print(f"Error getting video metadata: {e}")
            return GetVideoMetadataResponse(
                message=ConvertToVideoMetadataResult.SERVER_BUSY.value,
                result=ConvertToVideoMetadataResult.SERVER_BUSY,
                data=None
            )