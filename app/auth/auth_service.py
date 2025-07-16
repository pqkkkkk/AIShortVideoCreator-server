from abc import ABC, abstractmethod
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError, JWTClaimsError
from datetime import datetime, timedelta
from app.config import get_env_variable
from .result_status import ValidationAccessTokenResult
from fastapi import HTTPException, Depends
from app.common import oauth2_scheme


class auth_service(ABC):
    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        pass
    @abstractmethod
    def validate_access_token(self, token: str) -> ValidationAccessTokenResult:
        pass
    @abstractmethod
    def create_refresh_token(self, data: dict) -> str:
        pass
    @abstractmethod
    def validate_refresh_token(self, token: str) -> ValidationAccessTokenResult:
        pass
    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> str:
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

    def create_refresh_token(self, data: dict) -> str:
        # Refresh token có thời gian sống lâu hơn (ví dụ: 30 ngày)
        expire = datetime.utcnow() + timedelta(days=30)
        refresh_data = data.copy()
        refresh_data.update({"exp": expire, "type": "refresh"})
        return jwt.encode(refresh_data, self.secret_key, algorithm=self.algorithm)
    
    def validate_refresh_token(self, token: str) -> ValidationAccessTokenResult:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            token_type = payload.get("type")
            username = payload.get("sub")

            if username is None or token_type != "refresh":
                return ValidationAccessTokenResult.INVALID
            
            return ValidationAccessTokenResult.VALID
        except JWTError:
            return ValidationAccessTokenResult.INVALID
        except ExpiredSignatureError:
            return ValidationAccessTokenResult.EXPIRED
        except JWTClaimsError:
            return ValidationAccessTokenResult.INVALID

    def refresh_access_token(self, refresh_token: str) -> str:
        # Validate refresh token trước
        validation_result = self.validate_refresh_token(refresh_token)
        
        if validation_result != ValidationAccessTokenResult.VALID:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
        # Decode để lấy thông tin user
        payload = jwt.decode(refresh_token, self.secret_key, algorithms=[self.algorithm])
        username = payload.get("sub")
        
        # Tạo access token mới
        return self.create_access_token(data={"sub": username})

def validate_access_token( token: str) -> ValidationAccessTokenResult:
        try:
            payload = jwt.decode(token, get_env_variable("JWT_SECRET_KEY"), algorithms=[get_env_variable("JWT_ALGORITHM")])
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

def validate_token_dependency(token: str = Depends(oauth2_scheme)) -> str:
    """ Dependency function to validate the access token.
    This function can be used in FastAPI routes to ensure that the token is valid.
    """
    validation_result = validate_access_token(token)

    if validation_result == ValidationAccessTokenResult.VALID:
        return token
    elif validation_result == ValidationAccessTokenResult.EXPIRED:
        raise HTTPException(status_code=401, detail="Token expired")
    elif validation_result == ValidationAccessTokenResult.INVALID:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        raise HTTPException(status_code=500, detail="Error validating token")