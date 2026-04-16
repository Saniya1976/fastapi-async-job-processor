import uuid
from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
