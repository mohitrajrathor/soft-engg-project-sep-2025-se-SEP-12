"""
Analytics API schemas.

Pydantic models for admin analytics dashboard endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class OverviewMetrics(BaseModel):
    """Overall system metrics."""

    total_users: int = Field(..., description="Total number of users")
    total_queries: int = Field(..., description="Total number of queries")
    total_responses: int = Field(..., description="Total number of responses")
    total_knowledge_sources: int = Field(..., description="Total knowledge base sources")
    total_chat_sessions: int = Field(..., description="Total chat sessions")
    active_users_today: int = Field(..., description="Users active in last 24 hours")
    active_users_week: int = Field(..., description="Users active in last 7 days")
    queries_today: int = Field(..., description="Queries created today")
    queries_week: int = Field(..., description="Queries created this week")
    open_queries: int = Field(..., description="Currently open queries")
    resolved_queries: int = Field(..., description="Resolved queries")
    average_resolution_time_hours: Optional[float] = Field(None, description="Average time to resolve queries (hours)")

    class Config:
        json_schema_extra = {
            "example": {
                "total_users": 150,
                "total_queries": 450,
                "total_responses": 820,
                "total_knowledge_sources": 85,
                "total_chat_sessions": 320,
                "active_users_today": 45,
                "active_users_week": 120,
                "queries_today": 15,
                "queries_week": 78,
                "open_queries": 23,
                "resolved_queries": 380,
                "average_resolution_time_hours": 4.5
            }
        }


class FAQItem(BaseModel):
    """Frequently asked question item."""

    question: str = Field(..., description="Question text or title")
    count: int = Field(..., description="Number of times asked")
    category: Optional[str] = Field(None, description="Question category")
    last_asked: Optional[datetime] = Field(None, description="Last time this was asked")
    status: Optional[str] = Field(None, description="Most common status")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "How do I submit my assignment?",
                "count": 25,
                "category": "ASSIGNMENTS",
                "last_asked": "2025-11-27T10:30:00Z",
                "status": "RESOLVED"
            }
        }


class FAQsResponse(BaseModel):
    """Response for FAQs endpoint."""

    total_unique_questions: int = Field(..., description="Total unique questions")
    faqs: List[FAQItem] = Field(..., description="List of frequently asked questions")
    time_period: str = Field(..., description="Time period for analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "total_unique_questions": 150,
                "faqs": [
                    {
                        "question": "How do I submit my assignment?",
                        "count": 25,
                        "category": "ASSIGNMENTS",
                        "last_asked": "2025-11-27T10:30:00Z",
                        "status": "RESOLVED"
                    }
                ],
                "time_period": "last_30_days"
            }
        }


class PerformanceMetrics(BaseModel):
    """Performance and resolution metrics."""

    average_response_time_minutes: Optional[float] = Field(None, description="Average time to first response")
    average_resolution_time_hours: Optional[float] = Field(None, description="Average time to resolve query")
    median_resolution_time_hours: Optional[float] = Field(None, description="Median resolution time")
    resolution_rate_percentage: float = Field(..., description="Percentage of queries resolved")
    open_query_count: int = Field(..., description="Currently open queries")
    in_progress_count: int = Field(..., description="Queries in progress")
    resolved_count: int = Field(..., description="Resolved queries")
    closed_count: int = Field(..., description="Closed queries")
    queries_with_responses: int = Field(..., description="Queries that have at least one response")
    queries_without_responses: int = Field(..., description="Queries with no responses yet")
    average_responses_per_query: float = Field(..., description="Average number of responses per query")

    class Config:
        json_schema_extra = {
            "example": {
                "average_response_time_minutes": 15.5,
                "average_resolution_time_hours": 4.2,
                "median_resolution_time_hours": 3.5,
                "resolution_rate_percentage": 84.5,
                "open_query_count": 23,
                "in_progress_count": 12,
                "resolved_count": 380,
                "closed_count": 35,
                "queries_with_responses": 420,
                "queries_without_responses": 30,
                "average_responses_per_query": 1.8
            }
        }


class SentimentData(BaseModel):
    """Sentiment analysis data."""

    positive_count: int = Field(..., description="Number of positive feedback")
    neutral_count: int = Field(..., description="Number of neutral feedback")
    negative_count: int = Field(..., description="Number of negative feedback")
    total_feedback: int = Field(..., description="Total feedback entries")
    positive_percentage: float = Field(..., description="Percentage of positive feedback")
    neutral_percentage: float = Field(..., description="Percentage of neutral feedback")
    negative_percentage: float = Field(..., description="Percentage of negative feedback")
    average_rating: Optional[float] = Field(None, description="Average rating if applicable")

    class Config:
        json_schema_extra = {
            "example": {
                "positive_count": 320,
                "neutral_count": 85,
                "negative_count": 45,
                "total_feedback": 450,
                "positive_percentage": 71.1,
                "neutral_percentage": 18.9,
                "negative_percentage": 10.0,
                "average_rating": 4.2
            }
        }


class UsageStats(BaseModel):
    """Usage statistics."""

    active_users_today: int = Field(..., description="Users active today")
    active_users_week: int = Field(..., description="Users active this week")
    active_users_month: int = Field(..., description="Users active this month")
    total_chat_sessions: int = Field(..., description="Total chat sessions")
    chat_sessions_today: int = Field(..., description="Chat sessions today")
    chat_sessions_week: int = Field(..., description="Chat sessions this week")
    average_session_length_minutes: Optional[float] = Field(None, description="Average session duration")
    api_calls_today: int = Field(..., description="API calls today (estimated)")
    api_calls_week: int = Field(..., description="API calls this week (estimated)")
    knowledge_base_queries_count: int = Field(..., description="Knowledge base search count")
    chatbot_interactions_count: int = Field(..., description="Chatbot interactions count")
    peak_usage_hour: Optional[int] = Field(None, description="Hour with most activity (0-23)")
    user_growth_rate_percentage: Optional[float] = Field(None, description="User growth rate")

    class Config:
        json_schema_extra = {
            "example": {
                "active_users_today": 45,
                "active_users_week": 120,
                "active_users_month": 280,
                "total_chat_sessions": 850,
                "chat_sessions_today": 35,
                "chat_sessions_week": 180,
                "average_session_length_minutes": 12.5,
                "api_calls_today": 2500,
                "api_calls_week": 15000,
                "knowledge_base_queries_count": 450,
                "chatbot_interactions_count": 850,
                "peak_usage_hour": 14,
                "user_growth_rate_percentage": 15.5
            }
        }


class UserActivityByRole(BaseModel):
    """User activity broken down by role."""

    role: str = Field(..., description="User role")
    count: int = Field(..., description="Number of users with this role")
    active_count: int = Field(..., description="Active users with this role")


class UsageByCategory(BaseModel):
    """Usage statistics by category."""

    category: str = Field(..., description="Category name")
    count: int = Field(..., description="Number of items in this category")
    percentage: float = Field(..., description="Percentage of total")


class DetailedUsageResponse(BaseModel):
    """Detailed usage response with breakdowns."""

    usage_stats: UsageStats
    users_by_role: List[UserActivityByRole] = Field(default_factory=list)
    queries_by_category: List[UsageByCategory] = Field(default_factory=list)
    time_period: str = Field(..., description="Analysis time period")
