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
from app.rag.ingestion import VectorStoreManager


class ChatbotService:
    """Async chatbot service with streaming support."""

    def __init__(self):
        """Initialize Gemini LLM."""
        self.conversations: Dict[str, Any] = {}
        self.llm = None
        self.vector_store = None

        if not LANGCHAIN_AVAILABLE:
            print("[WARNING] Install: pip install langchain langchain-google-genai")
            return

        if not settings.GOOGLE_API_KEY:
            print("[WARNING] Add GOOGLE_API_KEY to .env file")
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
            
            # Initialize Vector Store
            try:
                self.vector_store = VectorStoreManager()
                print("✅ Vector Store initialized successfully")
            except Exception as e:
                print(f"⚠️  Vector Store initialization failed: {e}")
                
        except Exception as e:
            print(f"[ERROR] Failed to initialize Gemini: {e}")

    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        mode: ChatMode = ChatMode.GENERAL,
        use_rag: bool = True
    ) -> tuple[str, str]:
        """
        Generate chat response.

        Args:
            message: User's message
            conversation_id: Optional conversation ID for history
            mode: Chat mode (academic, general, etc.)
            use_rag: Whether to use RAG

        Returns:
            Tuple of (response, conversation_id)
        """
        if not conversation_id:
            conversation_id = f"conv-{uuid.uuid4().hex[:12]}"

        if not self.llm:
            return (
                "[WARNING] Chatbot not configured. Please add GOOGLE_API_KEY to .env and install dependencies.",
                conversation_id
            )

        try:
            # Get or create conversation
            memory = self._get_or_create_memory(conversation_id)

            # Get system prompt based on mode
            system_prompt = self._get_system_prompt(mode)
            
            # RAG Retrieval
            context = ""
            rag_success = False
            
            if use_rag and self.vector_store:
                try:
                    results = self.vector_store.search_similar(message, limit=3)
                    if results:
                        rag_success = True
                        context = "\n\nRelevant Context from Knowledge Base:\n"
                        for chunk in results:
                            context += f"- {chunk.content}\n"
                        context += "\nUse the above context to answer the user's question if relevant."
                    else:
                        # Fallback: No results found
                        print("⚠️ RAG returned no results. Escalating to admin.")
                        return await self._escalate_query(message, conversation_id)
                        
                except Exception as e:
                    print(f"RAG retrieval failed: {e}")
                    # If RAG fails completely, we might also want to escalate or fallback to general knowledge
                    # For now, let's escalate if it was a specific academic query
                    if mode in [ChatMode.ACADEMIC, ChatMode.DOUBT_CLARIFICATION]:
                         return await self._escalate_query(message, conversation_id)

            # Create conversation chain
            conversation = ConversationChain(
                llm=self.llm,
                memory=memory,
                verbose=False
            )

            # Generate response
            # We append context to the input message for the model to see it
            final_input = f"{system_prompt}\n\n{context}\n\nUser Question: {message}"
            
            response = await conversation.apredict(input=final_input)

            return response, conversation_id

        except Exception as e:
            print(f"Chat error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}", conversation_id

    async def _escalate_query(self, message: str, conversation_id: str) -> tuple[str, str]:
        """
        Escalate query to admin by creating a database record.
        """
        from app.core.db import SessionLocal
        from app.models.query import Query
        from app.schemas.query_schema import QueryStatus, QueryCategory, QueryPriority
        
        db = SessionLocal()
        try:
            # Determine student_id (mock for now, ideally from auth context if available)
            # In a real scenario, we'd pass the user_id to the chat method
            student_id = 1 # Default/System user for now
            
            new_query = Query(
                title=message[:50] + "..." if len(message) > 50 else message,
                description=message,
                student_id=student_id,
                status=QueryStatus.OPEN,
                priority=QueryPriority.MEDIUM,
                category=QueryCategory.ACADEMIC
            )
            db.add(new_query)
            db.commit()
            
            escalation_msg = (
                "I apologize, but I couldn't find a specific answer to your query in my knowledge base. "
                "I have escalated this to the administration team. "
                "They will review your query, and once answered, I will be able to help you with this in the future. "
                "You can check the status of your query in the 'My Queries' section."
            )
            return escalation_msg, conversation_id
            
        except Exception as e:
            print(f"Escalation failed: {e}")
            return "I apologize, but I don't have the answer right now. Please try asking a clearer question.", conversation_id
        finally:
            db.close()

    async def chat_stream(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        mode: ChatMode = ChatMode.GENERAL,
        use_rag: bool = True
    ) -> AsyncIterator[str]:
        """
        Generate streaming chat response.

        Args:
            message: User's message
            conversation_id: Optional conversation ID
            mode: Chat mode
            use_rag: Whether to use RAG

        Yields:
            Response chunks as they're generated
        """
        if not self.llm:
            yield "[WARNING] Chatbot not configured. Add GOOGLE_API_KEY to .env"
            return

        try:
            # For streaming, we'll use astream from LangChain
            memory = self._get_or_create_memory(conversation_id or f"conv-{uuid.uuid4().hex[:12]}")

            # RAG Retrieval
            context = ""
            if use_rag and self.vector_store:
                try:
                    results = self.vector_store.search_similar(message, limit=3)
                    if results:
                        context = "\n\nRelevant Context from Knowledge Base:\n"
                        for chunk in results:
                            context += f"- {chunk.content}\n"
                        context += "\nUse the above context to answer the user's question if relevant."
                except Exception as e:
                    print(f"RAG retrieval failed: {e}")

            # Add user message to memory
            # We store the original message in memory, but send augmented message to LLM
            memory.chat_memory.add_user_message(message)
            
            system_prompt = self._get_system_prompt(mode)
            final_input = f"{system_prompt}\n\n{context}\n\nUser Question: {message}"

            # Stream response
            full_response = ""
            async for chunk in self.llm.astream(final_input):
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
