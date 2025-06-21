from fastapi import APIRouter, Depends, HTTPException, Query
from .requests import SignInRequest, SignUpRequest
from .responses import SignInResponse, SignUpResponse, SignInToYoutubeResponse, GetYoutubeAccessTokenResponse
from .user_service import user_service_v1
from .result_status import SignInResult, SIgnUpResult
from typing import List
from app.external_service.external_platform.Youtube.models import StatisticInfo

user_service = user_service_v1()
api_router = APIRouter()

@api_router.post("/user/signin", response_model=SignInResponse)
async def sign_in(signInRequest : SignInRequest):
    sign_in_response = await user_service.sign_in(signInRequest.username, signInRequest.password)

    if sign_in_response.status == SignInResult.SUCCESS:
        return sign_in_response
    else:
        raise HTTPException(status_code=400, detail=sign_in_response.status.value)


@api_router.get("/user/signin/to-youtube", response_model=SignInToYoutubeResponse)
async def sign_in_to_youtube(redirect_uri:  str = Query(..., description="The redirect URI for YouTube OAuth")):
    response = user_service.sign_in_to_youtube(redirect_uri=redirect_uri)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to get YouTube authorization URL")
    
    return response

@api_router.get("/user/signin/to-youtube/access-token", response_model=GetYoutubeAccessTokenResponse)
async def get_youtube_accesstoken(code: str = Query(..., description="The authorization code from YouTube OAuth"),
                                   redirect_uri: str = Query(..., description="The redirect URI for YouTube OAuth")
                                ):
    try:
        response = user_service.get_youtube_access_token(code=code,redirect_uri=redirect_uri)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to obtain YouTube access token")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to obtain YouTube credentials: {str(e)}")

@api_router.post("/user/signup", response_model=SignUpResponse)
async def sign_up(signUpRequest: SignUpRequest):
    sign_up_result = await user_service.sign_up(signUpRequest=signUpRequest)

    if sign_up_result == SIgnUpResult.SUCCESS:
        return SignUpResponse(message="Sign up successful", status=sign_up_result, username=signUpRequest.username)
    elif sign_up_result == SIgnUpResult.UNKNOWN_ERROR:
        raise HTTPException(status_code=400, detail=sign_up_result.value)
    else:
        return SignUpResponse(message=sign_up_result.value, status=sign_up_result, username=signUpRequest.username)

@api_router.get("/user/{userId}/statistic", response_model=List[StatisticInfo])
async def getStatistic(userId: str):
    return await user_service.statistic(userId)