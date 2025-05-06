from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import get_env_variable

from image import Image
import video_script.models as video_script_models
from music_track.models import MusicTrack
from text_to_speech.models import Voice
async def init_db():
    data_source = get_env_variable("DATASOURCE_URL")
    database_name = get_env_variable("DATABASE_NAME")

    client = AsyncIOMotorClient(data_source)
    db = client.get_database(database_name)
    await init_beanie(database=db, document_models=[Image,video_script_models.Script,
                                                    video_script_models.Voice, MusicTrack, Voice])