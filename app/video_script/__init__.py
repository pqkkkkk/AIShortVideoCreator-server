from .models import Script, Voice
from .video_script_api import router
from .public_video_script_service import public_video_script_service_v1

video_script_api = router
public_video_script_service = public_video_script_service_v1()