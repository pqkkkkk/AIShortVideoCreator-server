from enum import Enum

class ValidationAccessTokenResult(Enum):
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    ERROR = "error"