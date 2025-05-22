from enum import Enum

class SignInResult(Enum):
    SUCCESS = "success"
    WRONG_PASSWORD = "wưrong password"
    USER_NOT_FOUND = "User not found"
    UNKNOWN_ERROR = "Unknown error"
class SIgnUpResult(Enum):
    SUCCESS = "success"
    USERNAME_EXISTS = "Username already exists"
    UNKNOWN_ERROR = "Unknown error",
    PASSWORD_MISMATCH = "Password mismatch"