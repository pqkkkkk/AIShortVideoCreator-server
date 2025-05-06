from storage.storage_service import cloudinary_storage_service
import os

cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

storage_service = cloudinary_storage_service(cloud_name, api_key, api_secret)