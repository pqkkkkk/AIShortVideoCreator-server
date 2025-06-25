from app.video.models import Video
from abc import ABC, abstractmethod
from .requests import VideoFilterObject
from .resposes import GetAllVideosResponse
from beanie.operators import And, RegEx

class video_dao(ABC):
    @abstractmethod
    async def insert_video(self, video: Video) -> Video:
        """Insert a new video into the database."""
        pass
    @abstractmethod
    async def get_video_by_id(self, id: str) -> Video:
        """Retrieve a video by its ID."""
        pass
    @abstractmethod
    async def get_all_videos(self) -> list[Video]:
        """Retrieve all videos from the database."""
        pass
    @abstractmethod
    async def update_video(self, video: Video) -> Video:
        """Update an existing video in the database."""
        pass

class video_dao_v1(video_dao):
    async def insert_video(self, video: Video) -> Video:
        """Insert a new video into the database."""
        return await Video.insert_one(video)
    
    async def update_video(self, video):
        return await Video.find_one(Video.public_id == video.public_id).replace_one(video)
    
    async def get_video_by_id(self, id: str) -> Video:
        """Retrieve a video by its ID."""
        return await Video.find_one(Video.public_id == id)

    async def get_all_videos(self) -> list[Video]:
        """Retrieve all videos from the database."""
        return await Video.find_all().to_list()
    async def get_all_videos_paginated(self, filter_object: VideoFilterObject) -> GetAllVideosResponse:
        """Retrieve all videos from the database with pagination."""
        conditions = []
        if filter_object.title and filter_object.title != "":
            conditions.append(RegEx(field=Video.title, pattern=filter_object.title, options="i"))
        if filter_object.user_id and filter_object.user_id != "":
            conditions.append(Video.userId == filter_object.user_id)
        if filter_object.status and filter_object.status != "":
            conditions.append(Video.status == filter_object.status)
        condition = And(*conditions) if conditions else None

        if condition:
            query = Video.find(condition)
        else:
            query = Video.find_all()

        total_videos = await query.count()
        total_pages = (total_videos // filter_object.page_size) + (1 if total_videos % filter_object.page_size > 0 else 0)
        skip = (filter_object.current_page_number - 1) * filter_object.page_size
        
        videos = await  (query
                    .skip(skip)
                    .limit(filter_object.page_size)
                    .to_list())
        
        return GetAllVideosResponse(
            items=videos,
            total_videos=total_videos,
            current_page_number=filter_object.current_page_number,
            total_pages=total_pages,
            page_size=filter_object.page_size,
            message="Videos retrieved successfully",
            status_code=200
        )
        

        