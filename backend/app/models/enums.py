"""
Shared enumeration types for the AURA application.

This module defines common enums used across different models.
"""

from enum import Enum


class CategoryEnum(str, Enum):
    """Categories for knowledge sources."""
    ADMISSION = "Admission"
    COURSES = "Courses"
    PLACEMENT = "Placement"
    QUERIES = "Queries"
    QUIZZES = "Quizzes"
    ASSIGNMENTS = "Assignments"
    PARADOX = "Paradox"


class TaskTypeEnum(str, Enum):
    """Types of background tasks."""
    EMBEDDING = "EMBEDDING"
    QUERY = "QUERY"
    REPORT_GENERATION = "REPORT_GENERATION"
    DATA_PROCESSING = "DATA_PROCESSING"
    EMAIL = "EMAIL"


class TaskStatusEnum(str, Enum):
    """Status of background tasks."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SourceTypeEnum(str, Enum):
    """Source type for queries (chat or call)."""
    CHAT = "CHAT"
    CALL = "CALL"


class CallStatusEnum(str, Enum):
    """Status of voice calls."""
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    MISSED = "MISSED"
