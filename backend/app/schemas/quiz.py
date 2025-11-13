from typing import List, Literal
from pydantic import BaseModel


class Question(BaseModel):
    id: int
    type: Literal["mcq", "msq", "boolean"]
    question_text: str
    options: List[str]
    answers: List[str]


class QuizContent(BaseModel):
    topic: str
    difficulty: Literal["easy", "medium", "hard"]
    questions_count: int
    tags: List[str]
    questions: List[Question]


class QuizResponse(BaseModel):
    ai_response: str
    quiz: QuizContent
