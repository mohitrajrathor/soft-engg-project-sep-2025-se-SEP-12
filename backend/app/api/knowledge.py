from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
import uuid
import logging

from app.core.db import get_db
from app.pipelines.knowledge import process_knowledge_source
from app.models.knowledge import KnowledgeSource
from app.models.enums import CategoryEnum
from app.utils.file_parser import parse_uploaded_file, get_file_info

logger = logging.getLogger(__name__)
router = APIRouter()

# Maximum file size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

class IngestRequest(BaseModel):
    title: str
    content: str
    category: CategoryEnum
    description: Optional[str] = None

    @classmethod
    def validate_category(cls, v):
        if isinstance(v, str):
            # Try to match case-insensitive
            for member in CategoryEnum:
                if member.value.lower() == v.lower():
                    return member
        return v

    # Pydantic v1/v2 compatibility
    try:
        from pydantic import validator
        _validate_category = validator('category', pre=True, allow_reuse=True)(validate_category)
    except ImportError:
        from pydantic import field_validator
        _validate_category = field_validator('category', mode='before')(validate_category)

@router.post("/ingest")
async def ingest_knowledge(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Ingest a new knowledge source.
    """
    try:
        # Create source record
        source = KnowledgeSource(
            title=request.title,
            content=request.content,
            category=request.category,
            description=request.description
        )
        db.add(source)
        db.commit()
        db.refresh(source)

        # Trigger pipeline in background
        background_tasks.add_task(process_knowledge_source, str(source.id))

        return {"message": "Ingestion started", "source_id": str(source.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Upload a file (PDF, DOCX, TXT, XLSX, XLS, CSV, Images) as knowledge source.
    Uses hybrid approach: direct extraction + OCR fallback for scanned documents.
    """
    try:
        #Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)} MB"
            )
        
        # Get file info
        file_info = get_file_info(file.filename, file_content)
        logger.info(f"Received file upload: {file_info}")
        
        # Validate category
        try:
            category_enum = CategoryEnum(category)
        except ValueError:
            valid_categories = [e.value for e in CategoryEnum]
            raise HTTPException(
                status_code=422,
                detail=f"Invalid category '{category}'. Valid options: {', '.join(valid_categories)}"
            )
        
        # Extract text from file (hybrid: direct extraction + OCR fallback)
        try:
            result = parse_uploaded_file(file.filename, file_content)
            # Handle tuple return (text, used_ocr) or just text
            if isinstance(result, tuple):
                extracted_text, used_ocr = result
            else:
                extracted_text = result
                used_ocr = False
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")
        
        # Check if text extraction was successful
        if not extracted_text or len(extracted_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Extracted text is too short or empty. Please ensure the file contains readable text."
            )
        
        # Use provided title or filename
        if not title or title.strip() == "":
            # Remove extension from filename for title
            title = file.filename.rsplit('.', 1)[0]
        
        # Create source record
        source = KnowledgeSource(
            title=title,
            content=extracted_text,
            category=category_enum,
            description=description or f"Uploaded from {file.filename}"
        )
        db.add(source)
        db.commit()
        db.refresh(source)
        
        # Trigger pipeline in background
        if background_tasks:
            background_tasks.add_task(process_knowledge_source, str(source.id))
        
        return {
            "message": "File uploaded and ingestion started",
            "source_id": str(source.id),
            "file_info": file_info,
            "extracted_text_length": len(extracted_text),
            "used_ocr": used_ocr,
            "title": title
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sources")
def get_knowledge_sources(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    is_active: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get paginated knowledge sources.
    """
    query = db.query(KnowledgeSource)

    if search:
        query = query.filter(KnowledgeSource.title.ilike(f"%{search}%"))
    
    if is_active and is_active != 'all':
        active_bool = is_active.lower() == 'true'
        query = query.filter(KnowledgeSource.is_active == active_bool)
    
    if category:
        query = query.filter(KnowledgeSource.category == category)

    total = query.count()
    
    # Pagination
    offset = (page - 1) * size
    sources = query.offset(offset).limit(size).all()
    
    # Calculate total pages
    import math
    pages = math.ceil(total / size)

    return {
        "items": sources,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

@router.get("/sources/{source_id}")
def get_knowledge_source_detail(source_id: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a knowledge source including all its chunks.
    """
    from app.models.knowledge import KnowledgeChunk
    
    # Get the source
    source = db.query(KnowledgeSource).filter(KnowledgeSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    # Get all chunks for this source
    chunks = db.query(KnowledgeChunk).filter(
        KnowledgeChunk.source_id == source_id
    ).order_by(KnowledgeChunk.index).all()
    
    # Format the response
    return {
        "id": str(source.id),
        "title": source.title,
        "description": source.description,
        "category": source.category,
        "content": source.content,
        "is_active": source.is_active,
        "created_at": source.created_at,
        "updated_at": source.updated_at,
        "chunk_count": len(chunks),
        "chunks": [
            {
                "id": str(chunk.id),
                "text": chunk.text,
                "index": chunk.index,
                "token_count": chunk.token_count,
                "word_count": chunk.word_count,
                "has_embedding": chunk.embedding is not None
            }
            for chunk in chunks
        ]
    }

@router.delete("/sources/{source_id}")
def delete_knowledge_source(source_id: str, db: Session = Depends(get_db)):
    """
    Delete a knowledge source.
    """
    source = db.query(KnowledgeSource).filter(KnowledgeSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    db.delete(source)
    db.commit()
    return {"message": "Source deleted"}

class UpdateSourceRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[CategoryEnum] = None
    is_active: Optional[bool] = None

@router.put("/sources/{source_id}")
def update_knowledge_source(
    source_id: str,
    request: UpdateSourceRequest,
    db: Session = Depends(get_db)
):
    """
    Update a knowledge source.
    """
    source = db.query(KnowledgeSource).filter(KnowledgeSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    if request.title:
        source.title = request.title
    if request.description:
        source.description = request.description
    if request.category:
        source.category = request.category
    if request.is_active is not None:
        source.is_active = request.is_active
        
    db.commit()
    db.refresh(source)
    return source
