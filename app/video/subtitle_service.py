from .models import VideoMetadata
from moviepy import TextClip
from moviepy.video.tools.subtitles import SubtitlesClip

from .text_service import font_path_map, FONT_FAMILY_DIRECTORY

def create_subtitles(scene_clips, video_metadata: VideoMetadata):
    subtitles = []
    cumulative_time = 0
    
    for idx, scene_clip in enumerate(scene_clips):
        text = video_metadata.scenes[idx].text
        start_time = cumulative_time
        end_time = cumulative_time + scene_clip.duration
        
        subtitles.append(((start_time, end_time), text))
        cumulative_time = end_time
    
    return subtitles

def make_text_clip_for_subtitles_custom(text: str):
    """Creates a custom text clip for subtitles using a specific font and style."""
    try:
        # Create a text clip with custom settings
        text_clip = TextClip(text=text,
                            font_size=24,
                            color='#ffffff',
                            font= font_path_map.get("Arial", f"{FONT_FAMILY_DIRECTORY}/arial.ttf"),
                            bg_color='#000000')
        
        return text_clip
    except Exception as e:
        print(f"Error creating custom text clip: {e}")
        return None

def create_subtitles_clip(subtitles):
    subtitles_clip = SubtitlesClip(subtitles=subtitles, make_textclip=make_text_clip_for_subtitles_custom)
    return subtitles_clip