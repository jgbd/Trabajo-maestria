from typing import List, Optional

from sqlalchemy import Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class PrestadoresServicios(Base):
    __tablename__ = 'Prestadores_Servicios'

    Nit: Mapped[str] = mapped_column(String(20), primary_key=True)
    Digito_Verificacion: Mapped[Optional[int]] = mapped_column(Integer)
    Persona_Prestadora: Mapped[Optional[str]] = mapped_column(VARCHAR(500))
    Registrada_SSPD: Mapped[Optional[str]] = mapped_column(String(10))

    Sistemas_Distriucion: Mapped[List['SistemasDistriucion']] = relationship('SistemasDistriucion', back_populates='Prestadores_Servicios')
    Puntos_Muestreo: Mapped[List['PuntosMuestreo']] = relationship('PuntosMuestreo', back_populates='Prestadores_Servicios')

