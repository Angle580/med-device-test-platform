from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sut.database import get_db
from sut.models import Patient

router = APIRouter()

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    device_id: str = None

@router.post("/")
def create_patient(body: PatientCreate, db: Session = Depends(get_db)):
    p = Patient(**body.model_dump())
    db.add(p)
    db.commit()
    return {"code": 0, "message": "创建成功", "data": {"id": p.id}}

@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="患者不存在")
    return {"code": 0, "data": {"id": p.id, "name": p.name, "age": p.age}}
