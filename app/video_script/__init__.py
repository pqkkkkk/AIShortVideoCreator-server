from .models import Script, Voice
from .video_script_api import router
from .video_script_api_v2 import router as router_v2
from .public_video_script_service import public_video_script_service_v1

video_script_api = router
video_script_api_v2 = router_v2
public_video_script_service = public_video_script_service_v1()