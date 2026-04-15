from typing import Any, List, Optional

from beanie import PydanticObjectId, init_beanie
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo import AsyncMongoClient

from models.events import Event
from models.users import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env")


async def initialize_database():
    settings = Settings()

    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in .env")

    client = AsyncMongoClient(settings.DATABASE_URL)
    db = client["planner"]

    await init_beanie(
        database=db,
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

        update_data = body.model_dump()
        update_data = {key: value for key, value in update_data.items() if value is not None}

        await doc.update({"$set": update_data})
        return await self.model.get(id)

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False

        await doc.delete()
        return True