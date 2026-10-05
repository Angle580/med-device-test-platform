from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sut.database import get_db
from sut.models import Device

router = APIRouter()

class DeviceRegister(BaseModel):
    device_id: str
    model: str

@router.post("/register")
def register_device(body: DeviceRegister, db: Session = Depends(get_db)):
    exist = db.query(Device).filter(Device.device_id == body.device_id).first()
    if exist:
        raise HTTPException(status_code=400, detail="设备已注册")
    dev = Device(device_id=body.device_id, model=body.model, status="online")
    db.add(dev)
    db.commit()
    return {"code": 0, "message": "注册成功", "data": {"id": dev.id}}

@router.get("/{device_id}")
def get_device(device_id: str, db: Session = Depends(get_db)):
    dev = db.query(Device).filter(Device.device_id == device_id).first()
    if not dev:
        raise HTTPException(status_code=404, detail="设备不存在")
    return {"code": 0, "data": {"device_id": dev.device_id, "status": dev.status}}

@router.post("/{device_id}/heartbeat")
def heartbeat(device_id: str, db: Session = Depends(get_db)):
    dev = db.query(Device).filter(Device.device_id == device_id).first()
    if not dev:
        raise HTTPException(status_code=404, detail="设备不存在")
    dev.status = "online"
    db.commit()
    return {"code": 0, "message": "心跳已接收"}
