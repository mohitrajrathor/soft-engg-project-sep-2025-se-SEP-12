"""
Tests for Seed API endpoints.

This module tests:
- POST /api/seed/populate - Populate database with mock data
- DELETE /api/seed/clear - Clear seed data from database
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.knowledge import KnowledgeSource, KnowledgeChunk
from app.models.task import Task
from app.models.query import Query, QueryResponse


@pytest.mark.api
@pytest.mark.seed
class TestPopulateDatabase:
    """Tests for database population endpoint."""

    def test_populate_database_success(self, client: TestClient, db_session: Session):
        """Test populating database with seed data."""
        response = client.post("/api/seed/populate")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "users_created" in data
        assert "knowledge_sources_created" in data
        assert "tasks_created" in data
        assert "queries_created" in data
        assert "message" in data
        assert "test_credentials" in data

        # Verify data was created
        assert data["users_created"] == 4  # student, ta, instructor, admin
        assert data["knowledge_sources_created"] == 10
        assert data["tasks_created"] == 5
        assert data["queries_created"] == 8

        # Verify test credentials provided
        assert "student" in data["test_credentials"]
        assert "ta" in data["test_credentials"]
        assert "instructor" in data["test_credentials"]
        assert "admin" in data["test_credentials"]

        # Verify users exist in database
        student = db_session.query(User).filter(User.email == "student@test.com").first()
        ta = db_session.query(User).filter(User.email == "ta@test.com").first()
        instructor = db_session.query(User).filter(User.email == "instructor@test.com").first()
        admin = db_session.query(User).filter(User.email == "admin@test.com").first()

        assert student is not None
        assert ta is not None
        assert instructor is not None
        assert admin is not None

        # Verify knowledge sources created
        sources = db_session.query(KnowledgeSource).all()
        assert len(sources) == 10

        # Verify tasks created
        tasks = db_session.query(Task).all()
        assert len(tasks) == 5

        # Verify queries created
        queries = db_session.query(Query).all()
        assert len(queries) == 8

    def test_populate_database_idempotent(self, client: TestClient, db_session: Session):
        """Test that populating database multiple times doesn't duplicate data."""
        # First population
        response1 = client.post("/api/seed/populate")
        assert response1.status_code == 200
        data1 = response1.json()

        # Second population (should skip existing data)
        response2 = client.post("/api/seed/populate")
        assert response2.status_code == 200
        data2 = response2.json()

        # No new users should be created
        assert data2["users_created"] == 0

        # Verify total count hasn't changed
        total_users = db_session.query(User).count()
        assert total_users == 4

    def test_populate_creates_knowledge_chunks(self, client: TestClient, db_session: Session):
        """Test that knowledge sources have associated chunks."""
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        # Get first knowledge source
        source = db_session.query(KnowledgeSource).first()
        assert source is not None

        # Verify it has chunks
        chunks = db_session.query(KnowledgeChunk).filter(
            KnowledgeChunk.source_id == source.id
        ).all()
        assert len(chunks) > 0

    def test_populate_creates_queries_with_responses(self, client: TestClient, db_session: Session):
        """Test that some queries have responses."""
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        # Find a resolved query (should have solution response)
        from app.schemas.query_schema import QueryStatus
        resolved_query = db_session.query(Query).filter(
            Query.status == QueryStatus.RESOLVED
        ).first()

        assert resolved_query is not None

        # Verify it has responses
        responses = db_session.query(QueryResponse).filter(
            QueryResponse.query_id == resolved_query.id
        ).all()

        assert len(responses) > 0

        # Check if any response is marked as solution
        has_solution = any(r.is_solution for r in responses)
        assert has_solution

    def test_populate_creates_diverse_categories(self, client: TestClient, db_session: Session):
        """Test that knowledge sources span multiple categories."""
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        # Get all knowledge sources
        sources = db_session.query(KnowledgeSource).all()

        # Extract unique categories
        categories = set(source.category for source in sources)

        # Should have multiple categories
        assert len(categories) >= 4  # COURSES, ASSIGNMENTS, QUIZZES, etc.

    def test_populate_creates_tasks_with_different_statuses(self, client: TestClient, db_session: Session):
        """Test that tasks have different statuses."""
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        # Get all tasks
        tasks = db_session.query(Task).all()

        # Extract unique statuses
        statuses = set(task.status for task in tasks)

        # Should have multiple statuses
        assert len(statuses) >= 3  # PENDING, IN_PROGRESS, COMPLETED, FAILED

    def test_populate_user_passwords_hashed(self, client: TestClient, db_session: Session):
        """Test that user passwords are properly hashed."""
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        student = db_session.query(User).filter(User.email == "student@test.com").first()

        # Password should not be plain text
        assert student.password != "student123"
        # Password should be a hash (bcrypt/argon2 hashes are long)
        assert len(student.password) > 50

    def test_populate_users_are_active(self, client: TestClient, db_session: Session):
        """Test that all seeded users are active."""
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        users = db_session.query(User).filter(
            User.email.in_([
                "student@test.com",
                "ta@test.com",
                "instructor@test.com",
                "admin@test.com"
            ])
        ).all()

        for user in users:
            assert user.is_active == True

    def test_populate_queries_have_tags(self, client: TestClient, db_session: Session):
        """Test that queries have tags."""
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        # Get all queries
        queries = db_session.query(Query).all()

        # At least some queries should have tags
        queries_with_tags = [q for q in queries if q.tags]
        assert len(queries_with_tags) > 0


@pytest.mark.api
@pytest.mark.seed
class TestClearSeedData:
    """Tests for clearing seed data endpoint."""

    def test_clear_seed_data_success(self, client: TestClient, db_session: Session):
        """Test clearing seed data."""
        # First populate
        populate_response = client.post("/api/seed/populate")
        assert populate_response.status_code == 200

        # Verify data exists
        assert db_session.query(KnowledgeSource).count() > 0
        assert db_session.query(Task).count() > 0
        assert db_session.query(Query).count() > 0

        # Clear data
        clear_response = client.delete("/api/seed/clear")

        assert clear_response.status_code == 200
        data = clear_response.json()
        assert data["message"] == "Seed data cleared successfully"

        # Verify data was cleared
        assert db_session.query(KnowledgeSource).count() == 0
        assert db_session.query(KnowledgeChunk).count() == 0
        assert db_session.query(Task).count() == 0

        # Test queries should be cleared
        test_user = db_session.query(User).filter(
            User.email == "student@test.com"
        ).first()

        if test_user:
            test_queries = db_session.query(Query).filter(
                Query.student_id == test_user.id
            ).count()
            assert test_queries == 0

    def test_clear_data_keeps_test_users(self, client: TestClient, db_session: Session):
        """Test that clearing data keeps test users."""
        # Populate
        client.post("/api/seed/populate")

        # Verify users exist
        initial_user_count = db_session.query(User).filter(
            User.email.in_([
                "student@test.com",
                "ta@test.com",
                "instructor@test.com",
                "admin@test.com"
            ])
        ).count()
        assert initial_user_count == 4

        # Clear data
        client.delete("/api/seed/clear")

        # Verify users still exist (as per documentation)
        final_user_count = db_session.query(User).filter(
            User.email.in_([
                "student@test.com",
                "ta@test.com",
                "instructor@test.com",
                "admin@test.com"
            ])
        ).count()
        assert final_user_count == 4

    def test_clear_data_on_empty_database(self, client: TestClient, db_session: Session):
        """Test clearing data when database is already empty."""
        response = client.delete("/api/seed/clear")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Seed data cleared successfully"

    def test_clear_data_removes_query_responses(self, client: TestClient, db_session: Session):
        """Test that query responses are also deleted."""
        # Populate (creates queries with responses)
        client.post("/api/seed/populate")

        # Verify responses exist
        initial_response_count = db_session.query(QueryResponse).count()
        assert initial_response_count > 0

        # Clear data
        client.delete("/api/seed/clear")

        # Verify responses were deleted
        final_response_count = db_session.query(QueryResponse).count()
        assert final_response_count == 0

    def test_clear_and_repopulate(self, client: TestClient, db_session: Session):
        """Test clearing and repopulating database."""
        # First population
        response1 = client.post("/api/seed/populate")
        assert response1.status_code == 200

        # Clear
        clear_response = client.delete("/api/seed/clear")
        assert clear_response.status_code == 200

        # Re-populate
        response2 = client.post("/api/seed/populate")
        assert response2.status_code == 200
        data2 = response2.json()

        # Should create new knowledge sources and tasks
        assert data2["knowledge_sources_created"] == 10
        assert data2["tasks_created"] == 5
        assert data2["queries_created"] == 8

        # Users already exist, so 0 new users
        assert data2["users_created"] == 0


@pytest.mark.api
@pytest.mark.seed
@pytest.mark.integration
class TestSeedDataIntegration:
    """Integration tests for seed data."""

    def test_can_login_with_seeded_users(self, client: TestClient, db_session: Session):
        """Test that seeded users can login."""
        # Populate
        client.post("/api/seed/populate")

        # Try to login as each role
        roles = {
            "student": {"email": "student@test.com", "password": "student123"},
            "ta": {"email": "ta@test.com", "password": "ta123"},
            "instructor": {"email": "instructor@test.com", "password": "instructor123"},
            "admin": {"email": "admin@test.com", "password": "admin123"}
        }

        for role_name, credentials in roles.items():
            response = client.post("/api/auth/login", json=credentials)
            assert response.status_code == 200, f"Failed to login as {role_name}"
            data = response.json()
            assert "access_token" in data
            assert "refresh_token" in data

    def test_seeded_queries_accessible_via_api(self, client: TestClient, db_session: Session):
        """Test that seeded queries are accessible via queries API."""
        # Populate
        client.post("/api/seed/populate")

        # Login as student
        login_response = client.post("/api/auth/login", json={
            "email": "student@test.com",
            "password": "student123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get queries
        response = client.get("/api/queries/", headers=headers)

        assert response.status_code == 200
        data = response.json()

        # Student should see their queries
        assert data["total"] > 0
        assert len(data["queries"]) > 0

    def test_seeded_knowledge_sources_valid(self, client: TestClient, db_session: Session):
        """Test that seeded knowledge sources have valid structure."""
        # Populate
        client.post("/api/seed/populate")

        # Get all knowledge sources
        sources = db_session.query(KnowledgeSource).all()

        for source in sources:
            # Verify required fields
            assert source.title is not None and len(source.title) > 0
            assert source.description is not None
            assert source.content is not None and len(source.content) > 0
            assert source.category is not None
            assert source.is_active == True
            assert source.created_at is not None

            # Verify chunk relationship
            assert source.chunk_count > 0

    def test_seeded_data_creates_realistic_scenario(self, client: TestClient, db_session: Session):
        """Test that seeded data creates a realistic usage scenario."""
        # Populate
        response = client.post("/api/seed/populate")
        assert response.status_code == 200

        # Verify we have:
        # 1. Multiple user roles
        users_by_role = {}
        for email, role in [
            ("student@test.com", "student"),
            ("ta@test.com", "ta"),
            ("instructor@test.com", "instructor"),
            ("admin@test.com", "admin")
        ]:
            user = db_session.query(User).filter(User.email == email).first()
            assert user is not None
            users_by_role[role] = user

        # 2. Queries in different states
        from app.schemas.query_schema import QueryStatus
        open_queries = db_session.query(Query).filter(Query.status == QueryStatus.OPEN).count()
        in_progress_queries = db_session.query(Query).filter(Query.status == QueryStatus.IN_PROGRESS).count()
        resolved_queries = db_session.query(Query).filter(Query.status == QueryStatus.RESOLVED).count()

        assert open_queries > 0
        assert resolved_queries > 0  # At least some resolved

        # 3. Query responses from TAs/instructors
        responses = db_session.query(QueryResponse).all()
        assert len(responses) > 0

        # Some responses should be from TAs/instructors
        ta_responses = [r for r in responses if r.user.role.value in ["ta", "instructor"]]
        assert len(ta_responses) > 0

        # 4. Knowledge sources across categories
        sources = db_session.query(KnowledgeSource).all()
        categories = set(s.category for s in sources)
        assert len(categories) >= 4

        # 5. Tasks with different statuses
        tasks = db_session.query(Task).all()
        task_statuses = set(t.status for t in tasks)
        assert len(task_statuses) >= 3
