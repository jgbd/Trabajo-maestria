"""
Request/Response Schemas for API Endpoints

Provides Pydantic models for request validation and response serialization.
Ensures type safety and automatic API documentation.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from app.core.constants import IRCARiskLevel, APIConstants


# ==================== Query Parameter Schemas ====================

class EstadisticasQueryParams(BaseModel):
    """
    Query parameters for estadisticas endpoint.
    
    Validates year ranges and municipality codes.
    """
    anioInicio: int = Field(
        default=APIConstants.DEFAULT_YEAR_START,
        ge=2000,
        le=2100,
        description="Start year for data range"
    )
    anioFin: int = Field(
        default=APIConstants.DEFAULT_YEAR_END,
        ge=2000,
        le=2100,
        description="End year for data range"
    )
    codigo_municipio: Optional[int] = Field(
        default=None,
        ge=1,
        description="Optional municipality code filter"
    )
    
    @field_validator('anioFin')
    @classmethod
    def validate_year_range(cls, v: int, info) -> int:
        """Ensure anioFin >= anioInicio."""
        if 'anioInicio' in info.data and v < info.data['anioInicio']:
            raise ValueError('anioFin must be greater than or equal to anioInicio')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "anioInicio": 2020,
                "anioFin": 2024,
                "codigo_municipio": 52001
            }
        }


# ==================== Response Schemas ====================

class ResultadoIRCA(BaseModel):
    """
    Single year IRCA result for a municipality.
    """
    anio: int = Field(description="Year of measurement")
    irca: float = Field(description="Average IRCA value for the year")
    estado: str = Field(description="Risk level classification")
    
    class Config:
        json_schema_extra = {
            "example": {
                "anio": 2024,
                "irca": 12.5,
                "estado": "BAJO"
            }
        }


class MunicipioEstadistica(BaseModel):
    """
    IRCA statistics for a single municipality.
    """
    municipio: str = Field(description="Municipality name")
    lat: Optional[float] = Field(default=None, description="Latitude coordinate")
    lng: Optional[float] = Field(default=None, description="Longitude coordinate")
    resultados: List[ResultadoIRCA] = Field(
        description="List of IRCA results by year"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "municipio": "Pasto",
                "lat": 1.2136,
                "lng": -77.2811,
                "resultados": [
                    {"anio": 2020, "irca": 8.5, "estado": "BAJO"},
                    {"anio": 2021, "irca": 6.2, "estado": "BAJO"},
                    {"anio": 2022, "irca": 4.8, "estado": "SIN RIESGO"}
                ]
            }
        }


class Municipio(BaseModel):
    """
    Basic municipality information.
    """
    Codigo: int = Field(description="Municipality code")
    Nombre: str = Field(description="Municipality name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "Codigo": 52001,
                "Nombre": "Pasto"
            }
        }


class ResultadoDetallado(BaseModel):
    """
    Detailed water quality test result.
    
    Contains all water quality parameters and their diagnostics.
    """
    # Color Aparente
    resultado_Color_Aparente: Optional[float] = Field(
        default=None,
        description="Color aparente result"
    )
    diagnostico_Color_Aparente: Optional[str] = Field(
        default=None,
        description="Color aparente diagnostic"
    )
    
    # Turbiedad
    resultado_Turbiedad: Optional[float] = Field(
        default=None,
        description="Turbidity result"
    )
    diagnostico_Turbiedad: Optional[str] = Field(
        default=None,
        description="Turbidity diagnostic"
    )
    
    # pH
    resultado_Ph: Optional[float] = Field(
        default=None,
        description="pH level result"
    )
    diagnostico_Ph: Optional[str] = Field(
        default=None,
        description="pH diagnostic"
    )
    
    # Cloro Residual Libre
    resultado_Cloro_Residual_Libre: Optional[float] = Field(
        default=None,
        description="Free residual chlorine result"
    )
    diagnostico_Cloro_Residual_Libre: Optional[str] = Field(
        default=None,
        description="Free residual chlorine diagnostic"
    )
    
    # Other parameters (keeping original structure)
    resultado_Alcalinidad_Total: Optional[float] = None
    diagnostico_Alcalinidad_Total: Optional[str] = None
    resultado_Aluminio: Optional[float] = None
    diagnostico_Aluminio: Optional[str] = None
    resultado_Cloruros: Optional[float] = None
    diagnostico_Cloruros: Optional[str] = None
    resultado_COT: Optional[float] = None
    diagnostico_COT: Optional[str] = None
    resultado_Dureza_Total: Optional[float] = None
    diagnostico_Dureza_Total: Optional[str] = None
    resultado_Fosfatos: Optional[float] = None
    diagnostico_Fosfatos: Optional[str] = None
    resultado_Manganeso: Optional[float] = None
    diagnostico_Manganeso: Optional[str] = None
    resultado_Nitratos: Optional[float] = None
    diagnostico_Nitratos: Optional[str] = None
    resultado_Nitritos: Optional[float] = None
    diagnostico_Nitritos: Optional[str] = None
    resultado_Sulfatos: Optional[float] = None
    diagnostico_Sulfatos: Optional[str] = None
    resultado_Coliformes_Totales: Optional[float] = None
    diagnostico_Coliformes_Totales: Optional[str] = None
    resultado_E_Coli: Optional[float] = None
    diagnostico_E_Coli: Optional[str] = None
    resultado_Floruros: Optional[float] = None
    diagnostico_Floruros: Optional[str] = None
    resultado_Hierro_Total: Optional[float] = None
    diagnostico_Hierro_Total: Optional[str] = None
    
    # IRCA
    IRCA: float = Field(description="IRCA index value (0-100)")
    nivel_Riesgo: str = Field(description="Risk level classification")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resultado_Color_Aparente": 5.2,
                "diagnostico_Color_Aparente": "ACEPTABLE",
                "resultado_Turbiedad": 2.1,
                "diagnostico_Turbiedad": "ACEPTABLE",
                "resultado_Ph": 7.2,
                "diagnostico_Ph": "ACEPTABLE",
                "resultado_Cloro_Residual_Libre": 0.8,
                "diagnostico_Cloro_Residual_Libre": "ACEPTABLE",
                "IRCA": 12.5,
                "nivel_Riesgo": "BAJO"
            }
        }


# ==================== Prediction Schemas ====================

class PredictionRequest(BaseModel):
    """
    Request schema for IRCA prediction endpoint.
    
    Contains water quality parameters used by the ML model.
    All parameters are required for prediction.
    """
    color_aparente: float = Field(
        ...,
        ge=0.0,
        le=1000.0,
        description="Apparent color (UPC)"
    )
    turbiedad: float = Field(
        ...,
        ge=0.0,
        le=1000.0,
        description="Turbidity (NTU)"
    )
    ph: float = Field(
        ...,
        ge=0.0,
        le=14.0,
        description="pH value"
    )
    cloro_residual_libre: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Free residual chlorine (mg/L)"
    )
    cloruros: float = Field(
        ...,
        ge=0.0,
        le=1000.0,
        description="Chlorides (mg/L)"
    )
    nitritos: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Nitrites (mg/L)"
    )
    coliformes_totales: float = Field(
        ...,
        ge=0.0,
        le=100000.0,
        description="Total coliforms (CFU/100mL)"
    )
    e_coli: float = Field(
        ...,
        ge=0.0,
        le=100000.0,
        description="E. coli (CFU/100mL)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "color_aparente": 5.0,
                "turbiedad": 2.5,
                "ph": 7.2,
                "cloro_residual_libre": 0.8,
                "cloruros": 15.0,
                "nitritos": 0.01,
                "coliformes_totales": 0.0,
                "e_coli": 0.0
            }
        }


class PredictionResponse(BaseModel):
    """
    Response schema for IRCA prediction.
    
    Contains predicted IRCA value, risk level, and model confidence.
    """
    irca_predicted: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Predicted IRCA value (0-100)"
    )
    nivel_riesgo: str = Field(
        ...,
        description="Risk level classification"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence (R² score)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "irca_predicted": 12.35,
                "nivel_riesgo": "BAJO",
                "confidence": 0.9914
            }
        }


class BatchPredictionRequest(BaseModel):
    """
    Request schema for batch prediction endpoint.
    
    Accepts multiple samples for prediction at once.
    """
    samples: List[PredictionRequest] = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="List of water quality samples (max 1000)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "samples": [
                    {
                        "color_aparente": 5.0,
                        "turbiedad": 2.5,
                        "ph": 7.2,
                        "cloro_residual_libre": 0.8,
                        "cloruros": 15.0,
                        "nitritos": 0.01,
                        "coliformes_totales": 0.0,
                        "e_coli": 0.0
                    },
                    {
                        "color_aparente": 8.0,
                        "turbiedad": 4.0,
                        "ph": 6.8,
                        "cloro_residual_libre": 0.5,
                        "cloruros": 20.0,
                        "nitritos": 0.02,
                        "coliformes_totales": 10.0,
                        "e_coli": 2.0
                    }
                ]
            }
        }


class BatchPredictionResponse(BaseModel):
    """
    Response schema for batch prediction.
    
    Contains list of predictions matching input samples.
    """
    predictions: List[PredictionResponse] = Field(
        ...,
        description="List of predictions"
    )
    total_samples: int = Field(
        ...,
        description="Total number of samples processed"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "predictions": [
                    {
                        "irca_predicted": 12.35,
                        "nivel_riesgo": "BAJO",
                        "confidence": 0.9914
                    },
                    {
                        "irca_predicted": 18.67,
                        "nivel_riesgo": "MEDIO",
                        "confidence": 0.9914
                    }
                ],
                "total_samples": 2
            }
        }


class ModelInfoResponse(BaseModel):
    """
    Response schema for model information endpoint.
    
    Provides metadata about the loaded model.
    """
    model_class: str = Field(..., description="Model type/class")
    parameters: dict = Field(..., description="Model hyperparameters")
    feature_names: List[str] = Field(..., description="Input feature names")
    metrics: dict = Field(..., description="Model performance metrics")
    n_features: int = Field(..., description="Number of input features")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_class": "RandomForestRegressor",
                "parameters": {
                    "n_estimators": 100,
                    "random_state": 42
                },
                "feature_names": [
                    "resultado_Color_Aparente",
                    "resultado_Turbiedad",
                    "resultado_Ph",
                    "resultado_Cloro_Residual_Libre",
                    "resultado_Cloruros",
                    "resultado_Nitritos",
                    "resultado_Coliformes_Totales",
                    "resultado_E_Coli"
                ],
                "metrics": {
                    "r2": 0.9914,
                    "rmse": 0.0932,
                    "mae": 0.0253
                },
                "n_features": 8
            }
        }
