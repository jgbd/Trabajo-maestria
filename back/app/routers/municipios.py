from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.municipios import get_municipios
from app.core.rate_limiter import limiter
from app.core.config import settings

router = APIRouter()

@router.get("/")
@limiter.limit(settings.RATE_LIMIT_MUNICIPIOS)  # "100/hour" - simple list endpoint
async def read_municipios(
    request: Request,  # Required by slowapi limiter
    response: Response,  # Required by slowapi for rate limit headers
    db: Session = Depends(get_db)
):
    """
    Get list of all municipalities.
    
    This is a simple lookup endpoint that returns static reference data.
    Rate limited to 100 requests per hour.
    """
    municipios = get_municipios(db)
    return municipios