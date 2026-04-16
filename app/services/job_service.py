import asyncio
import random
import logging
from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate
from app.db.database import SessionLocal

# Setup logger for this service
logger = logging.getLogger(__name__)

class JobService:
    @staticmethod
    def get_job_by_id(db: Session, job_id: str):
        """
        Retrieves a job from the database using its unique UUID.
        This is used by the GET /jobs/{id} endpoint.
        """
        return db.query(Job).filter(Job.id == str(job_id)).first()

    @staticmethod
    def get_all_jobs(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieves a list of jobs, sorted by the most recently created first.
        Pagination is supported via skip and limit.
        """
        return db.query(Job).order_by(Job.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_new_job(db: Session, job_data: JobCreate):
        """
        Initializes a new job entry in the database.
        Default state: "pending"
        """
        db_job = Job()
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        logger.info(f"New job created in database with ID: {db_job.id}")
        return db_job

    @staticmethod
    async def run_job_processing_logic(job_id: str):
        """
        This is the core background task logic.
        
        Lifecycle Explanation:
        1. PENDING (Initial) -> The job has been recorded but not started.
        2. IN_PROGRESS -> The worker has picked up the job and is currently 'thinking'.
        3. COMPLETED/FAILED -> Final states once the logic finishes or crashes.
        
        This function runs independently of the API request, allowing the user
        to receive their Job ID immediately while the work continues here.
        """
        db = SessionLocal()
        try:
            # 1. Fetch the job from DB to begin processing
            db_job = db.query(Job).filter(Job.id == str(job_id)).first()
            if not db_job:
                logger.warning(f"Background task attempted for non-existent Job ID: {job_id}")
                return
            
            # 2. Update status to 'in_progress'
            logger.info(f"Job {job_id}: Processing started")
            db_job.status = "in_progress"
            db.commit()
            
            # --- SIMULATION START ---
            # This simulates long-running background processing (like image resizing or data crunching)
            # We use a random delay between 5 to 10 seconds.
            delay = random.uniform(5, 10)
            await asyncio.sleep(delay)
            
            # Randomly determine if the job 'succeeded' or 'failed' to show robust error handling
            # 80% chance of success
            job_was_successful = random.random() < 0.8
            
            if job_was_successful:
                db_job.status = "completed"
                db_job.result = f"Task completed successfully after {delay:.2f} seconds."
                logger.info(f"Job {job_id}: Completed successfully")
            else:
                db_job.status = "failed"
                db_job.result = f"Task simulation failed after {delay:.2f} seconds."
                logger.info(f"Job {job_id}: Failed during execution")
            # --- SIMULATION END ---

            # 3. Save final status and results
            db.commit()
            
        except Exception as error:
            # If any unexpected code error occurs, ensure the job is marked as 'failed' instead of hanging
            db_job = db.query(Job).filter(Job.id == str(job_id)).first()
            if db_job:
                db_job.status = "failed"
                db_job.result = f"Unexpected system error: {str(error)}"
                db.commit()
            logger.error(f"Critical error in background worker for job {job_id}: {str(error)}", exc_info=True)
            
        finally:
            # Always close the database connection when the background task is done
            db.close()

    @staticmethod
    def update_job_entry(db: Session, job_id: str, job_update: JobUpdate):
        """
        Updates specific fields of a job record.
        Mainly used for administrative or internal state overrides.
        """
        db_job = db.query(Job).filter(Job.id == str(job_id)).first()
        if db_job:
            update_data = job_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_job, key, value)
            db.commit()
            db.refresh(db_job)
            logger.info(f"Job {job_id}: Manually updated to {db_job.status}")
        return db_job

    @staticmethod
    def delete_job_record(db: Session, job_id: str):
        """
        Permanently removes a job record from the database.
        """
        db_job = db.query(Job).filter(Job.id == str(job_id)).first()
        if db_job:
            db.delete(db_job)
            db.commit()
            logger.info(f"Job {job_id}: Deleted from system")
            return True
        return False
