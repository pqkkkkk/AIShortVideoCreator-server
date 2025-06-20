from beanie import Document

class Image(Document):
    image_url: str
    public_id: str
    class Settings:
        name = "Image"

    class Config:
        schema_extra = {
            "example": {
                "image_url": "https://example.com/image.jpg",
                "public_id": "12345abcde"
            }
        }