# from abc import ABC, abstractmethod
# from app.video.models import Video, UploadInfo

# class video_dao(ABC):
#     @abstractmethod
#     def saveUploadInfo(self, videoId, platform, info:UploadInfo):
#         pass
       
# class mongo_video_dao(video_dao):
#     async def saveUploadInfo(self, videoId, platform, info:UploadInfo):
#         try:
#             video = await Video.get(videoId)
#             if not video:
#                 raise ValueError("Video không tồn tại")
                
#             video.uploaded[platform].insert(UploadInfo(
#                 videoId = info.videoId,
#                 uploadedAt = info.uploadedAt
#             ))
                
#             await Video.save()
#         except Exception as e: 
#             raise Exception(e)                        
    
    