from pydantic import BaseModel
from user.result_status import SignInResult, SIgnUpResult

class SignInResponse(BaseModel):
    access_token: str
    status: SignInResult
    message: str
class SignUpResponse(BaseModel):
    message: str
    status: SIgnUpResult
    username: str