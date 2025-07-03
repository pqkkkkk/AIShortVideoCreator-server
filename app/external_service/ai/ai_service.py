from abc import ABC, abstractmethod
from google import genai
from google.genai import types
from app.config import get_env_variable
from app.common import thread_pool_manager
import asyncio

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

class gemini_service_v2():
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

# class flux_service(ai_service):
#     def __init__(self):
#         login(token=get_env_variable("HUGGINGFACE_ACCESS_TOKEN"))
#         self.pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev",
#                                                   torch_dtype=torch.bfloat16)
#         self.pipe.enable_model_cpu_offload()

#     def get_response(self, prompt):
#         return super().get_response(prompt)
#     def get_response_stream(self, prompt):
#         return super().get_response_stream(prompt)
#     def generate_image(self, prompt):
#         image = self.pipe(
#             prompt,
#             height=1024,
#             width=1024,
#             guidance_scale=3.5,
#             num_inference_steps=50,
#             max_sequence_length=512,
#             generator=torch.Generator("cpu").manual_seed(0)
#         ).images[0]    

#         image.save("flux-dev.png")

#         return image

# class flan_t5_base_service(ai_service):
#     def __init__(self):
#         self.model_name = "google/flan-t5-base"
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
#         self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
#     def get_response(self, prompt):
#         inputs = self.tokenizer(prompt, return_tensors="pt")

#         outputs = self.model.generate(**inputs, max_length=256, do_sample=False, num_beams=5)
#         response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

#         return response
#     def get_response_stream(self, prompt):
#         return super().get_response_stream(prompt)
#     def generate_image(self, prompt):
#         return super().generate_image(prompt)
