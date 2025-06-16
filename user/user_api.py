from fastapi import APIRouter, Depends, HTTPException
from .dto.requests import SignInRequest, SignUpRequest
from .dto.responses import SignInResponse, SignUpResponse
from .service import user_service
from .result_status import SignInResult, SIgnUpResult
api_router = APIRouter()
from typing import List
from externalPlatform.Youtube.models import StatisticInfo

@api_router.post("/user/signin")
async def sign_in(signInRequest : SignInRequest):
    sign_in_response = await user_service.sign_in(signInRequest.username, signInRequest.password)

    if sign_in_response.status == SignInResult.SUCCESS:
        return sign_in_response
    else:
        raise HTTPException(status_code=400, detail=sign_in_response.status.value)
    

@api_router.post("/user")
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