"""
Knowledge Base API Endpoints for AURA.

Provides CRUD operations for knowledge sources and semantic search capabilities.
Note: Some features require PostgreSQL with pgvector extension.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from uuid import UUID

from app.core.db import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.knowledge import KnowledgeSource, KnowledgeChunk
from app.models.task import Task
from app.models.enums import TaskTypeEnum, TaskStatusEnum, CategoryEnum
from app.schemas.knowledge_schema import (
    KnowledgeSourceCreate,
    KnowledgeSourceUpdate,
    KnowledgeSourceOut,
    KnowledgeChunkOut,
    SemanticSearchRequest,
    PaginatedKnowledgeSourceResponse,
    KnowledgeStats
)


router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


# ============================================================================
# KNOWLEDGE SOURCE ENDPOINTS
# ============================================================================

@router.post("/sources", response_model=KnowledgeSourceOut, status_code=status.HTTP_201_CREATED)
async def create_knowledge_source(
    source: KnowledgeSourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new knowledge source.

    - **title**: Source title (required)
    - **description**: Source description (optional)
    - **content**: Full text content (required)
    - **category**: Category for organization (required)
    - **is_active**: Whether source is active for search (default: true)

    Note: Automatic embedding generation requires background task setup.
    """
    try:
        # Create knowledge source
        db_source = KnowledgeSource(
            title=source.title,
            description=source.description,
            content=source.content,
            category=source.category,
            is_active=source.is_active
        )

        db.add(db_source)
        db.commit()
        db.refresh(db_source)

        # TODO: Trigger embedding generation when Celery is configured
        # process_document.delay(str(db_source.id))

        return db_source

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create knowledge source: {str(e)}"
        )


@router.get("/categories", response_model=List[str])
async def get_categories(
    current_user: User = Depends(get_current_user)
):
    """
    Get available categories for knowledge sources.

    Returns a list of all available category values.
    """
    return [category.value for category in CategoryEnum]


@router.get("/sources", response_model=PaginatedKnowledgeSourceResponse)
async def list_knowledge_sources(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List knowledge sources with pagination and filters.

    Supports:
    - Full-text search across title, description, and content
    - Category filtering
    - Active status filtering
    - Pagination
    """
    try:
        query = db.query(KnowledgeSource)

        # Apply search
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    KnowledgeSource.title.ilike(search_filter),
                    KnowledgeSource.description.ilike(search_filter),
                    KnowledgeSource.content.ilike(search_filter)
                )
            )

        # Apply filters
        if category:
            try:
                category_enum = CategoryEnum(category)
                query = query.filter(KnowledgeSource.category == category_enum)
            except ValueError:
                pass  # Invalid category, ignore filter

        if is_active is not None:
            query = query.filter(KnowledgeSource.is_active == is_active)

        # Get total count
        total = query.count()

        # Apply pagination
        query = query.order_by(KnowledgeSource.created_at.desc())
        skip = (page - 1) * size
        sources = query.offset(skip).limit(size).all()

        # Calculate pages
        pages = (total + size - 1) // size if total > 0 else 1

        return PaginatedKnowledgeSourceResponse(
            items=sources,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve knowledge sources: {str(e)}"
        )


@router.get("/sources/{source_id}", response_model=KnowledgeSourceOut)
async def get_knowledge_source(
    source_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific knowledge source by ID.

    Returns detailed information about a single knowledge source.
    """
    source = db.query(KnowledgeSource).filter(
        KnowledgeSource.id == source_id
    ).first()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge source not found"
        )

    return source


@router.put("/sources/{source_id}", response_model=KnowledgeSourceOut)
async def update_knowledge_source(
    source_id: UUID,
    source_update: KnowledgeSourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a knowledge source.

    - Only provided fields will be updated
    - If content is modified, re-embedding should be triggered (requires background tasks)
    """
    source = db.query(KnowledgeSource).filter(
        KnowledgeSource.id == source_id
    ).first()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge source not found"
        )

    try:
        content_modified = False

        # Update fields
        if source_update.title is not None:
            source.title = source_update.title
        if source_update.description is not None:
            source.description = source_update.description
        if source_update.content is not None:
            source.content = source_update.content
            content_modified = True
        if source_update.category is not None:
            source.category = source_update.category
        if source_update.is_active is not None:
            source.is_active = source_update.is_active

        db.commit()
        db.refresh(source)

        # TODO: Trigger re-embedding if content was modified and Celery is configured
        # if content_modified:
        #     process_document.delay(str(source_id))

        return source

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update knowledge source: {str(e)}"
        )


@router.delete("/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_source(
    source_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a knowledge source.

    This will also delete all associated chunks and embeddings.
    """
    source = db.query(KnowledgeSource).filter(
        KnowledgeSource.id == source_id
    ).first()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge source not found"
        )

    try:
        db.delete(source)
        db.commit()
        return None

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete knowledge source: {str(e)}"
        )


@router.get("/sources/{source_id}/chunks", response_model=List[KnowledgeChunkOut])
async def get_source_chunks(
    source_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all text chunks for a knowledge source.

    Returns all chunks with their embeddings (if generated).
    """
    source = db.query(KnowledgeSource).filter(
        KnowledgeSource.id == source_id
    ).first()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge source not found"
        )

    chunks = db.query(KnowledgeChunk).filter(
        KnowledgeChunk.source_id == source_id
    ).order_by(KnowledgeChunk.index).all()

    return chunks


@router.post("/search")
async def semantic_search(
    search_request: SemanticSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Perform semantic search across knowledge base.

    Note: This requires PostgreSQL with pgvector extension and embeddings to be generated.
    Currently returns a placeholder message.
    """
    return {
        "message": "Semantic search requires PostgreSQL with pgvector extension",
        "query": search_request.query,
        "status": "not_configured",
        "note": "Use text search via /knowledge/sources?search=query for now"
    }


@router.get("/stats", response_model=KnowledgeStats)
async def get_knowledge_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics about the knowledge base.

    Returns counts and metrics for knowledge sources and chunks.
    """
    try:
        total_sources = db.query(KnowledgeSource).count()
        active_sources = db.query(KnowledgeSource).filter(
            KnowledgeSource.is_active == True
        ).count()
        total_chunks = db.query(KnowledgeChunk).count()

        # Count sources by category
        sources_by_category = {}
        for category in CategoryEnum:
            count = db.query(KnowledgeSource).filter(
                KnowledgeSource.category == category
            ).count()
            sources_by_category[category.value] = count

        # Calculate average chunks per source
        avg_chunks = total_chunks / total_sources if total_sources > 0 else 0

        return KnowledgeStats(
            total_sources=total_sources,
            active_sources=active_sources,
            total_chunks=total_chunks,
            sources_by_category=sources_by_category,
            avg_chunks_per_source=round(avg_chunks, 2)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve knowledge statistics: {str(e)}"
        )
