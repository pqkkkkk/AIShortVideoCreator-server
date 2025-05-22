from fastapi import APIRouter, Depends, HTTPException
from .dto.requests import SignInRequest, SignUpRequest
from .dto.responses import SignInResponse, SignUpResponse
from .service import user_service
from .result_status import SignInResult, SIgnUpResult
api_router = APIRouter()


@api_router.post("/user/signin")
async def sign_in(signInRequest : SignInRequest):
    sign_in_result = await user_service.sign_in(signInRequest.username, signInRequest.password)

    if sign_in_result == SignInResult.SUCCESS:
        return SignInResponse(message="Sign in successful", access_token="your_access_token", status=sign_in_result)
    else:
        raise HTTPException(status_code=400, detail=sign_in_result.value)
@api_router.post("/user")
async def sign_up(signUpRequest: SignUpRequest):
    sign_up_result = await user_service.sign_up(signUpRequest=signUpRequest)

    if sign_up_result == SIgnUpResult.SUCCESS:
        return SignUpResponse(message="Sign up successful", status=sign_up_result, username=signUpRequest.username)
    elif sign_up_result == SIgnUpResult.UNKNOWN_ERROR:
        raise HTTPException(status_code=400, detail=sign_up_result.value)
    else:
        return SignUpResponse(message=sign_up_result.value, status=sign_up_result, username=signUpRequest.username)
