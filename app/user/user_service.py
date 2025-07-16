from abc import ABC, abstractmethod
from .dao import user_dao
from .models import User
from .result_status import SignInResult, SIgnUpResult
from .requests import SignInRequest, SignUpRequest
from .responses import SignInResponse, SignUpResponse, SignInToYoutubeResponse, GetYoutubeAccessTokenResponse
import traceback
import bcrypt
from app.auth import auth_service
from app.external_service.external_platform.Youtube import youtube_service, youtube_service_async
from typing import List, Dict
from app.video.models import Video, UploadInfo
from app.external_service.external_platform.Youtube.models import StatisticInfo
from datetime import datetime
from fastapi import status

class user_service(ABC):
    @abstractmethod
    async def sign_in(self, username: str, password: str) -> SignInResponse:
        pass
    def sign_in_to_youtube(self, redirect_uri: str) -> SignInToYoutubeResponse:
        pass
    def get_youtube_access_token(self, code: str, redirect_uri: str) -> GetYoutubeAccessTokenResponse:
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
                return SignInResponse(result=SignInResult.USER_NOT_FOUND,
                                    status_code = status.HTTP_404_NOT_FOUND,
                                    message= SignInResult.USER_NOT_FOUND.value,
                                    access_token="")
            elif not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return SignInResponse(result=SignInResult.WRONG_PASSWORD,
                                    status_code= status.HTTP_404_NOT_FOUND,
                                    message= SignInResult.WRONG_PASSWORD.value,
                                    access_token="")
            else:
                token = auth_service.create_access_token(data={"sub": user.username})
                return SignInResponse(result=SignInResult.SUCCESS,
                                    status_code= status.HTTP_200_OK,
                                    message= SignInResult.SUCCESS.value,
                                    username= user.username,
                                    access_token=token)
        except Exception as e:
            print(f"Error during sign in: {e}")
            return SignInResponse(result=SignInResult.UNKNOWN_ERROR,
                                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                                message= SignInResult.UNKNOWN_ERROR.value,
                                username="",
                                access_token="")
        
    def sign_in_to_youtube(self, redirect_uri: str) -> SignInToYoutubeResponse:
        try:
            auth_url = youtube_service_async.get_authorization_url(redirect_uri=redirect_uri)
            return SignInToYoutubeResponse(auth_url=auth_url, status_code=200)
        except Exception as e:
            print(f"Error during YouTube sign in: {e}")
            return SignInToYoutubeResponse(auth_url="", status_code=500)
    
    
    async def get_youtube_access_token(self, code: str, redirect_uri: str) -> GetYoutubeAccessTokenResponse:
        try:
            credentials = await youtube_service_async.get_credentials_from_code(code=code, redirect_uri=redirect_uri)
            if credentials:
                return GetYoutubeAccessTokenResponse(access_token=credentials.token, status_code=200)
            else:
                return GetYoutubeAccessTokenResponse(access_token="", status_code=400)
        except Exception as e:
            print(f"Error obtaining YouTube access token: {e}")
            return GetYoutubeAccessTokenResponse(access_token="", status_code=500)
        

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