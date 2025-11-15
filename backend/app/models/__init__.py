"""
Database models package.

This module exports all SQLAlchemy models for easy imports.
"""

from app.models.user import User
from app.models.query import Query, QueryResponse
from app.models.resource import Resource
from app.models.announcement import Announcement
from app.models.profile import Profile

# New models for knowledge base, calls, tasks
from app.models.enums import (
    CategoryEnum,
    TaskTypeEnum,
    TaskStatusEnum,
    SourceTypeEnum,
    CallStatusEnum
)
from app.models.knowledge import KnowledgeSource, KnowledgeChunk
from app.models.call import Call
from app.models.chat_session import ChatSession
from app.models.task import Task

__all__ = [
    # Original models
    "User",
    "Query",
    "QueryResponse",
    "Resource",
    "Announcement",
    "Profile",
    # Enums
    "CategoryEnum",
    "TaskTypeEnum",
    "TaskStatusEnum",
    "SourceTypeEnum",
    "CallStatusEnum",
    # Knowledge base
    "KnowledgeSource",
    "KnowledgeChunk",
    # Voice calls
    "Call",
    # Chat sessions
    "ChatSession",
    # Background tasks
    "Task",
]
