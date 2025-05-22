from abc import ABC, abstractmethod
from user.dao import user_dao
from user.models import User
from user.result_status import SignInResult, SIgnUpResult
from user.dto.requests import SignInRequest, SignUpRequest
import traceback
import bcrypt

class user_service(ABC):
    @abstractmethod
    async def sign_in(self, username: str, password: str) -> SignInResult:
        pass
    async def sign_up(self, username: str, password: str) -> SIgnUpResult:
        pass
class user_service_v1(user_service):
    async def sign_in(self, username: str, password: str) -> SignInResult:
        try:
            user = await user_dao.get_user(username)

            if not user:
                return SignInResult.USER_NOT_FOUND
            elif not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return SignInResult.WRONG_PASSWORD
            else:
                return SignInResult.SUCCESS
        except Exception as e:
            print(f"Error during sign in: {e}")
            traceback.print_exc()
            return SignInResult.UNKNOWN_ERROR
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