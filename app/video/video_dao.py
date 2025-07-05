from app.video.models import Video
from abc import ABC, abstractmethod
from .requests import VideoFilterObject
from .resposes import GetAllVideosResponse
from .models import UploadInfo
from beanie.operators import And, RegEx
import pymongo

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
    
    async def get_all_videos(self, user_id: str = None) -> list[Video]:
        """Retrieve all videos from the database."""
        if user_id:
            return await Video.find(Video.userId == user_id).to_list()
        return await Video.find_all().to_list()
    
    async def get_all_videos_count(self) -> int:
        """Retrieve the count of all videos in the database."""
        return await Video.find_all().count()
    
    async def get_uploaded_info_of_uploaded_videos(self):
        try:
            result = await Video.find_all().project(UploadInfo).to_list()
            return result
        except Exception as e:
            print(f"Error getting uploaded videos info: {e}")
            raise e
    

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
        
        # Convert order_direction string to sort format for Beanie
        sort_field = f"{'-' if filter_object.order_direction == 'desc' else ''}{filter_object.order_by}"
        
        videos = await  (query
                    .skip(skip)
                    .limit(filter_object.page_size)
                    .sort(sort_field)
                    .to_list())
        
        return videos, total_videos, total_pages
    
    async def get_video_count_statistics(self, start_date, end_date, user_id: str = None):
        """Retrieve video count statistics within a specified date range."""
        try:
            pipeline = [
                {
                    "$match": {
                        "created_at": {
                            "$gte": start_date,
                            "$lte": end_date
                        },
                        "userId": user_id if user_id else {"$exists": True} 
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "year": {"$year": "$created_at"},
                            "month": {"$month": "$created_at"},
                            "day": {"$dayOfMonth": "$created_at"}
                        },
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "date": {
                            "$dateFromParts": {
                                "year": "$_id.year",
                                "month": "$_id.month",
                                "day": "$_id.day"
                            }
                        },
                        "count": 1
                    }
                },
                {
                    "$sort": {"date": 1}
                }
            ]
            result = await Video.aggregate(pipeline).to_list()
            return result
        except Exception as e:
            print(f"Error getting video count statistics: {e}")
            raise e
        

        