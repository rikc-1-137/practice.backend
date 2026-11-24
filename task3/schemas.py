from pydantic import BaseModel, ConfigDict


class MasterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    specialization: str