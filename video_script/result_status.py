from enum import Enum

class AutoGenerateTextScriptResult(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    INVALID_INPUT = "invalid_input"
    SERVER_BUSY = "server_busy"

class ConvertToVideoMetadataResult(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    INVALID_INPUT = "invalid_input"
    SERVER_BUSY = "server_busy"