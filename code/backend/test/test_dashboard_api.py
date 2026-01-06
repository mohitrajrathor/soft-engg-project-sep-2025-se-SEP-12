"""
Tests for Dashboard API endpoints.

This module tests:
- GET /api/dashboard/statistics - Get comprehensive dashboard stats
- GET /api/dashboard/activity-timeline - Get activity timeline
- GET /api/dashboard/top-sources - Get top knowledge sources
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.knowledge import KnowledgeSource
from app.models.query import Query
from app.models.user import User
from app.models.enums import CategoryEnum


@pytest.mark.api
@pytest.mark.dashboard
class TestDashboardStatistics:
    """Tests for dashboard statistics endpoint."""

    def test_get_statistics_empty(self, client: TestClient, auth_headers: dict):
        """Test getting statistics with minimal data."""
        response = client.get("/api/dashboard/statistics", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()

        # Check structure
        assert "users" in stats
        assert "knowledge" in stats
        assert "queries" in stats
        assert "system" in stats

        # Check user stats
        assert "total" in stats["users"]
        assert "active" in stats["users"]

        # Check knowledge stats
        assert "total_sources" in stats["knowledge"]
        assert "active_sources" in stats["knowledge"]
        assert "recent_sources_7d" in stats["knowledge"]

        # Check system stats
        assert stats["system"]["status"] == "healthy"
        assert "timestamp" in stats["system"]

    def test_get_statistics_with_data(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session,
        create_test_user
    ):
        """Test getting statistics with actual data."""
        # Create users
        create_test_user(email="user1@test.com", is_active=True)
        create_test_user(email="user2@test.com", is_active=True)
        create_test_user(email="user3@test.com", is_active=False)

        # Create knowledge sources
        for i in range(5):
            source = KnowledgeSource(
                title=f"Source {i}",
                content=f"Content {i}",
                category=CategoryEnum.COURSES,
                is_active=i < 3  # 3 active, 2 inactive
            )
            db_session.add(source)
        db_session.commit()

        response = client.get("/api/dashboard/statistics", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()

        # At least 3 users (the test users we created)
        assert stats["users"]["total"] >= 3
        assert stats["users"]["active"] >= 2

        # Knowledge stats
        assert stats["knowledge"]["total_sources"] == 5
        assert stats["knowledge"]["active_sources"] == 3

    def test_get_statistics_recent_activity(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test that recent activity counts are tracked."""
        # Create a recent source (within 7 days)
        recent_source = KnowledgeSource(
            title="Recent Source",
            content="Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(recent_source)
        db_session.commit()

        response = client.get("/api/dashboard/statistics", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()
        assert stats["knowledge"]["recent_sources_7d"] >= 1

    def test_get_statistics_unauthorized(self, client: TestClient):
        """Test getting statistics without authentication."""
        response = client.get("/api/dashboard/statistics")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.dashboard
class TestActivityTimeline:
    """Tests for activity timeline endpoint."""

    def test_get_timeline_default(self, client: TestClient, auth_headers: dict):
        """Test getting activity timeline with default parameters."""
        response = client.get("/api/dashboard/activity-timeline", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        assert "period" in result
        assert "timeline" in result
        assert result["period"] == "last_7_days"
        assert len(result["timeline"]) == 7

        # Check timeline structure
        for day_data in result["timeline"]:
            assert "date" in day_data
            assert "knowledge_sources" in day_data
            assert "queries" in day_data

    def test_get_timeline_custom_days(self, client: TestClient, auth_headers: dict):
        """Test getting timeline for custom number of days."""
        response = client.get("/api/dashboard/activity-timeline?days=14", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        assert result["period"] == "last_14_days"
        assert len(result["timeline"]) == 14

    def test_get_timeline_max_days(self, client: TestClient, auth_headers: dict):
        """Test getting timeline with maximum allowed days."""
        response = client.get("/api/dashboard/activity-timeline?days=30", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert len(result["timeline"]) == 30

    def test_get_timeline_invalid_days(self, client: TestClient, auth_headers: dict):
        """Test getting timeline with invalid days parameter."""
        # Too many days (max is 30)
        response = client.get("/api/dashboard/activity-timeline?days=100", headers=auth_headers)
        assert response.status_code == 422

        # Negative days
        response = client.get("/api/dashboard/activity-timeline?days=-5", headers=auth_headers)
        assert response.status_code == 422

        # Zero days
        response = client.get("/api/dashboard/activity-timeline?days=0", headers=auth_headers)
        assert response.status_code == 422

    def test_get_timeline_with_data(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test timeline with actual activity data."""
        # Create sources for today
        for i in range(3):
            source = KnowledgeSource(
                title=f"Today Source {i}",
                content="Content",
                category=CategoryEnum.COURSES
            )
            db_session.add(source)
        db_session.commit()

        response = client.get("/api/dashboard/activity-timeline?days=7", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        # The most recent day should have 3 sources
        today_data = result["timeline"][-1]  # Timeline is reversed (oldest to newest)
        assert today_data["knowledge_sources"] == 3

    def test_get_timeline_unauthorized(self, client: TestClient):
        """Test getting timeline without authentication."""
        response = client.get("/api/dashboard/activity-timeline")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.dashboard
class TestTopSources:
    """Tests for top knowledge sources endpoint."""

    def test_get_top_sources_empty(self, client: TestClient, auth_headers: dict):
        """Test getting top sources with no data."""
        response = client.get("/api/dashboard/top-sources", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        assert "total" in result
        assert "sources" in result
        assert result["total"] == 0
        assert result["sources"] == []

    def test_get_top_sources_default_limit(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test getting top sources with default limit."""
        # Create 15 sources
        for i in range(15):
            source = KnowledgeSource(
                title=f"Source {i}",
                content="Content",
                category=CategoryEnum.COURSES,
                is_active=True
            )
            db_session.add(source)
        db_session.commit()

        response = client.get("/api/dashboard/top-sources", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        assert result["total"] == 10  # Default limit
        assert len(result["sources"]) == 10

    def test_get_top_sources_custom_limit(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test getting top sources with custom limit."""
        # Create 20 sources
        for i in range(20):
            source = KnowledgeSource(
                title=f"Source {i}",
                content="Content",
                category=CategoryEnum.COURSES,
                is_active=True
            )
            db_session.add(source)
        db_session.commit()

        response = client.get("/api/dashboard/top-sources?limit=5", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        assert result["total"] == 5
        assert len(result["sources"]) == 5

    def test_get_top_sources_max_limit(self, client: TestClient, auth_headers: dict):
        """Test getting top sources with maximum limit."""
        response = client.get("/api/dashboard/top-sources?limit=50", headers=auth_headers)
        assert response.status_code == 200

    def test_get_top_sources_invalid_limit(self, client: TestClient, auth_headers: dict):
        """Test getting top sources with invalid limit."""
        # Exceeds maximum
        response = client.get("/api/dashboard/top-sources?limit=100", headers=auth_headers)
        assert response.status_code == 422

        # Negative limit
        response = client.get("/api/dashboard/top-sources?limit=-5", headers=auth_headers)
        assert response.status_code == 422

        # Zero limit
        response = client.get("/api/dashboard/top-sources?limit=0", headers=auth_headers)
        assert response.status_code == 422

    def test_get_top_sources_structure(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test the structure of top sources response."""
        source = KnowledgeSource(
            title="Test Source",
            content="Content",
            category=CategoryEnum.COURSES,
            is_active=True,
            chunk_count=5
        )
        db_session.add(source)
        db_session.commit()

        response = client.get("/api/dashboard/top-sources?limit=5", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        assert len(result["sources"]) == 1
        source_data = result["sources"][0]

        # Check structure
        assert "id" in source_data
        assert "title" in source_data
        assert "category" in source_data
        assert "chunk_count" in source_data
        assert "created_at" in source_data
        assert "usage_count" in source_data

        # Check values
        assert source_data["title"] == "Test Source"
        assert source_data["category"] == "Courses"
        assert source_data["chunk_count"] == 5

    def test_get_top_sources_only_active(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test that only active sources are returned."""
        # Create active and inactive sources
        active_source = KnowledgeSource(
            title="Active Source",
            content="Content",
            category=CategoryEnum.COURSES,
            is_active=True
        )
        inactive_source = KnowledgeSource(
            title="Inactive Source",
            content="Content",
            category=CategoryEnum.COURSES,
            is_active=False
        )
        db_session.add_all([active_source, inactive_source])
        db_session.commit()

        response = client.get("/api/dashboard/top-sources", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()

        # Should only return 1 (the active source)
        assert result["total"] == 1
        assert result["sources"][0]["title"] == "Active Source"

    def test_get_top_sources_unauthorized(self, client: TestClient):
        """Test getting top sources without authentication."""
        response = client.get("/api/dashboard/top-sources")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.dashboard
@pytest.mark.integration
class TestDashboardIntegration:
    """Integration tests for dashboard endpoints."""

    def test_dashboard_complete_workflow(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session,
        create_test_user
    ):
        """Test complete dashboard workflow with all endpoints."""
        # Setup: Create test data
        create_test_user(email="test1@test.com")
        create_test_user(email="test2@test.com")

        for i in range(5):
            source = KnowledgeSource(
                title=f"Source {i}",
                content=f"Content {i}",
                category=CategoryEnum.COURSES if i < 3 else CategoryEnum.ADMISSION,
                is_active=True
            )
            db_session.add(source)
        db_session.commit()

        # Test 1: Get overall statistics
        stats_response = client.get("/api/dashboard/statistics", headers=auth_headers)
        assert stats_response.status_code == 200
        stats = stats_response.json()
        assert stats["knowledge"]["total_sources"] == 5

        # Test 2: Get activity timeline
        timeline_response = client.get("/api/dashboard/activity-timeline", headers=auth_headers)
        assert timeline_response.status_code == 200
        timeline = timeline_response.json()
        assert len(timeline["timeline"]) == 7

        # Test 3: Get top sources
        top_response = client.get("/api/dashboard/top-sources", headers=auth_headers)
        assert top_response.status_code == 200
        top_sources = top_response.json()
        assert top_sources["total"] == 5
