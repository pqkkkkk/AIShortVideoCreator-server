from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import atexit

class UploadVideoInfo(BaseModel):
    video_public_id: str
    title: str
    videoUrl: str
    description: str
    keyword: str
    category: str
    privateStatus: str
    accessToken: str



class ThreadPoolManager:
    _instance = None
    _thread_pool: ThreadPoolExecutor = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, max_workers=10):
        if not self._thread_pool:
            self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    def get_pool(self):
        if not self._thread_pool:
            raise RuntimeError("Thread pool chưa init")
        return self._thread_pool

    def shutdown(self):
        if self._thread_pool:
            self._thread_pool.shutdown(wait=True)
            self._thread_pool = None

thread_pool_manager = ThreadPoolManager()
    