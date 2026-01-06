"""
Resource-related Pydantic schemas for request/response validation.

This module defines all schemas related to educational resources,
study materials, and content management.
"""

from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ----------- Enums -----------


class ResourceType(str, Enum):
    """Resource type enumeration."""
    VIDEO = "video"
    PDF = "pdf"
    DOCUMENT = "document"
    LINK = "link"
    SLIDE = "slide"
    CODE = "code"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    OTHER = "other"


class ResourceVisibility(str, Enum):
    """Resource visibility/access level."""
    PUBLIC = "public"
    COURSE = "course"
    ROLE_SPECIFIC = "role_specific"
    PRIVATE = "private"


# ----------- Request Schemas -----------


class ResourceCreate(BaseModel):
    """
    Schema for creating a new resource.

    Attributes:
        title: Resource title
        description: Detailed description
        resource_type: Type of resource
        url: URL to the resource (if external)
        file_path: Path to uploaded file (if internal)
        course_id: Associated course
        visibility: Access level
        tags: Tags for searchability

    Example:
        {
            "title": "Introduction to Python",
            "description": "Comprehensive Python tutorial",
            "resource_type": "video",
            "url": "https://example.com/python-intro",
            "course_id": 1,
            "visibility": "course",
            "tags": ["python", "programming", "beginners"]
        }
    """
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Resource title"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed description"
    )
    resource_type: ResourceType = Field(
        ...,
        description="Type of resource"
    )
    url: Optional[HttpUrl] = Field(
        None,
        description="External resource URL"
    )
    file_path: Optional[str] = Field(
        None,
        description="Internal file path"
    )
    course_id: Optional[int] = Field(
        None,
        description="Associated course ID"
    )
    visibility: ResourceVisibility = Field(
        default=ResourceVisibility.PUBLIC,
        description="Access level"
    )
    tags: Optional[List[str]] = Field(
        default=[],
        description="Tags for searchability"
    )


class ResourceUpdate(BaseModel):
    """
    Schema for updating an existing resource.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated title
        description: Updated description
        resource_type: Updated type
        url: Updated URL
        visibility: Updated visibility
        tags: Updated tags
        is_active: Activate/deactivate resource

    Example:
        {
            "title": "Updated Python Tutorial",
            "visibility": "public"
        }
    """
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    resource_type: Optional[ResourceType] = None
    url: Optional[HttpUrl] = None
    visibility: Optional[ResourceVisibility] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


# ----------- Response Schemas -----------


class ResourceResponse(BaseModel):
    """
    Schema for resource data in API responses.

    Attributes:
        id: Resource unique identifier
        title: Resource title
        description: Resource description
        resource_type: Type of resource
        url: Resource URL (if external)
        file_path: File path (if internal)
        course_id: Associated course
        visibility: Access level
        tags: Resource tags
        created_by_id: ID of creator
        created_by_name: Name of creator
        download_count: Number of downloads
        view_count: Number of views
        is_active: Whether resource is active
        created_at: Creation timestamp
        updated_at: Last update timestamp

    Example:
        {
            "id": 1,
            "title": "Introduction to Python",
            "resource_type": "video",
            "url": "https://example.com/video",
            "created_by_name": "Dr. Smith",
            "download_count": 150,
            "created_at": "2025-01-15T10:30:00Z"
        }
    """
    id: int
    title: str
    description: Optional[str] = None
    resource_type: ResourceType
    url: Optional[str] = None
    file_path: Optional[str] = None
    course_id: Optional[int] = None
    visibility: ResourceVisibility
    tags: List[str] = []
    created_by_id: int
    created_by_name: Optional[str] = None
    download_count: int = 0
    view_count: int = 0
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ResourceListResponse(BaseModel):
    """
    Schema for paginated list of resources.

    Attributes:
        total: Total number of resources
        page: Current page number
        page_size: Number of items per page
        total_pages: Total number of pages
        resources: List of resources

    Example:
        {
            "total": 50,
            "page": 1,
            "page_size": 10,
            "total_pages": 5,
            "resources": [...]
        }
    """
    total: int = Field(..., description="Total number of resources")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    resources: List[ResourceResponse] = Field(
        default=[],
        description="List of resources"
    )


class ResourceStats(BaseModel):
    """
    Schema for resource statistics.

    Attributes:
        total_resources: Total number of resources
        resources_by_type: Breakdown by type
        most_viewed: Most viewed resources
        most_downloaded: Most downloaded resources
        recent_uploads: Recently uploaded resources

    Example:
        {
            "total_resources": 100,
            "resources_by_type": {
                "video": 30,
                "pdf": 40,
                "link": 30
            }
        }
    """
    total_resources: int
    resources_by_type: dict = Field(
        default={},
        description="Resource count by type"
    )
    most_viewed: List[ResourceResponse] = Field(
        default=[],
        max_length=5,
        description="Top 5 most viewed"
    )
    most_downloaded: List[ResourceResponse] = Field(
        default=[],
        max_length=5,
        description="Top 5 most downloaded"
    )
