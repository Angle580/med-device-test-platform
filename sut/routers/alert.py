from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sut.database import get_db
from sut.models import VitalsRecord
from sut.report_engine import calculate_risk_level

router = APIRouter()

@router.get("/")
def list_alerts(db: Session = Depends(get_db)):
    """扫描最近的体征数据，返回所有高危/告警记录"""
    records = db.query(VitalsRecord).order_by(VitalsRecord.id.desc()).limit(50).all()
    alerts = []
    for r in records:
        level = calculate_risk_level((r.systolic, r.diastolic), r.heart_rate)
        if level in ("高危", "过低告警"):
            alerts.append({
                "device_id": r.device_id,
                "risk_level": level,
                "systolic": r.systolic,
                "diastolic": r.diastolic,
                "heart_rate": r.heart_rate,
            })
    return {"code": 0, "data": alerts}
