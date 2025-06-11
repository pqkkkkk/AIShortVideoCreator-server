import os
import random
import time
from typing import List, Dict, Any
import requests
import httplib2
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from abc import ABC, abstractmethod
from config import get_env_variable
from externalPlatform.Youtube.models import ExternalItem

load_dotenv()

class PlatformService(ABC):
    @abstractmethod
    def getTopTrending(self, keyword: str) -> List[ExternalItem]:
        pass
    def upload_video(self, file_path: str, title: str, description: str,
                     tags: List[str], category_id: str,
                     privacy_status: str = "private") -> Dict[str, Any]:
        pass

class YouTubeService(PlatformService):
    def __init__(self):
        self.api_key = get_env_variable('YOUTUBE_API_KEY')
        self.client_secret_file = os.path.join(os.path.dirname(__file__), "client_secrets.json")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def getTopTrending(self, keyword: str) -> List[ExternalItem]:
        request = self.youtube.search().list(
            part="id,snippet",
            maxResults=10,
            q=keyword,
            type="video",
            order="viewCount"
        )
        response = request.execute()

        result = []
        video_ids = []
        
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            video_ids.append(video_id)
        
        stats_response = self.youtube.videos().list(
                part="statistics",
                id=",".join(video_ids)
            ).execute()
        stats_map = {item["id"]: item.get("statistics", {}) for item in stats_response.get("items", [])}

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            thumbnail = snippet["thumbnails"].get("high", {})
            statistics = stats_map.get(video_id, {})
            view_count = int(statistics.get("viewCount", 0))

            result.append(ExternalItem(
                id=video_id,
                title=snippet["title"],
                description=snippet["description"],
                thumbnailUrl=thumbnail.get("url", ""),
                thumbnailHeight=thumbnail.get("height", 0),
                thumbnailWidth=thumbnail.get("width", 0),
                viewCount=view_count
            ))
        
            
        

        return result

    # authentication user youtube account for get credentials
    def get_authenticated_service(self):
        flow = flow_from_clientsecrets(
            self.client_secret_file,
            scope=["https://www.googleapis.com/auth/youtube.upload"]
        )
        storage = Storage("youtube-oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build('youtube', 'v3', http=credentials.authorize(httplib2.Http()))

    def upload_video(self, file_path: str, title: str, description: str,
                     tags: List[str], category_id: str,
                     privacy_status: str ) -> Dict[str, Any]:
        youtube = self.get_authenticated_service()

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }

        insert_request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )

        print(f"Đang upload video: {title}")
        response = None
        retry = 0
        max_retries = 5

        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if status:
                    print(f"Đã upload {int(status.progress() * 100)}%")
            except Exception as e:
                print(f"Lỗi khi upload: {e}")
                retry += 1
                if retry > max_retries:
                    raise Exception("Vượt quá số lần thử lại.")
                sleep_seconds = random.random() * (2 ** retry)
                print(f"Đợi {sleep_seconds:.1f}s trước khi thử lại...")
                time.sleep(sleep_seconds)

        print(f"Upload hoàn tất! Video ID: {response['id']}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return response

    def download_file(url, local_path):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("download success")

    # Lấy thống kê gồm: số lượng video đã đăng
    # Tạo 1 bảng video Upload trong database để lưu thông tin các video 
    # đã upload lên các nền tảng
    # (khi upload thì upload xong thì lấy videoID trả ra từ platform 
    # (videoID này là ID của video trên platform, không phải ID của video) 
    # và insert vào bảng)
    # video_uploads (platform_video_ID, videoID của video, platform, uploaded_at)
    
    # cần access_token đăng nhập vào youtube để lấy statistic của 1 video của ngừoi dùng
    # => xử lý tương tự facebook
    