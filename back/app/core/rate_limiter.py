"""
Rate Limiting Configuration

Implements request rate limiting using slowapi to prevent API abuse.
Tracks requests by IP address for security monitoring.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


def get_remote_address_with_logging(request: Request) -> str:
    """
    Get remote IP address and log for security monitoring.
    
    This function is used as the key_func for slowapi rate limiting.
    It extracts the client IP address and logs it for abuse detection.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Client IP address as string
    """
    ip_address = get_remote_address(request)
    
    # Log rate-limited IPs (only when near limit)
    # This will be enhanced in Phase 3 with comprehensive logging
    
    return ip_address


# Initialize rate limiter
# default_limits applies to all endpoints unless overridden with @limiter.limit()
limiter = Limiter(
    key_func=get_remote_address_with_logging,
    default_limits=["100/hour", "30/minute"],  # Conservative defaults
    headers_enabled=True  # Include rate limit info in response headers
)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Custom handler for rate limit exceeded errors.
    
    Returns user-friendly error message with retry information.
    Logs the event with IP address for security monitoring.
    
    Args:
        request: FastAPI request object
        exc: RateLimitExceeded exception
        
    Returns:
        JSONResponse with 429 status code
    """
    ip_address = get_remote_address(request)
    logger.warning(f"Rate limit exceeded for IP {ip_address} on {request.url.path}")
    
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
            "detail": str(exc.detail),
            "path": request.url.path
        },
        headers={
            "Retry-After": "60"  # Suggest retry after 60 seconds
        }
    )
