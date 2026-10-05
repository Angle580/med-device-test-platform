from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sut.database import get_db
from sut.models import VitalsRecord

router = APIRouter()

class VitalsUpload(BaseModel):
    device_id: str
    systolic: int = Field(ge=0, le=300)
    diastolic: int = Field(ge=0, le=200)
    heart_rate: int = Field(ge=0, le=250)
    spo2: int = Field(default=None, ge=0, le=100)

@router.post("/upload")
def upload_vitals(body: VitalsUpload, db: Session = Depends(get_db)):
    # 业务校验：血压范围合理性
    if body.systolic <= body.diastolic:
        raise HTTPException(status_code=400, detail="收缩压必须大于舒张压")
    if body.systolic > 200 or body.systolic < 60:
        raise HTTPException(status_code=400, detail="血压超出合理范围")
    rec = VitalsRecord(
        device_id=body.device_id,
        systolic=body.systolic,
        diastolic=body.diastolic,
        heart_rate=body.heart_rate,
        spo2=body.spo2,
    )
    db.add(rec)
    db.commit()
    return {"code": 0, "message": "上报成功", "data": {"id": rec.id}}

@router.get("/{device_id}/latest")
def latest_vitals(device_id: str, db: Session = Depends(get_db)):
    rec = (db.query(VitalsRecord)
           .filter(VitalsRecord.device_id == device_id)
           .order_by(VitalsRecord.id.desc()).first())
    if not rec:
        raise HTTPException(status_code=404, detail="无数据")
    return {"code": 0, "data": {
        "systolic": rec.systolic, "diastolic": rec.diastolic,
        "heart_rate": rec.heart_rate, "spo2": rec.spo2}}
