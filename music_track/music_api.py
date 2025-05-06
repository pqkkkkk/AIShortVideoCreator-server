from fastapi import APIRouter
router = APIRouter()
from .music_service import my_music_service
from .models import MusicTrack, CutMusicRequest
from typing import List
from fastapi.responses import JSONResponse
musicService = my_music_service() 

@router.get("/music_track/", response_model=List[MusicTrack])
async def getMusicTrack():
    return await musicService.getTrack()

@router.get("/music_track/{query}", response_model=List[MusicTrack])
async def search_songs(query:str):
    return await musicService.search_songs(keyword=query)

@router.post("/music_track/cut") 
async def cutMusic(request: CutMusicRequest):
    if(musicService.cutMusicTrack(        
        musicId=request.musicId, 
        startTime=request.startTime, 
        endTime=request.endTime
        )):
        return JSONResponse(
        status_code=200,
        content={
            "message": "Cắt và upload thành công!",
            "start": request.startTime,
            "end": request.endTime
        }
    )
    else:
        return JSONResponse(
            status_code=400,
            content={"message": "Có lỗi xảy ra khi cắt nhạc."}
        )