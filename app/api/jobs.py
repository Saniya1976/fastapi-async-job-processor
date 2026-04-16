from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.schemas.job import JobResponse, JobCreate, JobUpdate, ApiResponse
from app.services.job_service import JobService

# Instantiate the router with a meaningful prefix
router = APIRouter(prefix="/jobs", tags=["Async Job Management"])

@router.post("/", response_model=ApiResponse[JobResponse], status_code=status.HTTP_201_CREATED)
def post_new_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    ENDPOINT: Create a new Job
    1. Creates a 'pending' record in the database.
    2. Offloads the 'heavy work' to a background task.
    3. Returns the Job ID immediately to the user.
    """
    # Create the db record
    new_job = JobService.create_new_job(db=db, job_data=JobCreate())
    
    # Start the background work without blocking the response
    background_tasks.add_task(JobService.run_job_processing_logic, str(new_job.id))
    
    return ApiResponse(
        data=JobResponse.model_validate(new_job), 
        message="Job successfully queued for processing"
    )

@router.get("/", response_model=ApiResponse[List[JobResponse]])
def get_all_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ENDPOINT: Fetch all jobs
    Sorted by latest first. Useful for a dashboard view.
    """
    jobs_list = JobService.get_all_jobs(db, skip=skip, limit=limit)
    return ApiResponse(
        data=[JobResponse.model_validate(job) for job in jobs_list],
        message=f"Successfully retrieved {len(jobs_list)} jobs"
    )

@router.get("/{job_id}", response_model=ApiResponse[JobResponse])
def get_job_status(job_id: UUID, db: Session = Depends(get_db)):
    """
    ENDPOINT: Check status of a specific job
    Users can poll this to see if the status has changed from 'pending' to 'completed'.
    """
    job = JobService.get_job_by_id(db, job_id=str(job_id))
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Job with ID {job_id} not found in the system"
        )
    return ApiResponse(
        data=JobResponse.model_validate(job),
        message="Job details retrieved successfully"
    )

@router.patch("/{job_id}", response_model=ApiResponse[JobResponse])
def patch_job_details(job_id: UUID, job_update: JobUpdate, db: Session = Depends(get_db)):
    """
    ENDPOINT: Manually update a job
    Used for administrative corrections or status overrides.
    """
    updated_job = JobService.update_job_entry(db, job_id=str(job_id), job_update=job_update)
    if updated_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Unable to update. Job with ID {job_id} not found"
        )
    return ApiResponse(
        data=JobResponse.model_validate(updated_job),
        message="Job record has been updated"
    )

@router.delete("/{job_id}", response_model=ApiResponse)
def delete_job_details(job_id: UUID, db: Session = Depends(get_db)):
    """
    ENDPOINT: Delete a job
    Permanently removes the job record from history.
    """
    was_deleted = JobService.delete_job_record(db, job_id=str(job_id))
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Unable to delete. Job with ID {job_id} not found"
        )
    return ApiResponse(
        success=True,
        message=f"Job {job_id} has been permanently deleted"
    )
