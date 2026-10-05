from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sut.database import Base

class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), unique=True, index=True)
    model = Column(String(50))
    status = Column(String(20), default="offline")
    created_at = Column(DateTime, server_default=func.now())

class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10))
    phone = Column(String(20))
    device_id = Column(String(50), ForeignKey("device.device_id"), nullable=True)

class VitalsRecord(Base):
    __tablename__ = "vitals_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), index=True)
    systolic = Column(Integer)
    diastolic = Column(Integer)
    heart_rate = Column(Integer)
    spo2 = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Report(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, index=True)
    risk_level = Column(String(20))
    summary = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
