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
    def create_video(request: CreateVideoRequest):
        pass
    def get_video_by_id(id: str):
        pass
    def get_all_videos():
        pass

class video_service_v1(video_service):
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