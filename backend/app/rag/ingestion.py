import logging
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
from app.core.db import SessionLocal
from app.models.document_chunk import DocumentChunk
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=settings.GOOGLE_API_KEY
        )

    def ingest_documents(self, chunks: List[str], source: str):
        """
        Generate embeddings for chunks and store them in the database.
        """
        if not chunks:
            return

        logger.info(f"Ingesting {len(chunks)} chunks from {source}")
        
        db: Session = SessionLocal()
        try:
            # Generate embeddings
            # Google's embedding model supports batching, but let's be safe with batch size
            batch_size = 10
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]
                try:
                    embeddings = self.embeddings.embed_documents(batch_chunks)
                    
                    for j, (chunk_text, embedding) in enumerate(zip(batch_chunks, embeddings)):
                        doc_chunk = DocumentChunk(
                            content=chunk_text,
                            source=source,
                            chunk_index=i + j,
                            embedding=embedding
                        )
                        db.add(doc_chunk)
                    
                    db.commit()
                    logger.info(f"Stored chunks {i} to {i + len(batch_chunks)}")
                    
                except Exception as e:
                    logger.error(f"Error generating embeddings for batch {i}: {e}")
                    db.rollback()
                    
        except Exception as e:
            logger.error(f"Error during ingestion: {e}")
        finally:
            db.close()

    def ingest_text(self, text: str, source: str):
        """
        Ingest a single text string (e.g., a resolved query).
        """
        self.ingest_documents([text], source)

    def search_similar(self, query: str, limit: int = 5) -> List[DocumentChunk]:
        """
        Search for similar documents using cosine similarity.
        """
        db: Session = SessionLocal()
        try:
            query_embedding = self.embeddings.embed_query(query)
            
            # Use pgvector's cosine distance operator (<=>)
            # We want the closest distance, so order by distance ASC
            results = db.query(DocumentChunk).order_by(
                DocumentChunk.embedding.cosine_distance(query_embedding)
            ).limit(limit).all()
            
            return results
        finally:
            db.close()
