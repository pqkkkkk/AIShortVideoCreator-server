from app.external_service.storage import storage_service
from app.external_service.text_to_speech import tts_service
from app.external_service.external_platform.Youtube import youtube_service, youtube_service_async
from app.common import UploadVideoInfo, thread_pool_manager
from app.utils import download_resource
from app.music_track import music_service
from app.image import public_image_service
from moviepy import (AudioFileClip, ColorClip, ImageClip,
                     VideoFileClip, CompositeAudioClip,
                      CompositeVideoClip, TextClip)
from moviepy import concatenate_videoclips
from moviepy.video.fx.MaskColor import MaskColor
from .requests import (CreateVideoRequest, EditVideoRequest, VideoFilterObject, AllVideoStatisticsRequest,
                       GetVideoCountStatisticsRequest, UploadVideoToYoutubeRequest)
from .resposes import (CreateVideoResponse, EditVideoResponse, UploadVideoToYoutubeResponse,
                       AllVideoStatisticsResponse,
                       VideoCountStatisticsItem,
                       GetVideoCountStatisticsResponse, GetVideoByIdResponse, GetAllVideosResponse)
from .models import (TextAttachment, EmojiAttachment, UploadInfo,
                     VideoStatisticsInfo,
                     Video, VideoMetadata, Scene)
from .subtitle_service import create_subtitles, create_subtitles_clip
from .text_service import handle_each_text_attachment
from.result_status import VideoStatus
from .video_dao import video_dao_v1
from abc import ABC, abstractmethod
import tempfile
import os
from fastapi import UploadFile, Depends
from fastapi.logger import logger
import requests
import datetime
import asyncio

video_dao = video_dao_v1()

class video_service(ABC):
    @abstractmethod
    def insert_video_data(video: Video):
        pass
    @abstractmethod
    def update_video_data(video: Video):
        pass
    @abstractmethod
    def create_video(request: CreateVideoRequest):
        pass
    @abstractmethod
    def edit_video(request: EditVideoRequest) -> EditVideoResponse:
        pass
    def get_video_data_by_id(id: str):
        pass
    def get_all_videos_data():
        pass
    async def upload_video_to_youtube(request: UploadVideoToYoutubeRequest) -> str:
        pass

class video_service_v2():
    """Video service with async capabilities and process pool for heavy tasks"""
    async def get_corresponding_bg_image_temp_path(self, bg_image_public_id: str,
                                                   background_image: UploadFile) -> str:
        if bg_image_public_id and bg_image_public_id != "":
            image_data = await public_image_service.get_image_by_id(bg_image_public_id)

            if image_data:
                response = requests.get(image_data.image_url)
                if response.status_code == 200:
                    temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_data.image_url)[1])
                    temp_image.write(response.content)
                    temp_image.close()
                    return temp_image.name
                else:
                    return None

        if background_image:
            temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(background_image.filename)[1])
            image_bytes = await background_image.read()
            temp_image.write(image_bytes)
            temp_image.close()

            return temp_image.name
        
        return None
    
    
    async def get_corresponding_bg_music_temp_path(self, bg_music_public_id: str,
                                                   background_music: UploadFile) -> str:
        if bg_music_public_id:
            music_track = await music_service.get_music_track_by_id(bg_music_public_id)
            if music_track:
                response = requests.get(music_track.musicUrl)
                if response.status_code == 200:
                    temp_music = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(music_track.musicUrl)[1])
                    temp_music.write(response.content)
                    temp_music.close()
                    return temp_music.name
                else:
                    return None
        elif background_music:
            temp_music = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(background_music.filename)[1])
            music_bytes = await background_music.read()
            temp_music.write(music_bytes)
            temp_music.close()
            return temp_music.name
        
        return None
        
    
    async def handle_each_scene(self, voiceId, scene: Scene,
                                bg_image_temp_path: str,
                                bg_music_temp_path: str):
        clip_to_close = []
        paths_to_remove = []

        try:
            # Tạo audio từ script
            audio_path = await tts_service.text_to_speech(scene.text, voiceId)
            tts_clip = AudioFileClip(audio_path)
            clip_to_close.append(tts_clip)
            paths_to_remove.append(audio_path)

            # Tạo background clip
            if bg_image_temp_path:
                background_clip = (ImageClip(bg_image_temp_path)
                                .with_duration(tts_clip.duration))
                paths_to_remove.append(bg_image_temp_path)
            else:
                background_clip = (ColorClip(size=(1280, 720), color=(0, 0, 0))
                                    .with_duration(tts_clip.duration))
            clip_to_close.append(background_clip)

            # Tạo nhạc nền nếu có
            audio_clips = [tts_clip]
            if bg_music_temp_path:
                music_clip = AudioFileClip(bg_music_temp_path).with_duration(tts_clip.duration)
                audio_clips.insert(0, music_clip)
                clip_to_close.append(music_clip)
                paths_to_remove.append(bg_music_temp_path)

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
    

    def write_video_file_with_moviepy(self,final_video, temp_video_path):
                try:
                    final_video.write_videofile(
                        temp_video_path,
                        codec="libx264",
                        audio_codec="aac",
                        fps=24,
                        
                    )
                    return True
                except Exception as e:
                    print(f"Error writing video file: {e}")
                    return False
    

    async def create_video(self, request : CreateVideoRequest,
                            background_images: list[UploadFile],
                            background_musics: list[UploadFile]):
        try:
            all_clips = []
            all_to_close = []
            all_temp_paths = []

            for idx, scene in enumerate(request.videoMetadata.scenes):
                background_image = (background_images[scene.bg_image_file_index]
                                    if scene.bg_image_file_index < len(background_images) and scene.bg_image_file_index >= 0
                                    else None)
                bg_image_temp_path = await self.get_corresponding_bg_image_temp_path(scene.bg_image_public_id, background_image)

                background_music = (background_musics[scene.bg_music_file_index]
                                    if scene.bg_music_file_index < len(background_musics) and scene.bg_music_file_index >= 0
                                    else None)
                bg_music_temp_path = await self.get_corresponding_bg_music_temp_path(scene.bg_music_public_id, background_music)

                scene_clip, clips_to_close, temp_paths = await self.handle_each_scene(request.voiceId, scene,
                                                                                      bg_image_temp_path, bg_music_temp_path)
                
                if scene_clip is None:
                    raise Exception(f"Failed to create scene clip for scene {idx}")
                
                all_clips.append(scene_clip)
                all_to_close += clips_to_close
                all_temp_paths += temp_paths
            
            
            final_video = concatenate_videoclips(all_clips, method="compose")

            subtitles = create_subtitles(all_clips, request.videoMetadata)
            subtitles_clip = create_subtitles_clip(subtitles)
            all_to_close.append(subtitles_clip)

            final_video_with_subtitles = CompositeVideoClip([final_video,
                                                            subtitles_clip.with_position(("center", final_video.size[1] - 50))])

            temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video_file.close()

            
            # Offload video writing to process pool
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                thread_pool_manager.get_pool(),
                self.write_video_file_with_moviepy,
                final_video_with_subtitles,
                temp_video_file.name
            )

            secure_url, public_id = await storage_service.uploadVideo(temp_video_file.name)

            os.remove(temp_video_file.name)

            for clip in all_to_close:
                try: clip.close()
                except: pass
            for path in all_temp_paths:
                if os.path.exists(path): os.remove(path)
            
            video_data = Video(
                public_id=public_id,
                title=request.title,
                status= VideoStatus.PROCESSING.value,
                can_edit=True,
                video_url=secure_url,
                userId=request.userId,
                duration=final_video.duration
            )
            await self.insert_video_data(video_data)

            return CreateVideoResponse(
                public_id=public_id,
                secure_url=secure_url,
                message="Video created successfully"
            )
        except Exception as e:
            print(f"Error creating video: {e}")
            return CreateVideoResponse(
                public_id="",
                secure_url="",
                message= "error creating video"
            )


    async def handle_each_emoji_attachment_v2(self, emoji_attachment: EmojiAttachment,
                                              parent_clip_width: int, parent_clip_height: int):
        if emoji_attachment:
            try:
                emoji_url = f"https://fonts.gstatic.com/s/e/notoemoji/latest/{emoji_attachment.codepoint}/512.gif"
                emoji_clip = VideoFileClip(emoji_url)
                mask_color = MaskColor(color=(255, 255, 255), threshold=0.1, stiffness=1)
                emoji_clip = mask_color.apply(emoji_clip)

                emoji_clip = (emoji_clip
                            .with_start(emoji_attachment.start_time)
                            .with_duration(emoji_attachment.end_time - emoji_attachment.start_time)
                            .resized(height=emoji_attachment.size, width=emoji_attachment.size))
                
                left = (parent_clip_width - emoji_attachment.size) * emoji_attachment.position.x
                top = (parent_clip_height - emoji_attachment.size) * emoji_attachment.position.y
                emoji_clip = emoji_clip.with_position((left, top))

                return emoji_clip
            except Exception as e:
                print(f"Error creating emoji clip: {e}")
                try: emoji_clip.close()
                except: pass
                return None
        
        return None
    
    async def handle_each_emoji_attachment_v3(self, emoji_attachment: EmojiAttachment,
                                              parent_clip_width: int, parent_clip_height: int):
        """ Handles each emoji attachment by creating a video clip from the emoji GIF.
        Args:
            emoji_attachment (EmojiAttachment): The emoji attachment containing details like codepoint, start_time, end_time, size, and position.
            parent_clip_width (int): The width of the parent clip where the emoji will be positioned.
            parent_clip_height (int): The height of the parent clip where the emoji will be positioned.
        Returns:
            VideoFileClip: A video clip of the emoji positioned at the specified location, or None if an error occurs.
            emoji_temp_path (str): The temporary path of the emoji GIF file or None if an error occurs.
        
        """
         
        if emoji_attachment:
            try:
                emoji_url = f"https://fonts.gstatic.com/s/e/notoemoji/latest/{emoji_attachment.codepoint}/512.gif"
                emoji_temp_path = await download_resource(emoji_url)
                if not emoji_temp_path:
                    return None, None
                
                emoji_clip = VideoFileClip(emoji_temp_path)
                mask_color = MaskColor(color=(255, 255, 255), threshold=0.1, stiffness=1)
                emoji_clip = mask_color.apply(emoji_clip)

                emoji_clip = (emoji_clip
                            .with_start(emoji_attachment.start_time)
                            .with_duration(emoji_attachment.end_time - emoji_attachment.start_time)
                            .resized(height=emoji_attachment.size, width=emoji_attachment.size))
                
                left = (parent_clip_width - emoji_attachment.size) * emoji_attachment.position.x
                top = (parent_clip_height - emoji_attachment.size) * emoji_attachment.position.y
                emoji_clip = emoji_clip.with_position((left, top))

                return emoji_clip, emoji_temp_path
            except Exception as e:
                print(f"Error creating emoji clip: {e}")
                try: 
                    emoji_clip.close()
                    if emoji_temp_path and os.path.exists(emoji_temp_path):
                        os.remove(emoji_temp_path)
                except: pass
                return None, None
        
        return None, None

    async def get_video_temp_path(self, secure_url: str) -> str:
        if secure_url:
            response = requests.get(secure_url)
            if response.status_code == 200:
                temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                temp_video.write(response.content)
                temp_video.close()
                return temp_video.name
        return None
    
    
    async def edit_video(self, request: EditVideoRequest) -> EditVideoResponse:
        try:
            video_data = await video_dao.get_video_by_id(request.public_id)
            if not video_data:
                return EditVideoResponse(
                    public_id=request.public_id,
                    secure_url="",
                    message="video not found"
                )
            
            old_video_temp_path = await self.get_video_temp_path(video_data.video_url)
            old_video = VideoFileClip(old_video_temp_path)

            text_clips = []
            emoji_clips = []
            all_clips = []
            clips_to_close = []
            paths_to_remove = [old_video_temp_path]

            for text_attachment in request.text_attachments:
                text_clip = await handle_each_text_attachment(text_attachment,
                                                            old_video.size[0], old_video.size[1])
                if text_clip:
                    text_clips.append(text_clip)
                    clips_to_close.append(text_clip)

            for emoji_attachment in request.emoji_attachments:
                emoji_clip, emoji_temp_path = await self.handle_each_emoji_attachment_v3(emoji_attachment,
                                                                        old_video.size[0], old_video.size[1])
                if emoji_clip:
                    emoji_clips.append(emoji_clip)
                    clips_to_close.append(emoji_clip)
                if emoji_temp_path:
                    paths_to_remove.append(emoji_temp_path)
            
            all_clips = [old_video]
            all_clips.extend(emoji_clips)
            all_clips.extend(text_clips)

            # Tạo video từ các clip
            final_video = CompositeVideoClip(all_clips, size=old_video.size)
            temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video_file.close()
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                thread_pool_manager.get_pool(),
                self.write_video_file_with_moviepy,
                final_video,
                temp_video_file.name
            )

            new_secure_url, public_id, duration = await storage_service.updateVideo(temp_video_file.name,
                                                                                 video_data.public_id)
            updated_video_data = Video(**video_data.__dict__)
            updated_video_data.video_url = new_secure_url
            updated_video_data.duration = duration
            updated_video_data.status = VideoStatus.DONE.value
            await self.update_video_data(updated_video_data)
            
            paths_to_remove.append(temp_video_file.name)

            for clip in clips_to_close:
                try: clip.close()
                except: pass
            for path in paths_to_remove:
                try: 
                    if os.path.exists(path):
                        os.remove(path)
                except: pass

            return EditVideoResponse(
                public_id=public_id,
                secure_url=new_secure_url,
                message="video edited successfully"
            )
        except Exception as e:
            print(f"Error editing video: {e}")
            for clip in clips_to_close:
                try: clip.close()
                except: pass
            return EditVideoResponse(
                public_id=request.public_id,
                secure_url="",
                message="error editing video"
            )
        
    
    async def insert_video_data(self, video: Video):
        await video_dao.insert_video(video)

    async def update_video_data(self, video: Video):
        await video_dao.update_video(video)

    async def get_video_data_by_id(self,id) -> GetVideoByIdResponse:
        try:
            video_data = await video_dao.get_video_by_id(id)

            youtube_video_ids = [info.videoId for info in video_data.uploaded_info if info.platform == "youtube"]
            stats = youtube_service.getStatisticsInfoBatch(youtube_video_ids)

            if stats:
                for info in video_data.uploaded_info:
                    if info.platform == "youtube":
                        stat = next((s for s in stats if s["video_id"] == info.videoId), None)
                        if stat:
                            info.statistics_info.view_count = stat["view_count"]
                            info.statistics_info.like_count = stat["like_count"]
                            info.statistics_info.favorite_count = stat["favorite_count"]
                            info.statistics_info.comment_count = stat["comment_count"]
        
            if not video_data:
                return GetVideoByIdResponse(
                    video_data=None,
                    can_edit=False,
                    status_code=404,
                    message="Video not found"
                )
            
            can_edit = video_data.status == VideoStatus.PROCESSING.value
            response = GetVideoByIdResponse(video_data=video_data,
                                            status_code=200,
                                            message="success",
                                            can_edit=can_edit)
            return response
        except Exception as e:
            print(f"Error getting video by id: {e}")
            return GetVideoByIdResponse(
                video_data=None,
                can_edit=False,
                message="error getting video by id",
                status_code=500
            )
    
    async def get_all_videos_statistics(self, request: AllVideoStatisticsRequest) -> AllVideoStatisticsResponse:
        try:
            videos = await video_dao.get_all_videos(user_id=request.user_id)

            if videos == None:
                raise Exception("error getting uploaded videos info")
            
            total_videos = len(videos)
            total_youtube_uploaded_videos = sum(1 for video in videos if
                                                video.uploaded_info and
                                                any(info.platform == "youtube" for info in video.uploaded_info))
            

            youtube_video_ids = [video.uploaded_info[0].videoId
                                for video in videos if video.uploaded_info and video.uploaded_info[0].platform == "youtube"]
            stats = await youtube_service_async.getStatisticsInfoBatch(youtube_video_ids)

            total_view_count = sum(stat["view_count"] for stat in stats if stat)
            total_like_count = sum(stat["like_count"] for stat in stats if stat)
            total_favorite_count = sum(stat["favorite_count"] for stat in stats if stat)
            total_comment_count = sum(stat["comment_count"] for stat in stats if stat)

            statistics_info = VideoStatisticsInfo(
                view_count=total_view_count,
                like_count=total_like_count,
                favorite_count=total_favorite_count,
                comment_count=total_comment_count
            )
            return AllVideoStatisticsResponse(
                statistics_info=statistics_info,
                total_youtube_uploaded_videos=total_youtube_uploaded_videos,
                total_videos=total_videos,
                status_code=200,
                message="success"
            )
        except Exception as e:
            logger.exception("Exception occurred while getting all videos statistics")
            return AllVideoStatisticsResponse(
                statistics_info = VideoStatisticsInfo(
                    view_count=0,
                    like_count=0,
                    favorite_count=0,
                    comment_count=0
                ),
                total_videos=0,
                status_code=500,
                message="error getting all videos statistics"
            )
    async def get_video_count_statistics(self, request: GetVideoCountStatisticsRequest) -> GetVideoCountStatisticsResponse:
        try:
            statistics_strategy = {
                "last_7_days": self.get_video_count_statistics_last_7_days,
                "last_30_days": self.get_video_count_statistics_last_30_days,
                "custom": lambda req: video_dao.get_video_count_statistics(req.start_date, req.end_date)
            }

            if request.time_range not in statistics_strategy:
                raise ValueError(f"Invalid time range: {request.time_range}")
            
            response = await statistics_strategy[request.time_range](request)
            if response.status_code != 200:
                raise Exception(response.message)
            
            return response
        except Exception as e:
            logger.error(f"Error getting video count statistics: {e}")
            return GetVideoCountStatisticsResponse(
                timely_video_count=[],
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=500,
                message="error getting video count statistics"
            )
    async def get_video_count_statistics_last_7_days(self, request: GetVideoCountStatisticsRequest) -> GetVideoCountStatisticsResponse:
        try:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=6)
            video_count_result = await video_dao.get_video_count_statistics(start_date, end_date, user_id=request.user_id)
            if video_count_result is None:
                raise Exception("No video count statistics found for the last 7 days")
            
            timely_video_count = []

            for i in range(7):
                current_date = (start_date + datetime.timedelta(days=i)).date()
                count = next((item["count"] for item in video_count_result if item["date"].date() == current_date), 0)
                
                timely_video_count.append(VideoCountStatisticsItem(
                    time=current_date.strftime("%Y-%m-%d"),
                    count=count
                ))
            
            return GetVideoCountStatisticsResponse(
                timely_video_count=timely_video_count,
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=200,
                message="success"
            )
        except Exception as e:
            logger.error(f"Error getting video count statistics for last 7 days: {e}")
            return GetVideoCountStatisticsResponse(
                timely_video_count=[],
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=500,
                message="error getting video count statistics for last 7 days"
            )
    async def get_video_count_statistics_last_30_days(self, request: GetVideoCountStatisticsRequest) -> GetVideoCountStatisticsResponse:
        try:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=29)
            video_count_result = await video_dao.get_video_count_statistics(start_date, end_date, user_id=request.user_id)
            if video_count_result is None:
                raise Exception("No video count statistics found for the last 30 days")
            
            timely_video_count = []

            for i in range(30):
                current_date = (start_date + datetime.timedelta(days=i)).date()
                count = next((item["count"] for item in video_count_result if item["date"].date() == current_date), 0)
                
                timely_video_count.append(VideoCountStatisticsItem(
                    time=current_date.strftime("%Y-%m-%d"),
                    count=count
                ))
            
            return GetVideoCountStatisticsResponse(
                timely_video_count=timely_video_count,
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=200,
                message="success"
            )
        except Exception as e:
            logger.error(f"Error getting video count statistics for last 30 days: {e}")
            return GetVideoCountStatisticsResponse(
                timely_video_count=[],
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=500,
                message="error getting video count statistics for last 30 days"
            )
    async def get_all_videos_data_paginated(self, filter_object : VideoFilterObject) -> GetAllVideosResponse:
        try:
            videos, total_videos, total_pages = await video_dao.get_all_videos_paginated(filter_object=filter_object)

            youtube_video_ids = [youtube_uploaded_info.videoId for video in videos
                                 for youtube_uploaded_info in video.uploaded_info
                                 if youtube_uploaded_info.platform == "youtube"]
            stats = await youtube_service_async.getStatisticsInfoBatch(youtube_video_ids)

            if stats:
                for video in videos:
                    video.uploaded_info = [info for info in video.uploaded_info if info.platform == "youtube"]
                    if video.uploaded_info:
                        youtube_info = video.uploaded_info[0]
                        stat = next((s for s in stats if s["video_id"] == youtube_info.videoId), None)
                        if stat:
                            youtube_info.statistics_info.view_count = stat["view_count"]
                            youtube_info.statistics_info.like_count = stat["like_count"]
                            youtube_info.statistics_info.favorite_count = stat["favorite_count"]
                            youtube_info.statistics_info.comment_count = stat["comment_count"]
            
            return GetAllVideosResponse(
                items=videos,
                total_videos=total_videos,
                total_pages=total_pages,
                current_page_number=filter_object.current_page_number,
                page_size=filter_object.page_size,
                message="success",
                status_code=200
            )
        except Exception as e:
            print(f"Error getting paginated videos: {e}")
            return GetAllVideosResponse(items=[], total_videos=0, total_pages=0,
                                        current_page_number=filter_object.current_page_number,
                                        page_size=filter_object.page_size,
                                        message="error getting paginated videos", status_code=500)
    
    async def upload_video_to_youtube(self,request: UploadVideoInfo):
        try:
            youtube_reponse = await youtube_service_async.upload_video_immediate(request)

            if not youtube_reponse:
                raise Exception("Error uploading video to YouTube")
            
            response = UploadVideoToYoutubeResponse(
                video_public_id=request.video_public_id,
                title=request.title,
                videoUrl=request.videoUrl,
                description=request.description,
                keyword=request.keyword,
                category=request.category,
                privateStatus=request.privateStatus,
                message="Video uploaded to YouTube successfully",
                status_code=200,
                youtube_video_id=youtube_reponse.get("id"),
                youtube_video_url=f"https://www.youtube.com/watch?v={youtube_reponse.get('id')}"
            )

            old_video_data = await video_dao.get_video_by_id(request.video_public_id)
            youtube_uploaded_info = UploadInfo(
                platform="youtube",
                videoId=response.youtube_video_id,
                uploadedAt= datetime.datetime.now()
            )
            old_video_data.uploaded_info.append(youtube_uploaded_info)
            await video_dao.update_video(old_video_data)

            return response
        except Exception as e:
            print(f"Error uploading video to YouTube: {e}")
            response = UploadVideoToYoutubeResponse(
                video_public_id=request.video_public_id,
                title=request.title,
                videoUrl=request.videoUrl,
                description=request.description,
                keyword=request.keyword,
                category=request.category,
                privateStatus=request.privateStatus,
                message="Error uploading video to YouTube",
                status_code=500
            )

            return response

class video_service_v1(video_service):  
    """Video service without async capabilities, does not use process pool for heavy tasks"""  
    async def get_corresponding_bg_image_temp_path(self, bg_image_public_id: str,
                                                   background_image: UploadFile) -> str:
        if bg_image_public_id and bg_image_public_id != "":
            image_data = await public_image_service.get_image_by_id(bg_image_public_id)

            if image_data:
                response = requests.get(image_data.image_url)
                if response.status_code == 200:
                    temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_data.image_url)[1])
                    temp_image.write(response.content)
                    temp_image.close()
                    return temp_image.name
                else:
                    return None

        if background_image:
            temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(background_image.filename)[1])
            image_bytes = await background_image.read()
            temp_image.write(image_bytes)
            temp_image.close()

            return temp_image.name
        
        return None
    
    
    async def get_corresponding_bg_music_temp_path(self, bg_music_public_id: str,
                                                   background_music: UploadFile) -> str:
        if bg_music_public_id:
            music_track = await music_service.get_music_track_by_id(bg_music_public_id)
            if music_track:
                response = requests.get(music_track.musicUrl)
                if response.status_code == 200:
                    temp_music = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(music_track.musicUrl)[1])
                    temp_music.write(response.content)
                    temp_music.close()
                    return temp_music.name
                else:
                    return None
        elif background_music:
            temp_music = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(background_music.filename)[1])
            music_bytes = await background_music.read()
            temp_music.write(music_bytes)
            temp_music.close()
            return temp_music.name
        
        return None
        
    
    async def handle_each_scene(self, voiceId, scene: Scene,
                                bg_image_temp_path: str,
                                bg_music_temp_path: str):
        clip_to_close = []
        paths_to_remove = []

        try:
            # Tạo audio từ script
            audio_path = await tts_service.text_to_speech(scene.text, voiceId)
            tts_clip = AudioFileClip(audio_path)
            clip_to_close.append(tts_clip)
            paths_to_remove.append(audio_path)

            # Tạo background clip
            if bg_image_temp_path:
                background_clip = (ImageClip(bg_image_temp_path)
                                .with_duration(tts_clip.duration))
                paths_to_remove.append(bg_image_temp_path)
            else:
                background_clip = (ColorClip(size=(1280, 720), color=(0, 0, 0))
                                    .with_duration(tts_clip.duration))
            clip_to_close.append(background_clip)

            # Tạo nhạc nền nếu có
            audio_clips = [tts_clip]
            if bg_music_temp_path:
                music_clip = AudioFileClip(bg_music_temp_path).with_duration(tts_clip.duration)
                audio_clips.insert(0, music_clip)
                clip_to_close.append(music_clip)
                paths_to_remove.append(bg_music_temp_path)

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
                background_image = (background_images[scene.bg_image_file_index]
                                    if scene.bg_image_file_index < len(background_images) and scene.bg_image_file_index >= 0
                                    else None)
                bg_image_temp_path = await self.get_corresponding_bg_image_temp_path(scene.bg_image_public_id, background_image)

                background_music = (background_musics[scene.bg_music_file_index]
                                    if scene.bg_music_file_index < len(background_musics) and scene.bg_music_file_index >= 0
                                    else None)
                bg_music_temp_path = await self.get_corresponding_bg_music_temp_path(scene.bg_music_public_id, background_music)

                scene_clip, clips_to_close, temp_paths = await self.handle_each_scene(request.voiceId, scene,
                                                                                      bg_image_temp_path, bg_music_temp_path)
                if scene_clip is None:
                    raise Exception(f"Failed to create scene clip for scene {idx}")
                
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
            
            video_data = Video(
                public_id=public_id,
                title=request.title,
                status= VideoStatus.PROCESSING.value,
                can_edit=True,
                video_url=secure_url,
                userId=request.userId,
                duration=final_video.duration
            )
            await self.insert_video_data(video_data)

            return CreateVideoResponse(
                public_id=public_id,
                secure_url=secure_url,
                message="Video created successfully"
            )
        except Exception as e:
            print(f"Error creating video: {e}")
            return CreateVideoResponse(
                public_id="",
                secure_url="",
                message= "error creating video"
            )

    async def handle_each_text_attachment_v2(self, text_attachment: TextAttachment,
                                             parent_clip_width: int, parent_clip_height: int):
        if text_attachment.text:
            try:
                text_clip = TextClip(text = text_attachment.text,
                                     color = text_attachment.color_hex,
                                     font_size = text_attachment.font_size,
                                     duration = (text_attachment.end_time - text_attachment.start_time),
                                      font = 'c:\Windows\Fonts\ARIAL.TTF')
                text_clip.start = text_attachment.start_time
                text_clip.end = text_attachment.end_time
                
                left = (parent_clip_width - text_attachment.font_size * len(text_attachment.text)) * text_attachment.position.x
                top = (parent_clip_height - text_attachment.font_size) * text_attachment.position.y
                text_clip = text_clip.with_position((left,top))

                return text_clip
            except Exception as e:
                print(f"Error creating text clip: {e}")
                try: text_clip.close()
                except: pass
                return None

        return None  


    async def handle_each_emoji_attachment_v2(self, emoji_attachment: EmojiAttachment,
                                              parent_clip_width: int, parent_clip_height: int):
        if emoji_attachment:
            try:
                emoji_url = f"https://fonts.gstatic.com/s/e/notoemoji/latest/{emoji_attachment.codepoint}/512.gif"
                emoji_clip = VideoFileClip(emoji_url)
                mask_color = MaskColor(color=(255, 255, 255), threshold=0.1, stiffness=1)
                emoji_clip = mask_color.apply(emoji_clip)

                emoji_clip = (emoji_clip
                            .with_start(emoji_attachment.start_time)
                            .with_duration(emoji_attachment.end_time - emoji_attachment.start_time)
                            .resized(height=emoji_attachment.size, width=emoji_attachment.size))
                
                left = (parent_clip_width - emoji_attachment.size) * emoji_attachment.position.x
                top = (parent_clip_height - emoji_attachment.size) * emoji_attachment.position.y
                emoji_clip = emoji_clip.with_position((left, top))

                return emoji_clip
            except Exception as e:
                print(f"Error creating emoji clip: {e}")
                try: emoji_clip.close()
                except: pass
                return None
        
        return None

    async def get_video_temp_path(self, secure_url: str) -> str:
        if secure_url:
            response = requests.get(secure_url)
            if response.status_code == 200:
                temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                temp_video.write(response.content)
                temp_video.close()
                return temp_video.name
        return None
    
    
    async def edit_video(self, request: EditVideoRequest) -> EditVideoResponse:
        try:
            video_data = await video_dao.get_video_by_id(request.public_id)
            if not video_data:
                return EditVideoResponse(
                    public_id=request.public_id,
                    secure_url="",
                    message="video not found"
                )
            old_video_temp_path = await self.get_video_temp_path(video_data.video_url)
            old_video = VideoFileClip(old_video_temp_path)

            text_clips = []
            emoji_clips = []
            all_clips = []
            clips_to_close = []

            for text_attachment in request.text_attachments:
                text_clip = await self.handle_each_text_attachment_v2(text_attachment,
                                                                    old_video.size[0], old_video.size[1])
                if text_clip:
                    text_clips.append(text_clip)
                    clips_to_close.append(text_clip)

            for emoji_attachment in request.emoji_attachments:
                emoji_clip = await self.handle_each_emoji_attachment_v2(emoji_attachment,
                                                                        old_video.size[0], old_video.size[1])
                if emoji_clip:
                    emoji_clips.append(emoji_clip)
                    clips_to_close.append(emoji_clip)
            
            all_clips = [old_video]
            all_clips.extend(emoji_clips)
            all_clips.extend(text_clips)

            # Tạo video từ các clip
            final_video = CompositeVideoClip(all_clips, size=old_video.size)
            temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video_file.close()
            final_video.write_videofile(temp_video_file.name, codec="libx264", audio_codec="aac", fps=24)

            new_secure_url, public_id, duration = await storage_service.updateVideo(temp_video_file.name,
                                                                                 video_data.public_id)
            updated_video_data = Video(**video_data.__dict__)
            updated_video_data.video_url = new_secure_url
            updated_video_data.duration = duration
            updated_video_data.status = VideoStatus.DONE.value
            await self.update_video_data(updated_video_data)
            os.remove(temp_video_file.name)

            for clip in clips_to_close:
                try: clip.close()
                except: pass

            return EditVideoResponse(
                public_id=public_id,
                secure_url=new_secure_url,
                message="video edited successfully"
            )
        except Exception as e:
            print(f"Error editing video: {e}")
            for clip in clips_to_close:
                try: clip.close()
                except: pass
            return EditVideoResponse(
                public_id=request.public_id,
                secure_url="",
                message="error editing video"
            )
        
    
    async def insert_video_data(self, video: Video):
        await video_dao.insert_video(video)

    async def update_video_data(self, video: Video):
        await video_dao.update_video(video)

    async def get_video_data_by_id(self,id) -> GetVideoByIdResponse:
        try:
            video_data = await video_dao.get_video_by_id(id)

            youtube_video_ids = [info.videoId for info in video_data.uploaded_info if info.platform == "youtube"]
            stats = youtube_service.getStatisticsInfoBatch(youtube_video_ids)

            if stats:
                for info in video_data.uploaded_info:
                    if info.platform == "youtube":
                        stat = next((s for s in stats if s["video_id"] == info.videoId), None)
                        if stat:
                            info.statistics_info.view_count = stat["view_count"]
                            info.statistics_info.like_count = stat["like_count"]
                            info.statistics_info.favorite_count = stat["favorite_count"]
                            info.statistics_info.comment_count = stat["comment_count"]
        
            if not video_data:
                return GetVideoByIdResponse(
                    video_data=None,
                    can_edit=False,
                    status_code=404,
                    message="Video not found"
                )
            
            can_edit = video_data.status == VideoStatus.PROCESSING.value
            response = GetVideoByIdResponse(video_data=video_data,
                                            status_code=200,
                                            message="success",
                                            can_edit=can_edit)
            return response
        except Exception as e:
            print(f"Error getting video by id: {e}")
            return GetVideoByIdResponse(
                video_data=None,
                can_edit=False,
                message="error getting video by id",
                status_code=500
            )
    
    async def get_all_videos_statistics(self) -> AllVideoStatisticsResponse:
        try:
            videos = await video_dao.get_all_videos()
            total_videos = len(videos)
            total_youtube_uploaded_videos = sum(1 for video in videos if
                                                video.uploaded_info and
                                                any(info.platform == "youtube" for info in video.uploaded_info))
            if not videos:
                raise Exception("error getting uploaded videos info")

            youtube_video_ids = [video.uploaded_info[0].videoId
                                for video in videos if video.uploaded_info and video.uploaded_info[0].platform == "youtube"]
            stats =  youtube_service.getStatisticsInfoBatch(youtube_video_ids)

            total_view_count = sum(stat["view_count"] for stat in stats if stat)
            total_like_count = sum(stat["like_count"] for stat in stats if stat)
            total_favorite_count = sum(stat["favorite_count"] for stat in stats if stat)
            total_comment_count = sum(stat["comment_count"] for stat in stats if stat)

            statistics_info = VideoStatisticsInfo(
                view_count=total_view_count,
                like_count=total_like_count,
                favorite_count=total_favorite_count,
                comment_count=total_comment_count
            )
            return AllVideoStatisticsResponse(
                statistics_info=statistics_info,
                total_youtube_uploaded_videos=total_youtube_uploaded_videos,
                total_videos=total_videos,
                status_code=200,
                message="success"
            )
        except Exception as e:
            logger.exception("Exception occurred while getting all videos statistics")
            return AllVideoStatisticsResponse(
                statistics_info=None,
                total_videos=0,
                status_code=500,
                message="error getting all videos statistics"
            )
    async def get_video_count_statistics(self, request: GetVideoCountStatisticsRequest) -> GetVideoCountStatisticsResponse:
        try:
            statistics_strategy = {
                "last_7_days": self.get_video_count_statistics_last_7_days,
                "last_30_days": self.get_video_count_statistics_last_7_days,  # Assuming similar logic for 30 days
                "custom": lambda req: video_dao.get_video_count_statistics(req.start_date, req.end_date)
            }

            if request.time_range not in statistics_strategy:
                raise ValueError(f"Invalid time range: {request.time_range}")
            
            response = await statistics_strategy[request.time_range](request)
            if response.status_code != 200:
                raise Exception(response.message)
            
            return response
        except Exception as e:
            logger.error(f"Error getting video count statistics: {e}")
            return GetVideoCountStatisticsResponse(
                timely_video_count=[],
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=500,
                message="error getting video count statistics"
            )
    async def get_video_count_statistics_last_7_days(self, request: GetVideoCountStatisticsRequest) -> GetVideoCountStatisticsResponse:
        try:
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=6)
            video_count_result = await video_dao.get_video_count_statistics(start_date, end_date)
            if not video_count_result:
                raise Exception("No video count statistics found for the last 7 days")
            
            timely_video_count = []

            for i in range(7):
                current_date = (start_date + datetime.timedelta(days=i)).date()
                count = next((item["count"] for item in video_count_result if item["date"].date() == current_date), 0)
                
                timely_video_count.append(VideoCountStatisticsItem(
                    time=current_date.strftime("%Y-%m-%d"),
                    count=count
                ))
            
            return GetVideoCountStatisticsResponse(
                timely_video_count=timely_video_count,
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=200,
                message="success"
            )
        except Exception as e:
            logger.error(f"Error getting video count statistics for last 7 days: {e}")
            return GetVideoCountStatisticsResponse(
                timely_video_count=[],
                time_unit=request.time_unit,
                time_range=request.time_range,
                status_code=500,
                message="error getting video count statistics for last 7 days"
            )
    async def get_all_videos_data_paginated(self, filter_object : VideoFilterObject) -> GetAllVideosResponse:
        try:
            videos, total_videos, total_pages = await video_dao.get_all_videos_paginated(filter_object=filter_object)

            youtube_video_ids = [youtube_uploaded_info.videoId for video in videos
                                 for youtube_uploaded_info in video.uploaded_info
                                 if youtube_uploaded_info.platform == "youtube"]
                 
            stats = youtube_service.getStatisticsInfoBatch(youtube_video_ids)

            if stats:
                for video in videos:
                    video.uploaded_info = [info for info in video.uploaded_info if info.platform == "youtube"]
                    if video.uploaded_info:
                        youtube_info = video.uploaded_info[0]
                        stat = next((s for s in stats if s["video_id"] == youtube_info.videoId), None)
                        if stat:
                            youtube_info.statistics_info.view_count = stat["view_count"]
                            youtube_info.statistics_info.like_count = stat["like_count"]
                            youtube_info.statistics_info.favorite_count = stat["favorite_count"]
                            youtube_info.statistics_info.comment_count = stat["comment_count"]
            
            return GetAllVideosResponse(
                items=videos,
                total_videos=total_videos,
                total_pages=total_pages,
                current_page_number=filter_object.current_page_number,
                page_size=filter_object.page_size,
                message="success",
                status_code=200
            )
        except Exception as e:
            print(f"Error getting paginated videos: {e}")
            return GetAllVideosResponse(items=[], total_videos=0, total_pages=0,
                                        current_page_number=filter_object.current_page_number,
                                        page_size=filter_object.page_size,
                                        message="error getting paginated videos", status_code=500)
    
    async def upload_video_to_youtube(self,request: UploadVideoInfo):
        try:
            youtube_reponse = await youtube_service.upload_video_immediate(request)

            if not youtube_reponse:
                raise Exception("Error uploading video to YouTube")
            
            response = UploadVideoToYoutubeResponse(
                video_public_id=request.video_public_id,
                title=request.title,
                videoUrl=request.videoUrl,
                description=request.description,
                keyword=request.keyword,
                category=request.category,
                privateStatus=request.privateStatus,
                message="Video uploaded to YouTube successfully",
                status_code=200,
                youtube_video_id=youtube_reponse.get("id"),
                youtube_video_url=f"https://www.youtube.com/watch?v={youtube_reponse.get('id')}"
            )

            old_video_data = await video_dao.get_video_by_id(request.video_public_id)
            youtube_uploaded_info = UploadInfo(
                platform="youtube",
                videoId=response.youtube_video_id,
                uploadedAt= datetime.datetime.now()
            )
            old_video_data.uploaded_info.append(youtube_uploaded_info)
            await video_dao.update_video(old_video_data)

            return response
        except Exception as e:
            print(f"Error uploading video to YouTube: {e}")
            response = UploadVideoToYoutubeResponse(
                video_public_id=request.video_public_id,
                title=request.title,
                videoUrl=request.videoUrl,
                description=request.description,
                keyword=request.keyword,
                category=request.category,
                privateStatus=request.privateStatus,
                message="Error uploading video to YouTube",
                status_code=500
            )

            return response