"""
Pydantic schemas for chat session API endpoints.

This module defines request and response models for chat session operations.
Note: This is separate from the chatbot conversation system.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
import uuid as uuid_module


class ChatSessionCreateRequest(BaseModel):
    """Request model for creating a new chat session."""
    ip_address: Optional[str] = Field(None, max_length=45)
    device_info: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=255)
    language: Optional[str] = Field(None, max_length=10)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ChatSessionCreateResponse(BaseModel):
    """Response model for chat session creation."""
    chat_id: str
    created_at: datetime
    message: str = "Chat session created successfully"


class ChatSessionQueryRequest(BaseModel):
    """Request model for submitting a query to a chat session."""
    chat_id: str
    input_text: str = Field(..., min_length=1, max_length=5000)

    @field_validator('input_text')
    @classmethod
    def validate_input_text(cls, v: str) -> str:
        """Validate and clean input text."""
        v = ' '.join(v.split())
        if not v:
            raise ValueError("Input text cannot be empty")
        return v

    @field_validator('chat_id')
    @classmethod
    def validate_chat_id(cls, v: str) -> str:
        """Validate chat_id is a valid UUID."""
        try:
            uuid_module.UUID(v)
        except ValueError:
            raise ValueError("Invalid chat_id format")
        return v


class ChatSessionQueryResponse(BaseModel):
    """Response model for chat query processing."""
    query_id: str
    answer: str
    has_answered: bool
    confidence: int = Field(ge=0, le=100)
    language: str
    response_time_ms: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ChatSessionHistoryRequest(BaseModel):
    """Request model for getting chat session history."""
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class ChatSessionHistoryItem(BaseModel):
    """Model for a single item in chat session history."""
    query_id: str
    input_text: str
    answer_text: Optional[str]
    has_answered: bool
    confidence: Optional[int]
    language: Optional[str]
    response_time_ms: Optional[int]
    created_at: datetime


class ChatSessionHistoryResponse(BaseModel):
    """Response model for chat session history."""
    chat_id: str
    total: int
    limit: int
    offset: int
    queries: List[ChatSessionHistoryItem]


class ChatSessionInfo(BaseModel):
    """Model for chat session information."""
    chat_id: str
    ip_address: Optional[str]
    device_info: Optional[str]
    location: Optional[str]
    language: Optional[str]
    created_at: datetime
    updated_at: datetime
    total_queries: int = 0
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ChatSessionAnalytics(BaseModel):
    """Model for chat session analytics data."""
    total_sessions: int
    total_queries: int
    avg_confidence: float
    avg_response_time_ms: float
    languages_used: Dict[str, int]
    success_rate: float
    time_period: str
