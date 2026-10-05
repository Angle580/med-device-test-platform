from fastapi import FastAPI
from sut.database import init_db
from sut.routers import device, vitals, patient, report, alert

app = FastAPI(title="Medical Device Monitor API", version="1.0.0")

init_db()

app.include_router(device.router, prefix="/api/v1/device", tags=["device"])
app.include_router(vitals.router, prefix="/api/v1/vitals", tags=["vitals"])
app.include_router(patient.router, prefix="/api/v1/patient", tags=["patient"])
app.include_router(report.router, prefix="/api/v1/report", tags=["report"])
app.include_router(alert.router, prefix="/api/v1/alerts", tags=["alerts"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
