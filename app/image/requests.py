from pydantic import BaseModel

class GenerateImageRequest(BaseModel):
    content: str
    style: str = "modern"
    image_ratio: str = "16:9"
    model : str = "gemini"  # Default to Gemini AI model