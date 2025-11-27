from pydantic import BaseModel
from typing import List


# -------------------
# Message for Upload
# -------------------
class DoubtMessageCreate(BaseModel):
    author_role: str
    text: str


# -------------------
# Upload Request Schema
# -------------------
class DoubtUploadCreate(BaseModel):
    course_code: str
    source: str
    messages: List[DoubtMessageCreate]


# -------------------
# Topic Cluster Schema
# -------------------
class DoubtTopic(BaseModel):
    label: str
    example_questions: List[str]


# -------------------
# Summary Response Schema
# -------------------
class DoubtSummaryResponse(BaseModel):
    course_code: str
    overall_summary: str
    topics: List[DoubtTopic]


# -------------------
# Insights Response Schema
# -------------------
class DoubtInsightsResponse(BaseModel):
    course_code: str
    insights: List[str]
