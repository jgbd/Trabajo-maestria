"""
Estadisticas Router

IRCA statistics and water quality results endpoints with pagination.
"""

import app.models
from app.services import resultado
from fastapi import APIRouter, Depends, Request, Response, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import estadisticas
from app.core.rate_limiter import limiter
from app.core.config import settings
from app.core.pagination import PaginationParams, paginate, PaginatedResponse
from app.schemas.schemas import (
    MunicipioEstadistica, 
    ResultadoDetallado, 
    EstadisticasQueryParams
)
from typing import List

router = APIRouter()

@router.get(
    '/',
    response_model=List[MunicipioEstadistica],
    summary="Get IRCA statistics by municipality",
    description="""
    Returns aggregated IRCA statistics for municipalities.
    
    - Groups data by municipality and year
    - Calculates average IRCA values
    - Classifies risk levels based on Colombian standards
    - **Rate limit**: 30 requests/minute
    
    Use query parameters to filter by year range and specific municipality.
    """
)
@limiter.limit(settings.RATE_LIMIT_ESTADISTICAS)  # "30/minute"
async def obtener_irca(
    request: Request,  # Required by slowapi limiter
    response: Response,  # Required by slowapi for rate limit headers
    anioInicio: int = Query(
        default=2020,
        ge=2000,
        le=2100,
        description="Start year for data range"
    ),
    anioFin: int = Query(
        default=2024,
        ge=2000,
        le=2100,
        description="End year for data range"
    ),
    codigo_municipio: int = Query(
        default=None,
        ge=1,
        description="Optional municipality code filter"
    ),
    db: Session = Depends(get_db)
):
    """
    Get IRCA statistics aggregated by municipality and year.
    
    This endpoint returns summarized data suitable for dashboards and visualizations.
    Data is not paginated as it returns aggregated statistics, not raw results.
    """
    # Validate year range
    if anioFin < anioInicio:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="anioFin must be greater than or equal to anioInicio"
        )
    
    return estadisticas.obtener_resumen_irca(db, anioInicio, anioFin, codigo_municipio)

@router.get(
    '/resultados',
    response_model=PaginatedResponse[ResultadoDetallado],
    summary="Get detailed water quality test results",
    description="""
    Returns paginated detailed water quality test results.
    
    - Contains all water quality parameters (pH, turbidity, chlorine, etc.)
    - Includes IRCA values and risk classifications
    - **Pagination required** - this endpoint returns large datasets
    - **Rate limit**: 10 requests/minute (restrictive due to data size)
    
    Use pagination parameters to navigate through results:
    - `page`: Page number (1-indexed)
    - `page_size`: Items per page (max 100, default 50)
    """
)
@limiter.limit(settings.RATE_LIMIT_RESULTADOS)  # "10/minute" - restrictive for large data
async def listar_resultados(
    request: Request,  # Required by slowapi limiter
    response: Response,  # Required by slowapi for rate limit headers
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(
        default=50, 
        ge=1, 
        le=100, 
        description="Items per page (max 100)"
    ),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of detailed water quality test results.
    
    **Important**: This endpoint must use pagination to prevent loading
    all results at once, which could crash the application.
    
    Returns detailed test results including all water quality parameters.
    """
    pagination = PaginationParams(page=page, page_size=page_size)
    
    # Get paginated results and total count
    items, total = resultado.get_resultados(db, pagination)
    
    # Return paginated response
    return paginate(items, total, pagination)
