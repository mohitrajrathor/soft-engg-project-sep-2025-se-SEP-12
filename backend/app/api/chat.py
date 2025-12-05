from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.core.db import get_db
from app.pipelines.chat import ChatPipeline
from app.models.chat import Chat
from app.models.query import RAGQuery

router = APIRouter()

class ChatRequest(BaseModel):
    input_text: str
    chat_id: Optional[str] = None
    device_info: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@router.post("/message")
async def chat_message(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Process a chat message using the RAG pipeline.
    """
    try:
        pipeline = ChatPipeline(db_session=db)
        # Merge device_info into metadata if present
        meta = request.metadata or {}
        if request.device_info:
            meta["device_info"] = request.device_info
            
        result = await pipeline.process(
            chat_id=request.chat_id,
            input_text=request.input_text,
            metadata=meta
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chat_id}/history")
async def get_chat_history(
    chat_id: str,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Retrieve chat history for a given chat session.
    """
    try:
        # Verify chat exists - Chat model uses 'id' not 'chat_id'
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Get queries for this chat
        queries = db.query(RAGQuery)\
            .filter(RAGQuery.chat_id == chat_id)\
            .order_by(RAGQuery.created_at)\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        return {
            "chat_id": chat_id,
            "queries": [
                {
                    "query_id": str(q.id),
                    "input_text": q.input_text,
                    "answer_text": q.answer_text,
                    "confidence": q.confidence,
                    "language": q.detected_language,
                    "created_at": q.created_at.isoformat() if q.created_at else None,
                    "sources": q.retrieved_sources or []
                }
                for q in queries
            ],
            "total": len(queries)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
