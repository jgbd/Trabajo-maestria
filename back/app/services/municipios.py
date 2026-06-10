from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.municipio import Municipios

def get_municipios(db: Session):
    query = db.query(Municipios.Codigo, Municipios.Nombre).all()
    municipios = [{"Codigo": municipio.Codigo, "Nombre": municipio.Nombre} for municipio in query]
    print(f"Municipios obtenidos: {municipios}")
    return municipios

