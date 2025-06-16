from abc import ABC, abstractmethod
from google import genai
from google.genai import types
from PIL import Image
from config import get_env_variable
from io import BytesIO

class ai_service(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass
    @abstractmethod
    def get_response_stream(self, prompt: str) -> str:
        pass
    @abstractmethod
    def generate_image(self, prompt: str):
        pass
class gemini_service(ai_service):
    def __init__(self):
        self.api_key = get_env_variable("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        
    def get_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text if response else None

    def get_response_stream(self, prompt: str) -> str:
        # Implement the logic to get a streaming response from the Gemini API
        pass
    def generate_image(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE', 'TEXT']
            )
        )
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                return part.inline_data.data
        return None