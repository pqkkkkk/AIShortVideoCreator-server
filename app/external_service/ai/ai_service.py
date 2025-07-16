from abc import ABC, abstractmethod
from google import genai
from google.genai import types
from app.config import get_env_variable
from app.common import thread_pool_manager
import asyncio
from huggingface_hub import InferenceClient, login

class ai_service(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass
    @abstractmethod
    def generate_image(self, prompt: str):
        pass
    @abstractmethod
    async def get_response_async(self, prompt: str) -> str:
        pass
    @abstractmethod
    async def generate_image_async(self, prompt):
        pass

class gemini_service_v2(ai_service):
    """Service for interacting with the Gemini AI API. Asynchronous support yet."""
    def __init__(self):
        self.api_key = get_env_variable("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        
    def get_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text if response else None
    async def get_response_async(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            thread_pool_manager.get_pool(),
            self.get_response,
            prompt
        )

        return response
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
    async def generate_image_async(self, prompt):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            thread_pool_manager.get_pool(),
            self.generate_image,
            prompt
        )
        return response
    
class gemini_service(ai_service):
    """Service for interacting with the Gemini AI API. No asynchronous support yet."""
    def __init__(self):
        self.api_key = get_env_variable("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        
    def get_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text if response else None

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

class huggingface_service(ai_service):
    def __init__(self):
        self.access_token = get_env_variable("HUGGINGFACE_ACCESS_TOKEN")
        self.client = InferenceClient(token=self.access_token)
    
    def get_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="deepseek-ai/DeepSeek-V3-0324"
        )
        return response.choices[0].message.content if response else None
    
    async def get_response_async(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            thread_pool_manager.get_pool(),
            self.get_response,
            prompt
        )
        return response
    
    def generate_image(self, prompt):
        image = self.client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-dev",
            height=720,
            width=1280
        )

        if image:
            return image
        
        return None
    
    async def generate_image_async(self, prompt):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            thread_pool_manager.get_pool(),
            self.generate_image,
            prompt
        )
        return response

class ai_service_manager():
    def __init__(self):
        self.options = {
            "gemini": gemini_service_v2(),
            "huggingface": huggingface_service()
        }

    def get_ai_service(self, model: str) -> ai_service:
        ai_service = self.options.get(model)

        if not ai_service:
            raise ValueError(f"AI model '{model}' is not supported. Available models: {', '.join(self.options.keys())}")
        
        return ai_service