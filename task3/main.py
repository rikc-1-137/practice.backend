from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import MasterOut

Base.metadata.create_all(bind=engine)   # создаём таблицы при старте (для учебного проекта ок)

app = FastAPI(title="Salon API")


# ---------- GET /masters (+ фильтр по specialization) ----------
@app.get("/masters", response_model=list[MasterOut])
def get_masters(
    specialization: str | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(models.Master).order_by(models.Master.id)

    if specialization is not None:
        stmt = stmt.where(models.Master.specialization == specialization)

    return db.execute(stmt).scalars().all()


# ---------- GET /masters/{master_id} ----------
@app.get("/masters/{master_id}", response_model=MasterOut)
def get_master(master_id: int, db: Session = Depends(get_db)):
    master = db.get(models.Master, master_id)

    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")

    return master