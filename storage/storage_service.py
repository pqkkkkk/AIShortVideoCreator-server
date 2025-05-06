import cloudinary
import cloudinary.uploader, cloudinary.utils

from abc import ABC, abstractmethod

class storage_service(ABC):
    @abstractmethod
    def upload(self, file_path: str, file_name: str) -> str:
        pass
    @abstractmethod
    def download(self, file_name: str, destination_path: str) -> None:
        pass
    @abstractmethod
    def delete(self, file_name: str) -> None:
        pass
    @abstractmethod
    def get_media(self, fil_url: str) -> str:
        pass

class cloudinary_storage_service(storage_service):
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )

    def upload(self, file_path: str, file_name: str) -> str:
        response = cloudinary.uploader.upload(file_path, public_id=file_name, resource_type="video")
        return response['secure_url']

    def download(self, file_name: str, destination_path: str) -> None:
        cloudinary.utils.download(file_name, destination_path)

    def delete(self, file_name: str) -> None:
        cloudinary.uploader.destroy(file_name)

    def get_media(self, fil_url: str) -> str:
        return cloudinary.CloudinaryImage(fil_url).build_url()