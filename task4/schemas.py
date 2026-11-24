from pydantic import BaseModel, ConfigDict, Field


# ---------- Master ----------
class MasterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    specialization: str


# ---------- Category ----------
class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    name: str
    services_count: int = Field(alias="servicesCount")


# ---------- Service ----------
class ServiceCreate(BaseModel):
    category_id: int = Field(alias="categoryId", gt=0)
    title: str = Field(min_length=1, max_length=100)
    desc: str = Field(min_length=1, max_length=100)
    duration: int = Field(ge=30, le=180)
    price: float = Field(gt=0)

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    category_id: int = Field(alias="categoryId")
    title: str
    desc: str
    duration: int
    price: float