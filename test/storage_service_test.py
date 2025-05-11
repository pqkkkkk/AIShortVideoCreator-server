from storage import storage_service
import asyncio

async def test_upload_video():
    with open("test_video.mp4", "rb") as file:
        file_content = file.read()
    
    secure_url, public_id = await storage_service.uploadVideo(file_content)
    print(f"Secure URL: {secure_url}")
    print(f"Public ID: {public_id}")

if __name__ == "__main__":
    asyncio.run(test_upload_video())