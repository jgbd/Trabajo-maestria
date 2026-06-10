"""
IRCA Prediction Service

Loads and uses the trained RandomForestRegressor model to predict IRCA values
based on water quality parameters.

Model Features (in order):
1. resultado_Color_Aparente
2. resultado_Turbiedad
3. resultado_Ph
4. resultado_Cloro_Residual_Libre
5. resultado_Cloruros
6. resultado_Nitritos
7. resultado_Coliformes_Totales
8. resultado_E_Coli

Model Performance:
- R² Score: 0.9914 (99.14% variance explained)
- RMSE: 0.093
- MAE: 0.025
- MAPE: 6.58%
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

# Model path
MODEL_PATH = Path(__file__).parent.parent / "llms" / "modelo_irca_best.joblib"

# Global model cache
_model_cache = None


def load_model() -> Dict:
    """
    Load the trained IRCA prediction model from disk.
    Uses caching to avoid reloading on every prediction.
    
    Returns:
        dict: Model dictionary containing:
            - modelo: The trained RandomForestRegressor
            - scaler_X: StandardScaler for input features
            - scaler_y: StandardScaler for target variable
            - feature_names: List of feature names in correct order
            - metadata: Model metadata and metrics
    """
    global _model_cache
    
    if _model_cache is None:
        try:
            logger.info(f"Loading IRCA prediction model from {MODEL_PATH}")
            _model_cache = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully")
            logger.info(f"Model type: {_model_cache['metadata']['model_class']}")
            logger.info(f"Features: {_model_cache['feature_names']}")
            logger.info(f"R² Score: {_model_cache['metadata']['metricas']['r2']:.4f}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Could not load prediction model: {e}")
    
    return _model_cache


def predict_irca(
    color_aparente: float,
    turbiedad: float,
    ph: float,
    cloro_residual_libre: float,
    cloruros: float,
    nitritos: float,
    coliformes_totales: float,
    e_coli: float
) -> Dict[str, float]:
    """
    Predict IRCA value based on water quality parameters.
    
    Args:
        color_aparente: Apparent color (UPC)
        turbiedad: Turbidity (NTU)
        ph: pH value
        cloro_residual_libre: Free residual chlorine (mg/L)
        cloruros: Chlorides (mg/L)
        nitritos: Nitrites (mg/L)
        coliformes_totales: Total coliforms (CFU/100mL)
        e_coli: E. coli (CFU/100mL)
    
    Returns:
        dict: Prediction result containing:
            - irca_predicted: Predicted IRCA value (0-100)
            - nivel_riesgo: Risk level classification
            - confidence: Model confidence (R² score)
    """
    # Load model
    model_data = load_model()
    model = model_data['modelo']
    scaler_X = model_data['scaler_X']
    scaler_y = model_data['scaler_y']
    
    # Prepare input features in correct order
    features = np.array([[
        color_aparente,
        turbiedad,
        ph,
        cloro_residual_libre,
        cloruros,
        nitritos,
        coliformes_totales,
        e_coli
    ]])
    
    # Scale input features
    features_scaled = scaler_X.transform(features)
    
    # Make prediction (scaled)
    prediction_scaled = model.predict(features_scaled)
    
    # Inverse transform to get actual IRCA value
    irca_predicted = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1))[0][0]
    
    # Ensure IRCA is within valid range [0, 100]
    irca_predicted = max(0.0, min(100.0, irca_predicted))
    
    # Determine risk level based on IRCA thresholds
    if irca_predicted > 80:
        nivel_riesgo = "INVIABLE"
    elif irca_predicted > 35:
        nivel_riesgo = "ALTO"
    elif irca_predicted > 14:
        nivel_riesgo = "MEDIO"
    elif irca_predicted > 5:
        nivel_riesgo = "BAJO"
    else:
        nivel_riesgo = "SIN RIESGO"
    
    return {
        "irca_predicted": round(irca_predicted, 2),
        "nivel_riesgo": nivel_riesgo,
        "confidence": round(model_data['metadata']['metricas']['r2'], 4)
    }


def predict_irca_batch(samples: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """
    Predict IRCA values for multiple samples at once.
    More efficient than calling predict_irca() multiple times.
    
    Args:
        samples: List of sample dictionaries with water quality parameters
    
    Returns:
        list: List of prediction dictionaries
    """
    # Load model once
    model_data = load_model()
    model = model_data['modelo']
    scaler_X = model_data['scaler_X']
    scaler_y = model_data['scaler_y']
    
    # Prepare all features
    features_list = []
    for sample in samples:
        features_list.append([
            sample['color_aparente'],
            sample['turbiedad'],
            sample['ph'],
            sample['cloro_residual_libre'],
            sample['cloruros'],
            sample['nitritos'],
            sample['coliformes_totales'],
            sample['e_coli']
        ])
    
    features = np.array(features_list)
    
    # Scale and predict
    features_scaled = scaler_X.transform(features)
    predictions_scaled = model.predict(features_scaled)
    predictions = scaler_y.inverse_transform(predictions_scaled.reshape(-1, 1)).flatten()
    
    # Prepare results
    results = []
    for irca_value in predictions:
        # Ensure within range
        irca_value = max(0.0, min(100.0, irca_value))
        
        # Determine risk level
        if irca_value > 80:
            nivel_riesgo = "INVIABLE"
        elif irca_value > 35:
            nivel_riesgo = "ALTO"
        elif irca_value > 14:
            nivel_riesgo = "MEDIO"
        elif irca_value > 5:
            nivel_riesgo = "BAJO"
        else:
            nivel_riesgo = "SIN RIESGO"
        
        results.append({
            "irca_predicted": round(irca_value, 2),
            "nivel_riesgo": nivel_riesgo,
            "confidence": round(model_data['metadata']['metricas']['r2'], 4)
        })
    
    return results


def get_model_info() -> Dict:
    """
    Get information about the loaded model.
    
    Returns:
        dict: Model metadata including features, metrics, and configuration
    """
    model_data = load_model()
    return {
        "model_class": model_data['metadata']['model_class'],
        "parameters": model_data['metadata']['params'],
        "feature_names": model_data['feature_names'],
        "metrics": model_data['metadata']['metricas'],
        "n_features": len(model_data['feature_names'])
    }
