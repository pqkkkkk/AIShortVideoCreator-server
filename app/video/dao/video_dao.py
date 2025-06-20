from app.video.models import Video
from abc import ABC, abstractmethod

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