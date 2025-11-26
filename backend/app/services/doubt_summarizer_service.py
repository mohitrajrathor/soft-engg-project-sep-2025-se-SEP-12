import logging
import json
from typing import List, Dict, Any, Optional
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

# Robust config import for local testing
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

# ============================================================================
# ⬇️ INTEGRATION POINT: PERSON 1 (MODELS) & PERSON 2 (SCHEMAS)
# ============================================================================
# When Aryan (Person 1) & Taniya (Person 2) are done:
# 1. DELETE the 'Placeholder Classes' block below.
# 2. UNCOMMENT the 'Real Imports' block.

# --- [START] Placeholder Classes (Delete later) ---
class DoubtUpload: pass  # Person 1 Model
class DoubtMessage: pass # Person 1 Model
class DoubtUploadCreate(BaseModel): # Person 2 Schema
    course_code: str
    source: str
    messages: List[Dict[str, str]]

# Person 2 Response Schemas (Internal use for LLM parsing)
class TopicCluster(BaseModel):
    label: str = Field(description="Topic name")
    trend: str = Field(description="Trend")
    count: int = Field(description="Count")
    sample_questions: List[str] = Field(description="Examples")

class LearningGap(BaseModel):
    issue_title: str = Field(description="Gap title")
    category: str = Field(description="Category")
    student_count: int = Field(description="Affected students")

class WeeklySummaryResponse(BaseModel):
    course_code: str = Field(description="Course code")
    overall_summary: str = Field(description="Summary")
    topics: List[TopicCluster] = Field(description="Topics")
    learning_gaps: List[LearningGap] = Field(description="Gaps")
    insights: List[str] = Field(description="Tips")
# --- [END] Placeholder Classes ---

# --- [START] Real Imports (Uncomment later) ---
# from app.models.doubts import DoubtUpload, DoubtMessage
# from app.schemas.doubts import DoubtUploadCreate, WeeklySummaryResponse
# ----------------------------------------------


# ============================================================================
# ✅ SERVICE LOGIC (Person 3)
# ============================================================================

class DoubtSummarizerService:
    def __init__(self):
        self.llm = None
        self.parser = JsonOutputParser(pydantic_object=WeeklySummaryResponse)

        if not settings.GOOGLE_API_KEY:
            logger.warning("Google API Key missing. LLM features disabled.")
            return

        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.2,
                convert_system_message_to_human=True
            )
            logger.info("DoubtSummarizerService initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")

    # ---------------------------------------------------------
    # Task 1: Save Upload & Messages (Database Logic)
    # ---------------------------------------------------------
    def create_doubt_upload(self, db: Session, upload_in: Any, user_id: int):
        """
        Saves the upload metadata and the individual messages to the database.
        """
        # 1. Create the Upload Record
        # (This matches the fields Person 1 was assigned to create)
        new_upload = DoubtUpload(
            course_code=upload_in.course_code,
            source=upload_in.source,
            created_by_id=user_id
        )
        
        # NOTE: If Person 1 hasn't pushed models yet, this 'db.add' will fail locally.
        # Keep it commented out until models exist if you are testing locally.
        # db.add(new_upload)
        # db.commit()
        # db.refresh(new_upload)

        logger.info(f"Created upload record for {upload_in.course_code}")

        # 2. Save individual messages
        # for msg in upload_in.messages:
        #     new_message = DoubtMessage(
        #         upload_id=new_upload.id,
        #         author_role=msg.get("author_role", "student"),
        #         text=msg.get("text")
        #     )
        #     db.add(new_message)
        
        # db.commit()
        
        return {"status": "success", "message": "Upload saved (Mock)"} # Return actual obj later

    # ---------------------------------------------------------
    # Task 2: Fetch Recent Messages
    # ---------------------------------------------------------
    def get_recent_messages_for_course(self, db: Session, course_code: str, limit: int = 100) -> List[str]:
        """
        Queries the database for the most recent doubt messages for a specific course.
        """
        # Logic for Person 1 Integration:
        # return db.query(DoubtMessage.text)\
        #    .join(DoubtUpload)\
        #    .filter(DoubtUpload.course_code == course_code)\
        #    .order_by(DoubtUpload.created_at.desc())\
        #    .limit(limit)\
        #    .all()
        
        # Return mock data until DB is ready
        return [
            "How do I use a for loop?",
            "What is a primary key in SQL?",
            "Recursion is confusing me.",
            "Difference between list and tuple?"
        ]

    # ---------------------------------------------------------
    # Task 3: LLM Generation (The Logic we built earlier)
    # ---------------------------------------------------------
    async def generate_summary_topics_insights(self, messages: List[str], course_code: str) -> Dict[str, Any]:
        """
        Sends raw messages to Gemini and returns structured analysis.
        """
        if not self.llm:
            return {"error": "LLM not configured"}
        
        if not messages:
            return self._empty_state(course_code)

        prompt = PromptTemplate(
            template="""
            You are an expert academic analyst for "{course_code}".
            Analyze these student doubts:
            {doubts_text}

            Output strictly valid JSON (no markdown) with:
            - overall_summary (3 sentences)
            - topics (clusters with counts)
            - learning_gaps (misconceptions)
            - insights (teaching tips)

            {format_instructions}
            """,
            input_variables=["course_code", "doubts_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser

        try:
            doubts_text = "\n".join([f"- {msg}" for msg in messages])
            return await chain.ainvoke({
                "course_code": course_code,
                "doubts_text": doubts_text
            })
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return {"error": str(e)}

    def _empty_state(self, course_code):
        return {
            "course_code": course_code,
            "overall_summary": "No data.",
            "topics": [], "learning_gaps": [], "insights": []
        }

# Global Instance
doubt_summarizer_service = DoubtSummarizerService()