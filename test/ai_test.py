from ai import ai_service
import asyncio

def test_generate_image():
    prompt = "A beautiful sunset over the mountains"
    ai_service.generate_image(prompt=prompt)

if __name__ == "__main__":
    test_generate_image()