from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.schemas.job import JobResponse, JobCreate, JobUpdate, ApiResponse
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=ApiResponse[JobResponse], status_code=status.HTTP_201_CREATED)
def create_job(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = JobService.create_job(db=db, job=JobCreate())
    background_tasks.add_task(JobService.process_job, str(job.id))
    return ApiResponse(
        data=JobResponse.model_validate(job), 
        message="Job created and processing started"
    )

@router.get("/", response_model=ApiResponse[List[JobResponse]])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = JobService.get_jobs(db, skip=skip, limit=limit)
    return ApiResponse(
        data=[JobResponse.model_validate(job) for job in jobs],
        message=f"Retrieved {len(jobs)} jobs"
    )

@router.get("/{job_id}", response_model=ApiResponse[JobResponse])
def read_job(job_id: UUID, db: Session = Depends(get_db)):
    db_job = JobService.get_job(db, job_id=str(job_id))
    if db_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Job with ID {job_id} not found"
        )
    return ApiResponse(
        data=JobResponse.model_validate(db_job),
        message="Job details retrieved"
    )

@router.patch("/{job_id}", response_model=ApiResponse[JobResponse])
def update_job(job_id: UUID, job_update: JobUpdate, db: Session = Depends(get_db)):
    db_job = JobService.update_job(db, job_id=str(job_id), job_update=job_update)
    if db_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Job with ID {job_id} not found"
        )
    return ApiResponse(
        data=JobResponse.model_validate(db_job),
        message="Job updated successfully"
    )

@router.delete("/{job_id}", response_model=ApiResponse)
def delete_job(job_id: UUID, db: Session = Depends(get_db)):
    success = JobService.delete_job(db, job_id=str(job_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Job with ID {job_id} not found"
        )
    return ApiResponse(
        success=True,
        message=f"Job {job_id} deleted successfully"
    )
