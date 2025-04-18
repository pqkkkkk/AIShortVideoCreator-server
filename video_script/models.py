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
    id : str
    voiceUrl: str

    class Settings:
        collection = "voice"

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "voiceUrl": "https://example.com/image.jpg",
            }
        }