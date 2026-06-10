"""
Security Utilities

API key verification for admin operations.
"""

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Define API key header
API_KEY_HEADER = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


def verify_admin_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """
    Verify admin API key for write operations.
    
    This dependency should be used on all POST, PUT, DELETE endpoints
    that modify data. It checks for a valid API key in the X-Admin-API-Key header.
    
    Args:
        api_key: API key from request header
        
    Returns:
        The verified API key string
        
    Raises:
        HTTPException: 401 if key is missing, 403 if invalid
        
    Usage:
        @router.post("/", dependencies=[Depends(verify_admin_api_key)])
        def create_resource(...):
            # API key is verified before this function executes
            pass
            
        # Or for access in function:
        def create_resource(api_key: str = Depends(verify_admin_api_key)):
            # api_key variable contains the verified key
            pass
    """
    if api_key is None:
        logger.warning("API key missing in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Include X-Admin-API-Key header for admin operations.",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    if api_key != settings.ADMIN_API_KEY:
        logger.warning(f"Invalid API key attempt: {api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key. Access denied."
        )
    
    logger.info("Admin API key verified successfully")
    return api_key
