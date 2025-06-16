from abc import ABC, abstractmethod
from user.dao import user_dao
from user.models import User
from user.result_status import SignInResult, SIgnUpResult
from user.dto.requests import SignInRequest, SignUpRequest
from user.dto.responses import SignInResponse, SignUpResponse
import traceback
import bcrypt
from auth import auth_service
from externalPlatform.Youtube import YouTubeService
from typing import List, Dict
youtube_service = YouTubeService()
from video.models import Video, UploadInfo
from externalPlatform.Youtube.models import StatisticInfo
from datetime import datetime

class user_service(ABC):
    @abstractmethod
    async def sign_in(self, username: str, password: str) -> SignInResponse:
        pass
    async def sign_up(self, username: str, password: str) -> SIgnUpResult:
        pass
    async def statistic(self, userId):
        pass
class user_service_v1(user_service):
    async def sign_in(self, username: str, password: str) -> SignInResponse:
        try:
            user = await user_dao.get_user(username)

            if not user:
                return SignInResponse(status=SignInResult.USER_NOT_FOUND,
                                       message="User not found",
                                        access_token="")
            elif not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return SignInResponse(status=SignInResult.INVALID_PASSWORD,
                                       message="Invalid password",
                                       access_token="")
            else:
                token = auth_service.create_access_token(data={"sub": user.username})
                return SignInResponse(status=SignInResult.SUCCESS,
                                       message="Sign in successful",
                                       access_token=token)
        except Exception as e:
            print(f"Error during sign in: {e}")
            return SignInResponse(status=SignInResult.UNKNOWN_ERROR,
                                   message="An unknown error occurred",
                                   access_token="")
        
        
    async def sign_up(self, signUpRequest: SignUpRequest) -> SIgnUpResult:
        try:
            same_user = await user_dao.get_user(signUpRequest.username)
            if same_user:
                return SIgnUpResult.USERNAME_EXISTS
            
            if signUpRequest.password != signUpRequest.confirmPassword:
                return SIgnUpResult.PASSWORD_MISMATCH
            
            hashed_password = bcrypt.hashpw(signUpRequest.password.encode('utf-8'), bcrypt.gensalt())
            user = User(username=signUpRequest.username, password=hashed_password.decode('utf-8'))
            await user_dao.create_user(user)
            return SIgnUpResult.SUCCESS
        except Exception as e:
            print(f"Error during sign up: {e}")
            traceback.print_exc()
            return SIgnUpResult.UNKNOWN_ERROR
        
    async def statistic(self, userId) -> List[StatisticInfo]: 
        videos = await Video.find(Video.userId == userId).to_list()
        print(videos)
        statisticInfos = []
        for video in videos:
            upload_infos = video.uploaded.get("youtube")
            if not upload_infos:
                raise ValueError(f"Video {video.id} chưa có thông tin upload youtube")
            
            for upload_info in upload_infos:
                info = youtube_service.getStatisticInfo(upload_info.videoId)
                statisticInfos.append(info) 
                    
        return statisticInfos