from pydantic import BaseModel

class AutoGenerateScriptRequest(BaseModel):
    prompt: str