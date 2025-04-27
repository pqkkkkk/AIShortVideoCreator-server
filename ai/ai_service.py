from abc import ABC, abstractmethod
import google.generativeai as genai
from config import load_dotenv
class ai_service(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass

    @abstractmethod
    def get_response_stream(self, prompt: str) -> str:
        pass
class gemini_service(ai_service):
    def __init__(self):
        self.api_key = load_dotenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel("gemini-2.0-flash")

    def get_response(self, prompt: str) -> str:
        response = self.client.generate_content(prompt)
        return response.text if response else None

    def get_response_stream(self, prompt: str) -> str:
        # Implement the logic to get a streaming response from the Gemini API
        pass