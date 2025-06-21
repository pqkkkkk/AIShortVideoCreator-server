import uvicorn
from fastapi import FastAPI
from app.image import image_api
from app.user import user_api
from app.music_track import music_api
from app.video_script import video_script_api
from app.video import video_api
from app.trending import trending_api
from app.db import init_db
from app.config import get_env_variable
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.logger import logger

@asynccontextmanager
async def lifespan(app:FastAPI):
    load_dotenv()
    data_source_url = get_env_variable("DATASOURCE_URL")
    print(f"Connecting to database at {data_source_url}")
    await init_db()
    yield
 
app = FastAPI(lifespan=lifespan)

app.include_router(image_api, prefix="/api/v1", tags=["image"])
app.include_router(user_api, prefix="/api/v1", tags=["user"])
app.include_router(music_api, prefix="/api/v1", tags=["music"])
app.include_router(video_script_api, prefix="/api/v1", tags=["video_script"])
app.include_router(video_api, prefix="/api/v1", tags=["video"])
app.include_router(trending_api, prefix="/api/v1", tags=["trending"])
# app.include_router(fb_api, prefix="/api/v1", tags=["facebook"])
# app.include_router(youtube_api, prefix="/api/v1", tags=["youtube"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)