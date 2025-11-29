from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import database session dependency
from app.core.db import get_db

# Import schemas
from app.schemas.doubts import DoubtUploadCreate, WeeklySummaryResponse

# Import the service
from app.services.doubt_summarizer_service import doubt_summarizer_service

# Create FastAPI router
router = APIRouter(
    prefix="/ta/doubts",
    tags=["Doubt Summarizer"]
)

# Upload Doubt Messages
@router.post("/upload", response_model=dict)
def upload_doubts(payload: DoubtUploadCreate, db: Session = Depends(get_db), user_id: int = 1):
    """
    Upload student doubts for a course with metadata.
    user_id can be replaced with authentication dependency.
    """
    try:
        return doubt_summarizer_service.create_doubt_upload(db, payload, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get Summary + Insights
@router.get("/summary/{course_code}", response_model=WeeklySummaryResponse)
async def get_doubt_summary(course_code: str, db: Session = Depends(get_db)):
    """
    Generate weekly summary + insights for a course.
    """
    try:
        messages = doubt_summarizer_service.get_recent_messages_for_course(db, course_code)
        return await doubt_summarizer_service.generate_summary_topics_insights(messages, course_code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get Topic Clusters + Confusion Counts
@router.get("/topics/{course_code}", response_model=List[dict])
async def get_topic_clusters(course_code: str, db: Session = Depends(get_db)):
    """
    Get topic clusters with confusion counts.
    """
    try:
        messages = doubt_summarizer_service.get_recent_messages_for_course(db, course_code)
        summary = await doubt_summarizer_service.generate_summary_topics_insights(messages, course_code)
        return summary.get("topics", [])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get Teacher Insights Only
@router.get("/insights/{course_code}", response_model=List[str])
async def get_teacher_insights(course_code: str, db: Session = Depends(get_db)):
    """
    Get only teacher insights for a course.
    """
    try:
        messages = doubt_summarizer_service.get_recent_messages_for_course(db, course_code)
        summary = await doubt_summarizer_service.generate_summary_topics_insights(messages, course_code)
        return summary.get("insights", [])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
