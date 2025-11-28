"""
Chat session model for AURA.

This module defines the Chat session model for tracking user chat interactions.
Note: This is different from the chatbot conversation tracking.
"""

import uuid
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import Column, String, DateTime, Index, JSON, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type when available, otherwise uses
    CHAR(36) for SQLite compatibility, storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            else:
                return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid.UUID):
                return value
            else:
                return uuid.UUID(value)


class ChatSession(Base):
    """
    Represents a chat session with a user.

    Stores session information including device details, location,
    and detected language preferences.
    """
    __tablename__ = "chat_sessions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    device_info = Column(String(500), nullable=True)  # User-agent or fingerprint
    location = Column(String(255), nullable=True)  # From GeoIP
    language = Column(String(10), nullable=True)  # Language code (e.g., 'en', 'hi')
    metadata_ = Column(JSON, nullable=True, default=dict)  # Extra data
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    # TODO: Enable when Query model is enhanced with chat_session_id foreign key
    # queries = relationship("Query", back_populates="chat_session", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_chat_session_created_at", "created_at"),
        Index("idx_chat_session_language", "language"),
        Index("idx_chat_session_ip_address", "ip_address"),
    )

    def __repr__(self) -> str:
        return f"<ChatSession(id={self.id}, language={self.language}, created_at={self.created_at})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary for API responses."""
        return {
            "id": str(self.id),
            "ip_address": self.ip_address,
            "device_info": self.device_info,
            "location": self.location,
            "language": self.language,
            "metadata": self.metadata_ or {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
