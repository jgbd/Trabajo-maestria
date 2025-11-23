from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.municipios import get_municipios

router = APIRouter()
@router.get("/")
async def read_municipios( db: Session = Depends(get_db)):
    municipios = get_municipios(db)
    return municipios