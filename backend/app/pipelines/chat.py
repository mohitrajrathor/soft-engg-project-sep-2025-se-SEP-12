"""
Multilingual Chat Pipeline
Production-ready LangGraph pipeline for AURA's multilingual chat system.
"""

from typing import Dict, Any, List, Optional, TypedDict
from datetime import datetime
from uuid import UUID, uuid4
import logging
import json
import os
import re

from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session
import requests

# Patch langchain for langgraph compatibility
import langchain
if not hasattr(langchain, 'debug'):
    langchain.debug = False

from app.core.db import SessionLocal
from app.models.chat import Chat
from app.models.query import RAGQuery, SourceTypeEnum
from app.models.knowledge import KnowledgeChunk, KnowledgeSource
from app.pipelines.search import call_gemini_embedding_api, semantic_search
from app.core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Configuration
GOOGLE_API_KEY = settings.GOOGLE_API_KEY
EMBEDDING_MODEL = "text-embedding-004"
LLM_MODEL = settings.LLM_MODEL
EMBEDDING_DIMENSION = 768

# Chat-specific configuration
MIN_TOKEN_COUNT = 3
SIMILARITY_THRESHOLD = 0.3
MAX_CONTEXT_TOKENS = 4000
DEFAULT_TOP_K = 5
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30


# ============================================================================
# STATE DEFINITION
# ============================================================================

class ChatState(TypedDict, total=False):
    """
    Graph state for multilingual chat pipeline.
    """
    # Input
    chat_id: str
    input_text: str
    user_id: Optional[str]

    # Language processing
    detected_language: Optional[str]
    translated_text: Optional[str]
    is_english: Optional[bool]
    token_count: Optional[int]

    # Search and retrieval
    query_embedding: Optional[List[float]]
    search_results: Optional[List[Dict[str, Any]]]
    relevant_chunks: Optional[List[Dict[str, Any]]]
    has_relevant_context: Optional[bool]
    similarity_score: Optional[float]

    # Response generation
    answer_text: Optional[str]
    confidence: Optional[float]
    has_answered: Optional[bool]
    translated_answer: Optional[str]

    # Metadata
    processing_time_ms: Optional[int]
    token_usage: Optional[Dict[str, int]]
    retrieved_document_ids: Optional[List[str]]
    db_session: Optional[Session]
    input_metadata: Optional[Dict[str, Any]]

    # Error handling
    error: Optional[str]
    retry_count: Optional[int]
    status: Optional[str]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def estimate_token_count(text: str) -> int:
    return len(text.split())

def validate_input_tokens(text: str) -> bool:
    return estimate_token_count(text) >= MIN_TOKEN_COUNT

def fallback_language_detection(text: str) -> str:
    try:
        from langdetect import detect, detect_langs
        text_clean = text.strip()
        if len(text_clean) < 3:
            return 'en'
        langs = detect_langs(text_clean)
        if langs and len(langs) > 0:
            detected_lang = langs[0].lang
            confidence = langs[0].prob
            if confidence > 0.5:
                return detected_lang
        return detect(text_clean)
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return "en"

def detect_language_universal(text: str) -> str:
    """
    Detect language with high confidence threshold.
    Defaults to English unless very confident it's another language.
    """
    try:
        from langdetect import detect, detect_langs
        text_clean = text.strip()
        if len(text_clean) < 3:
            return 'en'
        langs = detect_langs(text_clean)
        if langs and len(langs) > 0:
            detected_lang = langs[0].lang
            confidence = langs[0].prob
            # Only accept non-English if confidence is very high (>0.9)
            # This prevents misdetecting English phrases as French
            if detected_lang == 'en':
                return 'en'
            elif confidence > 0.9:
                return detected_lang
            else:
                # Low confidence, default to English
                return 'en'
    except Exception:
        pass
    
    # Fallback to English
    return 'en'

def _try_gemini_language_detection(text: str) -> str:
    if not GOOGLE_API_KEY:
        return 'unknown'
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{LLM_MODEL}:generateContent"
    prompt = f"Language of this text: {text}\nReturn only 2-letter code (en/es/hi/fr/de/etc):"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 5}
    }
    try:
        response = requests.post(f"{endpoint}?key={GOOGLE_API_KEY}", json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                detected_lang = candidates[0]["content"]["parts"][0]["text"].strip().lower()
                if len(detected_lang) == 2 and detected_lang.isalpha():
                    return detected_lang
    except Exception:
        pass
    return 'unknown'

def call_gemini_translate_api(text: str, target_language: str = 'English') -> str:
    if not GOOGLE_API_KEY:
        return text
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{LLM_MODEL}:generateContent"
    prompt = f"Translate the following text to {target_language}.\nOnly return the translated text, nothing else.\n\nText to translate: {text}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2000}
    }
    try:
        response = requests.post(f"{endpoint}?key={GOOGLE_API_KEY}", json=payload, headers={"Content-Type": "application/json"}, timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                return candidates[0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        logger.error(f"Translation failed: {e}")
    return text

def get_language_name(language_code: str) -> str:
    if language_code == 'en': return 'English'
    if not GOOGLE_API_KEY: return language_code
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{LLM_MODEL}:generateContent"
    prompt = f"What is the full name of the language with code '{language_code}'?\nReturn only the language name."
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 50}
    }
    try:
        response = requests.post(f"{endpoint}?key={GOOGLE_API_KEY}", json=payload, headers={"Content-Type": "application/json"}, timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                return candidates[0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
    return language_code

def call_gemini_llm_api(prompt: str, context: str) -> Dict[str, Any]:
    if not GOOGLE_API_KEY:
        return {"error": "API key not available"}
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{LLM_MODEL}:generateContent"
    full_prompt = f"""You are AURA, an AI assistant for IITM BS Degree students.
Provide helpful, accurate, and concise answers based on the context provided.

Context:
{context}

Question: {prompt}

Instructions:
1. Answer only based on the provided context
2. If the context doesn't contain relevant information, say so clearly
3. Be concise but comprehensive
4. Use a helpful and friendly tone
5. Format your response clearly

Response:"""
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048, "topP": 0.8, "topK": 40}
    }
    try:
        response = requests.post(f"{endpoint}?key={GOOGLE_API_KEY}", json=payload, headers={"Content-Type": "application/json"}, timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                answer_text = candidates[0]["content"]["parts"][0]["text"].strip()
                confidence = calculate_response_confidence(answer_text, context)
                return {
                    "answer": answer_text,
                    "confidence": confidence,
                    "token_usage": result.get("usageMetadata", {}),
                    "success": True
                }
        return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def calculate_response_confidence(answer: str, context: str) -> float:
    if not answer or "I don't have information" in answer:
        return 0.2
    if len(answer) < 20:
        return 0.4
    elif len(answer) < 50:
        return 0.6
    elif any(phrase in answer.lower() for phrase in ["based on", "according to", "specific"]):
        return 0.9
    else:
        return 0.7


# ============================================================================
# PIPELINE NODES
# ============================================================================

def validate_and_detect_language(state: ChatState) -> ChatState:
    try:
        input_text = state["input_text"]
        if not input_text or len(input_text.strip()) == 0:
            state["error"] = "Input text cannot be empty"
            state["status"] = "failed"
            return state

        if not validate_input_tokens(input_text):
            state["error"] = f"Input must contain at least {MIN_TOKEN_COUNT} tokens"
            state["status"] = "failed"
            return state

        detected_language = detect_language_universal(input_text)
        state["detected_language"] = detected_language
        state["is_english"] = (detected_language == 'en')
        state["token_count"] = estimate_token_count(input_text)
        state["status"] = "language_detected"
        return state
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state

def translate_to_english(state: ChatState) -> ChatState:
    if state.get("error") or state.get("is_english"):
        state["translated_text"] = state["input_text"]
        return state
    try:
        translated = call_gemini_translate_api(state["input_text"], "English")
        state["translated_text"] = translated
        state["status"] = "translated"
        return state
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state

def generate_query_embedding_node(state: ChatState) -> ChatState:
    if state.get("error"): return state
    try:
        query_text = state.get("translated_text")
        embedding = call_gemini_embedding_api(query_text)
        if not embedding:
            state["error"] = "Failed to generate query embedding"
            state["status"] = "failed"
            return state
        state["query_embedding"] = embedding
        state["status"] = "embedding_generated"
        return state
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state

def search_knowledge_base(state: ChatState) -> ChatState:
    if state.get("error"): return state
    session = state.get("db_session") or SessionLocal()
    close_session = not state.get("db_session")
    try:
        embedding = state["query_embedding"]
        search_results = semantic_search(session=session, embedding=embedding, top_k=DEFAULT_TOP_K, filters={})
        state["search_results"] = search_results or []
        
        relevant_chunks = []
        max_similarity = 0.0
        for result in state["search_results"]:
            score = result.get("score", 0.0)
            if score >= SIMILARITY_THRESHOLD:
                relevant_chunks.append(result)
                max_similarity = max(max_similarity, score)
        
        state["relevant_chunks"] = relevant_chunks
        state["similarity_score"] = max_similarity
        state["has_relevant_context"] = len(relevant_chunks) > 0
        state["retrieved_document_ids"] = [c["source_id"] for c in relevant_chunks]
        state["status"] = "search_completed"
        return state
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state
    finally:
        if close_session: session.close()

def generate_response(state: ChatState) -> ChatState:
    if state.get("error"): return state
    try:
        query_text = state["translated_text"]
        relevant_chunks = state.get("relevant_chunks", [])
        
        if not state.get("has_relevant_context"):
            state["answer_text"] = "I don't have specific information about your question in my knowledge base. Could you please rephrase your question or ask about IITM BS Degree programs, admissions, courses, or related topics?"
            state["confidence"] = 0.2
            state["has_answered"] = False
            state["status"] = "no_context_response"
            return state

        context_parts = []
        for chunk in relevant_chunks[:3]:
            source_title = chunk.get('source_title', 'Unknown Source')
            content = chunk.get('content', '')
            if content:
                context_parts.append(f"Source: {source_title}\nContent: {content}")
        context = "\n\n".join(context_parts)

        llm_result = call_gemini_llm_api(query_text, context)
        if llm_result.get("error"):
            state["error"] = llm_result["error"]
            state["status"] = "llm_failed"
            return state

        answer_text = llm_result["answer"]
        
        # ================================================================
        # INTELLIGENT ESCALATION SYSTEM (Two-Stage)
        # ================================================================
        
        from app.services.escalation_service import EscalationService
        from app.services.query_classifier import get_classifier
        from app.core.db import SessionLocal

        classifier = get_classifier()
        
        # STAGE 1: Pre-LLM Escalation (Low retrieval scores)
        should_escalate_retrieval, reason_retrieval = classifier.should_escalate(
            context_score=state.get('similarity_score', 0.0),
            retrieved_chunks=len(state.get('relevant_chunks', [])),
            query=state.get('translated_text', state.get('input_text', ''))
        )
        
        # STAGE 2: Post-LLM Escalation (LLM couldn't answer despite having context)
        # Check if LLM response indicates inability to answer
        unable_to_answer_phrases = [
            "i don't have",
            "i cannot answer",
            "i am unable to",
            "does not contain",
            "no information about",
            "cannot provide",
            "i'm sorry",
            "unfortunately",
            "not available",
            "not found in"
        ]
        
        answer_lower = answer_text.lower()
        llm_cannot_answer = any(phrase in answer_lower for phrase in unable_to_answer_phrases)
        
        # Combine both escalation triggers
        should_escalate = should_escalate_retrieval or llm_cannot_answer
        
        if llm_cannot_answer:
            reason = "llm_unable_to_answer"
            print(f"🔔 POST-LLM ESCALATION: LLM could not answer despite {len(state.get('relevant_chunks', []))} chunks")
        elif should_escalate_retrieval:
            reason = reason_retrieval
        else:
            reason = None

        if should_escalate:
            print(f"🔔 ESCALATION TRIGGERED: Query='{state.get('translated_text')}', Reason={reason}")
            print(f"   Context Score: {state.get('similarity_score', 0.0):.4f}")
            print(f"   Chunks Retrieved: {len(state.get('relevant_chunks', []))}")
            print(f"   LLM Cannot Answer: {llm_cannot_answer}")
            
            # Create escalation (synchronous)
            db = SessionLocal()
            try:
                service = EscalationService(db)
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        escalation = loop.run_until_complete(service.escalate_query(
                            query_text=state.get('translated_text', state.get('input_text', '')),
                            student_id=int(state.get('user_id')) if state.get('user_id') else 1,
                            query_language=state.get('detected_language', 'en'),
                            context_score=state.get('similarity_score', 0.0),
                            original_chat_id=state.get('chat_id')
                        ))
                    else:
                        escalation = loop.run_until_complete(service.escalate_query(
                            query_text=state.get('translated_text', state.get('input_text', '')),
                            student_id=int(state.get('user_id')) if state.get('user_id') else 1,
                            query_language=state.get('detected_language', 'en'),
                            context_score=state.get('similarity_score', 0.0),
                            original_chat_id=state.get('chat_id')
                        ))
                except RuntimeError:
                    escalation = asyncio.run(service.escalate_query(
                        query_text=state.get('translated_text', state.get('input_text', '')),
                        student_id=int(state.get('user_id')) if state.get('user_id') else 1,
                        query_language=state.get('detected_language', 'en'),
                        context_score=state.get('similarity_score', 0.0),
                        original_chat_id=state.get('chat_id')
                    ))
                
                # Get escalation notification message
                notification = service.get_escalation_message(
                    state.get('detected_language', 'en'),
                    escalation.category
                )
                print(f"✅ Escalation created! ID={escalation.id}, Category={escalation.category}")
                print(f"📧 Notification message: {notification[:100]}...")
                
                # IMPORTANT: Replace the "I don't have info" message with escalation notification
                if llm_cannot_answer:
                    # If LLM couldn't answer, replace entire response with notification
                    answer_text = notification
                else:
                    # If low score, append notification
                    answer_text = answer_text + "\n\n" + notification
                
                # Store escalation metadata
                state['metadata'] = state.get('metadata', {})
                state['metadata']['escalated'] = True
                state['metadata']['escalation_id'] = escalation.id
                state['metadata']['escalation_category'] = escalation.category
                state['metadata']['escalation_reason'] = reason
                
            except Exception as e:
                print(f"❌ Warning: Failed to create escalation: {e}")
                import traceback
                traceback.print_exc()
            finally:
                db.close()

        if not answer_text:
            state["answer_text"] = "I apologize, but I couldn't generate a response. Please try asking again."
            state["confidence"] = 0.0
            state["has_answered"] = False
            state["status"] = "empty_response"
            return state

        state["answer_text"] = answer_text
        state["confidence"] = llm_result["confidence"]
        state["has_answered"] = True
        state["token_usage"] = llm_result.get("token_usage", {})
        state["status"] = "response_generated"
        return state
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state

def translate_response(state: ChatState) -> ChatState:
    if state.get("error") or state.get("is_english"):
        state["translated_answer"] = state.get("answer_text", "")
        state["status"] = "completed"
        return state
    try:
        answer_text = state.get("answer_text", "")
        detected_language = state.get("detected_language", "en")
        target_language = get_language_name(detected_language)
        translated = call_gemini_translate_api(answer_text, target_language)
        state["translated_answer"] = translated
        state["status"] = "completed"
        return state
    except Exception as e:
        state["translated_answer"] = state.get("answer_text", "")
        state["status"] = "completed"
        return state

def store_query(state: ChatState) -> ChatState:
    session = state.get("db_session") or SessionLocal()
    close_session = not state.get("db_session")
    try:
        query = RAGQuery(
            chat_id=UUID(state["chat_id"]),
            source_type=SourceTypeEnum.CHAT,
            input_text=state["input_text"],
            has_answered=state.get("has_answered", False),
            answer_text=state.get("translated_answer", ""),
            answer_confidence=int(state.get("confidence", 0.0) * 100),
            language=state.get("detected_language"),
            response_time_ms=state.get("processing_time_ms", 0),
            metadata_={
                "similarity_score": state.get("similarity_score", 0.0),
                "retrieved_document_ids": state.get("retrieved_document_ids", []),
                "token_usage": state.get("token_usage", {}),
                "translated_text": state.get("translated_text"),
                "processing_status": state.get("status"),
                "error": state.get("error"),
                "client_metadata": state.get("input_metadata", {})
            }
        )
        session.add(query)
        session.commit()
        return state
    except Exception as e:
        logger.error(f"Error storing query: {e}")
        return state
    finally:
        if close_session: session.close()


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def build_chat_graph() -> StateGraph:
    graph = StateGraph(ChatState)
    graph.add_node("validate_and_detect_language", validate_and_detect_language)
    graph.add_node("translate_to_english", translate_to_english)
    graph.add_node("generate_query_embedding", generate_query_embedding_node)
    graph.add_node("search_knowledge_base", search_knowledge_base)
    graph.add_node("generate_response", generate_response)
    graph.add_node("translate_response", translate_response)
    graph.add_node("store_query", store_query)

    graph.set_entry_point("validate_and_detect_language")

    graph.add_conditional_edges(
        "validate_and_detect_language",
        lambda x: "translate_to_english" if not x.get("error") else "store_query",
        {"translate_to_english": "translate_to_english", "store_query": "store_query"}
    )

    graph.add_edge("translate_to_english", "generate_query_embedding")
    graph.add_edge("generate_query_embedding", "search_knowledge_base")
    graph.add_edge("search_knowledge_base", "generate_response")
    graph.add_edge("generate_response", "translate_response")
    graph.add_edge("translate_response", "store_query")
    graph.add_edge("store_query", END)

    return graph.compile()


class ChatPipeline:
    def __init__(self, db_session: Optional[Session] = None):
        self.db_session = db_session
        self.graph = build_chat_graph()

    async def process(self, input_text: str, chat_id: Optional[str] = None, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # If chat_id is missing, create a new chat session
        if not chat_id:
            chat_session = Chat(
                device_info=metadata.get("device_info", "unknown") if metadata else "unknown",
                language="en" # Default, will be updated
            )
            if self.db_session:
                self.db_session.add(chat_session)
                self.db_session.commit()
                self.db_session.refresh(chat_session)
                chat_id = str(chat_session.id)
            else:
                # Fallback if no session (shouldn't happen in API)
                chat_id = str(uuid4())

        initial_state = ChatState(
            chat_id=chat_id,
            input_text=input_text,
            user_id=user_id,
            db_session=self.db_session,
            input_metadata=metadata,
            status="pending"
        )
        final_state = await self.graph.ainvoke(initial_state)
        return {
            "chat_id": chat_id,
            "answer": final_state.get("translated_answer"),
            "confidence": final_state.get("confidence"),
            "language": final_state.get("detected_language"),
            "sources": final_state.get("relevant_chunks", []),
            "error": final_state.get("error")
        }
