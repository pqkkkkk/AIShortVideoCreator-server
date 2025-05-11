from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import get_env_variable

from image import Image
from user import User
from video.models import Video
from music_track.models import MusicTrack
from video_script.models import Voice, Script
async def init_db():
    data_source = get_env_variable("DATASOURCE_URL")
    database_name = get_env_variable("DATABASE_NAME")

    client = AsyncIOMotorClient(data_source)
    db = client.get_database(database_name)

    await init_beanie(database=db, document_models=[Image, Script, User,
                                                    Video, Voice, MusicTrack])
