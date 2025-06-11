from video_script.models import VideoMetadata

class GetVideoMetadataResponse:
    message: str
    data: VideoMetadata | None

    def __init__(self, message: str, data: VideoMetadata | None):
        self.message = message
        self.data = data