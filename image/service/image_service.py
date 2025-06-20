from abc import ABC, abstractmethod
from ai import ai_service
from storage import storage_service
from fastapi import logger
from image.dto.responses import GenerateImageResponse
from image.dto.requests import GenerateImageRequest
from image.models import Image
from image.dao import image_dao

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
    async def insert_image_data(self, image_data: Image):
        pass
    @abstractmethod
    async def get_image_from_ai(self, request: GenerateImageRequest) -> GenerateImageResponse:
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
    async def insert_image_data(self, image_data):
        await image_dao.insert_image(image_data)

    async def get_image_from_ai(self, request: GenerateImageRequest) -> GenerateImageResponse:
        try:
            prompt = f"""
            Generate an image based on the following prompt: {request.content}
            Ensure the image is high quality and relevant to the prompt.
            with width: {request.width}, height: {request.height}
                            """
            
            image_data = ai_service.generate_image(prompt)
            if not image_data:
                raise ValueError("No image data returned from AI service")
            
            image_url,public_id = await storage_service.uploadImage(image_data)
            if not image_url:
                raise ValueError("Image upload failed, no URL returned")
            
            await self.insert_image_data(
                Image(
                    public_id=public_id,
                    image_url=image_url,
                )
            )
            return GenerateImageResponse(
                image_url=image_url,
                public_id=public_id,
                status_code=200,
                message="Image generated successfully"
            )
        except Exception as e:
            logger.logger.error(f"Error generating image by AI: {str(e)}")
            return GenerateImageResponse(
                image_url="",
                public_id="",
                status_code=500,
                message=f"Error generating image: {str(e)}"
            )