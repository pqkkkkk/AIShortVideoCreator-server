from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import get_env_variable

import image.model.Image as Image
import video_script.models as video_script_models

async def init_db():
    data_source = get_env_variable("DATASOURCE_URL")
    database_name = get_env_variable("DATABASE_NAME")

    client = AsyncIOMotorClient(data_source)
    db = client.get_database(database_name)
    await init_beanie(database=db, document_models=[Image,video_script_models.Script,
                                                    video_script_models.Voice])