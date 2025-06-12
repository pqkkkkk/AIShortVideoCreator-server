from video_script import public_video_script_service
import asyncio
from db import init_db

async def test_get_video_metadata():
    script = "This is a sample script for testing."
    video_metadata = await public_video_script_service.GetVideoMetadata(script)
    print(video_metadata)
async def test_prepare_voice():
    await init_db()
    await public_video_script_service.prepareVoice(lang='vi')

if __name__ == "__main__":
    asyncio.run(test_prepare_voice())