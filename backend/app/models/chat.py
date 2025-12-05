"""
Chat model for Aura multilingual support system.

This module defines the Chat session model for tracking user chat interactions.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List

from sqlalchemy import Column, String, DateTime, Text, Index, Boolean, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db import Base


class Chat(Base):
    """
    Represents a chat session with a user.

    Stores session information including device details, location,
    and detected language preferences.
    """
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    device_info = Column(String(500), nullable=True)  # User-agent or fingerprint
    location = Column(String(255), nullable=True)  # From GeoIP
    language = Column(String(10), nullable=True)  # Language code (e.g., 'en', 'hi')
    metadata_ = Column(JSONB, nullable=True, default=dict)  # Extra data
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    rag_queries = relationship("RAGQuery", back_populates="chat", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_chat_created_at", "created_at"),
        Index("idx_chat_language", "language"),
        Index("idx_chat_ip_address", "ip_address"),
    )

    def __repr__(self) -> str:
        return f"<Chat(id={self.id}, language={self.language}, created_at={self.created_at})>"

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
