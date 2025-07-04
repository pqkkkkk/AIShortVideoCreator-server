from fastapi import APIRouter, HTTPException, Query
router = APIRouter()
from .service import FacebookService
from .models import UploadRequest
fb_service = FacebookService()

# # đã test, oke nhưng fb kh cấp quyền
@router.get("/facebook/login-url")
def get_facebook_login_url(redirect_uri: str = Query(..., description="URL to redirect after login")):
    return {"auth_url": fb_service.get_login_url(redirect_uri)}

# đã test, fb kh cấp quyền
@router.post("/facebook/upload")
def upload_video(req: UploadRequest):
    try:
        result = fb_service.uploadVideo(req.videoId, req.access_token)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# đã test, oke nhưng fb kh cấp quyền
@router.get("/facebook/callback")
def exchange_token(code: str, redirect_uri: str):
    try:
        access_token = fb_service.exchangeCodeForAccessToken(code, redirect_uri)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
