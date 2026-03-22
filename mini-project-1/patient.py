from fastapi import APIRouter, HTTPException
from models import Patient
import asyncio

patient_router = APIRouter()

patients = []

@patient_router.get("/patients/")
async def get_patients():
    await asyncio.sleep(1)
    return patients


@patient_router.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            return patient
    raise HTTPException(
    status_code=404,
    detail=f"Patient with ID {patient_id} was not found"
)


@patient_router.post("/patients/")
async def create_patient(patient: Patient):
    patients.append(patient)
    return patient


@patient_router.put("/patients/{patient_id}")
async def update_patient(patient_id: int, updated_patient: Patient):
    for index, patient in enumerate(patients):
        if patient.id == patient_id:
            patients[index] = updated_patient
            return updated_patient
    raise HTTPException(
    status_code=404,
    detail=f"Patient with ID {patient_id} was not found"
)


@patient_router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            patients.remove(patient)
            return {"message": "Patient deleted"}
    raise HTTPException(
    status_code=404,
    detail=f"Patient with ID {patient_id} was not found"
)