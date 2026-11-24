from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import CategoryOut, MasterOut, ServiceCreate, ServiceOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Salon API")


# ==================== MASTERS ====================

@app.get("/masters", response_model=list[MasterOut])
def get_masters(
    specialization: str | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(models.Master).order_by(models.Master.id)
    if specialization is not None:
        stmt = stmt.where(models.Master.specialization == specialization)
    return db.execute(stmt).scalars().all()


@app.get("/masters/{master_id}", response_model=MasterOut)
def get_master(master_id: int, db: Session = Depends(get_db)):
    master = db.get(models.Master, master_id)
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return master


# ==================== CATEGORIES ====================

@app.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    stmt = (
        select(
            models.Category.id,
            models.Category.name,
            func.count(models.Service.id).label("servicesCount"),
        )
        .outerjoin(models.Service, models.Service.category_id == models.Category.id)
        .group_by(models.Category.id, models.Category.name)
        .order_by(models.Category.id)
    )
    rows = db.execute(stmt).all()
    return [
        CategoryOut(id=r.id, name=r.name, servicesCount=r.servicesCount)
        for r in rows
    ]


@app.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(
            models.Category.id,
            models.Category.name,
            func.count(models.Service.id).label("servicesCount"),
        )
        .outerjoin(models.Service, models.Service.category_id == models.Category.id)
        .where(models.Category.id == category_id)
        .group_by(models.Category.id, models.Category.name)
    )
    row = db.execute(stmt).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Сategory not found")
    return CategoryOut(id=row.id, name=row.name, servicesCount=row.servicesCount)


# ==================== SERVICES ====================

@app.post("/services", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    category = db.get(models.Category, payload.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    service = models.Service(
        category_id=payload.category_id,
        title=payload.title,
        desc=payload.desc,
        duration=payload.duration,
        price=payload.price,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service