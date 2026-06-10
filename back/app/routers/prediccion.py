"""
Prediction Router

API endpoints for IRCA prediction using the trained ML model.

Endpoints:
- POST /api/prediccion/predict - Single prediction
- POST /api/prediccion/batch - Batch predictions
- GET /api/prediccion/model-info - Model information
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from app.schemas.schemas import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    ModelInfoResponse
)
from app.services.prediccion import (
    predict_irca,
    predict_irca_batch,
    get_model_info
)
from app.core.rate_limiter import limiter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/prediccion",
    tags=["Predicción IRCA"],
    responses={
        500: {"description": "Error interno del servidor"},
        422: {"description": "Error de validación de datos"}
    }
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predecir valor IRCA",
    description="""
    Predice el valor IRCA basado en parámetros de calidad del agua.
    
    **Modelo:** RandomForestRegressor  
    **R² Score:** 0.9914 (99.14% de varianza explicada)  
    **RMSE:** 0.093  
    **MAE:** 0.025  
    
    **Parámetros de entrada:**
    - color_aparente: Color aparente (UPC)
    - turbiedad: Turbiedad (NTU)
    - ph: Valor de pH
    - cloro_residual_libre: Cloro residual libre (mg/L)
    - cloruros: Cloruros (mg/L)
    - nitritos: Nitritos (mg/L)
    - coliformes_totales: Coliformes totales (UFC/100mL)
    - e_coli: E. coli (UFC/100mL)
    
    **Respuesta:**
    - irca_predicted: Valor IRCA predicho (0-100)
    - nivel_riesgo: Nivel de riesgo (SIN RIESGO, BAJO, MEDIO, ALTO, INVIABLE)
    - confidence: Confianza del modelo (R² score)
    """,
    response_description="Predicción exitosa del valor IRCA"
)
@limiter.limit("60/minute")
async def predict_single(
    request: Request,
    response: Response,
    data: PredictionRequest
) -> PredictionResponse:
    """
    Predict IRCA value for a single water quality sample.
    
    Rate limit: 60 requests/minute
    """
    try:
        logger.info(f"Prediction request received with pH={data.ph}, cloro={data.cloro_residual_libre}")
        
        result = predict_irca(
            color_aparente=data.color_aparente,
            turbiedad=data.turbiedad,
            ph=data.ph,
            cloro_residual_libre=data.cloro_residual_libre,
            cloruros=data.cloruros,
            nitritos=data.nitritos,
            coliformes_totales=data.coliformes_totales,
            e_coli=data.e_coli
        )
        
        logger.info(f"Prediction successful: IRCA={result['irca_predicted']}, Risk={result['nivel_riesgo']}")
        
        return PredictionResponse(**result)
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar la predicción: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=BatchPredictionResponse,
    summary="Predicciones por lote",
    description="""
    Predice valores IRCA para múltiples muestras a la vez.
    
    Más eficiente que llamar /predict múltiples veces.
    Límite: 1000 muestras por solicitud.
    
    **Uso típico:**
    - Análisis de múltiples puntos de muestreo
    - Procesamiento de datos históricos
    - Validación de modelos
    """,
    response_description="Predicciones exitosas para todas las muestras"
)
@limiter.limit("30/minute")
async def predict_batch(
    request: Request,
    response: Response,
    data: BatchPredictionRequest
) -> BatchPredictionResponse:
    """
    Predict IRCA values for multiple samples at once.
    
    Rate limit: 30 requests/minute
    """
    try:
        n_samples = len(data.samples)
        logger.info(f"Batch prediction request received with {n_samples} samples")
        
        # Convert samples to dict format
        samples_dict = [
            {
                "color_aparente": s.color_aparente,
                "turbiedad": s.turbiedad,
                "ph": s.ph,
                "cloro_residual_libre": s.cloro_residual_libre,
                "cloruros": s.cloruros,
                "nitritos": s.nitritos,
                "coliformes_totales": s.coliformes_totales,
                "e_coli": s.e_coli
            }
            for s in data.samples
        ]
        
        # Get predictions
        results = predict_irca_batch(samples_dict)
        
        # Convert to response format
        predictions = [PredictionResponse(**r) for r in results]
        
        logger.info(f"Batch prediction successful: {n_samples} samples processed")
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_samples=n_samples
        )
    
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar las predicciones por lote: {str(e)}"
        )


@router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    summary="Información del modelo",
    description="""
    Obtiene información sobre el modelo de predicción cargado.
    
    Incluye:
    - Tipo de modelo
    - Hiperparámetros
    - Nombres de características
    - Métricas de rendimiento
    - Número de características
    """,
    response_description="Información del modelo"
)
@limiter.limit("100/minute")
async def model_information(
    request: Request,
    response: Response
) -> ModelInfoResponse:
    """
    Get information about the loaded prediction model.
    
    Rate limit: 100 requests/minute
    """
    try:
        logger.info("Model info request received")
        
        info = get_model_info()
        
        return ModelInfoResponse(**info)
    
    except Exception as e:
        logger.error(f"Failed to get model info: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener información del modelo: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check",
    description="Verifica que el servicio de predicción esté funcionando correctamente",
    response_description="Estado del servicio"
)
@limiter.limit("200/minute")
async def health_check(
    request: Request,
    response: Response
):
    """
    Health check endpoint for the prediction service.
    
    Returns 200 if model is loaded and service is operational.
    """
    try:
        # Try to get model info to verify model is loaded
        info = get_model_info()
        
        return {
            "status": "healthy",
            "service": "prediccion",
            "model_loaded": True,
            "model_type": info['model_class'],
            "r2_score": info['metrics']['r2']
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "prediccion",
                "model_loaded": False,
                "error": str(e)
            }
        )
