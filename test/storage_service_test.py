from storage import storage_service
import asyncio

async def test_upload_video():
    with open("test_video.mp4", "rb") as file:
        file_content = file.read()
    
    secure_url, public_id = await storage_service.uploadVideo(file_content)
    print(f"Secure URL: {secure_url}")
    print(f"Public ID: {public_id}")
async def test_upload_image():
    secure_url, public_id = await storage_service.uploadImage("sample.jpg")
    print(f"Secure URL: {secure_url}")
    print(f"Public ID: {public_id}")
async def test_update_image(public_id: str):
    secure_url, updated_public_id = await storage_service.updateImage("sample2.jpg", public_id)
    print(f"Updated Secure URL: {secure_url}")
    print(f"Updated Public ID: {updated_public_id}")
if __name__ == "__main__":
    asyncio.run(test_update_image("laxzz2klwgntd4mk6ipe"))