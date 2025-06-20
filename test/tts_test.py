from text_to_speech import tts_service
import asyncio
from storage import storage_service

async def main():
    temp_file_path = await tts_service.text_to_speech(
        text="Xin chào, đây là một bài kiểm tra.",
        voiceId="vi-VN-NamMinhNeural",
        lang="vi"
    )
    print(f"Audio saved to: {temp_file_path}")

    await storage_service.uploadVideo(temp_file_path)
async def list_voices():
    voices = await tts_service.list_voice(lang='en-US')
    for voice in voices:
        print(f"ShortName : {voice['ShortName']}, Gender:{voice['Gender']}")
if __name__ == "__main__":
    asyncio.run(list_voices())