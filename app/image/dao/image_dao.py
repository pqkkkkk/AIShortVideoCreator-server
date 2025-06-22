from abc import ABC, abstractmethod
from app.image.models import Image
class image_dao(ABC):
    async def get_images(self):
        pass
    async def insert_image(self, image_data):
        pass
    async def get_image_by_id(self, image_public_id):
        pass

class mongo_image_dao(image_dao):
    async def insert_image(self, image_data):
        await Image.insert_one(image_data)
    async def get_image_by_id(self, image_public_id):
        return await Image.find_one({"public_id": image_public_id})