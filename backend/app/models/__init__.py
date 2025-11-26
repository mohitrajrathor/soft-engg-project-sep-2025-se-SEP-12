"""
Database models package.

This module exports all SQLAlchemy models for easy imports and
ensures they are registered with SQLAlchemy's Base registry.
"""

from app.models.user import User
from app.models.query import Query, QueryResponse
from app.models.resource import Resource
from app.models.announcement import Announcement
from app.models.profile import Profile
from app.models.course import Course
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.doubts import DoubtUpload, DoubtMessage
from app.models.slide_deck import SlideDeck
from app.models.tag import Tag
# (and any others that appear in relationship("...") strings)

__all__ = [
    "User",
    "Query",
    "QueryResponse",
    "Resource",
    "Announcement",
    "Profile",
    "Course",
    "Quiz",
    "QuizAttempt",
    "DoubtUpload",
    "DoubtMessage",
    "SlideDeck",
    "Tag",
    # add others here if needed
]
