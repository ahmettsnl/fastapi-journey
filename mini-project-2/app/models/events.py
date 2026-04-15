from beanie import Document
from pydantic import BaseModel
from typing import Optional, List


class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Settings:
        name = "events"

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }


class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated FastAPI Book Launch",
                "image": "https://linktomyimage.com/new-image.png",
                "description": "Updated event description",
                "tags": ["python", "fastapi"],
                "location": "Hybrid"
            }
        }