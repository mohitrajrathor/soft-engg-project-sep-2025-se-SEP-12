"""
Tests for Background Tasks API endpoints.

This module tests:
- GET /api/tasks/ - List all tasks
- GET /api/tasks/{id} - Get specific task
- DELETE /api/tasks/{id} - Delete task
- GET /api/tasks/statistics/summary - Get task statistics
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.models.task import Task
from app.models.knowledge import KnowledgeSource
from app.models.enums import TaskTypeEnum, TaskStatusEnum, CategoryEnum


@pytest.mark.api
@pytest.mark.tasks
class TestTasksList:
    """Tests for listing background tasks."""

    def test_list_tasks_empty(self, client: TestClient, auth_headers: dict):
        """Test listing tasks when none exist."""
        response = client.get("/api/tasks/", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) == 0

    def test_list_tasks_with_data(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test listing tasks with existing data."""
        # Create test tasks
        for i in range(5):
            task = Task(
                task_type=TaskTypeEnum.EMBEDDING.value,
                status=TaskStatusEnum.COMPLETED.value
            )
            db_session.add(task)
        db_session.commit()

        response = client.get("/api/tasks/", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 5

    def test_list_tasks_pagination(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test pagination of tasks."""
        # Create 25 test tasks
        for i in range(25):
            task = Task(
                task_type=TaskTypeEnum.EMBEDDING.value,
                status=TaskStatusEnum.COMPLETED.value
            )
            db_session.add(task)
        db_session.commit()

        # Page 1
        response = client.get("/api/tasks/?page=1&size=20", headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 20

        # Page 2
        response = client.get("/api/tasks/?page=2&size=20", headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 5

    def test_list_tasks_filter_by_type(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test filtering tasks by type."""
        # Create different types of tasks
        embedding_task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        query_task = Task(
            task_type=TaskTypeEnum.QUERY.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        db_session.add_all([embedding_task, query_task])
        db_session.commit()

        # Filter by EMBEDDING
        response = client.get(
            f"/api/tasks/?task_type={TaskTypeEnum.EMBEDDING.value}",
            headers=auth_headers
        )
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["task_type"] == TaskTypeEnum.EMBEDDING.value

    def test_list_tasks_filter_by_status(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test filtering tasks by status."""
        # Create tasks with different statuses
        pending_task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.PENDING.value
        )
        completed_task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        failed_task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.FAILED.value
        )
        db_session.add_all([pending_task, completed_task, failed_task])
        db_session.commit()

        # Filter by COMPLETED
        response = client.get(
            f"/api/tasks/?status={TaskStatusEnum.COMPLETED.value}",
            headers=auth_headers
        )
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == TaskStatusEnum.COMPLETED.value

    def test_list_tasks_combined_filters(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test filtering tasks with multiple filters."""
        # Create various tasks
        task1 = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        task2 = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.FAILED.value
        )
        task3 = Task(
            task_type=TaskTypeEnum.QUERY.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        db_session.add_all([task1, task2, task3])
        db_session.commit()

        # Filter by type AND status
        response = client.get(
            f"/api/tasks/?task_type={TaskTypeEnum.EMBEDDING.value}&status={TaskStatusEnum.COMPLETED.value}",
            headers=auth_headers
        )
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1

    def test_list_tasks_unauthorized(self, client: TestClient):
        """Test listing tasks without authentication."""
        response = client.get("/api/tasks/")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.tasks
class TestTasksGet:
    """Tests for getting a specific task."""

    def test_get_task_success(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test getting a specific task by ID."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value,
            metadata_='{"key": "value"}'
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        response = client.get(f"/api/tasks/{task.id}", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert result["id"] == str(task.id)
        assert result["task_type"] == TaskTypeEnum.EMBEDDING.value
        assert result["status"] == TaskStatusEnum.COMPLETED.value

    def test_get_task_with_source(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test getting task associated with a knowledge source."""
        # Create knowledge source
        source = KnowledgeSource(
            title="Test Source",
            content="Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)

        # Create task linked to source
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value,
            source_id=source.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        response = client.get(f"/api/tasks/{task.id}", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert result["source_id"] == str(source.id)

    def test_get_task_with_error(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test getting task with error message."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.FAILED.value,
            error_message="Failed to process document"
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        response = client.get(f"/api/tasks/{task.id}", headers=auth_headers)

        assert response.status_code == 200
        result = response.json()
        assert result["status"] == TaskStatusEnum.FAILED.value
        assert result["error_message"] == "Failed to process document"

    def test_get_task_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting a non-existent task."""
        fake_id = uuid4()
        response = client.get(f"/api/tasks/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_get_task_invalid_uuid(self, client: TestClient, auth_headers: dict):
        """Test getting task with invalid UUID."""
        response = client.get("/api/tasks/invalid-uuid", headers=auth_headers)
        assert response.status_code == 422

    def test_get_task_unauthorized(self, client: TestClient, db_session: Session):
        """Test getting task without authentication."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        response = client.get(f"/api/tasks/{task.id}")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.tasks
class TestTasksDelete:
    """Tests for deleting tasks."""

    def test_delete_completed_task(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test deleting a completed task."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        task_id = task.id

        response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify deletion
        deleted = db_session.query(Task).filter_by(id=task_id).first()
        assert deleted is None

    def test_delete_failed_task(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test deleting a failed task."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.FAILED.value
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        task_id = task.id

        response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify deletion
        deleted = db_session.query(Task).filter_by(id=task_id).first()
        assert deleted is None

    def test_delete_pending_task(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test cannot delete pending task."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.PENDING.value
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        response = client.delete(f"/api/tasks/{task.id}", headers=auth_headers)
        assert response.status_code == 400
        assert "pending" in response.json()["detail"].lower()

    def test_delete_in_progress_task(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test cannot delete in-progress task."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.IN_PROGRESS.value
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        response = client.delete(f"/api/tasks/{task.id}", headers=auth_headers)
        assert response.status_code == 400

    def test_delete_task_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting a non-existent task."""
        fake_id = uuid4()
        response = client.delete(f"/api/tasks/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_task_unauthorized(self, client: TestClient, db_session: Session):
        """Test deleting task without authentication."""
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.COMPLETED.value
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        response = client.delete(f"/api/tasks/{task.id}")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.tasks
class TestTaskStatistics:
    """Tests for task statistics endpoint."""

    def test_get_statistics_empty(self, client: TestClient, auth_headers: dict):
        """Test getting statistics with no tasks."""
        response = client.get("/api/tasks/statistics/summary", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()

        assert stats["total"] == 0
        assert stats["by_status"]["pending"] == 0
        assert stats["by_status"]["in_progress"] == 0
        assert stats["by_status"]["completed"] == 0
        assert stats["by_status"]["failed"] == 0
        assert stats["by_type"]["embedding"] == 0
        assert stats["by_type"]["query"] == 0
        assert stats["success_rate"] == 0

    def test_get_statistics_with_data(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test getting statistics with tasks."""
        # Create tasks with different statuses
        tasks_data = [
            (TaskTypeEnum.EMBEDDING, TaskStatusEnum.COMPLETED),
            (TaskTypeEnum.EMBEDDING, TaskStatusEnum.COMPLETED),
            (TaskTypeEnum.EMBEDDING, TaskStatusEnum.FAILED),
            (TaskTypeEnum.QUERY, TaskStatusEnum.PENDING),
            (TaskTypeEnum.QUERY, TaskStatusEnum.IN_PROGRESS),
        ]

        for task_type, status in tasks_data:
            task = Task(
                task_type=task_type.value,
                status=status.value
            )
            db_session.add(task)
        db_session.commit()

        response = client.get("/api/tasks/statistics/summary", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()

        # Check totals
        assert stats["total"] == 5

        # Check by status
        assert stats["by_status"]["completed"] == 2
        assert stats["by_status"]["failed"] == 1
        assert stats["by_status"]["pending"] == 1
        assert stats["by_status"]["in_progress"] == 1

        # Check by type
        assert stats["by_type"]["embedding"] == 3
        assert stats["by_type"]["query"] == 2

        # Check success rate (2 completed / 5 total = 40%)
        assert stats["success_rate"] == 40.0

    def test_get_statistics_all_completed(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test statistics when all tasks are completed."""
        for i in range(10):
            task = Task(
                task_type=TaskTypeEnum.EMBEDDING.value,
                status=TaskStatusEnum.COMPLETED.value
            )
            db_session.add(task)
        db_session.commit()

        response = client.get("/api/tasks/statistics/summary", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()

        assert stats["total"] == 10
        assert stats["by_status"]["completed"] == 10
        assert stats["success_rate"] == 100.0

    def test_get_statistics_all_failed(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test statistics when all tasks have failed."""
        for i in range(5):
            task = Task(
                task_type=TaskTypeEnum.EMBEDDING.value,
                status=TaskStatusEnum.FAILED.value
            )
            db_session.add(task)
        db_session.commit()

        response = client.get("/api/tasks/statistics/summary", headers=auth_headers)

        assert response.status_code == 200
        stats = response.json()

        assert stats["total"] == 5
        assert stats["by_status"]["failed"] == 5
        assert stats["success_rate"] == 0.0

    def test_get_statistics_unauthorized(self, client: TestClient):
        """Test getting statistics without authentication."""
        response = client.get("/api/tasks/statistics/summary")
        assert response.status_code in [401, 403]


@pytest.mark.api
@pytest.mark.tasks
@pytest.mark.integration
class TestTasksIntegration:
    """Integration tests for tasks API."""

    def test_tasks_complete_workflow(
        self,
        client: TestClient,
        auth_headers: dict,
        db_session: Session
    ):
        """Test complete task workflow."""
        # Create a knowledge source
        source = KnowledgeSource(
            title="Test Source",
            content="Content",
            category=CategoryEnum.COURSES
        )
        db_session.add(source)
        db_session.commit()
        db_session.refresh(source)

        # Create a task for the source
        task = Task(
            task_type=TaskTypeEnum.EMBEDDING.value,
            status=TaskStatusEnum.PENDING.value,
            source_id=source.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        # List tasks - should see 1 pending task
        list_response = client.get("/api/tasks/", headers=auth_headers)
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        # Get specific task
        get_response = client.get(f"/api/tasks/{task.id}", headers=auth_headers)
        assert get_response.status_code == 200
        assert get_response.json()["status"] == TaskStatusEnum.PENDING.value

        # Check statistics
        stats_response = client.get("/api/tasks/statistics/summary", headers=auth_headers)
        assert stats_response.status_code == 200
        stats = stats_response.json()
        assert stats["total"] == 1
        assert stats["by_status"]["pending"] == 1

        # Update task to completed (simulating background processing)
        task.status = TaskStatusEnum.COMPLETED.value
        db_session.commit()

        # Delete the completed task
        delete_response = client.delete(f"/api/tasks/{task.id}", headers=auth_headers)
        assert delete_response.status_code == 204

        # Verify task is deleted
        list_response = client.get("/api/tasks/", headers=auth_headers)
        assert len(list_response.json()) == 0
