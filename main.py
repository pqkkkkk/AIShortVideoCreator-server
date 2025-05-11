import uvicorn
from fastapi import FastAPI
from image import image_api
from user import user_api
from music_track import music_api
from video_script import video_script_api
from video import video_api
from db import init_db 
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
 
app = FastAPI(lifespan=lifespan)

app.include_router(image_api, prefix="/api/v1", tags=["image"])
app.include_router(user_api, prefix="/api/v1", tags=["user"])
app.include_router(music_api, prefix="/api/v1", tags=["music"])
app.include_router(video_script_api, prefix="/api/v1", tags=["video_script"])
app.include_router(video_api, prefix="/api/v1", tags=["video"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)