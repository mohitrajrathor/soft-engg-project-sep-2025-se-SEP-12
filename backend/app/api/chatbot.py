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
