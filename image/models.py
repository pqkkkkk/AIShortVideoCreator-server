from beanie import Document

class Image(Document):
    id : str
    image_url: str
    topic : str
    public_id: str
    class Settings:
        collection = "image"

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "imageUrl": "https://example.com/image.jpg",
                "topic": "nature"
            }
        }