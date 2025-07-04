from .models import TextAttachment
from moviepy import TextClip
from app.config import get_env_variable
FONT_FAMILY_DIRECTORY = get_env_variable("FONT_FAMILY_DIRECTORY")

font_path_map = {
    "Arial": f"{FONT_FAMILY_DIRECTORY}/arial.ttf",
    "Courier New": f"{FONT_FAMILY_DIRECTORY}/couri.ttf",
    "Times New Roman": f"{FONT_FAMILY_DIRECTORY}/times.ttf",
    "Verdana": f"{FONT_FAMILY_DIRECTORY}/verdana.ttf",
    "Georgia": f"{FONT_FAMILY_DIRECTORY}/georgia.ttf",
}

        
async def handle_each_text_attachment(text_attachment: TextAttachment,
                                             parent_clip_width: int, parent_clip_height: int):
        if text_attachment.text:
            try:
                font_path = font_path_map.get(text_attachment.font_family, f"{FONT_FAMILY_DIRECTORY}/arial.ttf")

                text_clip = TextClip(text = text_attachment.text,
                                     color = text_attachment.color_hex,
                                     font_size = text_attachment.font_size,
                                     duration = (text_attachment.end_time - text_attachment.start_time),
                                      font = font_path)
                text_clip.start = text_attachment.start_time
                text_clip.end = text_attachment.end_time
                
                left = (parent_clip_width - text_attachment.font_size * len(text_attachment.text)) * text_attachment.position.x
                top = (parent_clip_height - text_attachment.font_size) * text_attachment.position.y
                text_clip = text_clip.with_position((left,top))

                return text_clip
            except Exception as e:
                print(f"Error creating text clip: {e}")
                try: text_clip.close()
                except: pass
                return None

        return None

async def save_text_attachment_to_temp_file(text_clip: TextClip):
    if text_clip:
         with open("text_clip.mp4", "wb") as f:
            text_clip.write_videofile(f.name, codec='libx264', audio_codec='aac',fps = 24)
            text_clip.close()
            print("Text clip saved successfully.")
    else:
        print("No text clip to save.")
    return None
