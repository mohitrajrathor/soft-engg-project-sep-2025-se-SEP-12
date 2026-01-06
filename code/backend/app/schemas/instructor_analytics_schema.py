"""
Instructor Analytics API schemas.

Pydantic models for instructor discussion summaries and analytics endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class DiscussionMetric(BaseModel):
    """Single metric for discussion overview."""
    title: str = Field(..., description="Metric title")
    value: str = Field(..., description="Metric value (formatted)")
    subtitle: str = Field(default="", description="Additional context")


class SentimentBreakdown(BaseModel):
    """Sentiment percentage breakdown."""
    positive: float = Field(..., description="Positive sentiment percentage")
    neutral: float = Field(..., description="Neutral sentiment percentage")
    negative: float = Field(..., description="Negative sentiment percentage")


class DiscussionTopic(BaseModel):
    """Individual discussion topic with sentiment."""
    id: int = Field(..., description="Query/Topic ID")
    title: str = Field(..., description="Discussion title")
    description: str = Field(..., description="Discussion description or preview")
    participants: List[str] = Field(default_factory=list, description="Participant names")
    sentiment: SentimentBreakdown = Field(..., description="Sentiment breakdown")
    thread_count: int = Field(default=0, description="Number of responses/threads")
    category: Optional[str] = Field(None, description="Discussion category")
    created_at: Optional[datetime] = Field(None, description="When discussion started")
    status: Optional[str] = Field(None, description="Discussion status")


class SentimentTrendData(BaseModel):
    """Sentiment trend over time for charts."""
    months: List[str] = Field(..., description="Month labels")
    positive: List[float] = Field(..., description="Positive sentiment values")
    neutral: List[float] = Field(..., description="Neutral sentiment values")
    negative: List[float] = Field(..., description="Negative sentiment values")


class SentimentDriverData(BaseModel):
    """Sentiment by topic/category for bar chart."""
    labels: List[str] = Field(..., description="Topic/Category labels")
    positive: List[float] = Field(..., description="Positive counts per topic")
    negative: List[float] = Field(..., description="Negative counts per topic")


class SentimentInsights(BaseModel):
    """Grouped insights by sentiment type."""
    positive: List[str] = Field(default_factory=list, description="Positive insights")
    neutral: List[str] = Field(default_factory=list, description="Neutral insights")
    negative: List[str] = Field(default_factory=list, description="Negative insights")


class InstructorDiscussionSummaryResponse(BaseModel):
    """Complete response for instructor discussion summaries."""
    metrics: List[DiscussionMetric] = Field(..., description="Overview metrics")
    topics: List[DiscussionTopic] = Field(..., description="Top discussion topics")
    trends: SentimentTrendData = Field(..., description="Sentiment trend data for chart")
    drivers: SentimentDriverData = Field(..., description="Sentiment drivers for bar chart")
    insights: SentimentInsights = Field(..., description="Sentiment insights")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When data was generated")

    class Config:
        json_schema_extra = {
            "example": {
                "metrics": [
                    {"title": "Total Discussions", "value": "156", "subtitle": "All time"},
                    {"title": "Active Threads", "value": "23", "subtitle": "Currently open"},
                    {"title": "Average Sentiment", "value": "72%", "subtitle": "Positive"},
                    {"title": "Unresolved Queries", "value": "12", "subtitle": "Needs attention"}
                ],
                "topics": [
                    {
                        "id": 1,
                        "title": "Understanding Recursion",
                        "description": "Students discuss recursive algorithms",
                        "participants": ["Alice", "Bob"],
                        "sentiment": {"positive": 60, "neutral": 25, "negative": 15},
                        "thread_count": 5,
                        "category": "technical",
                        "status": "resolved"
                    }
                ],
                "trends": {
                    "months": ["Jan", "Feb", "Mar"],
                    "positive": [70, 75, 80],
                    "neutral": [20, 18, 15],
                    "negative": [10, 7, 5]
                },
                "drivers": {
                    "labels": ["Recursion", "Pointers", "Sorting"],
                    "positive": [50, 40, 70],
                    "negative": [20, 35, 15]
                },
                "insights": {
                    "positive": ["Students found examples engaging"],
                    "neutral": ["Some requested slower pacing"],
                    "negative": ["Base case logic needs more examples"]
                }
            }
        }


class TopicCluster(BaseModel):
    """Topic cluster from query analysis."""
    cluster_name: str = Field(..., description="Cluster/topic name")
    query_count: int = Field(..., description="Number of queries in cluster")
    keywords: List[str] = Field(default_factory=list, description="Top keywords")
    sentiment_score: float = Field(..., description="Average sentiment score (0-1)")
    sample_queries: List[str] = Field(default_factory=list, description="Sample query titles")


class TopicClusteringResponse(BaseModel):
    """Response for topic clustering endpoint."""
    clusters: List[TopicCluster] = Field(..., description="Topic clusters")
    total_queries_analyzed: int = Field(..., description="Total queries analyzed")
    time_period: str = Field(..., description="Analysis time period")


class RealTimeSentimentPoint(BaseModel):
    """Single point for real-time sentiment chart."""
    timestamp: datetime = Field(..., description="Data point timestamp")
    positive: int = Field(..., description="Positive count")
    neutral: int = Field(..., description="Neutral count")
    negative: int = Field(..., description="Negative count")
    total: int = Field(..., description="Total count")


class RealTimeSentimentResponse(BaseModel):
    """Response for real-time sentiment data."""
    data_points: List[RealTimeSentimentPoint] = Field(..., description="Time series data")
    current_sentiment: SentimentBreakdown = Field(..., description="Current sentiment state")
    trend_direction: str = Field(..., description="Trend direction: improving, declining, stable")
