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
from app.services.chatbot_service import chatbot_service
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
    return {
        "configured": chatbot_service.llm is not None,
        "model": chatbot_service.llm.model if chatbot_service.llm else None,
        "available_modes": [mode.value for mode in ChatMode],
        "message": "Chatbot ready" if chatbot_service.llm else "Configure GOOGLE_API_KEY in .env"
    }
