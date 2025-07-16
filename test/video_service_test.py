from app.video.video_service import video_service_v2
from app.video.requests import CreateVideoRequest
from app.video.resposes import CreateVideoResponse
from app.video.models import TextAttachment, Position, EmojiAttachment, VideoMetadata
from app.video.text_service import handle_each_text_attachment, save_text_attachment_to_temp_file
import asyncio
import os
from app.db import init_db
from app.common import thread_pool_manager
from dotenv import load_dotenv

load_dotenv()
video_service = video_service_v2()
thread_pool_manager.initialize()

async def get_corresponding_bg_music_temp_path_test():
    try:
        await init_db()
        bg_music_temp_path = await video_service.get_corresponding_bg_music_temp_path("iafl7dyzcdx8j7dtnlzk", None)
        print(f"Background music temp path: {bg_music_temp_path}")
        # Remove the temporary file if it exists
        if bg_music_temp_path and os.path.exists(bg_music_temp_path):
            os.remove(bg_music_temp_path)
            print(f"Temporary file {bg_music_temp_path} removed successfully.")
    except Exception as e:
        print(f"Error retrieving background music temp path: {e}")
async def test_handle_each_text_attachment():
    try:
        text_attachment = TextAttachment(
            text =  "Tôi là một đoạn văn bản mẫu để kiểm tra chức năng xử lý văn bản.",
            start_time =  0,
            end_time = 6,
            position = Position(x=0.5, y=0.5),
            font_size=  24,
            font_family = "Arial",
            color_hex =  "#FFFFFF"
        )
        text_clip = await handle_each_text_attachment(text_attachment=text_attachment,
                                                        parent_clip_height= 720,
                                                        parent_clip_width= 1280)
        if text_clip:
            await save_text_attachment_to_temp_file(text_clip=text_clip)

    except Exception as e:
        print(f"Error processing text attachment: {e}")
async def test_handle_each_emoji_attachment():
    try:
        emoji_attachment = EmojiAttachment(
            emoji= "",
            codepoint="1f600",  
            start_time = 2,
            end_time = 4,
            position = Position(x=0.5, y=0.5),
            size = 50
        )
        emoji_clip = await video_service.handle_each_emoji_attachment(emoji_attachment=emoji_attachment)
        if emoji_clip:
            emoji_clip.close()
        print("Emoji attachment processed successfully.")
    except Exception as e:
        print(f"Error processing emoji attachment: {e}")
async def test_create_video():
    try:
        await init_db()
        request = CreateVideoRequest(
            title="Sample Video",
            userId="user123",
            videoMetadata= VideoMetadata(
                scenes=[
                    {
                        "scene_id": 1,
                        "start_time": 0,
                        "end_time": 5,
                        "text": "This is a sample scene",
                        "bg_image_public_id": "",
                        "bg_music_public_id": "",
                        "bg_image_file_index": -1,
                        "bg_music_file_index": -1
                    },{
                        "scene_id": 2,
                        "start_time": 5,
                        "end_time": 10,
                        "text": "This is another sample scene",
                        "bg_image_public_id": "",
                        "bg_music_public_id": "",
                        "bg_image_file_index": -1,
                        "bg_music_file_index": -1
                    }
                ]
            )
        )
        response = await video_service.create_video(request,[],[])

        if response.secure_url != "":
            print("Video created successfully")
            print(f"Video path: {response.secure_url}")
            print(f"Video ID: {response.public_id}")
    except Exception as e:
        print(f"Error creating video: {e}")
if __name__ == "__main__":
    asyncio.run(test_create_video())