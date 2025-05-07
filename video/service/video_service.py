from storage import storage_service
from text_to_speech import tts_service
from moviepy import (AudioFileClip, ColorClip,
                      CompositeVideoClip, TextClip)
from video.dto.requests import CreateVideoRequest
from abc import ABC, abstractmethod
import tempfile
import os

class video_service(ABC):
    @abstractmethod
    def create_video(request: CreateVideoRequest):
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

            secure_url= await storage_service.uploadVideo(temp_video_path)

            temp_video_file.close()
            os.remove(temp_video_path)

            return secure_url
        except Exception as e:
            print(f"Error creating video: {e}")
            return "error"