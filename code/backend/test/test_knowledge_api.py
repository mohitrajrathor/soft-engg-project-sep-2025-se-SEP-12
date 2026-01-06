"""
Tests for Knowledge Base API endpoints.

This module tests:
- POST /api/knowledge/sources - Create knowledge source
- GET /api/knowledge/categories - Get categories
- GET /api/knowledge/sources - List knowledge sources
- GET /api/knowledge/sources/{id} - Get specific source
- PUT /api/knowledge/sources/{id} - Update source
- DELETE /api/knowledge/sources/{id} - Delete source
- GET /api/knowledge/sources/{id}/chunks - Get chunks
- POST /api/knowledge/search - Semantic search
- GET /api/knowledge/stats - Get statistics
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.knowledge import KnowledgeSource, KnowledgeChunk
from app.models.enums import CategoryEnum


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeSourceCreate:
    """Tests for creating knowledge sources."""

    def test_create_knowledge_source_success(self, client: TestClient, auth_headers: dict):
        """Test successful creation of a knowledge source."""
        data = {
            "title": "Introduction to Python",
            "description": "Python programming basics",
            "content": "Python is a high-level programming language known for its simplicity...",
            "category": "Courses",
            "is_active": True
        }

        response = client.post(
            "/api/knowledge/sources",
            json=data,
            headers=auth_headers
        )

        assert response.status_code == 201
        result = response.json()
        assert result["title"] == data["title"]
        assert result["description"] == data["description"]
        assert result["category"] == data["category"]
        assert result["is_active"] == data["is_active"]
        assert "id" in result
        assert "created_at" in result

    def test_create_knowledge_source_minimal(self, client: TestClient, auth_headers: dict):
        """Test creating knowledge source with minimal required fields."""
        data = {
            "title": "Quick Guide",
            "content": "Some content here",
            "category": "Courses"
        }

        response = client.post(
            "/api/knowledge/sources",
            json=data,
            headers=auth_headers
        )

        assert response.status_code == 201
        result = response.json()
        assert result["title"] == data["title"]
        assert result["description"] is None
        assert result["is_active"] is True  # Default value

    def test_create_knowledge_source_unauthorized(self, client: TestClient):
        """Test creating knowledge source without authentication."""
        data = {
            "title": "Test Source",
            "content": "Content",
            "category": "Courses"
        }

        response = client.post("/api/knowledge/sources", json=data)
        assert response.status_code in [401, 403]

    def test_create_knowledge_source_invalid_category(self, client: TestClient, auth_headers: dict):
        """Test creating knowledge source with invalid category."""
        data = {
            "title": "Test Source",
            "content": "Content",
            "category": "InvalidCategory"
        }

        response = client.post(
            "/api/knowledge/sources",
            json=data,
            headers=auth_headers
        )

        assert response.status_code == 422  # Validation error

    def test_create_knowledge_source_missing_required_fields(self, client: TestClient, auth_headers: dict):
        """Test creating knowledge source without required fields."""
        data = {
            "title": "Test Source"
            # Missing content and category
        }

        response = client.post(
            "/api/knowledge/sources",
            json=data,
            headers=auth_headers
        )

        assert response.status_code == 422


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeCategories:
    """Tests for getting knowledge categories."""

    def test_get_categories(self, client: TestClient, auth_headers: dict):
        """Test getting available categories."""
        response = client.get("/api/knowledge/categories", headers=auth_headers)

        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) > 0
        assert "Courses" in categories
        assert "Admission" in categories

    def test_get_categories_unauthorized(self, client: TestClient):
        """Test getting categories without authentication."""
        response = client.get("/api/knowledge/categories")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeSourceList:
    """Tests for listing knowledge sources."""

    def test_list_sources_empty(self, client: TestClient, auth_headers: dict):
        """Test listing sources when none exist."""
        response = client.get("/api/knowledge/sources", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 0
        assert result["items"] == []
        assert result["page"] == 1

    def test_list_sources_with_data(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test listing sources with existing data."""
        # Create test sources
        for i in range(5):
            source = KnowledgeSource(
                title=f"Source {i}",
                content=f"Content {i}",
                category=CategoryEnum.COURSES
            )
            db_session.add(source)
        db_session.commit()

        response = client.get("/api/knowledge/sources", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 5
        assert len(result["items"]) == 5

    def test_list_sources_pagination(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test pagination of knowledge sources."""
        # Create 15 test sources
        for i in range(15):
            source = KnowledgeSource(
                title=f"Source {i}",
                content=f"Content {i}",
                category=CategoryEnum.COURSES
            )
            db_session.add(source)
        db_session.commit()

        # Page 1
        response = client.get("/api/knowledge/sources?page=1&size=10", headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 15
        assert len(result["items"]) == 10
        assert result["page"] == 1
        assert result["pages"] == 2

        # Page 2
        response = client.get("/api/knowledge/sources?page=2&size=10", headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert len(result["items"]) == 5

    def test_list_sources_search(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test searching knowledge sources."""
        # Create sources with different titles
        sources_data = [
            ("Python Basics", "Learn Python programming"),
            ("Java Introduction", "Learn Java programming"),
            ("Python Advanced", "Advanced Python topics")
        ]

        for title, content in sources_data:
            source = KnowledgeSource(
                title=title,
                content=content,
                category=CategoryEnum.COURSES
            )
            db_session.add(source)
        db_session.commit()

        # Search for "Python"
        response = client.get("/api/knowledge/sources?search=Python", headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 2
        assert all("Python" in item["title"] for item in result["items"])

    def test_list_sources_filter_category(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test filtering sources by category."""
        # Create sources in different categories
        source1 = KnowledgeSource(title="Course 1", content="Content", category=CategoryEnum.COURSES)
        source2 = KnowledgeSource(title="Admission 1", content="Content", category=CategoryEnum.ADMISSION)
        db_session.add_all([source1, source2])
        db_session.commit()

        response = client.get("/api/knowledge/sources?category=Courses", headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 1
        assert result["items"][0]["category"] == "Courses"

    def test_list_sources_filter_active(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test filtering sources by active status."""
        source1 = KnowledgeSource(title="Active", content="Content", category=CategoryEnum.COURSES, is_active=True)
        source2 = KnowledgeSource(title="Inactive", content="Content", category=CategoryEnum.COURSES, is_active=False)
        db_session.add_all([source1, source2])
        db_session.commit()

        response = client.get("/api/knowledge/sources?is_active=true", headers=auth_headers)
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 1
        assert result["items"][0]["is_active"] is True


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeSourceGet:
    """Tests for getting a specific knowledge source."""

    def test_get_source_success(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test getting a specific source by ID."""
        source = KnowledgeSource(
            title="Test Source",
            content="Test Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)

        response = client.get(f"/api/knowledge/sources/{source.id}", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert result["id"] == str(source.id)
        assert result["title"] == source.title

    def test_get_source_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting a non-existent source."""
        fake_id = uuid4()
        response = client.get(f"/api/knowledge/sources/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_get_source_invalid_uuid(self, client: TestClient, auth_headers: dict):
        """Test getting source with invalid UUID."""
        response = client.get("/api/knowledge/sources/invalid-uuid", headers=auth_headers)
        assert response.status_code == 422


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeSourceUpdate:
    """Tests for updating knowledge sources."""

    def test_update_source_success(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test successful update of a knowledge source."""
        source = KnowledgeSource(
            title="Original Title",
            content="Original Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)

        update_data = {
            "title": "Updated Title",
            "description": "New description"
        }

        response = client.put(
            f"/api/knowledge/sources/{source.id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        result = response.json()
        assert result["title"] == "Updated Title"
        assert result["description"] == "New description"
        assert result["content"] == "Original Content"  # Unchanged

    def test_update_source_partial(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test partial update of knowledge source."""
        source = KnowledgeSource(
            title="Original",
            content="Content",
            category=CategoryEnum.COURSES,
            is_active=True
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)

        response = client.put(
            f"/api/knowledge/sources/{source.id}",
            json={"is_active": False},
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["is_active"] is False

    def test_update_source_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating a non-existent source."""
        fake_id = uuid4()
        response = client.put(
            f"/api/knowledge/sources/{fake_id}",
            json={"title": "New Title"},
            headers=auth_headers
        )
        assert response.status_code == 404


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeSourceDelete:
    """Tests for deleting knowledge sources."""

    def test_delete_source_success(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test successful deletion of a knowledge source."""
        source = KnowledgeSource(
            title="To Delete",
            content="Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)
        source_id = source.id

        response = client.delete(f"/api/knowledge/sources/{source_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify deletion
        deleted = db_session.query(KnowledgeSource).filter_by(id=source_id).first()
        assert deleted is None

    def test_delete_source_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting a non-existent source."""
        fake_id = uuid4()
        response = client.delete(f"/api/knowledge/sources/{fake_id}", headers=auth_headers)
        assert response.status_code == 404


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeChunks:
    """Tests for knowledge chunks endpoints."""

    def test_get_source_chunks_empty(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test getting chunks for a source with no chunks."""
        source = KnowledgeSource(
            title="Test Source",
            content="Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)

        response = client.get(f"/api/knowledge/sources/{source.id}/chunks", headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == []

    def test_get_source_chunks_with_data(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test getting chunks for a source with chunks."""
        source = KnowledgeSource(
            title="Test Source",
            content="Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)

        # Create chunks
        for i in range(3):
            chunk = KnowledgeChunk(
                source_id=source.id,
                text=f"Chunk {i}",
                index=i,
                token_count=10,
                word_count=5
            )
            db_session.add(chunk)
        db_session.commit()

        response = client.get(f"/api/knowledge/sources/{source.id}/chunks", headers=auth_headers)

        assert response.status_code == 200
        chunks = response.json()
        assert len(chunks) == 3
        assert chunks[0]["index"] == 0
        assert chunks[1]["index"] == 1


@pytest.mark.api
@pytest.mark.knowledge
class TestSemanticSearch:
    """Tests for semantic search endpoint."""

    def test_semantic_search_placeholder(self, client: TestClient, auth_headers: dict):
        """Test semantic search returns placeholder message."""
        data = {
            "query": "Python programming",
            "top_k": 5
        }

        response = client.post("/api/knowledge/search", json=data, headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert "not_configured" in result["status"]


@pytest.mark.api
@pytest.mark.knowledge
class TestKnowledgeStats:
    """Tests for knowledge statistics endpoint."""

    def test_get_stats_empty(self, client: TestClient, auth_headers: dict):
        """Test getting stats with no data."""
        response = client.get("/api/knowledge/stats", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()
        assert stats["total_sources"] == 0
        assert stats["active_sources"] == 0
        assert stats["total_chunks"] == 0

    def test_get_stats_with_data(self, client: TestClient, auth_headers: dict, db_session: Session):
        """Test getting stats with data."""
        # Create sources
        source1 = KnowledgeSource(
            title="Active Course",
            content="Content",
            category=CategoryEnum.COURSES,
            is_active=True
        )
        source2 = KnowledgeSource(
            title="Inactive Admission",
            content="Content",
            category=CategoryEnum.ADMISSION,
            is_active=False
        )
        db_session.add_all([source1, source2])
        db_session.commit()

        response = client.get("/api/knowledge/stats", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()
        assert stats["total_sources"] == 2
        assert stats["active_sources"] == 1
        assert "sources_by_category" in stats
        assert stats["sources_by_category"]["Courses"] == 1
        assert stats["sources_by_category"]["Admission"] == 1
