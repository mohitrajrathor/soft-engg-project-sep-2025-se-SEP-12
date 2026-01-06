"""
Announcement-related Pydantic schemas for request/response validation.

This module defines all schemas related to announcements and notifications.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ----------- Enums -----------


class AnnouncementType(str, Enum):
    """Announcement type enumeration."""
    GENERAL = "general"
    URGENT = "urgent"
    DEADLINE = "deadline"
    EVENT = "event"
    MAINTENANCE = "maintenance"
    UPDATE = "update"


class AnnouncementTarget(str, Enum):
    """Target audience for announcements."""
    ALL = "all"
    STUDENTS = "students"
    TAS = "tas"
    INSTRUCTORS = "instructors"
    COURSE_SPECIFIC = "course_specific"


# ----------- Request Schemas -----------


class AnnouncementCreate(BaseModel):
    """
    Schema for creating a new announcement.

    Attributes:
        title: Announcement title
        content: Announcement content
        announcement_type: Type of announcement
        target_audience: Who should see this announcement
        course_id: Course ID (if course-specific)
        expires_at: Expiration date (optional)
        is_pinned: Pin to top of announcements

    Example:
        {
            "title": "Midterm Exam Schedule",
            "content": "The midterm exam will be held on...",
            "announcement_type": "deadline",
            "target_audience": "students",
            "course_id": 1,
            "is_pinned": true
        }
    """
    title: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Announcement title"
    )
    content: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Announcement content"
    )
    announcement_type: AnnouncementType = Field(
        default=AnnouncementType.GENERAL,
        description="Type of announcement"
    )
    target_audience: AnnouncementTarget = Field(
        default=AnnouncementTarget.ALL,
        description="Target audience"
    )
    course_id: Optional[int] = Field(
        None,
        description="Course ID for course-specific announcements"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="Expiration date"
    )
    is_pinned: bool = Field(
        default=False,
        description="Pin announcement to top"
    )


class AnnouncementUpdate(BaseModel):
    """
    Schema for updating an existing announcement.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated title
        content: Updated content
        announcement_type: Updated type
        target_audience: Updated target audience
        expires_at: Updated expiration date
        is_pinned: Pin/unpin announcement
        is_active: Activate/deactivate announcement

    Example:
        {
            "is_pinned": true,
            "expires_at": "2025-02-01T00:00:00Z"
        }
    """
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=10, max_length=5000)
    announcement_type: Optional[AnnouncementType] = None
    target_audience: Optional[AnnouncementTarget] = None
    expires_at: Optional[datetime] = None
    is_pinned: Optional[bool] = None
    is_active: Optional[bool] = None


# ----------- Response Schemas -----------


class AnnouncementResponse(BaseModel):
    """
    Schema for announcement data in API responses.

    Attributes:
        id: Announcement unique identifier
        title: Announcement title
        content: Announcement content
        announcement_type: Type of announcement
        target_audience: Target audience
        course_id: Associated course (if any)
        created_by_id: ID of creator
        created_by_name: Name of creator
        created_by_role: Role of creator
        is_pinned: Whether announcement is pinned
        is_active: Whether announcement is active
        view_count: Number of views
        expires_at: Expiration date
        created_at: Creation timestamp
        updated_at: Last update timestamp

    Example:
        {
            "id": 1,
            "title": "Midterm Exam Schedule",
            "content": "The exam will be held...",
            "announcement_type": "deadline",
            "target_audience": "students",
            "created_by_name": "Dr. Smith",
            "is_pinned": true,
            "created_at": "2025-01-15T10:30:00Z"
        }
    """
    id: int
    title: str
    content: str
    announcement_type: AnnouncementType
    target_audience: AnnouncementTarget
    course_id: Optional[int] = None
    created_by_id: int
    created_by_name: Optional[str] = None
    created_by_role: Optional[str] = None
    is_pinned: bool = False
    is_active: bool = True
    view_count: int = 0
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AnnouncementListResponse(BaseModel):
    """
    Schema for paginated list of announcements.

    Attributes:
        total: Total number of announcements
        page: Current page number
        page_size: Number of items per page
        total_pages: Total number of pages
        announcements: List of announcements

    Example:
        {
            "total": 50,
            "page": 1,
            "page_size": 10,
            "total_pages": 5,
            "announcements": [...]
        }
    """
    total: int = Field(..., description="Total number of announcements")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    announcements: List[AnnouncementResponse] = Field(
        default=[],
        description="List of announcements"
    )
