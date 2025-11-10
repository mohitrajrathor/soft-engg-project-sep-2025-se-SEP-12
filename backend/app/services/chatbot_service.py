"""
Async Chatbot Service using LangChain and Google Gemini.
"""

import uuid
from typing import Dict, Optional, AsyncIterator, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    # Define fallback types when LangChain is not available
    ChatGoogleGenerativeAI = None  # type: ignore
    ConversationBufferMemory = None  # type: ignore
    ConversationChain = None  # type: ignore

from app.core.config import settings
from app.schemas.chatbot_schema import ChatMode


class ChatbotService:
    """Async chatbot service with streaming support."""

    def __init__(self):
        """Initialize Gemini LLM."""
        self.conversations: Dict[str, Any] = {}
        self.llm = None

        if not LANGCHAIN_AVAILABLE:
            print("⚠️  Install: pip install langchain langchain-google-genai")
            return

        if not settings.GOOGLE_API_KEY:
            print("⚠️  Add GOOGLE_API_KEY to .env file")
            return

        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
                convert_system_message_to_human=True
            )
            print("✅ Gemini LLM initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")

    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        mode: ChatMode = ChatMode.GENERAL
    ) -> tuple[str, str]:
        """
        Generate chat response.

        Args:
            message: User's message
            conversation_id: Optional conversation ID for history
            mode: Chat mode (academic, general, etc.)

        Returns:
            Tuple of (response, conversation_id)
        """
        if not conversation_id:
            conversation_id = f"conv-{uuid.uuid4().hex[:12]}"

        if not self.llm:
            return (
                "⚠️ Chatbot not configured. Please add GOOGLE_API_KEY to .env and install dependencies.",
                conversation_id
            )

        try:
            # Get or create conversation
            memory = self._get_or_create_memory(conversation_id)

            # Get system prompt based on mode
            system_prompt = self._get_system_prompt(mode)

            # Create conversation chain
            conversation = ConversationChain(
                llm=self.llm,
                memory=memory,
                verbose=False
            )

            # Generate response
            response = await conversation.apredict(input=message)

            return response, conversation_id

        except Exception as e:
            print(f"Chat error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}", conversation_id

    async def chat_stream(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        mode: ChatMode = ChatMode.GENERAL
    ) -> AsyncIterator[str]:
        """
        Generate streaming chat response.

        Args:
            message: User's message
            conversation_id: Optional conversation ID
            mode: Chat mode

        Yields:
            Response chunks as they're generated
        """
        if not self.llm:
            yield "⚠️ Chatbot not configured. Add GOOGLE_API_KEY to .env"
            return

        try:
            # For streaming, we'll use astream from LangChain
            memory = self._get_or_create_memory(conversation_id or f"conv-{uuid.uuid4().hex[:12]}")

            # Add user message to memory
            memory.chat_memory.add_user_message(message)

            # Stream response
            full_response = ""
            async for chunk in self.llm.astream(message):
                content = chunk.content if hasattr(chunk, 'content') else str(chunk)
                full_response += content
                yield content

            # Add assistant response to memory
            memory.chat_memory.add_ai_message(full_response)

        except Exception as e:
            yield f"Error: {str(e)}"

    def _get_or_create_memory(self, conversation_id: str) -> Any:
        """Get or create conversation memory."""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="history"
            )
        return self.conversations[conversation_id]

    def _get_system_prompt(self, mode: ChatMode) -> str:
        """Get system prompt based on mode."""
        prompts = {
            ChatMode.ACADEMIC: "You are AURA, an academic AI assistant. Provide clear, educational explanations with examples.",
            ChatMode.DOUBT_CLARIFICATION: "You are AURA, helping students clarify doubts. Ask clarifying questions and provide step-by-step explanations.",
            ChatMode.STUDY_HELP: "You are AURA, a study assistant. Help with study strategies, time management, and learning techniques.",
            ChatMode.GENERAL: "You are AURA, an AI teaching assistant. Be helpful, educational, and encouraging."
        }
        return prompts.get(mode, prompts[ChatMode.GENERAL])

    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation history."""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    def get_conversation_history(self, conversation_id: str) -> list:
        """Get conversation history."""
        if conversation_id in self.conversations:
            memory = self.conversations[conversation_id]
            return memory.chat_memory.messages
        return []


# Global chatbot instance
chatbot_service = ChatbotService()
