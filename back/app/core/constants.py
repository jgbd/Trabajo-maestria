"""
IRCA Water Quality Risk Index Constants

This module defines risk level thresholds and enums used throughout
the application for water quality classification.
"""

from enum import Enum


class IRCARiskLevel(str, Enum):
    """
    IRCA risk level classifications based on Colombian water quality standards.
    
    Values represent the safety level of water for human consumption.
    """
    NO_RISK = "SIN RIESGO"
    LOW = "BAJO"
    MEDIUM = "MEDIO"
    HIGH = "ALTO"
    UNSANITARY = "INVIABLE SANITARIAMENTE"


class IRCARiskThresholds:
    """
    IRCA (Índice de Riesgo de la Calidad del Agua) threshold values.
    
    These thresholds are used to classify water quality based on the IRCA index.
    IRCA ranges from 0 to 100, where:
    - Lower values indicate better water quality
    - Higher values indicate greater health risks
    
    Reference: Colombian water quality standards (Decree 1575 of 2007)
    """
    
    # Threshold values
    UNSANITARY = 80  # > 80: Water is not safe for consumption
    HIGH = 35        # > 35: High risk - significant quality issues
    MEDIUM = 14      # > 14: Medium risk - moderate quality concerns
    LOW = 5          # > 5: Low risk - minor quality issues
    # <= 5: No risk - water is safe for consumption
    
    @classmethod
    def get_risk_level(cls, irca_value: float) -> IRCARiskLevel:
        """
        Calculate risk level classification from IRCA numeric value.
        
        Args:
            irca_value: IRCA index value (0-100)
            
        Returns:
            IRCARiskLevel enum corresponding to the IRCA value
            
        Example:
            >>> IRCARiskThresholds.get_risk_level(12.5)
            <IRCARiskLevel.LOW: 'BAJO'>
            
            >>> IRCARiskThresholds.get_risk_level(85.0)
            <IRCARiskLevel.UNSANITARY: 'INVIABLE SANITARIAMENTE'>
        """
        if irca_value > cls.UNSANITARY:
            return IRCARiskLevel.UNSANITARY
        elif irca_value > cls.HIGH:
            return IRCARiskLevel.HIGH
        elif irca_value > cls.MEDIUM:
            return IRCARiskLevel.MEDIUM
        elif irca_value > cls.LOW:
            return IRCARiskLevel.LOW
        return IRCARiskLevel.NO_RISK


# API Configuration Constants
class APIConstants:
    """General API configuration constants"""
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 100
    DEFAULT_API_PREFIX = "/api"
    DEFAULT_YEAR_START = 2020
    DEFAULT_YEAR_END = 2024
