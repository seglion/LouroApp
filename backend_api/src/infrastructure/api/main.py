from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.infrastructure.db.database import get_db

app = FastAPI(
    title="API GIS Saneamiento - Field Collection",
    version="1.0.0",
    description="Backend microservice using Clean Architecture"
)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Verifica el estado del servicio y la base de datos"""
    db_status = False
    try:
        # Check DB connection
        db.execute(text("SELECT 1"))
        db_status = True
    except Exception:
        db_status = False
        
    return {"status": "ok", "db_connected": db_status}
