"""
API tests for the Slide Deck endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import AsyncMock

from app.models.user import User
from app.models.course import Course
from app.models.slide_deck import SlideDeck

# Mark all tests in this file
pytestmark = [pytest.mark.api, pytest.mark.slides]

# Sample AI-generated slide data for mocking
MOCK_SLIDE_CONTENT = {
    "slides": [
        {
            "title": "Introduction to Python",
            "content": "# Welcome to Python\n\n- Python is a versatile language.\n- You can use it for everything from web development to data science.",
            "graph_data": {
                "type": "bar",
                "title": "Language Popularity",
                "labels": ["Python", "JavaScript", "Java"],
                "datasets": [{"label": "Usage %", "data": [45, 30, 25]}]
            }
        },
        {
            "title": "Basic Data Types",
            "content": "## Common Data Types\n\n- **Integers**: `x = 10`\n- **Floats**: `y = 3.14`\n- **Strings**: `name = \"AURA\"`",
            "graph_data": None
        }
    ]
}

MOCK_PREVIEW_OUTLINE = {
    "outline": [
        "Slide 1: Introduction to Python - overview of language features",
        "Slide 2: Basic Data Types - integers, floats, strings",
    ]
}


@pytest.fixture
def test_slide_deck(db_session: Session, test_course: Course, authenticated_ta: User) -> SlideDeck:
    """Creates a sample slide deck in the database for testing."""
    deck = SlideDeck(
        title="Sample Slide Deck",
        description="A deck created for testing.",
        course_id=test_course.id,
        created_by_id=authenticated_ta.id,
        slides=MOCK_SLIDE_CONTENT["slides"],
    )
    db_session.add(deck)
    db_session.commit()
    db_session.refresh(deck)
    return deck


@pytest.mark.asyncio
async def test_generate_slide_deck_preview_as_ta(
    client: TestClient, ta_auth_headers: dict, test_course: Course, monkeypatch
):
    """Tests that a TA can generate a preview of a slide deck."""
    mock_preview = AsyncMock(return_value=MOCK_PREVIEW_OUTLINE)
    monkeypatch.setattr("app.api.slide_deck_router.slide_deck_service.generate_preview", mock_preview)

    request_data = {
        "course_id": test_course.id,
        "title": "Preview Test",
        "description": "Testing preview generation.",
        "topics": ["Python syntax", "Data types"],
        "num_slides": 2,
        "format": "presentation",
    }

    response = client.post("/api/slide-decks/preview", headers=ta_auth_headers, json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "outline" in data
    assert isinstance(data["outline"], list)
    assert len(data["outline"]) > 0
    mock_preview.assert_called_once()


@pytest.mark.asyncio
async def test_generate_slide_deck_as_ta(
    client: TestClient, ta_auth_headers: dict, test_course: Course, monkeypatch
):
    """Tests that a TA can successfully generate and save a slide deck."""
    mock_generate = AsyncMock(return_value=MOCK_SLIDE_CONTENT)
    monkeypatch.setattr("app.api.slide_deck_router.slide_deck_service.generate_slides", mock_generate)

    request_data = {
        "course_id": test_course.id,
        "title": "New AI-Generated Slides",
        "description": "Slides about Python basics.",
        "topics": ["Python syntax", "Data types"],
        "num_slides": 2,
        "format": "presentation",
        "include_graphs": True,
        "graph_types": ["bar", "line"],
    }

    response = client.post("/api/slide-decks/", headers=ta_auth_headers, json=request_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New AI-Generated Slides"
    assert data["course_id"] == test_course.id
    assert data["slides"] == MOCK_SLIDE_CONTENT["slides"]
    assert data["creator"]["id"] is not None
    # Verify graph_data is present in the first slide
    assert data["slides"][0].get("graph_data") is not None
    mock_generate.assert_called_once()


@pytest.mark.asyncio
async def test_generate_slide_deck_as_student(client: TestClient, auth_headers: dict, test_course: Course):
    """Tests that a student cannot generate a slide deck."""
    request_data = {
        "course_id": test_course.id,
        "title": "Student Slide Attempt",
        "topics": ["Python basics"],
        "num_slides": 2,
        "format": "presentation",
    }
    response = client.post("/api/slide-decks/", headers=auth_headers, json=request_data)
    assert response.status_code == 403


def test_get_all_slide_decks(client: TestClient, auth_headers: dict, test_slide_deck: SlideDeck):
    """Tests that an authenticated user can list slide decks."""
    response = client.get("/api/slide-decks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(d["id"] == test_slide_deck.id for d in data)


def test_get_slide_deck_by_id(client: TestClient, auth_headers: dict, test_slide_deck: SlideDeck):
    """Tests retrieving a single slide deck by its ID."""
    response = client.get(f"/api/slide-decks/{test_slide_deck.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_slide_deck.id
    assert data["title"] == test_slide_deck.title


def test_get_non_existent_slide_deck(client: TestClient, auth_headers: dict):
    """Tests retrieving a non-existent slide deck."""
    response = client.get("/api/slide-decks/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_slide_deck_as_creator(
    client: TestClient, ta_auth_headers: dict, test_slide_deck: SlideDeck
):
    """Tests that the creator of a slide deck can update it."""
    update_data = {
        "title": "Updated Deck Title",
        "slides": [
            {
                "title": "Updated Slide 1",
                "content": "This content has been updated."
            }
        ]
    }
    response = client.put(
        f"/api/slide-decks/{test_slide_deck.id}",
        headers=ta_auth_headers,
        json=update_data,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Deck Title"
    assert len(data["slides"]) == 1
    assert data["slides"][0]["title"] == "Updated Slide 1"


def test_update_slide_deck_as_other_user(
    client: TestClient, admin_auth_headers: dict, test_slide_deck: SlideDeck
):
    """Tests that another user (even an admin) cannot update a deck they did not create."""
    update_data = {"title": "Unauthorized Update Attempt"}
    response = client.put(
        f"/api/slide-decks/{test_slide_deck.id}",
        headers=admin_auth_headers,
        json=update_data,
    )
    assert response.status_code == 403
    assert "You can only update slide decks you have created" in response.json()["detail"]


def test_delete_slide_deck_as_creator(
    client: TestClient, ta_auth_headers: dict, test_slide_deck: SlideDeck
):
    """Tests that the creator can delete their own slide deck."""
    response = client.delete(f"/api/slide-decks/{test_slide_deck.id}", headers=ta_auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/api/slide-decks/{test_slide_deck.id}", headers=ta_auth_headers)
    assert get_response.status_code == 404


def test_delete_slide_deck_as_other_user(
    client: TestClient, admin_auth_headers: dict, test_slide_deck: SlideDeck
):
    """Tests that a user who is not the creator cannot delete the slide deck."""
    response = client.delete(f"/api/slide-decks/{test_slide_deck.id}", headers=admin_auth_headers)
    assert response.status_code == 403
    assert "You can only delete slide decks you have created" in response.json()["detail"]


@pytest.mark.asyncio
async def test_generate_slides_ai_service_error(
    client: TestClient, ta_auth_headers: dict, test_course: Course, monkeypatch
):
    """Tests the API's response when the AI service returns an error."""
    mock_generate = AsyncMock(return_value={"error": "AI model is offline"})
    monkeypatch.setattr("app.api.slide_deck_router.slide_deck_service.generate_slides", mock_generate)

    request_data = {
        "course_id": test_course.id,
        "title": "Test AI Error",
        "topics": ["Error handling"],
        "num_slides": 1,
        "format": "presentation",
    }

    response = client.post("/api/slide-decks/", headers=ta_auth_headers, json=request_data)

    assert response.status_code == 500
    assert "AI service error: AI model is offline" in response.json()["detail"]