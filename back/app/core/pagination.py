"""
Pagination Models and Utilities

Provides standardized pagination for API endpoints to prevent
loading large datasets that could crash the application.
"""

from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field, field_validator
from app.core.constants import APIConstants


T = TypeVar('T')


class PaginationParams(BaseModel):
    """
    Query parameters for pagination.
    
    Used as a dependency in route handlers to extract and validate
    pagination parameters from the request.
    """
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (1-indexed)"
    )
    page_size: int = Field(
        default=APIConstants.DEFAULT_PAGE_SIZE,
        ge=1,
        le=APIConstants.MAX_PAGE_SIZE,
        description=f"Number of items per page (max: {APIConstants.MAX_PAGE_SIZE})"
    )
    
    @field_validator('page_size')
    @classmethod
    def validate_page_size(cls, v: int) -> int:
        """Ensure page_size doesn't exceed maximum."""
        if v > APIConstants.MAX_PAGE_SIZE:
            return APIConstants.MAX_PAGE_SIZE
        return v
    
    @property
    def skip(self) -> int:
        """Calculate the number of records to skip."""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get the limit for the query."""
        return self.page_size


class PaginationMeta(BaseModel):
    """
    Metadata about the paginated response.
    
    Includes information about current page, total pages, and item counts.
    """
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    total_items: int = Field(description="Total number of items across all pages")
    total_pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_previous: bool = Field(description="Whether there is a previous page")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.
    
    Wraps any list of items with pagination metadata.
    
    Example:
        ```python
        @router.get("/items", response_model=PaginatedResponse[ItemModel])
        def get_items(pagination: PaginationParams = Depends()):
            items = get_items_from_db(pagination.skip, pagination.limit)
            total = count_items_in_db()
            return paginate(items, total, pagination)
        ```
    """
    items: List[T] = Field(description="List of items for the current page")
    meta: PaginationMeta = Field(description="Pagination metadata")


def paginate(
    items: List[T],
    total: int,
    params: PaginationParams
) -> PaginatedResponse[T]:
    """
    Create a paginated response from a list of items.
    
    Args:
        items: List of items for the current page
        total: Total number of items across all pages
        params: Pagination parameters from the request
        
    Returns:
        PaginatedResponse with items and metadata
        
    Example:
        ```python
        items = db.query(Model).offset(params.skip).limit(params.limit).all()
        total = db.query(Model).count()
        return paginate(items, total, params)
        ```
    """
    total_pages = (total + params.page_size - 1) // params.page_size  # Ceiling division
    
    meta = PaginationMeta(
        page=params.page,
        page_size=params.page_size,
        total_items=total,
        total_pages=total_pages,
        has_next=params.page < total_pages,
        has_previous=params.page > 1
    )
    
    return PaginatedResponse(items=items, meta=meta)


class ErrorDetail(BaseModel):
    """
    Detailed error information.
    
    Provides structured error details for validation errors or specific issues.
    """
    field: Optional[str] = Field(
        default=None,
        description="Field name that caused the error (for validation errors)"
    )
    message: str = Field(description="Human-readable error message")
    code: Optional[str] = Field(
        default=None,
        description="Machine-readable error code"
    )


class ErrorResponse(BaseModel):
    """
    Standardized error response model.
    
    Used for all API error responses to provide consistent error format.
    """
    error: str = Field(description="Error type or title")
    message: str = Field(description="Detailed error message")
    details: Optional[List[ErrorDetail]] = Field(
        default=None,
        description="List of detailed errors (for validation errors)"
    )
    path: Optional[str] = Field(
        default=None,
        description="Request path where error occurred"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation Error",
                "message": "Invalid input parameters",
                "details": [
                    {
                        "field": "page_size",
                        "message": "Page size must be between 1 and 100",
                        "code": "value_error"
                    }
                ],
                "path": "/api/resultados"
            }
        }
