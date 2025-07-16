from pydantic import BaseModel
from .result_status import SignInResult, SIgnUpResult

class SignInResponse(BaseModel):
    access_token: str  = ""
    result: SignInResult
    status_code: int
    message: str = ""
    username: str = ""
class SignInToYoutubeResponse(BaseModel):
    auth_url: str
    status_code: int = 200
class GetYoutubeAccessTokenResponse(BaseModel):
    access_token: str
    status_code: int = 200
class SignUpResponse(BaseModel):
    message: str
    status: SIgnUpResult
    username: str