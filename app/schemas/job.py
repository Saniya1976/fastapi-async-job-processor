from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Generic, TypeVar, List
from uuid import UUID

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """
    The Standard Response Wrapper for every API call.
    Helps frontend developers by providing a consistent JSON structure.
    """
    success: bool = Field(True, description="Indicates if the request was handled successfully")
    data: Optional[T] = Field(None, description="The actual payload (Job object, list, etc.)")
    message: str = Field("Operation successful", description="A human-readable status message")

class JobBase(BaseModel):
    """Common attributes for Jobs."""
    pass

class JobCreate(JobBase):
    """
    Fields required to initiate a new job. 
    Currently empty but serves as an extension point for job inputs.
    """
    pass

class JobUpdate(BaseModel):
    """Fields that can be updated after a job is created."""
    status: Optional[str] = Field(None, description="The new status of the job")
    result: Optional[str] = Field(None, description="The result data for the job")

class JobResponse(JobBase):
    """
    The detailed view of a job record returned to the user.
    """
    id: UUID = Field(..., description="Unique Job Identifier")
    status: str = Field(..., description="Current state: pending | in_progress | completed | failed")
    result: Optional[str] = Field(None, description="Outcomes or error logs from the worker")
    created_at: datetime
    updated_at: datetime

    # Tell Pydantic to read data from SQLAlchemy ORM models
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "result": "Task finished in 7.5s",
                "created_at": "2024-03-20T12:00:00Z",
                "updated_at": "2024-03-20T12:07:30Z"
            }
        }
    )
