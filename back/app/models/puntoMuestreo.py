from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class PuntosMuestreo(Base):
    __tablename__ = 'Puntos_Muestreo'
    __table_args__ = (
        ForeignKeyConstraint(['Codigo_Vereda'], ['Veredas.Codigo'], name='Puntos_Muestreo_ibfk_1'),
        ForeignKeyConstraint(['Nit_Prestador'], ['Prestadores_Servicios.Nit'], name='Puntos_Muestreo_ibfk_2'),
        Index('Codigo_Vereda', 'Codigo_Vereda'),
        Index('ix_punto_muestreo_nit_prestador', 'Nit_Prestador')
    )

    Codigo: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    Descripcion: Mapped[Optional[str]] = mapped_column(String(255))
    Direccion: Mapped[Optional[str]] = mapped_column(String(255))
    Codigo_Vereda: Mapped[Optional[int]] = mapped_column(Integer)
    Tipo_Punto: Mapped[Optional[str]] = mapped_column(String(50))
    Clasificacion: Mapped[Optional[str]] = mapped_column(TEXT)
    Tipo_Dispositivo: Mapped[Optional[str]] = mapped_column(String(50))
    Georreferenciacion: Mapped[Optional[str]] = mapped_column(String(100))
    Nit_Prestador: Mapped[Optional[str]] = mapped_column(String(20))

    Veredas_: Mapped[Optional['Veredas']] = relationship('Veredas', back_populates='Puntos_Muestreo')
    Prestadores_Servicios: Mapped[Optional['PrestadoresServicios']] = relationship('PrestadoresServicios', back_populates='Puntos_Muestreo')
    Resultados: Mapped[List['Resultados']] = relationship('Resultados', back_populates='Puntos_Muestreo')
