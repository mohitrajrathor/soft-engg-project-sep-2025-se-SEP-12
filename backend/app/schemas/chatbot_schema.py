"""
Chatbot-related Pydantic schemas for request/response validation.

This module defines all schemas related to the AI chatbot/assistant.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ----------- Enums -----------


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMode(str, Enum):
    """Chat mode for different contexts."""
    GENERAL = "general"
    ACADEMIC = "academic"
    DOUBT_CLARIFICATION = "doubt_clarification"
    STUDY_HELP = "study_help"


# ----------- Request Schemas -----------


class ChatMessage(BaseModel):
    """
    Schema for a single chat message.

    Attributes:
        role: Message sender role (user, assistant, system)
        content: Message content
        timestamp: Message timestamp

    Example:
        {
            "role": "user",
            "content": "What is binary search?",
            "timestamp": "2025-01-15T10:30:00Z"
        }
    """
    role: MessageRole = Field(..., description="Message sender role")
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    timestamp: Optional[datetime] = Field(default=None, description="Message timestamp")

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    """
    Schema for chat request.

    Attributes:
        message: User's message
        conversation_id: Optional conversation ID for history
        mode: Chat mode (general, academic, etc.)
        context: Optional context for the conversation

    Example:
        {
            "message": "Explain recursion in Python",
            "conversation_id": "conv-123",
            "mode": "academic",
            "context": "I'm studying data structures"
        }
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's message"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Conversation ID for maintaining history"
    )
    mode: ChatMode = Field(
        default=ChatMode.GENERAL,
        description="Chat mode"
    )
    context: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional context"
    )


class ChatStreamRequest(BaseModel):
    """
    Schema for streaming chat request.

    For real-time streaming responses.

    Attributes:
        message: User's message
        conversation_id: Conversation ID
        mode: Chat mode
    """
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = None
    mode: ChatMode = ChatMode.GENERAL


# ----------- Response Schemas -----------


class ChatResponse(BaseModel):
    """
    Schema for chat response.

    Attributes:
        response: AI assistant's response
        conversation_id: Conversation ID for tracking
        sources: Optional sources/references used
        tokens_used: Number of tokens used (for analytics)
        model: Model used for generation
        timestamp: Response timestamp

    Example:
        {
            "response": "Recursion is a programming technique...",
            "conversation_id": "conv-123",
            "sources": ["Python docs", "Course notes"],
            "tokens_used": 150,
            "model": "gemini-pro",
            "timestamp": "2025-01-15T10:30:05Z"
        }
    """
    response: str = Field(..., description="AI assistant's response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: Optional[List[str]] = Field(
        default=[],
        description="Sources or references used"
    )
    tokens_used: Optional[int] = Field(
        None,
        description="Number of tokens used"
    )
    model: str = Field(default="gemini-pro", description="Model used")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationHistory(BaseModel):
    """
    Schema for conversation history.

    Attributes:
        conversation_id: Unique conversation ID
        messages: List of messages in conversation
        created_at: Conversation start time
        updated_at: Last message time
        user_id: User who owns this conversation

    Example:
        {
            "conversation_id": "conv-123",
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi! How can I help?"}
            ],
            "created_at": "2025-01-15T10:00:00Z",
            "updated_at": "2025-01-15T10:30:00Z",
            "user_id": 1
        }
    """
    conversation_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class ConversationListResponse(BaseModel):
    """
    Schema for list of conversations.

    Attributes:
        conversations: List of conversation summaries
        total: Total number of conversations

    Example:
        {
            "conversations": [
                {
                    "conversation_id": "conv-123",
                    "last_message": "Explain recursion",
                    "updated_at": "2025-01-15T10:30:00Z"
                }
            ],
            "total": 10
        }
    """
    conversations: List[dict]
    total: int


class ChatbotStats(BaseModel):
    """
    Schema for chatbot usage statistics.

    Attributes:
        total_conversations: Total number of conversations
        total_messages: Total messages exchanged
        average_response_time: Average response time in seconds
        most_common_topics: Most discussed topics

    Example:
        {
            "total_conversations": 50,
            "total_messages": 500,
            "average_response_time": 2.5,
            "most_common_topics": ["Python", "Data Structures", "Algorithms"]
        }
    """
    total_conversations: int
    total_messages: int
    average_response_time: float
    most_common_topics: List[str] = []
