from storage import storage_service
from text_to_speech import tts_service
from ai import ai_service
from moviepy import (AudioFileClip, ColorClip, ImageClip,
                     VideoFileClip, CompositeAudioClip,
                      CompositeVideoClip, TextClip)
from moviepy import concatenate_videoclips
from PIL import Image
from video.dto.requests import CreateVideoRequest
from abc import ABC, abstractmethod
from video.models import Video, VideoMetadata, Scene
import tempfile
import os
import json
import numpy as np
from io import BytesIO
from fastapi import UploadFile

class video_service(ABC):
    @abstractmethod
    def create_video(request: CreateVideoRequest):
        pass
    def get_video_by_id(id: str):
        pass
    def get_all_videos():
        pass
class video_service_v2(video_service):
    async def get_corresponding_bg_image_path(self, bg_image_secure_url: str, background_images: list[UploadFile]) -> str:
        pass
    async def get_corresponding_bg_music_path(self, bg_music_secure_url, background_musics: list[UploadFile]) -> str:
        pass
    async def handle_each_scene(self, voiceId, scene: Scene, background_image, background_music):
        clip_to_close = []
        paths_to_remove = []

        try:
            # Tạo audio từ script
            audio_path = await tts_service.text_to_speech(scene.text, voiceId)
            paths_to_remove.append(audio_path)
            tts_clip = AudioFileClip(audio_path)
            clip_to_close.append(tts_clip)

            # Tạo background clip
            if background_image:
                temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(background_image.filename)[1])
                image_bytes = await background_image.read()
                temp_image.write(image_bytes)
                temp_image.close()
                paths_to_remove.append(temp_image.name)

                background_clip = (ImageClip(temp_image.name)
                                .with_duration(tts_clip.duration))
            
            else:
                background_clip = (ColorClip(size=(1280, 720), color=(0, 0, 0))
                                    .with_duration(tts_clip.duration))
            clip_to_close.append(background_clip)

            # Tạo nhạc nền nếu có
            audio_clips = [tts_clip]
            if background_music:
                temp_music = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(background_music.filename)[1])
                music_bytes = await background_music.read()
                temp_music.write(music_bytes)
                temp_music.close()
                paths_to_remove.append(temp_music.name)

                music_clip = AudioFileClip(temp_music.name)
                clip_to_close.append(music_clip)
                audio_clips.insert(0, music_clip)

            # Ghép audio với nhạc nền
            combined_audio = CompositeAudioClip(audio_clips)
            clip_to_close.append(combined_audio)
            # Tạo scene clip
            scene_clip = background_clip.with_audio(combined_audio)

            return scene_clip, clip_to_close, paths_to_remove
        except Exception as e:
            print(f"Error in scene {scene.scene_id}: {e}")
            # dọn tạm nếu có
            for c in clip_to_close:
                try: c.close()
                except: pass
            for p in paths_to_remove:
                if os.path.exists(p): os.remove(p)
            return None, [], []
    

    async def create_video(self, request : CreateVideoRequest,
                            background_images: list[UploadFile],
                            background_musics: list[UploadFile]):
        try:
            all_clips = []
            all_to_close = []
            all_temp_paths = []

            for idx, scene in enumerate(request.videoMetadata.scenes):
                background_image = background_images[scene.bg_image_file_index] if scene.bg_image_file_index < len(background_images) and scene.bg_image_file_index >= 0 else None
                background_music = background_musics[scene.bg_music_file_index] if scene.bg_music_file_index < len(background_musics) and scene.bg_music_file_index >= 0 else None

                scene_clip, clips_to_close, temp_paths = await self.handle_each_scene(request.voiceId, scene, background_image, background_music)
                if scene_clip is None:
                    return "error", "error"
                
                all_clips.append(scene_clip)
                all_to_close += clips_to_close
                all_temp_paths += temp_paths
            
            final_video = concatenate_videoclips(all_clips, method="compose")

            temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video_file.close()
            final_video.write_videofile(temp_video_file.name, codec="libx264", audio_codec="aac", fps=24)

            secure_url, public_id = await storage_service.uploadVideo(temp_video_file.name)
            os.remove(temp_video_file.name)

            for clip in all_to_close:
                try: clip.close()
                except: pass
            for path in all_temp_paths:
                if os.path.exists(path): os.remove(path)
            
            return secure_url, public_id
        except Exception as e:
            print(f"Error creating video: {e}")
            return "error", "error"
        
        
    async def get_video_by_id(self,id):
        return await Video.get(id)
    

    async def get_all_videos(self):
        return await Video.all().to_list()
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