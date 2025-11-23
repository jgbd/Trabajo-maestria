from typing import Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class SistemasDistriucion(Base):
    __tablename__ = 'Sistemas_Distriucion'
    __table_args__ = (
        ForeignKeyConstraint(['Nit_Prestador'], ['Prestadores_Servicios.Nit'], name='Sistemas_Distriucion_ibfk_1'),
        Index('Nit_Prestador', 'Nit_Prestador')
    )

    Codigo: Mapped[int] = mapped_column(Integer, primary_key=True)
    Tipo_Suministro: Mapped[Optional[str]] = mapped_column(VARCHAR(500))
    Sistema_Distribucion: Mapped[Optional[str]] = mapped_column(VARCHAR(500))
    Suscriptores_Area_Urbana: Mapped[Optional[int]] = mapped_column(Integer)
    Suscriptores_Area_Rural: Mapped[Optional[int]] = mapped_column(Integer)
    Total_Poblacion: Mapped[Optional[int]] = mapped_column(Integer)
    Usuarios_Poblacion_Atendida: Mapped[Optional[int]] = mapped_column(Integer)
    Total_Poblacion_Atendida: Mapped[Optional[int]] = mapped_column(Integer)
    Nit_Prestador: Mapped[Optional[str]] = mapped_column(String(20))

    Prestadores_Servicios: Mapped[Optional['PrestadoresServicios']] = relationship('PrestadoresServicios', back_populates='Sistemas_Distriucion')
