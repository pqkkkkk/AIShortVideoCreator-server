import os
import random
import time
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from abc import ABC, abstractmethod
from app.config import get_env_variable
from .models import ExternalItem, uploadVideo, StatisticInfo
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
#from .dao import videoDao
from datetime import datetime
from tempfile import NamedTemporaryFile
from app.common import UploadVideoInfo

load_dotenv()

class PlatformService(ABC):
    @abstractmethod
    def getTopTrending(self, keyword: str) -> List[ExternalItem]:
        pass
    async def upload_video(self ,upload_video: uploadVideo, youtube_token: str ) -> Dict[str, Any]:
        pass
    def getStatisticInfo(self, videoId):
        pass
        
class YouTubeService(PlatformService):
    def __init__(self):
        self.api_key = get_env_variable('YOUTUBE_API_KEY')
        #self.client_secret_file = os.path.join(os.path.dirname(__file__), "client_secrets.json")
        self.client_secret_file = get_env_variable('YOUTUBE_CLIENT_SECRET_JSON_FILE_PATH')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        #self.dao = videoDao

    def getTopTrending(self, keyword: str) -> List[ExternalItem]:
        request = self.youtube.search().list(
            part="id,snippet",
            maxResults=10,
            q=keyword,
            type="video",
            order="relevance",
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
    async def upload_video(self ,upload_video: uploadVideo, youtube_token: str ) -> Dict[str, Any]:
        # Tạo credentials từ access_token
        credentials = Credentials(token=youtube_token)
        self.youtube = build("youtube", "v3", credentials=credentials)
        body = {
            'snippet': {
                'title': upload_video.title,
                'description': upload_video.description,
                'tags': upload_video.keyword.split(',') if upload_video.keyword else [],
                'categoryId': upload_video.category
            },
            'status': {
                'privacyStatus': upload_video.privateStatus
            }
        }
        video_temp_path = await self.get_video_temp_path(upload_video.videoUrl)
        media = MediaFileUpload(video_temp_path, chunksize=-1, resumable=True)
        try: 
            insert_request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        except Exception as e:
            print(f"Lỗi khi upload: {e}")

        print(f"Đang upload video: {upload_video.title}")
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
        
        # if os.path.exists(video_temp_path):
        #     os.remove(video_temp_path)

        # Lưu giá trị videoId trên youtube vào db
        # uploadInfo = UploadInfo(videoId=response['id'], uploadedAt=datetime.now())
        # await self.dao.saveUploadInfo(self, upload_video.id , "youtube", uploadInfo)
        return response
    

    async def upload_video_immediate(self, request: UploadVideoInfo):
        try:
            # Tạo credentials từ access_token
            credentials = Credentials(token=request.accessToken)
            self.youtube = build("youtube", "v3", credentials=credentials)
            body = {
                'snippet': {
                    'title': request.title,
                    'description': request.description,
                    'tags': request.keyword.split(',') if request.keyword else [],
                    'categoryId': request.category
                },
                'status': {
                    'privacyStatus': request.privateStatus
                }
            }
            video_temp_path = await self.get_video_temp_path(request.videoUrl)
            media = MediaFileUpload(video_temp_path, chunksize=-1, resumable=True)

            insert_request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            print(f"Đang upload video: {request.title}")

            response = insert_request.execute()
            if response:
                print(f"Upload hoàn tất! Video ID: {response['id']}")
            else:
                raise Exception("Không thể upload video, không có phản hồi từ YouTube.")
            
            # if os.path.exists(video_temp_path):
            #     os.remove(video_temp_path)

            return response
        except Exception as e:
            print(f"Lỗi khi upload video lên youtube: {e}")
            raise Exception("Lỗi khi upload video lên YouTube.") from e


    async def get_video_temp_path(self, secure_url: str) -> str:
        if secure_url:
            response = requests.get(secure_url)
            if response.status_code == 200:
                temp_video = NamedTemporaryFile(delete=False, suffix=".mp4")
                temp_video.write(response.content)
                temp_video.close()
                return temp_video.name
        return None
    
    def get_authorization_url(self,redirect_uri: str):
        flow = Flow.from_client_secrets_file(
            self.client_secret_file,
            scopes=['https://www.googleapis.com/auth/youtube.upload'],
            redirect_uri = redirect_uri
        )
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
        )
        return auth_url

    def get_credentials_from_code(self, code: str, redirect_uri: str):
        flow = Flow.from_client_secrets_file(
            self.client_secret_file,
            scopes=['https://www.googleapis.com/auth/youtube.upload'],
            redirect_uri=redirect_uri
        )
        flow.fetch_token(code=code)
        self.youtube = build("youtube", "v3", credentials=flow.credentials)
        return flow.credentials
    
    def getStatisticInfo(self, videoId) -> StatisticInfo:
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = self.youtube.videos().list(
            part="statistics",
            id=videoId
        )
        response = request.execute()
        print("YouTube API response:", response)
        
        items = response.get('items', [])
        if items:
            stats = items[0].get('statistics', {})
            return StatisticInfo(
                id=videoId,
                viewCount=int(stats.get("viewCount", 0)),
                likeCount=int(stats.get("likeCount", 0)),
                commentCount=int(stats.get("commentCount", 0)),
                favoriteCount=int(stats.get("favoriteCount", 0))
            )
        else:
            return StatisticInfo(id=videoId)

    def getStatisticsInfoBatch(self, videoIds: List[str]) -> Dict[str, dict]:
        """ Get statistics for a batch of video IDs.
        Args:
            videoIds (List[str]): List of YouTube video IDs.
        Returns:
            List[dict]: A list of dictionaries containing statistics for each video.
        Example:
            [
                {
                    "platform": "youtube",
                    "video_id": "abc123",
                    "view_count": 1000,
                    "like_count": 100,
                    "favorite_count": 50,
                    "comment_count": 10
                },
                ...
            ]
        """
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            request = self.youtube.videos().list(
                part="statistics",
                id=",".join(videoIds)
            )
            response = request.execute()
            
            stats_list = []
            for item in response.get('items', []):
                video_id = item['id']
                stats = item.get('statistics', {})
                stats_list.append({
                    "platform": "youtube",
                    "video_id": video_id,
                    "view_count": int(stats.get("viewCount", 0)),
                    "like_count": int(stats.get("likeCount", 0)),
                    "favorite_count": int(stats.get("favoriteCount", 0)),
                    "comment_count": int(stats.get("commentCount", 0))
                })
            
            return stats_list    
        except Exception as e:
            return None        
        
    