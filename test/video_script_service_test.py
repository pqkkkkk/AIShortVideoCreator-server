from video_script import public_video_script_service
import asyncio

async def test_get_video_metadata():
    script = "This is a sample script for testing."
    video_metadata = await public_video_script_service.GetVideoMetadata(script)
    print(video_metadata)

if __name__ == "__main__":
    asyncio.run(test_get_video_metadata())