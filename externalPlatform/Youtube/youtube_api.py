from fastapi import APIRouter, HTTPException, Query, Header
from .models import ExternalItem, uploadVideo
from typing import List
from .service import YouTubeService
import traceback

youtube_service = YouTubeService()
router = APIRouter()

# Oke, không có platforn vì tiktok kh search được
@router.get("/search/{keyword}", response_model=List[ExternalItem])
def search(keyword: str):
    return youtube_service.getTopTrending(keyword=keyword)

@router.get("/youtube/login")
def login_with_youtube(redirect_uri):
    auth_url = youtube_service.get_authorization_url(redirect_uri)
    return {"auth_url": auth_url}

@router.get("/youtube/callback")
def youtube_callback(redirect_uri: str , code: str = Query(...)):
    credentials = youtube_service.get_credentials_from_code(code, redirect_uri)
    # (Lưu access_token vào DB hoặc cache session)
    return {"access_token": credentials.token}


# Upload đã oke, cần xác định lại tham số truyền vào từ UI là gì khi gọi
@router.post("/upload_video")
async def upload_video(request: uploadVideo, youtube_token: str = Header(..., alias="youtube-token")):
    try:
        response = await youtube_service.upload_video(request, youtube_token)
        return {"id": response["id"]}
    except Exception as e:
        print("Lỗi chi tiết:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Lấy statistic các video đã đăng => 