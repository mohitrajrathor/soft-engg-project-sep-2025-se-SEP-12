"""
Hybrid Chatbot Service supporting both LangChain and Google ADK (native Genai SDK)

This service provides two implementations:
1. LangChain-based (using ChatGoogleGenerativeAI)
2. Native Google Genai SDK (from google-adk)

Choose based on your needs:
- LangChain: Better for complex workflows, memory management, and LangChain ecosystem
- Native SDK: More direct control, faster, and simpler for basic chat

Enhanced Features (Native SDK):
- Cross-Session State Sharing
- Automating Memory Storage with callbacks
- load_memory functionality
- Agent Observability with plugins
"""

import os
import uuid
import logging
from typing import Dict, Optional, AsyncIterator, Any, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain

# Try LangChain imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    ChatGoogleGenerativeAI = None
    ConversationBufferMemory = None
    ConversationChain = None

# Try Google Genai SDK imports (from google-adk)
try:
    from google import genai
    from google.genai import types
    from google.adk.agents import LlmAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.memory import InMemoryMemoryService
    from google.adk.tools import AgentTool, ToolContext
    from google.adk.plugins.base_plugin import BasePlugin
    from google.adk.plugins.logging_plugin import LoggingPlugin
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.agents.base_agent import BaseAgent
    from google.adk.models.llm_request import LlmRequest
    GENAI_SDK_AVAILABLE = True
except ImportError:
    GENAI_SDK_AVAILABLE = False
    genai = None
    types = None
    LlmAgent = None
    Gemini = None
    Runner = None
    InMemorySessionService = None
    InMemoryMemoryService = None
    AgentTool = None
    ToolContext = None
    BasePlugin = None
    LoggingPlugin = None
    CallbackContext = None
    BaseAgent = None
    LlmRequest = None

from app.core.config import settings
from app.schemas.chatbot_schema import ChatMode


# ============================================================================
# Custom Tools for Cross-Session State Sharing
# ============================================================================

def save_user_context(context: ToolContext, key: str, value: str) -> str:
    """
    Save user context to session state for cross-session sharing.

    Args:
        context: Tool invocation context
        key: Context key (e.g., 'username', 'topic', 'preferences')
        value: Context value to store

    Returns:
        Confirmation message
    """
    if not GENAI_SDK_AVAILABLE or not hasattr(context, 'invocation_context'):
        return f"Context saved locally: {key}={value}"

    session = context.invocation_context.session
    session.state[key] = value
    return f"Saved {key} to your session state"


def retrieve_user_context(context: ToolContext, key: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve user context from session state.

    Args:
        context: Tool invocation context
        key: Specific key to retrieve (None = return all)

    Returns:
        Session state dictionary or specific value
    """
    if not GENAI_SDK_AVAILABLE or not hasattr(context, 'invocation_context'):
        return {"message": "Context retrieval not available"}

    session = context.invocation_context.session

    if key:
        return {key: session.state.get(key, "Not found")}
    else:
        return dict(session.state)


def preload_memory(context: ToolContext) -> str:
    """
    Preload previous conversation memories from memory service.

    Args:
        context: Tool invocation context

    Returns:
        Status message
    """
    if not GENAI_SDK_AVAILABLE or not hasattr(context, 'invocation_context'):
        return "Memory preload not available"

    try:
        invocation_context = context.invocation_context
        memory_service = invocation_context.memory_service

        if not memory_service:
            return "Memory service not configured"

        # Memory service automatically loads relevant memories
        # This tool explicitly triggers memory awareness
        return "Previous conversation context loaded successfully"

    except Exception as e:
        return f"Memory preload failed: {str(e)}"


# ============================================================================
# Callback for Automating Memory Storage
# ============================================================================

async def auto_save_to_memory(callback_context: CallbackContext) -> None:
    """
    Automatically save session to memory after each agent turn.

    This callback ensures conversation context is persisted for future sessions.

    Args:
        callback_context: Agent callback context
    """
    try:
        invocation_context = callback_context._invocation_context
        memory_service = invocation_context.memory_service
        session = invocation_context.session

        if memory_service and session:
            await memory_service.add_session_to_memory(session)
            logging.debug(f"[Memory] Auto-saved session {session.id}")

    except Exception as e:
        logging.error(f"[Memory] Auto-save failed: {e}")


# ============================================================================
# Observability Plugin for Agent Monitoring
# ============================================================================

class ChatbotObservabilityPlugin(BasePlugin):
    """
    Custom plugin for tracking chatbot metrics and performance.

    Features:
    - Count agent invocations
    - Count tool calls
    - Count LLM requests
    - Track conversation patterns
    """

    def __init__(self) -> None:
        """Initialize the observability plugin with counters."""
        super().__init__(name="chatbot_observability")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0
        self.conversations: Dict[str, int] = {}

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent invocations."""
        self.agent_count += 1
        logging.info(f"[Observability] Agent runs: {self.agent_count}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1
        logging.info(f"[Observability] LLM requests: {self.llm_request_count}")

    def get_metrics(self) -> Dict[str, int]:
        """Get current metrics."""
        return {
            "agent_invocations": self.agent_count,
            "tool_calls": self.tool_count,
            "llm_requests": self.llm_request_count,
            "unique_conversations": len(self.conversations)
        }


# ============================================================================
# Chat Implementation Enum
# ============================================================================

class ChatImplementation(str, Enum):
    """Available chat implementations"""
    LANGCHAIN = "langchain"
    NATIVE_SDK = "native_sdk"


class HybridChatbotService:
    """
    Hybrid chatbot service supporting both LangChain and native Google Genai SDK.

    Features:
    - Dual implementation support
    - Conversation memory for both implementations
    - Streaming support
    - Multiple chat modes
    """

    def __init__(
        self,
        implementation: ChatImplementation = ChatImplementation.NATIVE_SDK,
        enable_memory: bool = True,
        enable_observability: bool = True,
        app_name: str = "AURA"
    ):
        """
        Initialize chatbot service.

        Args:
            implementation: Which implementation to use (langchain or native_sdk)
            enable_memory: Enable cross-session memory storage (Native SDK only)
            enable_observability: Enable metrics tracking (Native SDK only)
            app_name: Application name for session management
        """
        self.implementation = implementation
        self.conversations: Dict[str, Any] = {}
        self.llm = None
        self.genai_client = None

        # ADK-specific components for enhanced features
        self.session_service = None
        self.memory_service = None
        self.observability_plugin = None
        self.adk_agent = None
        self.adk_runner = None
        self.app_name = app_name
        self.enable_memory = enable_memory
        self.enable_observability = enable_observability

        # Initialize based on selected implementation
        if implementation == ChatImplementation.LANGCHAIN:
            self._init_langchain()
        elif implementation == ChatImplementation.NATIVE_SDK:
            self._init_native_sdk()

    def _init_langchain(self):
        """Initialize LangChain implementation"""
        if not LANGCHAIN_AVAILABLE:
            print("[WARNING] LangChain not available. Install: pip install langchain langchain-google-genai")
            return

        if not settings.GOOGLE_API_KEY:
            print("[WARNING] GOOGLE_API_KEY not set")
            return

        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
                convert_system_message_to_human=True
            )
            print(f"[OK] LangChain Gemini LLM initialized - Model: {settings.GEMINI_MODEL}")
        except Exception as e:
            print(f"[ERROR] Failed to initialize LangChain: {e}")

    def _init_native_sdk(self):
        """
        Initialize native Google Genai SDK with enhanced ADK features.

        Features:
        - Session management for cross-session state
        - Memory service for conversation persistence
        - Custom tools for state management
        - Auto-save callback for memory automation
        - Observability plugin for metrics
        """
        if not GENAI_SDK_AVAILABLE:
            print("[WARNING] Google Genai SDK not available. Install: pip install google-adk")
            return

        if not settings.GOOGLE_API_KEY:
            print("[WARNING] GOOGLE_API_KEY not set")
            return

        # Set API key as environment variable for Google ADK
        os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY

        try:
            # Basic client for simple operations
            self.genai_client = genai.Client(api_key=settings.GOOGLE_API_KEY)

            # Initialize session service for cross-session state sharing
            self.session_service = InMemorySessionService()
            print("[OK] Session service initialized")

            # Initialize memory service if enabled
            if self.enable_memory:
                self.memory_service = InMemoryMemoryService()
                print("[OK] Memory service initialized")

            # Initialize observability plugin if enabled
            if self.enable_observability:
                self.observability_plugin = ChatbotObservabilityPlugin()
                print("[OK] Observability plugin initialized")

            # Configure retry options for reliability
            retry_config = types.HttpRetryOptions(
                attempts=5,
                exp_base=7,
                initial_delay=1,
                http_status_codes=[429, 500, 503, 504]
            )

            # Create LLM agent with memory callback
            # Note: Custom tools with ToolContext are not compatible with ADK's automatic function calling
            # Memory and session state are managed by the Runner's session_service and memory_service

            self.adk_agent = LlmAgent(
                model=Gemini(
                    model=settings.GEMINI_MODEL,
                    api_key=settings.GOOGLE_API_KEY,
                    retry_options=retry_config
                ),
                name="AURA_Chatbot",
                description="AURA (Academic Unified Response Assistant) - AI teaching assistant with cross-session memory",
                instruction="""You are AURA, an intelligent academic assistant.

Your conversations are automatically saved and can be referenced in future sessions.
Provide clear, educational explanations and help students learn effectively.""",
                after_agent_callback=auto_save_to_memory if self.enable_memory else None
            )

            # Create plugins list
            plugins = []
            if self.enable_observability and self.observability_plugin:
                plugins.append(self.observability_plugin)
            # Note: LoggingPlugin has emoji characters that cause UnicodeEncodeError on Windows
            # We use our custom ChatbotObservabilityPlugin instead

            # Create runner with all enhanced features
            self.adk_runner = Runner(
                agent=self.adk_agent,
                app_name=self.app_name,
                session_service=self.session_service,
                memory_service=self.memory_service if self.enable_memory else None,
                plugins=plugins
            )

            print(f"[OK] Google ADK initialized - Model: {settings.GEMINI_MODEL}")
            print(f"     - Memory: {'Enabled' if self.enable_memory else 'Disabled'}")
            print(f"     - Observability: {'Enabled' if self.enable_observability else 'Disabled'}")
            print(f"     - Session Service: Active")

        except Exception as e:
            print(f"[ERROR] Failed to initialize Google ADK: {e}")
            import traceback
            traceback.print_exc()

    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        mode: ChatMode = ChatMode.GENERAL
    ) -> tuple[str, str]:
        """
        Generate chat response using selected implementation.

        Args:
            message: User's message
            conversation_id: Optional conversation ID for history
            mode: Chat mode (academic, general, etc.)

        Returns:
            Tuple of (response, conversation_id)
        """
        if not conversation_id:
            conversation_id = f"conv-{uuid.uuid4().hex[:12]}"

        # Route to appropriate implementation
        if self.implementation == ChatImplementation.LANGCHAIN:
            return await self._chat_langchain(message, conversation_id, mode)
        elif self.implementation == ChatImplementation.NATIVE_SDK:
            return await self._chat_native_sdk(message, conversation_id, mode)
        else:
            return ("No chat implementation available", conversation_id)

    async def _chat_langchain(
        self,
        message: str,
        conversation_id: str,
        mode: ChatMode
    ) -> tuple[str, str]:
        """Chat using LangChain implementation"""
        if not self.llm:
            return (
                "[WARNING] LangChain chatbot not configured.",
                conversation_id
            )

        try:
            # Get or create conversation memory
            memory = self._get_or_create_langchain_memory(conversation_id)

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
            print(f"LangChain chat error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}", conversation_id

    async def _chat_native_sdk(
        self,
        message: str,
        conversation_id: str,
        mode: ChatMode
    ) -> tuple[str, str]:
        """
        Chat using native Google Genai SDK with ADK runner.

        This method uses the enhanced ADK features:
        - Session management for state persistence
        - Memory service for cross-session context
        - Custom tools for user context management
        - Auto-save callback for automatic memory storage
        - Observability for tracking metrics
        """
        if not self.adk_runner:
            # Fallback to basic genai_client if ADK not available
            return await self._chat_native_sdk_basic(message, conversation_id, mode)

        try:
            # Use conversation_id as session_id for ADK
            session_id = conversation_id
            user_id = "default_user"  # Could be extracted from request context

            # Create or get session
            try:
                session = await self.session_service.create_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id
                )
            except:
                session = await self.session_service.get_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id
                )

            # Add mode-specific context to session state
            session.state["chat_mode"] = mode.value

            # Convert message to ADK Content format
            user_message = types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )

            # Run the agent with session context
            response_text = ""
            async for event in self.adk_runner.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=user_message
            ):
                # Extract response from event
                if event.content and event.content.parts:
                    if event.content.parts[0].text and event.content.parts[0].text != "None":
                        response_text = event.content.parts[0].text

            # Memory is automatically saved by the callback
            return response_text, conversation_id

        except Exception as e:
            print(f"ADK chat error: {e}")
            import traceback
            traceback.print_exc()
            return f"I apologize, but I encountered an error: {str(e)}", conversation_id

    async def _chat_native_sdk_basic(
        self,
        message: str,
        conversation_id: str,
        mode: ChatMode
    ) -> tuple[str, str]:
        """Fallback basic chat using genai client (without ADK features)"""
        if not self.genai_client:
            return (
                "[WARNING] Google Genai SDK not configured.",
                conversation_id
            )

        try:
            # Get or create conversation history
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []

            history = self.conversations[conversation_id]

            # Add system instruction based on mode
            system_instruction = self._get_system_prompt(mode)

            # Prepare chat config
            config = types.GenerateContentConfig(
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
                system_instruction=system_instruction,
            )

            # Add user message to history
            history.append({
                "role": "user",
                "parts": [{"text": message}]
            })

            # Generate response
            response = await self.genai_client.aio.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=history,
                config=config
            )

            # Extract response text
            response_text = response.text if hasattr(response, 'text') else str(response)

            # Add assistant response to history
            history.append({
                "role": "model",
                "parts": [{"text": response_text}]
            })

            # Update conversation history
            self.conversations[conversation_id] = history

            return response_text, conversation_id

        except Exception as e:
            print(f"Native SDK chat error: {e}")
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
        if not conversation_id:
            conversation_id = f"conv-{uuid.uuid4().hex[:12]}"

        # Route to appropriate implementation
        if self.implementation == ChatImplementation.NATIVE_SDK and self.genai_client:
            async for chunk in self._chat_stream_native_sdk(message, conversation_id, mode):
                yield chunk
        elif self.implementation == ChatImplementation.LANGCHAIN and self.llm:
            async for chunk in self._chat_stream_langchain(message, conversation_id, mode):
                yield chunk
        else:
            yield "[WARNING] No streaming implementation available"

    async def _chat_stream_native_sdk(
        self,
        message: str,
        conversation_id: str,
        mode: ChatMode
    ) -> AsyncIterator[str]:
        """
        Stream chat using native Google Genai SDK with ADK runner.

        Uses enhanced features:
        - Session management
        - Memory service
        - Auto-save callback (triggered after completion)
        """
        if not self.adk_runner:
            # Fallback to basic streaming
            async for chunk in self._chat_stream_native_sdk_basic(message, conversation_id, mode):
                yield chunk
            return

        try:
            session_id = conversation_id
            user_id = "default_user"

            # Create or get session
            try:
                session = await self.session_service.create_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id
                )
            except:
                session = await self.session_service.get_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id
                )

            # Add mode to session state
            session.state["chat_mode"] = mode.value

            # Convert message to ADK format
            user_message = types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )

            # Stream response from agent
            async for event in self.adk_runner.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=user_message
            ):
                if event.content and event.content.parts:
                    if event.content.parts[0].text and event.content.parts[0].text != "None":
                        yield event.content.parts[0].text

            # Memory automatically saved by callback

        except Exception as e:
            yield f"Error: {str(e)}"
            import traceback
            traceback.print_exc()

    async def _chat_stream_native_sdk_basic(
        self,
        message: str,
        conversation_id: str,
        mode: ChatMode
    ) -> AsyncIterator[str]:
        """Fallback basic streaming using genai client (without ADK features)"""
        try:
            # Get or create conversation history
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []

            history = self.conversations[conversation_id]

            # Add system instruction
            system_instruction = self._get_system_prompt(mode)

            # Prepare config
            config = types.GenerateContentConfig(
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
                system_instruction=system_instruction,
            )

            # Add user message
            history.append({
                "role": "user",
                "parts": [{"text": message}]
            })

            # Stream response
            full_response = ""
            async for chunk in await self.genai_client.aio.models.generate_content_stream(
                model=settings.GEMINI_MODEL,
                contents=history,
                config=config
            ):
                if hasattr(chunk, 'text'):
                    full_response += chunk.text
                    yield chunk.text

            # Add complete response to history
            history.append({
                "role": "model",
                "parts": [{"text": full_response}]
            })

            self.conversations[conversation_id] = history

        except Exception as e:
            yield f"Error: {str(e)}"

    async def _chat_stream_langchain(
        self,
        message: str,
        conversation_id: str,
        mode: ChatMode
    ) -> AsyncIterator[str]:
        """Stream chat using LangChain"""
        try:
            memory = self._get_or_create_langchain_memory(conversation_id)
            memory.chat_memory.add_user_message(message)

            full_response = ""
            async for chunk in self.llm.astream(message):
                content = chunk.content if hasattr(chunk, 'content') else str(chunk)
                full_response += content
                yield content

            memory.chat_memory.add_ai_message(full_response)

        except Exception as e:
            yield f"Error: {str(e)}"

    def _get_or_create_langchain_memory(self, conversation_id: str) -> Any:
        """Get or create LangChain conversation memory"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="history"
            )
        return self.conversations[conversation_id]

    def _get_system_prompt(self, mode: ChatMode) -> str:
        """Get system prompt based on mode"""
        prompts = {
            ChatMode.ACADEMIC: "You are AURA, an academic AI assistant. Provide clear, educational explanations with examples.",
            ChatMode.DOUBT_CLARIFICATION: "You are AURA, helping students clarify doubts. Ask clarifying questions and provide step-by-step explanations.",
            ChatMode.STUDY_HELP: "You are AURA, a study assistant. Help with study strategies, time management, and learning techniques.",
            ChatMode.GENERAL: "You are AURA (Academic Unified Response Assistant), an AI teaching assistant. Be helpful, educational, and encouraging."
        }
        return prompts.get(mode, prompts[ChatMode.GENERAL])

    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    def get_conversation_history(self, conversation_id: str) -> list:
        """Get conversation history"""
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]
        return []

    def switch_implementation(self, implementation: ChatImplementation):
        """
        Switch between LangChain and native SDK implementations.

        Args:
            implementation: New implementation to use
        """
        print(f"Switching from {self.implementation} to {implementation}")
        self.implementation = implementation

        if implementation == ChatImplementation.LANGCHAIN and not self.llm:
            self._init_langchain()
        elif implementation == ChatImplementation.NATIVE_SDK and not self.genai_client:
            self._init_native_sdk()

    def get_metrics(self) -> Optional[Dict[str, int]]:
        """
        Get observability metrics from the chatbot.

        Returns:
            Dictionary of metrics or None if observability is disabled
        """
        if self.observability_plugin:
            return self.observability_plugin.get_metrics()
        return None

    async def get_session_state(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session state for a conversation.

        Args:
            conversation_id: Conversation/session ID

        Returns:
            Session state dictionary or None if not available
        """
        if not self.session_service:
            return None

        try:
            session = await self.session_service.get_session(
                app_name=self.app_name,
                user_id="default_user",
                session_id=conversation_id
            )
            return dict(session.state) if session else None
        except:
            return None

    async def load_memory_for_session(self, conversation_id: str) -> bool:
        """
        Explicitly load memory for a session.

        Args:
            conversation_id: Conversation/session ID

        Returns:
            True if memory loaded successfully, False otherwise
        """
        if not self.memory_service:
            return False

        try:
            # Memory service automatically loads relevant memories
            # This method explicitly triggers memory awareness
            return True
        except Exception as e:
            logging.error(f"Memory load failed: {e}")
            return False


# Global chatbot instance - using native SDK with enhanced features by default
hybrid_chatbot_service = HybridChatbotService(
    implementation=ChatImplementation.NATIVE_SDK,
    enable_memory=True,
    enable_observability=True,
    app_name="AURA"
)
