"""
API tests for the Tag CRUD endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.tag import Tag

# Mark all tests in this file as 'api' and 'tag' tests
pytestmark = [pytest.mark.api, pytest.mark.tag]


@pytest.fixture
def test_tag(db_session: Session, authenticated_ta: "User") -> Tag:
    """Creates a sample tag in the database for testing."""
    tag = Tag(name="pytest-tag", created_by_id=authenticated_ta.id)
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    return tag


def test_create_tag_as_ta(client: TestClient, ta_auth_headers: dict, db_session: Session):
    """Tests that a TA can successfully create a new tag."""
    response = client.post(
        "/api/tags/",
        headers=ta_auth_headers,
        json={"name": "New TA Tag"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "new ta tag"  # Should be lowercased
    assert data["creator"]["email"] is not None

    tag = db_session.query(Tag).filter(Tag.id == data["id"]).first()
    assert tag is not None


def test_create_tag_as_admin(client: TestClient, admin_auth_headers: dict):
    """Tests that an Admin can also create a new tag."""
    response = client.post(
        "/api/tags/",
        headers=admin_auth_headers,
        json={"name": "New Admin Tag"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "new admin tag"


def test_create_tag_as_student(client: TestClient, auth_headers: dict):
    """Tests that a student cannot create a tag."""
    response = client.post(
        "/api/tags/",
        headers=auth_headers,
        json={"name": "Student Tag Attempt"},
    )
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


def test_create_duplicate_tag(client: TestClient, ta_auth_headers: dict, test_tag: Tag):
    """Tests that creating a tag with a duplicate name fails."""
    response = client.post(
        "/api/tags/",
        headers=ta_auth_headers,
        json={"name": test_tag.name},
    )
    assert response.status_code == 409
    assert "tag with this name already exists" in response.json()["detail"]


def test_get_all_tags(client: TestClient, auth_headers: dict, test_tag: Tag):
    """Tests that any authenticated user can retrieve a list of all tags."""
    response = client.get("/api/tags/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(t["id"] == test_tag.id for t in data)


def test_search_tags(client: TestClient, auth_headers: dict, test_tag: Tag):
    """Tests searching for tags by name."""
    # Search for a specific tag
    response = client.get(f"/api/tags/?search={test_tag.name}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == test_tag.id

    # Search for a partial name
    response = client.get("/api/tags/?search=pytest", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Search for a non-existent tag
    response = client.get("/api/tags/?search=nonexistenttag", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_tag_by_id(client: TestClient, auth_headers: dict, test_tag: Tag):
    """Tests successful retrieval of a single tag by its ID."""
    response = client.get(f"/api/tags/{test_tag.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_tag.id
    assert data["name"] == test_tag.name


def test_get_tag_by_id_not_found(client: TestClient, auth_headers: dict):
    """Tests that requesting a non-existent tag ID returns a 404 error."""
    response = client.get("/api/tags/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_tag_as_ta(client: TestClient, ta_auth_headers: dict, test_tag: Tag):
    """Tests that a TA can successfully update an existing tag."""
    updated_name = "updated-pytest-tag"
    response = client.put(
        f"/api/tags/{test_tag.id}",
        headers=ta_auth_headers,
        json={"name": updated_name},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_tag.id
    assert data["name"] == updated_name


def test_update_tag_as_student(client: TestClient, auth_headers: dict, test_tag: Tag):
    """Tests that a student cannot update a tag."""
    response = client.put(
        f"/api/tags/{test_tag.id}",
        headers=auth_headers,
        json={"name": "student-update-attempt"},
    )
    assert response.status_code == 403


def test_delete_tag_as_admin(client: TestClient, admin_auth_headers: dict, test_tag: Tag):
    """Tests that an admin can successfully delete a tag."""
    response = client.delete(f"/api/tags/{test_tag.id}", headers=admin_auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/api/tags/{test_tag.id}", headers=admin_auth_headers)
    assert get_response.status_code == 404


def test_delete_tag_as_student(client: TestClient, auth_headers: dict, test_tag: Tag):
    """Tests that a student cannot delete a tag."""
    response = client.delete(f"/api/tags/{test_tag.id}", headers=auth_headers)
    assert response.status_code == 403