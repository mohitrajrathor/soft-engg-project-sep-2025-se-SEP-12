from typing import List
from pydantic import BaseModel, Field

# ------------------------
# Request Schema (Upload)
# ------------------------

class DoubtMessageCreate(BaseModel):
    author_role: str = "student"
    text: str

class DoubtUploadCreate(BaseModel):
    course_code: str
    source: str
    messages: List[DoubtMessageCreate]


# ------------------------
# Response Schema (LLM Output)
# ------------------------

class TopicCluster(BaseModel):
    label: str = Field(description="Topic name")
    trend: str = Field(description="Trend direction")
    count: int = Field(description="How many times this topic appeared")
    sample_questions: List[str] = Field(description="Example questions")

class LearningGap(BaseModel):
    issue_title: str = Field(description="Misconception or gap title")
    category: str = Field(description="Type of gap")
    student_count: int = Field(description="Affected students")

class WeeklySummaryResponse(BaseModel):
    course_code: str
    overall_summary: str
    topics: List[TopicCluster]
    learning_gaps: List[LearningGap]
    insights: List[str]

    class Config:
        from_attributes = True   # replaces orm_mode=True
