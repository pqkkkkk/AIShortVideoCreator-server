from abc import ABC, abstractmethod
from ai import ai_service
from storage import storage_service
class image_service(ABC):
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
    @abstractmethod
    async def get_image_from_ai(self, prompt: str) -> str:
        """
        Generates an image based on a prompt using AI.
        """
        pass
class image_service_v1(image_service):
    """
    Implementation of the image_service interface for version 1.
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
    async def get_image_from_ai(self, prompt: str) -> str:
        try:
            image_data = ai_service.generate_image(prompt)
            if not image_data:
                raise ValueError("No image data returned from AI service")
            
            image_url,public_id = await storage_service.uploadImage(image_data)
            if not image_url:
                raise ValueError("Image upload failed, no URL returned")
            
            return image_url
        except Exception as e:
            raise Exception(f"Error generating image from AI service: {str(e)}")