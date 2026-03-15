from fastapi import FastAPI
from models import Patient
import asyncio

app = FastAPI()

patients = []

@app.get("/patients/")
async def get_patients():
    return patients


@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    return {"error": "Patient not found"}