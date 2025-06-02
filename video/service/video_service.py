from storage import storage_service
from text_to_speech import tts_service
from ai import ai_service
from moviepy import (AudioFileClip, ColorClip,
                      CompositeVideoClip, TextClip)
from video.dto.requests import CreateVideoRequest
from abc import ABC, abstractmethod
from video.models import Video, VideoMetadata, Scene
import tempfile
import os
import json
class video_service(ABC):
    @abstractmethod
    def create_prompt_to_convert_script_to_object(request: CreateVideoRequest):
        pass
    def get_json_content_from_response():
        pass
    def get_video_metadata():
        pass
    @abstractmethod
    def create_video(request: CreateVideoRequest):
        pass
    def get_video_by_id(id: str):
        pass
    def get_all_videos():
        pass

class video_service_v1(video_service):
    def create_prompt_to_convert_script_to_object(self, request: CreateVideoRequest) -> str:
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
            {request.script}
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
    async def get_video_metadata(self, request: CreateVideoRequest) -> VideoMetadata:
        try:
            prompt = self.create_prompt_to_convert_script_to_object(request)
            response_text = await ai_service.get_response(prompt)
            
            video_metadata_json = await self.get_json_content_from_response(response_text)
            if not video_metadata_json:
                raise ValueError("Parsed video metadata is empty or invalid")
            
            video_metadata = VideoMetadata(**video_metadata_json)
            return video_metadata
        except Exception as e:
            print(f"Error getting video metadata: {e}")
            return None
    async def create_video(self,request: CreateVideoRequest):
        try:
            # Tạo audio từ script
            script_audio_path = await tts_service.text_to_speech(request.script, None)
            audio = AudioFileClip(script_audio_path)
            duration = audio.duration

            video_bg = ColorClip(size=(1280, 720), color=(0, 0, 0)).with_duration(duration)
            final = CompositeVideoClip([video_bg]).with_audio(audio)

            temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video_path = temp_video_file.name
            final.write_videofile(temp_video_path, codec="libx264", audio_codec="aac", fps=24)

            secure_url ,public_id = await storage_service.uploadVideo(temp_video_path)
        
            temp_video_file.close()
            os.remove(temp_video_path)

            video = Video(
                id=public_id,
                title=request.title,
                status="done",
                video_url=secure_url,
                userId=request.userId
            )
            await video.insert()

            return secure_url, public_id
        except Exception as e:
            print(f"Error creating video: {e}")
            return "error", "error"
    async def get_video_by_id(self,id):
        return await Video.get(id)
    async def get_all_videos(self):
        return await Video.all().to_list()