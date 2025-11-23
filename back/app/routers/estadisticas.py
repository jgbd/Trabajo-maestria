import app.models
from app.services import resultado
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import estadisticas

router = APIRouter()

@router.get('/')
async def obtener_irca(anioInicio: int = 2020, anioFin: int = 2024, codigo_municipio: int = None, db: Session = Depends(get_db)):
    return estadisticas.obtener_resumen_irca(db, anioInicio, anioFin, codigo_municipio)

@router.get('/resultados')
async def listar_resultados(db: Session = Depends(get_db)):
    return resultado.get_resultados(db)