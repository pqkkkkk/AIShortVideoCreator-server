from music_track import music_service
from core.db import init_db
import os
import asyncio

async def test_prepare_music_track():
    await init_db()
    await music_service.prepareMusicTrack()

if __name__ == "__main__":
    asyncio.run(test_prepare_music_track())