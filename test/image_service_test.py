from app.image import public_image_service
import asyncio

async def test_get_image_from_ai():
    prompt = "A beautiful sunset over the mountains"
    image_url = await public_image_service.get_image_from_ai(prompt=prompt)
    print(f"Generated image URL: {image_url}")

if __name__ == "__main__":
    asyncio.run(test_get_image_from_ai())