import cloudinary
import cloudinary.uploader, cloudinary.utils

from abc import ABC, abstractmethod

import cloudinary.uploader
from app.config import get_env_variable

class storage_service(ABC):
    @abstractmethod
    def uploadImage(self, file_content):
        pass
    @abstractmethod
    def updateImage(self,file_content, public_id):
        pass
    @abstractmethod
    def updateVideo(self,file_content, public_id):
        pass
    @abstractmethod
    def uploadVideo(self, file_content):
        pass
    @abstractmethod
    def uploadVideoWithReturningDuration(self, file_content):
        pass
    @abstractmethod
    def delete(self, public_id : str, is_video : bool) -> str:
        pass

class cloudinary_storage_service(storage_service):
    def __init__(self):
        cloudinary.config(
            cloud_name=get_env_variable("CLOUDINARY_CLOUD_NAME"),
            api_key=get_env_variable("CLOUDINARY_API_KEY"),
            api_secret=get_env_variable("CLOUDINARY_API_SECRET"),
        )

    async def uploadImage(self, file_content) -> str:
        response =  cloudinary.uploader.upload(file_content)
        print(response)
        
        if response['secure_url'] is None:
            raise Exception("Upload failed, secure URL is None")
        
        return response['secure_url'], response['public_id']
    
    async def updateImage(self, file_content, public_id):
        response = cloudinary.uploader.upload(file_content, public_id=public_id,
                                              invalidate=True,
                                               overwrite=True)
        return response['secure_url'], response['public_id']
         
    async def uploadVideo(self, file_content):
        response =  cloudinary.uploader.upload(file_content, resource_type="video")
        if response['secure_url'] is None:
            raise Exception("Upload failed, secure URL is None")
        
        return response['secure_url'], response['public_id']
    
    async def updateVideo(self, file_content, public_id):
        response = cloudinary.uploader.upload(file_content, public_id=public_id,
                                              invalidate=True,
                                               resource_type="video", overwrite=True)
        if response['secure_url'] is None:
            raise Exception("Update failed, secure URL is None")
        
        return response['secure_url'], response['public_id'], response['duration']
    async def uploadVideoWithReturningDuration(self, file_content):
        response =  cloudinary.uploader.upload(file_content, resource_type="video")
        if response['secure_url'] is None:
            raise Exception("Upload failed, secure URL is None")
        
        return response['secure_url'], response['public_id'], response['duration']
    
    async def delete(self, public_id: str, is_video: bool) -> str:
        if is_video:
            response =  cloudinary.uploader.destroy(public_id, resource_type="video")
            if response['result'] != 'ok':
                raise Exception("Delete failed, result is not ok")
            
            return response['result']
        else:
            response =  cloudinary.uploader.destroy(public_id)
            if response['result'] != 'ok':
                raise Exception("Delete failed, result is not ok")
            
            return response['result']