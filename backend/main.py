"""
AURA - Academic Unified Response Assistant API

Main FastAPI application entry point.

This module initializes the FastAPI application with:
- CORS middleware for frontend integration
- Database initialization on startup
- API route registration
- Comprehensive API documentation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Try to import LangChain (optional dependency)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    ChatGoogleGenerativeAI = None

from app.core.config import settings
from app.core.db import init_db
from app.api.auth import auth_router
from app.api.chatbot import chatbot_router
from app.api.course_router import router as course_router



# ============================================================================
# Application Lifecycle Management
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events:
    - Startup: Initialize database tables
    - Shutdown: Cleanup resources (if needed)
    """
    # Startup: Initialize database
    print("Starting AURA API...")
    print(f"Database: {settings.DATABASE_URL}")
    init_db()
    print("Database initialized")

    yield

    # Shutdown: Cleanup (if needed)
    print("Shutting down AURA API...")


# ============================================================================
# FastAPI Application Instance
# ============================================================================


# Create description dynamically
environment_name = "Development" if settings.DEBUG else "Production"
api_description = f"""
## AURA - Academic Unified Response Assistant

A comprehensive educational platform API supporting:
- **Multi-role authentication** (Students, TAs, Instructors, Admins)
- **Query/Doubt management** system
- **Resource sharing** and management
- **Announcements** and notifications
- **User profiles** with statistics
- **Role-based access control** (RBAC)

### Authentication

Most endpoints require authentication using JWT Bearer tokens.

**How to authenticate:**
1. Register: `POST /api/auth/signup`
2. Login: `POST /api/auth/login`
3. Use the `access_token` in Authorization header: `Bearer <token>`

### User Roles

- **student**: Regular students - can post queries, view resources
- **ta**: Teaching assistants - can respond to queries, manage resources
- **instructor**: Course instructors - full course management
- **admin**: System administrators - full system access

### Features

#### 🔐 Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control
- Secure password hashing with Argon2

#### ❓ Query Management
- Students can post doubts/questions
- TAs/Instructors can respond and resolve queries
- Priority levels and status tracking
- Query analytics and statistics

#### 📚 Resource Management
- Upload and share educational materials
- Multiple resource types (videos, PDFs, links, etc.)
- Access control (public, course-specific, private)
- Download and view tracking

#### 📢 Announcements
- Institution-wide and course-specific announcements
- Target specific user roles
- Urgent/deadline notifications
- Pin important announcements

#### 👤 User Profiles
- Extended user information
- Academic details and interests
- Activity statistics
- Reputation scoring

### Rate Limiting

API rate limit: 60 requests per minute per user (configurable)

### Support

For issues or questions, please contact the development team.

---
**Version:** {settings.APP_VERSION}
**Environment:** {environment_name}
"""

load_dotenv()


app = FastAPI(
    title=settings.APP_NAME,
    description=api_description,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
    contact={
        "name": "AURA Development Team",
        "email": "support@aura.edu",
    },
    license_info={
        "name": "MIT License",
    },
)


# ============================================================================
# CORS Middleware Configuration
# ============================================================================


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# ============================================================================
# API Router Registration
# ============================================================================


# Authentication routes
app.include_router(
    auth_router,
    prefix=settings.API_PREFIX,
    tags=["Authentication"]
)

# Chatbot routes
app.include_router(
    chatbot_router,
    prefix=f"{settings.API_PREFIX}/ai/chatbot",
    tags=["Chatbot"]
)

# Course routes
app.include_router(
    course_router,
    prefix=f"{settings.API_PREFIX}/courses",
    tags=["Courses"]
)


# ============================================================================
# Root and Health Check Endpoints
# ============================================================================


@app.get(
    "/",
    include_in_schema=False,
    summary="Root endpoint"
)
async def root():
    """Redirect to API documentation."""
    return RedirectResponse(url="/docs")


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check endpoint",
    description="Check if the API is running and database is accessible."
)
async def health_check():
    """
    Health check endpoint.

    Returns API status and basic system information.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production",
        "database": "connected"
    }


@app.get(
    "/api",
    tags=["Info"],
    summary="API information",
    description="Get API version and available endpoints."
)
async def api_info():
    """
    API information endpoint.

    Returns API metadata and available route groups.
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Academic Unified Response Assistant API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json",
        "endpoints": {
            "authentication": f"{settings.API_PREFIX}/auth",
            "health": "/health",
            "documentation": "/docs"
        }
    }


# ============================================================================
# Application Entry Point (for development)
# ============================================================================


if __name__ == "__main__":
    import uvicorn

    env_display = "Development" if settings.DEBUG else "Production"
    print(f"""
    ================================================================

       AURA - Academic Unified Response Assistant

       Version: {settings.APP_VERSION:<50}
       Environment: {env_display:<44}

       API Documentation: http://localhost:8000/docs
       ReDoc: http://localhost:8000/redoc
       Health Check: http://localhost:8000/health

    ================================================================
    """)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )