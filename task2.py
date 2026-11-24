from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)


class CategoryOut(BaseModel):
    id: int
    name: str
    servicesCount: int


app = FastAPI()


@app.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    stmt = (
        select(
            Category.id,
            Category.name,
            func.count(Service.id).label("servicesCount"),
        )
        .outerjoin(Service, Service.category_id == Category.id)
        .group_by(Category.id, Category.name)
        .order_by(Category.id)
    )
    rows = db.execute(stmt).all()
    return [
        CategoryOut(id=row.id, name=row.name, servicesCount=row.servicesCount)
        for row in rows
    ]


@app.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(
            Category.id,
            Category.name,
            func.count(Service.id).label("servicesCount"),
        )
        .outerjoin(Service, Service.category_id == Category.id)
        .where(Category.id == category_id)
        .group_by(Category.id, Category.name)
    )
    row = db.execute(stmt).first()

    if row is None:
        raise HTTPException(status_code=404, detail="Сategory not found")

    return CategoryOut(id=row.id, name=row.name, servicesCount=row.servicesCount)