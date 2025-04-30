from beanie import Document

class User(Document):
    username: str
    password: str

    class Settings:
        collection = "user"
    
    class Config:
        schema_extra = {
            "example": {
                "username": "pqkiet854",
                "password": "pqkiet854"
            }
        }