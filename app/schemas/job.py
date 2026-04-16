from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Generic, TypeVar, List
from uuid import UUID

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    message: str = "Operation successful"

class JobBase(BaseModel):
    """Base schema for Job fields."""
    pass

class JobCreate(JobBase):
    """Schema for creating a new Job. Currently empty but allows for future inputs."""
    pass

class JobUpdate(BaseModel):
    """Schema for updating an existing Job."""
    status: Optional[str] = Field(None, description="The current status of the job")
    result: Optional[str] = Field(None, description="The result of the job execution")

class JobResponse(JobBase):
    """Schema for the Job response, following the clean architecture patterns."""
    id: UUID
    status: str
    result: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "pending",
                "result": None,
                "created_at": "2024-03-20T12:00:00Z",
                "updated_at": "2024-03-20T12:00:00Z"
            }
        }
    )
