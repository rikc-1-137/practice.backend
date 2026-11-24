from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Master(Base):
    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<Master(id={self.id}, name='{self.name}', spec='{self.specialization}')>"