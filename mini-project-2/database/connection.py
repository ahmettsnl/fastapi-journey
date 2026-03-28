from typing import Any, List, Optional

from beanie import PydanticObjectId, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from models.events import Event
from models.users import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"


async def initialize_database():
    settings = Settings()
    client = AsyncIOMotorClient(settings.DATABASE_URL)

    await init_beanie(
        database=client.get_default_database(),
        document_models=[Event, User]
    )


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc = await self.get(id)
        if not doc:
            return False

        update_data = body.dict()
        update_data = {key: value for key, value in update_data.items() if value is not None}

        await doc.update({"$set": update_data})
        return await self.model.get(id)

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False

        await doc.delete()
        return True