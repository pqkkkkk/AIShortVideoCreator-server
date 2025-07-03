import uvicorn
from fastapi import FastAPI, Depends
from app.common import thread_pool_manager
from app.auth.auth_service import validate_token_dependency
from app.image import image_api
from app.user import user_api
from app.music_track import music_api
from app.video_script import video_script_api
from app.video import video_api, video_api_v2
from app.trending import trending_api
from app.db import init_db
from app.config import get_env_variable
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app:FastAPI):
    load_dotenv()
    await init_db()

    thread_pool_manager.initialize(max_workers=10)

    yield

    thread_pool_manager.shutdown()
 
app = FastAPI(lifespan=lifespan)

app.include_router(image_api, prefix="/api/v1", tags=["image"], dependencies=[Depends(validate_token_dependency)])
app.include_router(user_api, prefix="/api/v1", tags=["user"])
app.include_router(music_api, prefix="/api/v1", tags=["music"], dependencies=[Depends(validate_token_dependency)])
app.include_router(video_script_api, prefix="/api/v1", tags=["video_script"], dependencies=[Depends(validate_token_dependency)])
app.include_router(video_api, prefix="/api/v1", tags=["video"], dependencies=[Depends(validate_token_dependency)])
app.include_router(video_api_v2, prefix="/api/v2", tags=["video_v2"], dependencies=[Depends(validate_token_dependency)])
app.include_router(trending_api, prefix="/api/v1", tags=["trending"], dependencies=[Depends(validate_token_dependency)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)