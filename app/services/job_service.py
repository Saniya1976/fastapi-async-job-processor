import asyncio
import random
import logging
from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)

class JobService:
    @staticmethod
    def get_job(db: Session, job_id: str):
        return db.query(Job).filter(Job.id == str(job_id)).first()

    @staticmethod
    def get_jobs(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Job).order_by(Job.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_job(db: Session, job: JobCreate):
        db_job = Job()
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        logger.info(f"Job created: {db_job.id}")
        return db_job

    @staticmethod
    def update_job(db: Session, job_id: str, job_update: JobUpdate):
        db_job = db.query(Job).filter(Job.id == str(job_id)).first()
        if db_job:
            update_data = job_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_job, key, value)
            db.commit()
            db.refresh(db_job)
            logger.info(f"Job updated: {job_id} - status: {db_job.status}")
        return db_job

    @staticmethod
    def delete_job(db: Session, job_id: str):
        db_job = db.query(Job).filter(Job.id == str(job_id)).first()
        if db_job:
            db.delete(db_job)
            db.commit()
            logger.info(f"Job deleted: {job_id}")
            return True
        return False

    @staticmethod
    async def process_job(job_id: str):
        """Simulate a long running background task with random outcomes."""
        db = SessionLocal()
        try:
            # Update to in_progress
            db_job = db.query(Job).filter(Job.id == str(job_id)).first()
            if not db_job:
                logger.warning(f"Process job task started for non-existent job: {job_id}")
                return
            
            logger.info(f"Starting background processing for job: {job_id}")
            db_job.status = "in_progress"
            db.commit()
            
            # Simulate work with random duration (5-10 seconds)
            delay = random.uniform(5, 10)
            await asyncio.sleep(delay)
            
            # Randomly determine success (80% success rate)
            success = random.random() < 0.8
            
            if success:
                db_job.status = "completed"
                db_job.result = f"Task completed successfully after {delay:.2f}s"
                logger.info(f"Job completed successfully: {job_id}")
            else:
                db_job.status = "failed"
                db_job.result = f"Task failed after {delay:.2f}s due to random error"
                logger.info(f"Job failed (randomly): {job_id}")
            
            db.commit()
        except Exception as e:
            db_job = db.query(Job).filter(Job.id == str(job_id)).first()
            if db_job:
                db_job.status = "failed"
                db_job.result = f"Unexpected error: {str(e)}"
                db.commit()
            logger.error(f"Error processing job {job_id}: {str(e)}", exc_info=True)
        finally:
            db.close()
