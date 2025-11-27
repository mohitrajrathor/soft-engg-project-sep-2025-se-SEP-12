"""
Task model for AURA background job tracking.

This module defines the Task model for tracking asynchronous background tasks
like embedding generation, query processing, etc.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime
import uuid
from app.models.enums import TaskTypeEnum, TaskStatusEnum


class Task(Base):
    """
    Represents a background task (Celery job).

    Tracks status, progress, and results of async operations.
    """
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_type = Column(String, nullable=False)  # TaskTypeEnum value
    status = Column(String, nullable=False, default=TaskStatusEnum.PENDING.value)  # TaskStatusEnum value
    source_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_sources.id"), nullable=True)
    metadata_ = Column(Text)  # JSON string for additional task data
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    source = relationship("KnowledgeSource")

    # Indexes
    __table_args__ = (
        Index('ix_tasks_status_created', 'status', 'created_at'),
        Index('ix_tasks_type_status', 'task_type', 'status'),
    )
