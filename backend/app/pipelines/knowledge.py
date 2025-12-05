"""
Knowledge Processing Pipeline
LangGraph + LangChain + Gemini (gemini-embedding-004) embedding pipeline.

Steps:
1. Load KnowledgeSource from DB
2. Split into chunks with RecursiveCharacterTextSplitter
3. Generate embeddings with Gemini Embedding API (English only)
4. Persist KnowledgeChunks with embeddings to Postgres (pgvector)
5. Update task status and cleanup
"""

from typing import Dict, Any, List, Optional, TypedDict
from datetime import datetime
from uuid import UUID
import logging
import json
import os

from langgraph.graph import StateGraph, END
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
import requests

from app.core.db import SessionLocal
from app.models.knowledge import KnowledgeSource, KnowledgeChunk
from app.models.task import Task
from app.models.enums import TaskStatusEnum, TaskTypeEnum
from app.pipelines.search import call_gemini_embedding_api
from app.core.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE_CHARS", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP_CHARS", "200"))
GOOGLE_API_KEY = settings.GOOGLE_API_KEY
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 768
TOKEN_LIMIT = 2048


# ============================================================================
# STATE DEFINITION
# ============================================================================

class KnowledgeState(TypedDict, total=False):
    """
    Graph state for knowledge processing pipeline.
    """
    source_id: str
    task_id: Optional[str]
    source_data: Optional[Dict[str, Any]]
    chunks: Optional[List[str]]
    embeddings: Optional[List[List[float]]]
    metadata: Optional[Dict[str, Any]]
    error: Optional[str]
    status: Optional[str]


# ============================================================================
# PIPELINE NODES
# ============================================================================

def load_and_validate(state: KnowledgeState) -> KnowledgeState:
    """Node 1: Load KnowledgeSource from database and validate"""
    session: Session = SessionLocal()
    try:
        source_id = UUID(state["source_id"])
        source = session.query(KnowledgeSource).filter(KnowledgeSource.id == source_id).first()

        if not source:
            state["error"] = f"KnowledgeSource {source_id} not found"
            state["status"] = "failed"
            return state

        if not source.content or len(source.content.strip()) == 0:
            state["error"] = "Source content is empty"
            state["status"] = "failed"
            return state

        state["source_data"] = {
            "id": str(source.id),
            "title": source.title,
            "content": source.content,
            "category": source.category
        }
        state["status"] = "validated"
        state["metadata"] = {
            "source_id": str(source.id),
            "title": source.title,
            "category": source.category,
            "content_length": len(source.content)
        }

        if state.get("task_id"):
            task = session.query(Task).filter(Task.id == UUID(state["task_id"])).first()
            if task:
                task.status = TaskStatusEnum.IN_PROGRESS.value
                session.commit()

        return state

    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state
    finally:
        session.close()


def chunk_document(state: KnowledgeState) -> KnowledgeState:
    """Node 2: Split content into chunks using LangChain"""
    if state.get("error"): return state
    try:
        source_data = state["source_data"]
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""],
            length_function=len
        )
        docs = splitter.create_documents([source_data["content"]])
        state["chunks"] = [doc.page_content for doc in docs]
        state["status"] = "chunked"
        state["metadata"]["chunk_count"] = len(docs)
        return state
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state


def generate_embeddings(state: KnowledgeState) -> KnowledgeState:
    """Node 3: Generate embeddings using Gemini embedding model"""
    if state.get("error"): return state
    try:
        chunks = state["chunks"]
        if not chunks:
            state["error"] = "No chunks to embed"
            state["status"] = "failed"
            return state

        all_embeddings = []
        for chunk in chunks:
            emb = call_gemini_embedding_api(chunk)
            all_embeddings.append(emb)

        state["embeddings"] = all_embeddings
        state["status"] = "embedded"
        state["metadata"]["embeddings_generated"] = len(all_embeddings)
        return state
    except Exception as e:
        state["error"] = str(e)
        state["status"] = "failed"
        return state


def store_chunks(state: KnowledgeState) -> KnowledgeState:
    """Node 4: Store chunks and embeddings in PostgreSQL with pgvector"""
    if state.get("error"): return state
    session: Session = SessionLocal()
    try:
        source_data = state["source_data"]
        chunks = state["chunks"]
        embeddings = state["embeddings"]
        source_id = UUID(source_data["id"])

        source = session.query(KnowledgeSource).filter(KnowledgeSource.id == source_id).first()
        if not source:
            state["error"] = "Source not found"
            state["status"] = "failed"
            return state

        # Delete old chunks
        session.query(KnowledgeChunk).filter(KnowledgeChunk.source_id == source.id).delete()
        session.commit()

        # Store new chunks
        stored_chunks = []
        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            chunk = KnowledgeChunk(
                source_id=source.id,
                text=chunk_text,
                index=i,
                embedding=embedding,
                token_count=len(chunk_text.split()),
                word_count=len(chunk_text.split())
            )
            session.add(chunk)
            stored_chunks.append(chunk)

        source.chunk_count = len(stored_chunks)
        source.updated_at = datetime.utcnow()
        session.add(source)
        session.commit()

        state["status"] = "stored"
        state["metadata"]["chunks_stored"] = len(stored_chunks)
        return state
    except Exception as e:
        session.rollback()
        state["error"] = str(e)
        state["status"] = "failed"
        return state
    finally:
        session.close()


def finalize_task(state: KnowledgeState) -> KnowledgeState:
    """Node 5: Update task status and cleanup"""
    session: Session = SessionLocal()
    try:
        if not state.get("task_id"): return state
        task_id = UUID(state["task_id"])
        task = session.query(Task).filter(Task.id == task_id).first()

        if task:
            if state.get("error"):
                task.status = TaskStatusEnum.FAILED.value
                task.error_message = state["error"]
            else:
                task.status = TaskStatusEnum.COMPLETED.value
                task.completed_at = datetime.utcnow()
                
                if task.metadata_:
                    metadata = json.loads(task.metadata_)
                else:
                    metadata = {}
                metadata.update(state.get("metadata", {}))
                task.metadata_ = json.dumps(metadata)
            
            session.commit()

        state["status"] = "completed" if not state.get("error") else "failed"
        return state
    except Exception as e:
        return state
    finally:
        session.close()


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def build_knowledge_graph() -> StateGraph:
    graph = StateGraph(KnowledgeState)
    graph.add_node("load_and_validate", load_and_validate)
    graph.add_node("chunk_document", chunk_document)
    graph.add_node("generate_embeddings", generate_embeddings)
    graph.add_node("store_chunks", store_chunks)
    graph.add_node("finalize_task", finalize_task)

    graph.set_entry_point("load_and_validate")

    graph.add_conditional_edges(
        "load_and_validate",
        lambda x: "chunk_document" if not x.get("error") else "finalize_task",
        {"chunk_document": "chunk_document", "finalize_task": "finalize_task"}
    )

    graph.add_edge("chunk_document", "generate_embeddings")
    graph.add_edge("generate_embeddings", "store_chunks")
    graph.add_edge("store_chunks", "finalize_task")
    graph.add_edge("finalize_task", END)

    return graph.compile()


async def process_knowledge_source(source_id: str, task_id: Optional[str] = None) -> Dict[str, Any]:
    try:
        graph = build_knowledge_graph()
        initial_state = KnowledgeState(
            source_id=source_id,
            task_id=task_id,
            status="pending",
            metadata={}
        )
        final_state = await graph.ainvoke(initial_state)
        return {
            "success": not bool(final_state.get("error")),
            "status": final_state.get("status", "unknown"),
            "source_id": source_id,
            "chunks_created": final_state.get("metadata", {}).get("chunk_count", 0),
            "error": final_state.get("error")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
