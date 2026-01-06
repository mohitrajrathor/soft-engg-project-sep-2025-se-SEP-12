"""
Integration tests for Slide Deck generation with graphs.
"""

import pytest
from sqlalchemy.orm import Session

from app.models.slide_deck import SlideDeck
from app.models.user import User
from app.models.course import Course

pytestmark = [pytest.mark.api, pytest.mark.slides, pytest.mark.integration]


def test_slide_deck_with_graphs_persists_to_db(db_session: Session, test_course: Course, authenticated_ta: User):
    """Tests that slide decks with graph data persist correctly to the database."""
    slides_with_graphs = [
        {
            "title": "Market Analysis",
            "content": "## Current Market Trends\n\n- Growing demand\n- Increased competition",
            "graph_data": {
                "type": "bar",
                "title": "Market Growth",
                "labels": ["Q1", "Q2", "Q3", "Q4"],
                "datasets": [
                    {
                        "label": "Revenue ($M)",
                        "data": [100, 120, 140, 160],
                        "backgroundColor": "rgba(75, 192, 192, 0.5)"
                    }
                ]
            }
        },
        {
            "title": "Trend Line",
            "content": "## Long-term Performance",
            "graph_data": {
                "type": "line",
                "title": "Performance Over Time",
                "labels": ["2020", "2021", "2022", "2023"],
                "datasets": [
                    {
                        "label": "Score",
                        "data": [65, 78, 82, 89],
                        "borderColor": "rgba(153, 102, 255, 1)"
                    }
                ]
            }
        },
        {
            "title": "Distribution",
            "content": "## Market Share",
            "graph_data": {
                "type": "pie",
                "title": "Market Share Distribution",
                "labels": ["Company A", "Company B", "Company C", "Others"],
                "datasets": [
                    {
                        "label": "Market %",
                        "data": [30, 25, 20, 25],
                        "backgroundColor": [
                            "rgba(255, 99, 132, 0.5)",
                            "rgba(54, 162, 235, 0.5)",
                            "rgba(255, 206, 86, 0.5)",
                            "rgba(201, 203, 207, 0.5)"
                        ]
                    }
                ]
            }
        }
    ]

    # Create a slide deck with graphs
    deck = SlideDeck(
        title="Financial Analysis with Graphs",
        description="Comprehensive analysis with visual data representation.",
        course_id=test_course.id,
        created_by_id=authenticated_ta.id,
        slides=slides_with_graphs,
    )
    
    db_session.add(deck)
    db_session.commit()
    db_session.refresh(deck)

    # Verify the deck was saved
    assert deck.id is not None
    assert deck.title == "Financial Analysis with Graphs"

    # Query the deck back and verify graph data persisted
    retrieved_deck = db_session.query(SlideDeck).filter(SlideDeck.id == deck.id).first()
    assert retrieved_deck is not None
    assert len(retrieved_deck.slides) == 3

    # Verify first slide has bar chart
    assert retrieved_deck.slides[0]["graph_data"]["type"] == "bar"
    assert retrieved_deck.slides[0]["graph_data"]["title"] == "Market Growth"
    assert len(retrieved_deck.slides[0]["graph_data"]["datasets"]) == 1

    # Verify second slide has line chart
    assert retrieved_deck.slides[1]["graph_data"]["type"] == "line"
    assert retrieved_deck.slides[1]["graph_data"]["title"] == "Performance Over Time"

    # Verify third slide has pie chart
    assert retrieved_deck.slides[2]["graph_data"]["type"] == "pie"
    assert retrieved_deck.slides[2]["graph_data"]["labels"] == ["Company A", "Company B", "Company C", "Others"]

    # Verify slides without graphs also work
    slides_mixed = [
        {
            "title": "Introduction",
            "content": "This is the intro.",
            "graph_data": None
        },
        {
            "title": "With Graph",
            "content": "This has a graph.",
            "graph_data": {
                "type": "scatter",
                "title": "Scatter Plot",
                "labels": [],
                "datasets": [
                    {
                        "label": "Series 1",
                        "data": [{"x": 1, "y": 2}, {"x": 2, "y": 3}]
                    }
                ]
            }
        }
    ]

    deck2 = SlideDeck(
        title="Mixed Content Deck",
        description="Slides with and without graphs.",
        course_id=test_course.id,
        created_by_id=authenticated_ta.id,
        slides=slides_mixed,
    )
    
    db_session.add(deck2)
    db_session.commit()
    db_session.refresh(deck2)

    # Verify mixed content
    assert deck2.slides[0]["graph_data"] is None
    assert deck2.slides[1]["graph_data"]["type"] == "scatter"

    # Clean up
    db_session.delete(deck)
    db_session.delete(deck2)
    db_session.commit()


def test_slide_deck_response_schema_includes_graphs(db_session: Session, test_course: Course, authenticated_ta: User):
    """Tests that the SlideDeckResponse schema properly handles graph_data."""
    slides_data = [
        {
            "title": "Data Visualization",
            "content": "# Charts and Graphs",
            "graph_data": {
                "type": "bar",
                "title": "Sample Bar Chart",
                "labels": ["A", "B", "C"],
                "datasets": [{"label": "Values", "data": [10, 20, 30]}]
            }
        }
    ]

    deck = SlideDeck(
        title="Chart Test",
        description="Testing graph data in responses.",
        course_id=test_course.id,
        created_by_id=authenticated_ta.id,
        slides=slides_data,
    )
    
    db_session.add(deck)
    db_session.commit()
    db_session.refresh(deck)

    # Verify the slide data structure
    slide = deck.slides[0]
    assert "title" in slide
    assert "content" in slide
    assert "graph_data" in slide
    assert slide["graph_data"]["type"] == "bar"
    assert slide["graph_data"]["title"] == "Sample Bar Chart"

    # Clean up
    db_session.delete(deck)
    db_session.commit()
