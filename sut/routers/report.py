from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sut.database import get_db
from sut.models import Report, VitalsRecord
from sut.report_engine import calculate_risk_level, generate_summary

router = APIRouter()

class ReportRequest(BaseModel):
    patient_id: int
    device_id: str

@router.post("/generate")
def generate_report(body: ReportRequest, db: Session = Depends(get_db)):
    rec = (db.query(VitalsRecord)
           .filter(VitalsRecord.device_id == body.device_id)
           .order_by(VitalsRecord.id.desc()).first())
    if not rec:
        raise HTTPException(status_code=404, detail="该设备无体征数据")
    bp = (rec.systolic, rec.diastolic)
    risk = calculate_risk_level(bp, rec.heart_rate)
    summary = generate_summary(risk, bp, rec.heart_rate)
    r = Report(patient_id=body.patient_id, risk_level=risk, summary=summary)
    db.add(r)
    db.commit()
    return {"code": 0, "data": {"report_id": r.id, "risk_level": risk, "summary": summary}}
