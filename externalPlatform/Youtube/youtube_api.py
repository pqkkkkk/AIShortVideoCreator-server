from fastapi import APIRouter, HTTPException
router = APIRouter()
from .models import ExternalItem
from typing import List
from externalPlatform.Youtube.service import YouTubeService

# Oke, không có platforn vì tiktok kh search được
@router.get("/search/{keyword}", response_model=List[ExternalItem])
def search(keyword: str):
    return YouTubeService.getTopTrending(keyword=keyword)


# Upload đã oke, cần xác định lại tham số truyền vào từ UI là gì khi gọi
@router.post("/upload_video")
def upload_video(request: ExternalItem):
    try:
        response = YouTubeService.upload_video(
            file_path=request.file_path,
            title=request.title,
            description=request.description,
            tags=request.tags,
            category_id=request.category_id,
            privacy_status=request.privacy_status
        )
        return {"message": "Upload thành công", "video_id": response["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lấy statistic các video đã đăng => 