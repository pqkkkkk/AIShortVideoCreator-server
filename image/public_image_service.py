from abc import ABC, abstractmethod
class public_image_service(ABC):
    @abstractmethod
    async def upload_image(self, image: bytes) -> str:
        """
        Uploads an image and returns its URL.
        """
        pass

    @abstractmethod
    async def delete_image(self, url: str) -> None:
        """
        Deletes an image given its URL.
        """
        pass

    @abstractmethod
    async def get_image(self, url: str) -> bytes:
        """
        Retrieves an image given its URL.
        """
        pass

class public_image_service_v1(public_image_service):
    """
    Implementation of the public_image_service interface for version 1.
    """
    def upload_image(self, image: bytes) -> str:
        # Implementation for uploading an image
        pass

    def delete_image(self, url: str) -> None:
        # Implementation for deleting an image
        pass

    def get_image(self, url: str) -> bytes:
        # Implementation for retrieving an image
        pass