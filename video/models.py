from beanie import Document

class Video(Document):
    id: str
    title: str
    #topic: str
    status: str
    video_url: str
    #created_at: str
    userId: str

    class Settings:
        collection = "video"
