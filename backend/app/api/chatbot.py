"""
Chatbot API endpoints with streaming support.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import User
from app.schemas.chatbot_schema import ChatRequest, ChatResponse, ChatMode
from app.api.dependencies import get_current_user
from app.services.chatbot_service_hybrid import hybrid_chatbot_service as chatbot_service
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


chatbot_router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@chatbot_router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI assistant",
    description="""
    Send a message to the AI chatbot and get a response.

    **Features:**
    - Conversation memory (maintains context)
    - Multiple chat modes (academic, general, study help, doubt clarification)
    - Powered by Google Gemini AI

    **Example:**
    ```json
    {
      "message": "Explain binary search algorithm",
      "mode": "academic",
      "conversation_id": "conv-abc123"
    }
    ```
    """
)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI assistant.

    Requires authentication.
    """
    try:
        # Generate response
        response, conv_id = await chatbot_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
            mode=request.mode
        )

        return ChatResponse(
            response=response,
            conversation_id=conv_id,
            model=chatbot_service.llm.model if chatbot_service.llm else "fallback",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        )


@chatbot_router.post(
    "/chat/stream",
    summary="Stream chat response",
    description="""
    Send a message and get a streaming response (real-time).

    **Features:**
    - Real-time streaming responses
    - See AI typing in real-time
    - Better UX for long responses

    **Response:** Server-Sent Events (SSE) stream
    """
)
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Stream chat response in real-time.

    Returns Server-Sent Events (SSE) stream.
    """
    async def generate():
        try:
            async for chunk in chatbot_service.chat_stream(
                message=request.message,
                conversation_id=request.conversation_id,
                mode=request.mode
            ):
                yield f"data: {chunk}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@chatbot_router.delete(
    "/conversation/{conversation_id}",
    summary="Clear conversation history",
    description="Delete conversation history for a specific conversation ID."
)
async def clear_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Clear conversation history."""
    success = chatbot_service.clear_conversation(conversation_id)

    if success:
        return {"message": "Conversation cleared successfully", "conversation_id": conversation_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )


@chatbot_router.get(
    "/conversation/{conversation_id}/history",
    summary="Get conversation history",
    description="Retrieve the message history for a conversation."
)
async def get_conversation_history(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get conversation history."""
    history = chatbot_service.get_conversation_history(conversation_id)

    if not history:
        return {"conversation_id": conversation_id, "messages": [], "total": 0}

    messages = []
    for msg in history:
        messages.append({
            "role": msg.type,  # 'human' or 'ai'
            "content": msg.content,
        })

    return {
        "conversation_id": conversation_id,
        "messages": messages,
        "total": len(messages)
    }


@chatbot_router.get(
    "/status",
    summary="Get chatbot status",
    description="Check if chatbot is configured and ready."
)
async def get_chatbot_status():
    """Get chatbot configuration status."""
    from app.core.config import settings

    # Check if any implementation is available
    is_configured = (
        chatbot_service.llm is not None or
        chatbot_service.genai_client is not None or
        chatbot_service.adk_runner is not None
    )

    # Get model name
    model_name = None
    if chatbot_service.llm and hasattr(chatbot_service.llm, 'model'):
        model_name = chatbot_service.llm.model
    else:
        model_name = settings.GEMINI_MODEL

    # Get implementation info
    impl_info = {
        "implementation": chatbot_service.implementation.value,
        "adk_runner": chatbot_service.adk_runner is not None,
        "session_service": chatbot_service.session_service is not None,
        "memory_service": chatbot_service.memory_service is not None,
        "observability": chatbot_service.observability_plugin is not None
    }

    return {
        "configured": is_configured,
        "model": model_name,
        "available_modes": [mode.value for mode in ChatMode],
        "features": impl_info,
        "message": "Chatbot ready with enhanced features" if is_configured else "Configure GOOGLE_API_KEY in .env"
    }


@chatbot_router.get(
    "/metrics",
    summary="Get chatbot metrics",
    description="Get observability metrics (agent invocations, LLM requests, etc.)"
)
async def get_chatbot_metrics(
    current_user: User = Depends(get_current_user)
):
    """Get chatbot observability metrics."""
    metrics = chatbot_service.get_metrics()

    if metrics:
        return {
            "metrics": metrics,
            "message": "Metrics retrieved successfully"
        }
    else:
        return {
            "metrics": None,
            "message": "Observability not enabled or not available"
        }


@chatbot_router.get(
    "/conversation/{conversation_id}/state",
    summary="Get conversation session state",
    description="Retrieve the session state for a conversation (user context, preferences, etc.)"
)
async def get_conversation_state(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get session state for a conversation."""
    state = await chatbot_service.get_session_state(conversation_id)

    if state:
        return {
            "conversation_id": conversation_id,
            "state": state,
            "message": "Session state retrieved successfully"
        }
    else:
        return {
            "conversation_id": conversation_id,
            "state": {},
            "message": "No session state found or session service not available"
        }

# ============================================================================
# Enhanced Chatbot Endpoints with Knowledge Base Integration
# ============================================================================


class EnhancedChatRequest(BaseModel):
    """Request model for enhanced chat with knowledge base."""
    message: str
    conversation_id: Optional[str] = None
    use_knowledge_base: bool = True
    mode: Optional[ChatMode] = ChatMode.ACADEMIC


class EnhancedChatResponse(BaseModel):
    """Response model for enhanced chat."""
    answer: str
    conversation_id: str
    knowledge_sources_used: int
    sources: List[Dict[str, str]]
    user_context: Dict[str, Any]
    timestamp: str


@chatbot_router.post(
    "/chat/enhanced",
    response_model=EnhancedChatResponse,
    summary="Enhanced chat with knowledge base integration",
    description="""
    Chat with AI assistant that integrates:
    - Knowledge base search for accurate, sourced information
    - User context (role, history, previous queries)
    - Personalized responses based on user profile

    **Features:**
    - Retrieval Augmented Generation (RAG) using knowledge base
    - Context-aware responses
    - Source citations
    - Role-based personalization
    """
)
async def chat_enhanced(
    request: EnhancedChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enhanced chat with knowledge base and context integration.

    This endpoint searches the knowledge base for relevant information
    and provides context-aware responses personalized to the user.
    """
    try:
        response = await chatbot_service.chat_with_context(
            db=db,
            user=current_user,
            message=request.message,
            conversation_id=request.conversation_id,
            use_knowledge_base=request.use_knowledge_base
        )

        return EnhancedChatResponse(
            answer=response["answer"],
            conversation_id=response["conversation_id"],
            knowledge_sources_used=response.get("knowledge_sources_used", 0),
            sources=response.get("sources", []),
            user_context=response.get("user_context", {}),
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enhanced chat failed: {str(e)}"
        )


@chatbot_router.post(
    "/chat/enhanced/stream",
    summary="Enhanced streaming chat with knowledge base",
    description="""
    Streaming version of enhanced chat with knowledge base integration.

    Returns Server-Sent Events (SSE) for real-time response streaming.
    """
)
async def chat_enhanced_stream(
    request: EnhancedChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enhanced streaming chat with knowledge base."""
    async def generate():
        try:
            async for chunk in chatbot_service.chat_stream_with_context(
                db=db,
                user=current_user,
                message=request.message,
                conversation_id=request.conversation_id,
                use_knowledge_base=request.use_knowledge_base
            ):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@chatbot_router.get(
    "/search-knowledge",
    summary="Search knowledge base",
    description="""
    Search the knowledge base for relevant information.

    This endpoint allows direct search of the knowledge base
    without going through the chatbot.
    """
)
async def search_knowledge(
    query: str,
    category: Optional[str] = None,
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search knowledge base directly."""
    try:
        from app.models.enums import CategoryEnum

        # Convert category string to enum if provided
        category_enum = None
        if category:
            try:
                category_enum = CategoryEnum(category)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid category: {category}"
                )

        results = chatbot_service.search_knowledge_base(
            db=db,
            query=query,
            category=category_enum,
            limit=limit
        )

        return {
            "query": query,
            "results_count": len(results),
            "results": results,
            "message": f"Found {len(results)} relevant knowledge sources"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Knowledge search failed: {str(e)}"
        )


@chatbot_router.post(
    "/answer-query/{query_id}",
    summary="Answer a specific query using AI and knowledge base",
    description="""
    Generate an AI answer for a specific query from the database.

    Uses knowledge base and context to provide comprehensive answers.
    """
)
async def answer_query(
    query_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Answer a specific query using enhanced chatbot."""
    try:
        response = await chatbot_service.answer_query(
            db=db,
            user=current_user,
            query_id=query_id
        )

        if "error" in response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response["error"]
            )

        return {
            "query_id": query_id,
            "answer": response["answer"],
            "sources_used": response.get("sources_used", []),
            "confidence": response.get("confidence", "medium"),
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query answering failed: {str(e)}"
        )


@chatbot_router.get(
    "/user-context",
    summary="Get user context for chatbot personalization",
    description="""
    Retrieve the user context that the chatbot uses for personalization.

    Includes:
    - User profile information
    - Recent queries
    - Active tasks
    - Usage statistics
    """
)
async def get_user_context(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user context for chatbot."""
    try:
        context = chatbot_service.get_user_context(db, current_user)

        return {
            "user_context": context,
            "relevant_categories": [
                cat.value for cat in chatbot_service.get_relevant_categories(current_user)
            ],
            "message": "User context retrieved successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user context: {str(e)}"
        )
