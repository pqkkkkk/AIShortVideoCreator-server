from user.models import User
from abc import ABC, abstractmethod

class user_dao(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user(self, username: str) -> User:
        pass

    @abstractmethod
    async def update_user(self, username: str, user: User) -> User:
        pass

    @abstractmethod
    async def delete_user(self, username: str) -> None:
        pass
class mongodb_user_dao(user_dao):
    async def create_user(self, user: User) -> User:
        await User.insert_one(user)

    async def get_user(self, username: str) -> User:
        return await User.find_one({"username": username})

    async def update_user(self, username: str, user: User) -> User:
        await User.update({"username": username}, {"$set": user.dict()})

    async def delete_user(self, username: str) -> None:
        await User.delete({"username": username})