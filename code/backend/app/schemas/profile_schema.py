"""
Profile-related Pydantic schemas for request/response validation.

This module defines all schemas related to user profiles and preferences.
"""

from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from datetime import datetime, date
from typing import Optional, List


# ----------- Request Schemas -----------


class ProfileCreate(BaseModel):
    """
    Schema for creating/completing user profile.

    Attributes:
        full_name: User's full name
        bio: Short biography
        avatar_url: Profile picture URL
        phone: Contact phone number
        date_of_birth: Date of birth
        department: Department/field of study
        year_of_study: Current year (for students)
        interests: List of interests/topics
        social_links: Social media links

    Example:
        {
            "full_name": "John Doe",
            "bio": "Computer Science student interested in AI",
            "department": "Computer Science",
            "year_of_study": 2,
            "interests": ["Machine Learning", "Python", "Data Science"]
        }
    """
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's full name"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="Short biography"
    )
    avatar_url: Optional[HttpUrl] = Field(
        None,
        description="Profile picture URL"
    )
    phone: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{1,14}$",
        description="Contact phone number"
    )
    date_of_birth: Optional[date] = Field(
        None,
        description="Date of birth"
    )
    department: Optional[str] = Field(
        None,
        max_length=100,
        description="Department/field"
    )
    year_of_study: Optional[int] = Field(
        None,
        ge=1,
        le=6,
        description="Current year of study"
    )
    interests: Optional[List[str]] = Field(
        default=[],
        description="Interests/topics"
    )
    social_links: Optional[dict] = Field(
        default={},
        description="Social media links"
    )


class ProfileUpdate(BaseModel):
    """
    Schema for updating user profile.

    All fields are optional - only provided fields will be updated.

    Example:
        {
            "bio": "Updated bio",
            "interests": ["AI", "ML", "Deep Learning"]
        }
    """
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[HttpUrl] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    date_of_birth: Optional[date] = None
    department: Optional[str] = Field(None, max_length=100)
    year_of_study: Optional[int] = Field(None, ge=1, le=6)
    interests: Optional[List[str]] = None
    social_links: Optional[dict] = None


# ----------- Response Schemas -----------


class ProfileResponse(BaseModel):
    """
    Schema for user profile data in API responses.

    Attributes:
        id: Profile unique identifier
        user_id: Associated user ID
        full_name: User's full name
        bio: Biography
        avatar_url: Profile picture URL
        phone: Phone number
        date_of_birth: Date of birth
        department: Department
        year_of_study: Year of study
        interests: List of interests
        social_links: Social media links
        query_count: Number of queries posted (students)
        resolved_count: Number of queries resolved (TAs/instructors)
        resource_count: Number of resources contributed
        reputation_score: User reputation score
        created_at: Profile creation timestamp
        updated_at: Last update timestamp

    Example:
        {
            "id": 1,
            "user_id": 1,
            "full_name": "John Doe",
            "bio": "Computer Science student",
            "department": "Computer Science",
            "year_of_study": 2,
            "query_count": 15,
            "reputation_score": 250,
            "created_at": "2025-01-15T10:30:00Z"
        }
    """
    id: int
    user_id: int
    full_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    department: Optional[str] = None
    year_of_study: Optional[int] = None
    interests: List[str] = []
    social_links: dict = {}
    query_count: int = 0
    resolved_count: int = 0
    resource_count: int = 0
    reputation_score: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProfileStats(BaseModel):
    """
    Schema for user profile statistics.

    Role-specific statistics for dashboards.

    Attributes:
        queries_posted: Total queries posted
        queries_resolved: Total queries resolved
        resources_uploaded: Total resources uploaded
        average_response_time: Average response time (hours)
        satisfaction_rating: User satisfaction rating
        streak_days: Consecutive active days
        achievements: List of achievements/badges

    Example:
        {
            "queries_posted": 20,
            "queries_resolved": 50,
            "average_response_time": 2.5,
            "satisfaction_rating": 4.7,
            "streak_days": 15
        }
    """
    queries_posted: int = 0
    queries_resolved: int = 0
    resources_uploaded: int = 0
    average_response_time: Optional[float] = None
    satisfaction_rating: Optional[float] = Field(None, ge=0, le=5)
    streak_days: int = 0
    achievements: List[str] = []
