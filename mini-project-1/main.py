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

@app.post("/patients/")
async def create_patient(patient: Patient):
    patients.append(patient)
    return patient

@app.put("/patients/{patient_id}")
async def update_patient(patient_id: int, updated_patient: Patient):
    for index, patient in enumerate(patients):
        if patient.id == patient_id:
            patients[index] = updated_patient
            return updated_patient
    return {"error": "Patient not found"}

@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    for patient in patients:
        if patient.id == patient_id:
            patients.remove(patient)
            return {"message": "Patient deleted"}
    return {"error": "Patient not found"}

@app.get("/patients/")
async def get_patients():
    await asyncio.sleep(1)
    return patients