from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Veredas(Base):
    __tablename__ = 'Veredas'
    __table_args__ = (
        ForeignKeyConstraint(['Codigo_Municipio'], ['Municipios.Codigo'], name='Veredas_ibfk_1'),
        Index('Codigo_Municipio', 'Codigo_Municipio')
    )

    Codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Nombre: Mapped[str] = mapped_column(String(100))
    Codigo_Municipio: Mapped[Optional[int]] = mapped_column(Integer)

    Municipios_: Mapped[Optional['Municipios']] = relationship('Municipios', back_populates='Veredas')
    Puntos_Muestreo: Mapped[List['PuntosMuestreo']] = relationship('PuntosMuestreo', back_populates='Veredas_')

