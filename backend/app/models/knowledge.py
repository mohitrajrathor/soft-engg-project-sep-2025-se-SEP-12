from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, Index, LargeBinary, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime
import uuid
from pgvector.sqlalchemy import Vector
from app.models.enums import CategoryEnum

class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    content = Column(Text, nullable=False)  # Main content to be embedded
    category = Column(Enum(CategoryEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chunks = relationship("KnowledgeChunk", back_populates="source", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('ix_knowledge_sources_title_category', 'title', 'category'),
    )

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_sources.id"), nullable=False)
    text = Column(Text, nullable=False)
    index = Column(Integer, nullable=False)  # Position in document
    embedding = Column(Vector(768))  # gemini-embedding-004 output dimension is 768
    token_count = Column(Integer, default=0)
    word_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    source = relationship("KnowledgeSource", back_populates="chunks")

    # Indexes for vector similarity search
    __table_args__ = (
        Index('ix_knowledge_chunks_embedding_cosine', 'embedding', postgresql_using='ivfflat', postgresql_ops={'embedding': 'vector_cosine_ops'}),
        Index('ix_knowledge_chunks_source_id', 'source_id'),
    )
