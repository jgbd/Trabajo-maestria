from typing import List

from sqlalchemy import  Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Departamentos(Base):
    __tablename__ = 'Departamentos'

    Codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Nombre: Mapped[str] = mapped_column(String(100))

    Municipios: Mapped[List['Municipios']] = relationship('Municipios', back_populates='Departamentos_')