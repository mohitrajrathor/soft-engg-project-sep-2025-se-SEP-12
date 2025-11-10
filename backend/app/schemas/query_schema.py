"""
Query/Doubt-related Pydantic schemas for request/response validation.

This module defines all schemas related to student queries, doubts,
and their management by TAs and instructors.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ----------- Enums -----------


class QueryStatus(str, Enum):
    """Query status enumeration for tracking query resolution."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    CLOSED = "closed"


class QueryPriority(str, Enum):
    """Query priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class QueryCategory(str, Enum):
    """Query category for classification."""
    TECHNICAL = "technical"
    CONCEPTUAL = "conceptual"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    GENERAL = "general"
    OTHER = "other"


# ----------- Request Schemas -----------


class QueryCreate(BaseModel):
    """
    Schema for creating a new query/doubt.

    Attributes:
        title: Brief summary of the query
        description: Detailed description of the query
        category: Query category for classification
        priority: Priority level (defaults to medium)
        course_id: Associated course (optional)
        tags: List of tags for better searchability

    Example:
        {
            "title": "How to implement binary search in Python?",
            "description": "I'm struggling with implementing the recursive...",
            "category": "technical",
            "priority": "medium",
            "tags": ["python", "algorithms", "recursion"]
        }
    """
    title: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Brief summary of the query"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Detailed description"
    )
    category: QueryCategory = Field(
        default=QueryCategory.GENERAL,
        description="Query category"
    )
    priority: QueryPriority = Field(
        default=QueryPriority.MEDIUM,
        description="Priority level"
    )
    course_id: Optional[int] = Field(
        None,
        description="Associated course ID"
    )
    tags: Optional[List[str]] = Field(
        default=[],
        description="Tags for searchability"
    )


class QueryUpdate(BaseModel):
    """
    Schema for updating an existing query.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated title
        description: Updated description
        status: Updated status
        priority: Updated priority
        assigned_to_id: ID of TA/instructor assigned to handle query
        resolution_notes: Notes added when resolving the query

    Example:
        {
            "status": "resolved",
            "resolution_notes": "Provided code example and explanation"
        }
    """
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    status: Optional[QueryStatus] = None
    priority: Optional[QueryPriority] = None
    assigned_to_id: Optional[int] = Field(
        None,
        description="Assigned TA/instructor ID"
    )
    resolution_notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Resolution details"
    )


class QueryResponseCreate(BaseModel):
    """
    Schema for adding a response to a query.

    Attributes:
        content: Response content
        is_solution: Mark this response as the accepted solution

    Example:
        {
            "content": "You can implement binary search using...",
            "is_solution": false
        }
    """
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Response content"
    )
    is_solution: bool = Field(
        default=False,
        description="Mark as accepted solution"
    )


# ----------- Response Schemas -----------


class QueryResponseItem(BaseModel):
    """
    Schema for a response to a query.

    Attributes:
        id: Response ID
        query_id: Associated query ID
        user_id: User who responded
        user_name: Name of responder
        user_role: Role of responder
        content: Response content
        is_solution: Whether this is the accepted solution
        created_at: Response creation timestamp
        updated_at: Last update timestamp

    Example:
        {
            "id": 1,
            "query_id": 5,
            "user_id": 2,
            "user_name": "Dr. Smith",
            "user_role": "instructor",
            "content": "Here's how you implement...",
            "is_solution": true,
            "created_at": "2025-01-15T10:30:00Z"
        }
    """
    id: int
    query_id: int
    user_id: int
    user_name: Optional[str] = None
    user_role: str
    content: str
    is_solution: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class QueryResponse(BaseModel):
    """
    Schema for query data in API responses.

    Attributes:
        id: Query unique identifier
        title: Query title
        description: Query description
        status: Current status
        priority: Priority level
        category: Query category
        student_id: ID of student who created the query
        student_name: Name of student
        assigned_to_id: ID of assigned TA/instructor
        assigned_to_name: Name of assigned person
        resolution_notes: Resolution notes (if resolved)
        course_id: Associated course
        tags: Query tags
        response_count: Number of responses
        view_count: Number of views
        created_at: Creation timestamp
        updated_at: Last update timestamp
        resolved_at: Resolution timestamp

    Example:
        {
            "id": 5,
            "title": "How to implement binary search?",
            "status": "resolved",
            "priority": "medium",
            "student_name": "John Doe",
            "assigned_to_name": "Dr. Smith",
            "response_count": 3,
            "created_at": "2025-01-15T10:30:00Z"
        }
    """
    id: int
    title: str
    description: str
    status: QueryStatus
    priority: QueryPriority
    category: QueryCategory
    student_id: int
    student_name: Optional[str] = None
    assigned_to_id: Optional[int] = None
    assigned_to_name: Optional[str] = None
    resolution_notes: Optional[str] = None
    course_id: Optional[int] = None
    tags: List[str] = []
    response_count: int = 0
    view_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class QueryWithResponses(QueryResponse):
    """
    Extended query response including all responses/comments.

    Attributes:
        responses: List of all responses to this query

    Example:
        {
            "id": 5,
            "title": "How to implement binary search?",
            ...
            "responses": [
                {
                    "id": 1,
                    "content": "Here's an implementation...",
                    "user_name": "Dr. Smith"
                }
            ]
        }
    """
    responses: List[QueryResponseItem] = []


class QueryListResponse(BaseModel):
    """
    Schema for paginated list of queries.

    Attributes:
        total: Total number of queries
        page: Current page number
        page_size: Number of items per page
        total_pages: Total number of pages
        queries: List of queries

    Example:
        {
            "total": 50,
            "page": 1,
            "page_size": 10,
            "total_pages": 5,
            "queries": [...]
        }
    """
    total: int = Field(..., description="Total number of queries")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    queries: List[QueryResponse] = Field(default=[], description="List of queries")


class QueryStats(BaseModel):
    """
    Schema for query statistics.

    Useful for dashboards and analytics.

    Attributes:
        total_queries: Total number of queries
        open_queries: Number of open queries
        in_progress_queries: Number of queries in progress
        resolved_queries: Number of resolved queries
        average_resolution_time: Average time to resolve (in hours)
        queries_by_category: Breakdown by category

    Example:
        {
            "total_queries": 150,
            "open_queries": 20,
            "resolved_queries": 120,
            "average_resolution_time": 4.5
        }
    """
    total_queries: int
    open_queries: int
    in_progress_queries: int
    resolved_queries: int
    escalated_queries: int
    average_resolution_time: Optional[float] = Field(
        None,
        description="Average resolution time in hours"
    )
    queries_by_category: dict = Field(
        default={},
        description="Query count by category"
    )
