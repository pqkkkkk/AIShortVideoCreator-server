from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import get_env_variable

from app.image import Image
from app.user import User
from app.video.models import Video
from app.music_track.models import MusicTrack
from app.video_script.models import Voice, Script
async def init_db():
    data_source = get_env_variable("DATASOURCE_CLOUD_URL")
    database_name = get_env_variable("DATABASE_CLOUD_NAME")

    client = AsyncIOMotorClient(data_source)
    db = client.get_database(database_name)

    await init_beanie(database=db, document_models=[Image, Script, User,
                                                    Video, Voice, MusicTrack])
