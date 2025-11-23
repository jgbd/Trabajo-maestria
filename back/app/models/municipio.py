from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Municipios(Base):
    __tablename__ = 'Municipios'
    __table_args__ = (
        ForeignKeyConstraint(['Codigo_Departamento'], ['Departamentos.Codigo'], name='Municipios_ibfk_1'),
        Index('Codigo_Departamento', 'Codigo_Departamento')
    )

    Codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Nombre: Mapped[str] = mapped_column(String(100))
    Codigo_Departamento: Mapped[Optional[int]] = mapped_column(Integer)
    Longitud : Mapped[Optional[float]] = mapped_column(Float)
    Latitud : Mapped[Optional[float]] = mapped_column(Float)

    Departamentos_: Mapped[Optional['Departamentos']] = relationship('Departamentos', back_populates='Municipios')
    Veredas: Mapped[List['Veredas']] = relationship('Veredas', back_populates='Municipios_')
