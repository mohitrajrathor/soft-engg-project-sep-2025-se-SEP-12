"""
Script to populate database with mock data.

Run this script to add test users, queries, knowledge sources, and tasks.
Usage: python populate_db.py
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta, timezone
import random
import uuid

from app.core.db import SessionLocal, engine, Base
from app.models.user import User
from app.models.knowledge import KnowledgeSource, KnowledgeChunk
from app.models.task import Task
from app.models.query import Query, QueryResponse
from app.models.enums import CategoryEnum, TaskTypeEnum, TaskStatusEnum
from app.schemas.user_schema import UserRole
from app.schemas.query_schema import QueryStatus, QueryCategory, QueryPriority
from app.core.security import hash_password


def populate_database():
    """Populate database with comprehensive mock data."""

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created\n")

    db = SessionLocal()

    try:
        result = {
            "users_created": 0,
            "knowledge_sources_created": 0,
            "tasks_created": 0,
            "queries_created": 0
        }

        # ============================================================
        # CREATE USERS
        # ============================================================
        print("Creating test users...")
        users_data = [
            {"email": "student@test.com", "full_name": "Test Student", "role": UserRole.STUDENT, "password": "student123"},
            {"email": "ta@test.com", "full_name": "Test TA", "role": UserRole.TA, "password": "ta123"},
            {"email": "instructor@test.com", "full_name": "Test Instructor", "role": UserRole.INSTRUCTOR, "password": "instructor123"},
            {"email": "admin@test.com", "full_name": "Test Admin", "role": UserRole.ADMIN, "password": "admin123"}
        ]

        created_users = {}
        for user_data in users_data:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    password=hash_password(user_data["password"]),
                    is_active=True
                )
                db.add(user)
                db.flush()
                created_users[user_data["role"].value] = user
                result["users_created"] += 1
                print(f"  ✓ Created user: {user_data['email']}")
            else:
                created_users[user_data["role"].value] = existing
                print(f"  - User already exists: {user_data['email']}")

        # ============================================================
        # CREATE KNOWLEDGE SOURCES
        # ============================================================
        print("\nCreating knowledge sources...")
        knowledge_data = [
            {
                "title": "Introduction to Software Engineering",
                "description": "Comprehensive guide to software engineering principles",
                "content": "Software Engineering covers SDLC, design patterns, best practices, and quality assurance. Key topics include requirements analysis, system design, implementation strategies, testing methodologies, and deployment practices.",
                "category": CategoryEnum.COURSES
            },
            {
                "title": "Data Structures and Algorithms",
                "description": "Essential data structures and algorithmic techniques",
                "content": "Core concepts: Arrays, Linked Lists, Trees, Graphs, Hash Tables. Algorithms: Sorting (Quick, Merge, Heap), Searching (Binary, DFS, BFS), Dynamic Programming, Greedy Algorithms.",
                "category": CategoryEnum.COURSES
            },
            {
                "title": "Assignment 1: REST API Development",
                "description": "Build a RESTful API using FastAPI",
                "content": "Create a Library Management System API with CRUD operations, authentication, and testing. Requirements: Books endpoint, Users endpoint, Borrow/return functionality, Input validation, JWT authentication.",
                "category": CategoryEnum.ASSIGNMENTS
            },
            {
                "title": "Quiz: Object-Oriented Programming",
                "description": "Test on OOP concepts",
                "content": "Topics: Classes and Objects, Inheritance, Polymorphism, Encapsulation, Abstraction, SOLID principles. Format: 20 MCQs + 5 short answers. Time: 45 minutes.",
                "category": CategoryEnum.QUIZZES
            },
            {
                "title": "Python Programming Best Practices",
                "description": "Guidelines for clean Python code",
                "content": "Follow PEP 8 style guide. Use list comprehensions, context managers, generators, decorators. Write unit tests with pytest, aim for >80% coverage. Use type hints and docstrings.",
                "category": CategoryEnum.COURSES
            },
        ]

        knowledge_sources = []
        for data in knowledge_data:
            existing = db.query(KnowledgeSource).filter(
                KnowledgeSource.title == data["title"]
            ).first()

            if not existing:
                source = KnowledgeSource(
                    title=data["title"],
                    description=data["description"],
                    content=data["content"],
                    category=data["category"],
                    is_active=True,
                    created_at=datetime.now(timezone.utc)
                )
                db.add(source)
                db.flush()

                # Create a chunk for each source
                chunk = KnowledgeChunk(
                    source_id=source.id,
                    text=data["content"],
                    index=0
                )
                db.add(chunk)

                knowledge_sources.append(source)
                result["knowledge_sources_created"] += 1
                print(f"  ✓ Created: {data['title']}")
            else:
                knowledge_sources.append(existing)
                print(f"  - Already exists: {data['title']}")

        # ============================================================
        # CREATE TASKS
        # ============================================================
        print("\nCreating background tasks...")

        # Use actual knowledge source IDs for tasks
        source_id_1 = knowledge_sources[0].id if knowledge_sources else None
        source_id_2 = knowledge_sources[1].id if len(knowledge_sources) > 1 else None

        tasks_data = [
            {
                "task_type": TaskTypeEnum.EMBEDDING.value,
                "status": TaskStatusEnum.COMPLETED.value,
                "source_id": source_id_1,
                "metadata_": '{"chunks_processed": 5, "model": "text-embedding-3-small"}',
                "created_at": datetime.now(timezone.utc) - timedelta(days=2),
                "completed_at": datetime.now(timezone.utc) - timedelta(days=2, hours=-1)
            },
            {
                "task_type": TaskTypeEnum.EMBEDDING.value,
                "status": TaskStatusEnum.IN_PROGRESS.value,
                "source_id": source_id_2,
                "metadata_": '{"chunks_processed": 3, "total_chunks": 5}',
                "created_at": datetime.now(timezone.utc) - timedelta(hours=2)
            },
            {
                "task_type": TaskTypeEnum.QUERY.value,
                "status": TaskStatusEnum.COMPLETED.value,
                "metadata_": '{"query": "What is polymorphism?", "response_time": 1.2}',
                "created_at": datetime.now(timezone.utc) - timedelta(hours=5),
                "completed_at": datetime.now(timezone.utc) - timedelta(hours=5, minutes=-30)
            },
            {
                "task_type": TaskTypeEnum.DATA_PROCESSING.value,
                "status": TaskStatusEnum.FAILED.value,
                "error_message": "Connection timeout while processing data",
                "metadata_": '{"retry_count": 3}',
                "created_at": datetime.now(timezone.utc) - timedelta(hours=1)
            },
        ]

        for data in tasks_data:
            task = Task(**data)
            db.add(task)
            result["tasks_created"] += 1
            print(f"  ✓ Created {data['task_type']} task ({data['status']})")

        # ============================================================
        # CREATE QUERIES WITH RESPONSES
        # ============================================================
        print("\nCreating queries with responses...")
        student = created_users.get("student")
        ta = created_users.get("ta")
        instructor = created_users.get("instructor")

        if student and ta and instructor:
            queries_data = [
                {
                    "title": "Help with Dijkstra complexity",
                    "description": "I implemented Dijkstra's algorithm using adjacency matrix and binary heap, but I'm getting O(n²) complexity. Is this expected for dense graphs? I thought using a heap would give me O((V+E)logV).",
                    "category": QueryCategory.TECHNICAL,
                    "priority": QueryPriority.MEDIUM,
                    "status": QueryStatus.OPEN,
                    "tags": ["algorithms", "graph-theory", "complexity"],
                    "days_ago": 0,
                    "responses": [
                        {
                            "user": "student",
                            "content": "I used adjacency matrix + binary heap and got O(n²). Is this expected for dense graphs?",
                            "hours_ago": 2
                        },
                        {
                            "user": "ta",
                            "content": "Yes. With an adjacency matrix the edge scans dominate at O(n²). Use adjacency lists; on dense graphs, a Fibonacci heap won't help asymptotically versus array/heap implementations. Check that you don't relax edges already finalized.",
                            "hours_ago": 1
                        }
                    ]
                },
                {
                    "title": "Systems lab Docker error",
                    "description": "Docker build fails on ARM machine with error 'exec format error'. Running on M1 Mac. Works fine on Intel machines.",
                    "category": QueryCategory.TECHNICAL,
                    "priority": QueryPriority.HIGH,
                    "status": QueryStatus.RESOLVED,
                    "tags": ["docker", "systems", "ARM"],
                    "days_ago": 1,
                    "responses": [
                        {
                            "user": "student",
                            "content": "Docker build fails on ARM machine. Getting 'exec format error'",
                            "hours_ago": 26
                        },
                        {
                            "user": "ta",
                            "content": "Use --platform linux/amd64 flag in your Dockerfile FROM statement. Or use docker buildx for multi-platform builds.",
                            "hours_ago": 24,
                            "is_solution": True
                        }
                    ]
                },
                {
                    "title": "Office hour booking confirmation",
                    "description": "Want to confirm the location for Friday office hours. Is it still Room 301 or has it moved?",
                    "category": QueryCategory.GENERAL,
                    "priority": QueryPriority.LOW,
                    "status": QueryStatus.OPEN,
                    "tags": ["office-hours", "logistics"],
                    "days_ago": 1,
                    "responses": []
                },
                {
                    "title": "How to implement binary search tree?",
                    "description": "Confused about BST insert operation. Should I use recursion or iteration? How do I handle duplicate values?",
                    "category": QueryCategory.TECHNICAL,
                    "priority": QueryPriority.MEDIUM,
                    "status": QueryStatus.IN_PROGRESS,
                    "tags": ["data-structures", "BST", "trees"],
                    "days_ago": 2,
                    "responses": [
                        {
                            "user": "ta",
                            "content": "Both recursion and iteration work. Recursion is more elegant. For duplicates, you can either reject them or store count in node.",
                            "hours_ago": 36
                        }
                    ]
                },
                {
                    "title": "Assignment deadline extension",
                    "description": "Medical emergency in family. Need extension for Assignment 2. Can provide medical certificate.",
                    "category": QueryCategory.ASSIGNMENT,
                    "priority": QueryPriority.HIGH,
                    "status": QueryStatus.IN_PROGRESS,
                    "tags": ["deadline", "extension"],
                    "days_ago": 3,
                    "responses": [
                        {
                            "user": "instructor",
                            "content": "Please email me the medical certificate. Extension granted till next Monday.",
                            "hours_ago": 60
                        }
                    ]
                },
                {
                    "title": "Quiz results when?",
                    "description": "When will OOP quiz results be published? It's been a week since we took the quiz.",
                    "category": QueryCategory.EXAM,
                    "priority": QueryPriority.LOW,
                    "status": QueryStatus.RESOLVED,
                    "tags": ["quiz", "results"],
                    "days_ago": 5,
                    "responses": [
                        {
                            "user": "instructor",
                            "content": "Results will be published tomorrow. Sorry for the delay.",
                            "hours_ago": 120,
                            "is_solution": True
                        }
                    ]
                },
                {
                    "title": "PhD program requirements",
                    "description": "What are the prerequisites for PhD in AI? Do I need research experience?",
                    "category": QueryCategory.GENERAL,
                    "priority": QueryPriority.MEDIUM,
                    "status": QueryStatus.OPEN,
                    "tags": ["PhD", "admission", "AI"],
                    "days_ago": 7,
                    "responses": []
                },
                {
                    "title": "Interview prep resources",
                    "description": "Looking for resources to prepare for FAANG interviews. Any recommendations?",
                    "category": QueryCategory.GENERAL,
                    "priority": QueryPriority.MEDIUM,
                    "status": QueryStatus.RESOLVED,
                    "tags": ["interview", "FAANG", "placement"],
                    "days_ago": 10,
                    "responses": [
                        {
                            "user": "instructor",
                            "content": "Check out LeetCode, Cracking the Coding Interview, and System Design Interview books. Practice daily.",
                            "hours_ago": 240,
                            "is_solution": True
                        }
                    ]
                }
            ]

            for data in queries_data:
                existing = db.query(Query).filter(Query.title == data["title"]).first()
                if not existing:
                    query = Query(
                        title=data["title"],
                        description=data["description"],
                        category=data["category"],
                        priority=data["priority"],
                        status=data["status"],
                        tags=data.get("tags", []),
                        student_id=student.id,
                        created_at=datetime.now(timezone.utc) - timedelta(days=data.get("days_ago", 0))
                    )
                    db.add(query)
                    db.flush()

                    # Add responses
                    for resp_data in data.get("responses", []):
                        responder = None
                        if resp_data["user"] == "student":
                            responder = student
                        elif resp_data["user"] == "ta":
                            responder = ta
                        elif resp_data["user"] == "instructor":
                            responder = instructor

                        if responder:
                            response = QueryResponse(
                                query_id=query.id,
                                user_id=responder.id,
                                content=resp_data["content"],
                                is_solution=resp_data.get("is_solution", False),
                                created_at=datetime.now(timezone.utc) - timedelta(hours=resp_data.get("hours_ago", 0))
                            )
                            db.add(response)

                    result["queries_created"] += 1
                    print(f"  ✓ Created: {data['title']} ({len(data.get('responses', []))} responses)")
                else:
                    print(f"  - Already exists: {data['title']}")

        # ============================================================
        # COMMIT ALL CHANGES
        # ============================================================
        print("\nCommitting changes to database...")
        db.commit()
        print("✓ All changes committed!\n")

        # ============================================================
        # SUMMARY
        # ============================================================
        print("=" * 60)
        print("DATABASE POPULATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"✓ Users created: {result['users_created']}")
        print(f"✓ Knowledge sources created: {result['knowledge_sources_created']}")
        print(f"✓ Tasks created: {result['tasks_created']}")
        print(f"✓ Queries created: {result['queries_created']}")
        print()
        print("=" * 60)
        print("TEST CREDENTIALS:")
        print("=" * 60)
        print("Student:    student@test.com    / student123")
        print("TA:         ta@test.com         / ta123")
        print("Instructor: instructor@test.com / instructor123")
        print("Admin:      admin@test.com      / admin123")
        print("=" * 60)

        return result

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("AURA DATABASE POPULATION SCRIPT")
    print("=" * 60)
    print()

    try:
        populate_database()
        print("\n✅ Success! Database is ready to use.")
        print("\nNext steps:")
        print("  1. Start backend:  python main.py")
        print("  2. Start frontend: cd ../frontend && npm run dev")
        print("  3. Login with:     student@test.com / student123")
        print("  4. Visit queries:  http://localhost:5173/student/queries")
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
