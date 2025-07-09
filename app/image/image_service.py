from abc import ABC, abstractmethod
from app.external_service.ai import gemini_ai_service, ai_service_manager
from app.external_service.storage import storage_service
from fastapi import logger
from app.image.responses import GenerateImageResponse
from app.image.requests import GenerateImageRequest
from app.image.models import Image
from app.image.dao import image_dao

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
    @abstractmethod
    async def get_image_by_id(self, image_public_id: str) -> Image:
        """
        Retrieves an image by its public ID.
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
    
    async def get_image_by_id(self, image_public_id: str) -> Image:
        image = await image_dao.get_image_by_id(image_public_id)
        if not image:
            return None
        return image
    
    async def get_image_from_ai(self, request: GenerateImageRequest) -> GenerateImageResponse:
        """ Using Gemini AI to generate an image based on the request content """
        try:
            prompt = f"""
            Generate an image based with image description: {request.content}
            Ensure the image is high quality and relevant to the prompt.
            with style: {request.style}
            with image ratio: {request.image_ratio}
                            """
            
            image_data = await gemini_ai_service.generate_image_async(prompt)
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
        
    async def get_image_from_ai_v2(self, request: GenerateImageRequest) -> GenerateImageResponse:
        """Support for multiple AI models """
        try:
            prompt = f"""
            Generate an image based with image description: {request.content}
            Ensure the image is high quality and relevant to the prompt.
            with style: {request.style}
            with image ratio: {request.image_ratio}
                            """
            
            ai_service = ai_service_manager.get_ai_service(request.model)

            image_data = await ai_service.generate_image_async(prompt)
            if not image_data:
                raise ValueError("No image data returned from AI service")
            
            # Convert PIL Image to bytes if needed
            if hasattr(image_data, 'save'):  # Check if it's a PIL Image
                import io
                img_bytes = io.BytesIO()
                image_data.save(img_bytes, format='PNG')
                image_data = img_bytes.getvalue()
            
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