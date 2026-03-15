from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Appointment(BaseModel):
    id: int
    doctor: str = Field(..., min_length=2, max_length=50)
    reason: str = Field(..., min_length=3, max_length=100)
    date: date


class Patient(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    email: str
    appointments: List[Appointment] = []