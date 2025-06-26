from abc import ABC, abstractmethod
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError, JWTClaimsError
from datetime import datetime, timedelta
from app.config import get_env_variable
from .result_status import ValidationAccessTokenResult
from fastapi import HTTPException

class auth_service(ABC):
    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        pass
    @abstractmethod
    def validate_access_token(self, token: str) -> ValidationAccessTokenResult:
        pass
    @abstractmethod
    def refresh_access_token(self, token: str) -> str:
        pass


class auth_service_v1(auth_service):
    def __init__(self):
        self.secret_key = get_env_variable("JWT_SECRET_KEY")
        self.algorithm = get_env_variable("JWT_ALGORITHM")
        self.access_token_expire_minutes = int(get_env_variable("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        data.update({"exp": expire})
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def validate_access_token(self, token: str) -> ValidationAccessTokenResult:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")

            if username is None:
                return ValidationAccessTokenResult.INVALID
            
            return ValidationAccessTokenResult.VALID
        except JWTError:
            return ValidationAccessTokenResult.INVALID
        except ExpiredSignatureError:
            return ValidationAccessTokenResult.EXPIRED
        except JWTClaimsError:
            return ValidationAccessTokenResult.INVALID

    def refresh_access_token(self, token: str) -> str:
        payload = self.validate_access_token(token, Exception("Invalid token"))
        return self.create_access_token(data=payload)