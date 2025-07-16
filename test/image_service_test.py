from app.image import public_image_service
from app.image.responses import GenerateImageResponse
from app.image.requests import GenerateImageRequest
import asyncio

async def test_get_image_from_ai():
    prompt = "A beautiful sunset over the mountains"
    image_url = await public_image_service.get_image_from_ai(prompt=prompt)
    print(f"Generated image URL: {image_url}")
async def test_get_image_from_ai_v2():
    prompt = "A futuristic city skyline at night"
    request = GenerateImageRequest(content=prompt, model="huggingface")
    response = await public_image_service.get_image_from_ai_v2(request=request)

    if response.status_code == 200:
        print(f"Generated image URL: {response.image_url}")
    else:
        print(f"Failed to generate image: {response.message}")
if __name__ == "__main__":
    asyncio.run(test_get_image_from_ai_v2())