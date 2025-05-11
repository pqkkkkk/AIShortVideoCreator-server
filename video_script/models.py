from beanie import Document

class Script(Document):
    id : str
    content: str
    class Settings:
        collection = "image"
    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "content": "https://example.com/image.jpg",
            }
        }
    
class Voice(Document):
    type: str
    voiceUrl: str
    shortName: str
    publicId: str
    class Settings:
        name = "voice"