import cloudinary
import cloudinary.uploader, cloudinary.utils

from abc import ABC, abstractmethod

import cloudinary.uploader
from config import get_env_variable

class storage_service(ABC):
    @abstractmethod
    def uploadImage(self, file_content):
        pass
    @abstractmethod
    def uploadVideo(self, file_content):
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
              
    async def uploadVideo(self, file_content):
        response =  cloudinary.uploader.upload(file_content, resource_type="video")
        if response['secure_url'] is None:
            raise Exception("Upload failed, secure URL is None")
        
        return response['secure_url'], response['public_id']
    
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