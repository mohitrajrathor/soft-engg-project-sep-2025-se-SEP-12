import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# --- 1. SETUP & IMPORTS ---
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.prompts import PromptTemplate
    from pydantic import BaseModel, Field
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseModel = object
    Field = lambda **kwargs: None
    ChatGoogleGenerativeAI = None
    JsonOutputParser = None
    PromptTemplate = None

# Config import
try:
    from app.core.config import settings
except ImportError:
    import os
    class MockSettings:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        GEMINI_MODEL = "gemini-2.5-flash"
    settings = MockSettings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# REAL IMPORTS (Person 1 + Person 2)
# -----------------------------------------------------------------------------
from app.models.doubts import DoubtUpload, DoubtMessage
from app.schemas.doubts import DoubtUploadCreate, WeeklySummaryResponse

# -----------------------------------------------------------------------------
# SERVICE
# -----------------------------------------------------------------------------

class DoubtSummarizerService:
    def __init__(self):
        """Initialize LLM + JSON parser"""
        self.llm = None
        self.parser = JsonOutputParser(pydantic_object=WeeklySummaryResponse)

        if not settings.GOOGLE_API_KEY:
            logger.warning("⚠️ Google API Key missing — LLM disabled.")
            return

        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2,
                convert_system_message_to_human=True
            )
            logger.info("DoubtSummarizerService initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")

    # -------------------------------------------------------------------------
    # Task 1 — Save Upload + Messages
    # -------------------------------------------------------------------------
    def create_doubt_upload(self, db: Session, upload_in: DoubtUploadCreate, user_id: int):
        """
        Saves the upload metadata and related messages into the database.
        """

        # Create upload
        new_upload = DoubtUpload(
            course_code=upload_in.course_code,
            source=upload_in.source,
            created_by_id=user_id
        )
        db.add(new_upload)
        db.commit()
        db.refresh(new_upload)

        # Create messages
        for msg in upload_in.messages:
            new_message = DoubtMessage(
                upload_id=new_upload.id,
                author_role=msg.get("author_role", "student"),
                text=msg.get("text")
            )
            db.add(new_message)

        db.commit()
        return new_upload

    # -------------------------------------------------------------------------
    # Task 2 — Fetch Recent Messages
    # -------------------------------------------------------------------------
    def get_recent_messages_for_course(self, db: Session, course_code: str, limit: int = 100) -> List[str]:
        """
        Fetch the most recent messages for a course.
        """

        rows = (
            db.query(DoubtMessage.text)
            .join(DoubtUpload, DoubtMessage.upload_id == DoubtUpload.id)
            .filter(DoubtUpload.course_code == course_code)
            .order_by(DoubtUpload.created_at.desc())
            .limit(limit)
            .all()
        )

        return [r[0] for r in rows]

    # -------------------------------------------------------------------------
    # Task 3 — LLM Analysis (Summary + Topics + Insights)
    # -------------------------------------------------------------------------
    async def generate_summary_topics_insights(self, messages: List[str], course_code: str) -> Dict[str, Any]:
        """
        Sends messages to Gemini to generate structured summaries.
        """

        if not self.llm:
            return {"error": "LLM not configured"}

        if not messages:
            return self._empty_state(course_code)

        prompt = PromptTemplate(
            template="""
You are an expert academic assistant analyzing doubts for "{course_code}".

Analyze the following student queries:
{doubts_text}

Return ONLY valid JSON with:
- overall_summary
- topics (clusters)
- learning_gaps
- insights

{format_instructions}
            """,
            input_variables=["course_code", "doubts_text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            }
        )

        chain = prompt | self.llm | self.parser

        try:
            formatted = "\n".join([f"- {m}" for m in messages])
            return await chain.ainvoke({
                "course_code": course_code,
                "doubts_text": formatted
            })
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return {"error": str(e)}

    # -------------------------------------------------------------------------
    # Empty State
    # -------------------------------------------------------------------------
    def _empty_state(self, course_code: str):
        return {
            "course_code": course_code,
            "overall_summary": "No data.",
            "topics": [],
            "learning_gaps": [],
            "insights": []
        }


# GLOBAL INSTANCE
doubt_summarizer_service = DoubtSummarizerService()
