# AURA - Academic Unified Response Assistant

## Complete Project Documentation

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Team](#project-team)
3. [Technology Stack](#technology-stack)
4. [Architecture](#architecture)
5. [Setup Instructions](#setup-instructions)
6. [Environment Configuration](#environment-configuration)
7. [Authentication System](#authentication-system)
8. [API Endpoints](#api-endpoints)
9. [Chatbot Integration](#chatbot-integration)
10. [Testing](#testing)
11. [Contributing Guide](#contributing-guide)
12. [Deployment](#deployment)
13. [Troubleshooting](#troubleshooting)

---

## Project Overview

**AURA** (Academic Unified Response Assistant) is a comprehensive educational platform designed to facilitate communication and resource sharing between students, teaching assistants, and instructors.

### Key Features

- **Multi-role authentication** (Students, TAs, Instructors, Admins)
- **JWT-based security** with access and refresh tokens
- **Query/Doubt management** system for student questions
- **Resource sharing** and management (videos, PDFs, links)
- **AI-powered chatbot** using LangChain and Google Gemini
- **Real-time streaming** chatbot responses
- **Announcements** and notifications
- **User profiles** with statistics and reputation

---

## Project Team

- Aryan Kumar
- Aziz Ahmed
- Imran Ashraf
- Laxmi Kumari
- Mohit Raj Rathor
- Nooha Rahman C.P
- Taniya Chouhan
- Vikas Rathore

---

## Technology Stack

### Backend
- **FastAPI** - Modern, high-performance web framework
- **PostgreSQL + pgvector** - Primary database with vector support
- **Pinecone** - Vector database for embeddings
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **Pydantic** - Data validation and serialization
- **JWT** - Token-based authentication
- **Argon2** - Secure password hashing
- **LangChain + LangGraph** - LLM application framework
- **Google Gemini APIs** - Large Language Model
- **Docker** - Containerization

### Frontend
- **Vue.js** - Progressive JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **Pinia** - State management (replaces Vuex)
- **Vitest + jsdom + test-utils** - Unit testing framework
- **Vue Router** - Client-side routing
- **Axios** - HTTP client

---

## Architecture

### Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── chatbot.py           # Chatbot endpoints
│   │   └── dependencies.py      # FastAPI dependencies
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   ├── db.py                # Database connection
│   │   └── security.py          # JWT and password utilities
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── query.py             # Query model
│   │   ├── resource.py          # Resource model
│   │   ├── announcement.py      # Announcement model
│   │   └── profile.py           # Profile model
│   ├── schemas/
│   │   ├── user_schema.py       # User validation schemas
│   │   └── chatbot_schema.py    # Chatbot schemas
│   └── services/
│       └── chatbot_service.py   # Chatbot business logic
├── .env                          # Environment variables
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── COMPLETE_DOCUMENTATION.md     # This file
```

### Database Schema

#### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `password` (Argon2 hashed)
- `role` (STUDENT, TA, INSTRUCTOR, ADMIN)
- `full_name`
- `is_active`

#### Relationships
- User → Profile (One-to-One)
- User → Queries (One-to-Many)
- User → Resources (One-to-Many)
- User → Announcements (One-to-Many)

---

## Setup Instructions

### Prerequisites

- **Python 3.11+**
- **Node.js 16+** and npm
- **Git**
- **Google Gemini API Key** (for chatbot)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (see [Environment Configuration](#environment-configuration))

5. **Run the server:**
   ```bash
   # Development mode (auto-reload)
   python main.py

   # Or using uvicorn directly
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Access application:**
   - Frontend: http://localhost:5173

---

## Environment Configuration

### Backend Configuration

Create a `.env` file in the `backend/` directory:

```bash
# Application Settings
APP_NAME=AURA
APP_VERSION=1.0.0
DEBUG=true

# Database Configuration
DATABASE_URL=sqlite:///./app.db
# For PostgreSQL: postgresql://user:password@localhost/aura

# JWT Security
SECRET_KEY=your-secret-key-here-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]

# Google Gemini AI Configuration
GOOGLE_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1024
```

### Getting Google Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and add it to `.env` file

### Frontend Configuration

The frontend automatically connects to the backend at `http://localhost:8000/api`. To change this, edit `frontend/src/api/axios.js`:

```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api',  // Change this URL
  // ...
});
```

---

## Authentication System

### JWT Token Flow

1. **Registration/Login** → Receive access token and refresh token
2. **API Requests** → Include access token in Authorization header
3. **Token Expiry** → Use refresh token to get new access token
4. **Token Refresh** → Old refresh token is invalidated, new tokens issued

### User Roles

| Role | Code | Capabilities |
|------|------|--------------|
| Student | `student` | Post queries, view resources, use chatbot |
| TA | `ta` | Respond to queries, manage resources, moderate |
| Instructor | `instructor` | Full course management, create announcements |
| Admin | `admin` | Full system access, user management |

### Security Features

- **Argon2 Password Hashing** - Industry-standard secure hashing (no 72-byte limit like bcrypt)
- **JWT Tokens** - Stateless authentication with expiration
- **Token Rotation** - Refresh tokens are single-use for security
- **Role-Based Access Control** - Fine-grained permissions
- **Password Validation** - Minimum 8 characters required

---

## API Endpoints

### Base URL: `http://localhost:8000/api`

### Authentication Endpoints

#### POST `/auth/signup`
Register a new user account.

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "role": "student"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "student@example.com",
    "full_name": "John Doe",
    "role": "student",
    "is_active": true
  }
}
```

#### POST `/auth/login`
Authenticate and receive JWT tokens.

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "student@example.com",
    "role": "student"
  }
}
```

#### POST `/auth/refresh`
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### GET `/auth/me`
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "student@example.com",
  "full_name": "John Doe",
  "role": "student",
  "is_active": true
}
```

### Chatbot Endpoints

#### POST `/chatbot/chat`
Send a message to the AI chatbot and receive a response.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "message": "Explain binary search algorithm",
  "mode": "academic",
  "conversation_id": "conv-abc123"
}
```

**Response (200):**
```json
{
  "response": "Binary search is an efficient algorithm for finding...",
  "conversation_id": "conv-abc123",
  "model": "gemini-1.5-flash",
  "timestamp": "2025-11-06T10:30:00Z"
}
```

**Chat Modes:**
- `academic` - Academic explanations with examples
- `doubt_clarification` - Step-by-step doubt clarification
- `study_help` - Study strategies and time management
- `general` - General helpful responses

#### POST `/chatbot/chat/stream`
Stream chatbot response in real-time using Server-Sent Events.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "message": "What is machine learning?",
  "mode": "academic",
  "conversation_id": "conv-abc123"
}
```

**Response (SSE Stream):**
```
data: Machine
data:  learning
data:  is
data:  a
data:  subset
...
data: [DONE]
```

#### DELETE `/chatbot/conversation/{conversation_id}`
Clear conversation history.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Conversation cleared successfully",
  "conversation_id": "conv-abc123"
}
```

#### GET `/chatbot/conversation/{conversation_id}/history`
Get conversation message history.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "conversation_id": "conv-abc123",
  "messages": [
    {
      "role": "human",
      "content": "What is binary search?"
    },
    {
      "role": "ai",
      "content": "Binary search is an algorithm..."
    }
  ],
  "total": 2
}
```

#### GET `/chatbot/status`
Check chatbot configuration status.

**Response (200):**
```json
{
  "configured": true,
  "model": "gemini-1.5-flash",
  "available_modes": ["academic", "doubt_clarification", "study_help", "general"],
  "message": "Chatbot ready"
}
```

---

## Chatbot Integration

### Architecture

The chatbot system uses:
- **LangChain** - Framework for building LLM applications
- **Google Gemini** - Large Language Model (gemini-1.5-flash)
- **Conversation Memory** - Maintains context across messages
- **Async/Streaming** - Real-time responses with Server-Sent Events

### Features

1. **Conversation Memory** - Maintains context throughout the conversation
2. **Multiple Chat Modes** - Different prompts for different use cases
3. **Streaming Responses** - See AI typing in real-time
4. **Conversation Management** - Clear history, retrieve past messages
5. **Error Handling** - Graceful fallback when AI unavailable

### Using the Chatbot in Frontend

```javascript
// Simple chat request
const response = await axios.post('/api/chatbot/chat', {
  message: 'Explain quicksort algorithm',
  mode: 'academic',
  conversation_id: 'conv-12345'  // Optional
}, {
  headers: { Authorization: `Bearer ${token}` }
});

console.log(response.data.response);

// Streaming chat request
const eventSource = new EventSource(
  'http://localhost:8000/api/chatbot/chat/stream',
  {
    headers: { Authorization: `Bearer ${token}` }
  }
);

eventSource.onmessage = (event) => {
  if (event.data === '[DONE]') {
    eventSource.close();
  } else {
    console.log(event.data);  // Display chunk
  }
};
```

### Chatbot Service Implementation

The chatbot service (`app/services/chatbot_service.py`) provides:

```python
class ChatbotService:
    async def chat(message, conversation_id, mode) -> tuple[str, str]:
        """Generate chatbot response"""

    async def chat_stream(message, conversation_id, mode) -> AsyncIterator[str]:
        """Stream chatbot response"""

    def clear_conversation(conversation_id) -> bool:
        """Clear conversation history"""

    def get_conversation_history(conversation_id) -> list:
        """Get conversation messages"""
```

---

## Testing

### Manual API Testing

#### Test Authentication

```bash
# 1. Register a new user
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User",
    "role": "student"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Save the access_token from response

# 3. Get current user profile
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Test Chatbot

```bash
# 1. Simple chat request
curl -X POST http://localhost:8000/api/chatbot/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python?",
    "mode": "academic"
  }'

# 2. Check chatbot status
curl -X GET http://localhost:8000/api/chatbot/status

# 3. Get conversation history
curl -X GET http://localhost:8000/api/chatbot/conversation/conv-abc123/history \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Automated Testing Scripts

Run the provided test scripts:

```bash
# Windows
test_chatbot.bat

# Linux/macOS
bash test_chatbot.sh
```

### Frontend Testing

1. **Start both servers:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   .venv\Scripts\activate
   python main.py

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Test user flows:**
   - Registration (http://localhost:5173/signup)
   - Login (http://localhost:5173/login)
   - Dashboard access
   - Chatbot interaction

---

## Contributing Guide

### Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
3. **Add the main repo as a remote**:
   ```bash
   git remote add upstream https://github.com/<org-or-owner>/<repo-name>.git
   ```

### Creating a New Branch

Always create a separate branch for your work:

```bash
git checkout -b feature/add-new-endpoint
```

#### Branch Naming Convention

| Type              | Prefix     | Example                   |
| ----------------- | ---------- | ------------------------- |
| New feature       | `feature/` | `feature/add-auth-api`    |
| Bug fix           | `fix/`     | `fix/vue-login-redirect`  |
| Chore or refactor | `chore/`   | `chore/update-deps`       |
| Test-related      | `test/`    | `test/api-user-endpoints` |

> ⚠️ Never work directly on the `main` or `develop` branch.

### Making Code Changes

* Write **clear, small commits** for each logical change.
* Follow consistent code style:
  * **Backend:** use `black` and `isort`
  * **Frontend:** follow ESLint + Prettier conventions
* Run linters before committing:
  ```bash
  # Backend
  black app tests && isort app tests

  # Frontend
  npm run lint
  ```
* Commit with meaningful messages:
  ```bash
  git commit -m "feat(api): add JWT authentication to user login"
  ```

### Writing and Running Tests

#### Backend (FastAPI + pytest)

* Place tests inside the `tests/` directory.
* File naming: `test_<module>.py`
* Run backend tests:
  ```bash
  pytest --maxfail=1 --disable-warnings -q
  ```
* To test specific files:
  ```bash
  pytest tests/test_users.py
  ```

#### Frontend (Vue + Vitest)

* Place component tests in the same folder or under `src/tests/`.
* File naming: `<Component>.spec.ts` or `<Component>.spec.js`
* Run frontend tests:
  ```bash
  npm run test
  ```
* Run a specific test file:
  ```bash
  npx vitest run src/components/MyComponent.spec.ts
  ```

> ✅ All tests (both backend and frontend) **must pass before submitting a PR.**

### Keeping Your Branch Updated (Rebasing)

Before opening a pull request, always **rebase** to stay in sync with `main`:

```bash
git fetch upstream
git rebase upstream/main
```

If you hit merge conflicts:

```bash
git status   # see conflicted files
# fix conflicts manually
git add .
git rebase --continue
```

Then force-push your rebased branch:

```bash
git push origin feature/your-branch-name --force
```

> 💡 Rebase keeps the Git history clean and linear — **avoid merging main into your branch** unless necessary.

### Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-branch-name
   ```
2. On GitHub, open a **Pull Request**:
   * **Base branch:** `main` (or `develop`, if used)
   * **Compare branch:** your feature branch
3. Fill in:
   * A descriptive **title**
   * A short **summary** of your changes
   * Reference any related issues (e.g., `Closes #42`)
   * Mention reviewers or tag teammates

### After Merge: Cleaning Up

Once your PR is merged:

```bash
# Delete local branch
git branch -d feature/your-branch-name

# Delete remote branch
git push origin --delete feature/your-branch-name

# Update local main
git checkout main
git pull upstream main
```

### Quick Reference

| Action               | Command                                          | Notes             |
| -------------------- | ------------------------------------------------ | ----------------- |
| Create branch        | `git checkout -b feature/xyz`                    | Start new work    |
| Sync with main       | `git fetch upstream && git rebase upstream/main` | Stay updated      |
| Run backend tests    | `pytest`                                         | FastAPI backend   |
| Run frontend tests   | `npm run test`                                   | Vue frontend      |
| Push branch          | `git push origin feature/xyz`                    | Push to your fork |
| Delete merged branch | `git branch -d feature/xyz`                      | After merge       |

### Tips for Safe Contributions

* Always run **both back-end and front-end tests** before opening a PR.
* Keep PRs focused — one feature or fix per PR.
* Avoid large formatting-only changes.
* Communicate early if your work might overlap with someone else's.
* Keep a clean commit history — use **rebase** and **squash** when needed.

---

## Deployment

### Backend Deployment

#### Using Uvicorn (Production)

```bash
# Install production server
pip install uvicorn[standard] gunicorn

# Run with Gunicorn + Uvicorn workers
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

#### Environment Variables

Set these in production:

```bash
DEBUG=false
DATABASE_URL=postgresql://user:password@db-host/aura
SECRET_KEY=generate-a-secure-random-key-here
GOOGLE_API_KEY=your-production-gemini-key
CORS_ORIGINS=["https://yourdomain.com"]
```

#### Database Migration

```bash
# Initialize Alembic (one-time)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Frontend Deployment

#### Build for Production

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized static files.

#### Deploy to Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db/aura
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=aura
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'app'

**Solution:** Ensure you're running from the `backend/` directory and virtual environment is activated.

```bash
cd backend
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
python main.py
```

#### 2. NameError: name 'ConversationBufferMemory' is not defined

**Error:** Occurs when starting the server with uvicorn.

**Solution:** This has been fixed in the codebase. The chatbot service now uses `TYPE_CHECKING` and `Any` type hints to avoid import errors at class definition time. If you still encounter this:

1. Ensure you have the latest code
2. Restart the server:
   ```bash
   uvicorn main:app --reload
   ```

#### 3. CORS Errors in Frontend

**Solution:** Ensure backend `.env` has correct CORS origins:

```bash
CORS_ORIGINS=["http://localhost:5173"]
```

#### 4. Chatbot Not Working

**Check:**
- GOOGLE_API_KEY is set in `.env`
- LangChain dependencies are installed:
  ```bash
  pip install langchain langchain-google-genai google-generativeai langchain-community
  ```
- Check chatbot status endpoint: `/api/chatbot/status`

**Common Chatbot Errors:**

**Error:** `⚠️ Chatbot not configured`
- **Cause:** Missing GOOGLE_API_KEY in `.env` or LangChain not installed
- **Solution:** Add GOOGLE_API_KEY to `.env` and install dependencies

**Error:** `ImportError: cannot import name 'ChatGoogleGenerativeAI'`
- **Cause:** LangChain packages not installed
- **Solution:** Run `pip install langchain langchain-google-genai google-generativeai langchain-community`

#### 5. Database Errors

**Solution:** Delete and recreate database:

```bash
rm app.db
python main.py  # Will recreate tables
```

#### 6. JWT Token Errors

**Check:**
- SECRET_KEY is set in `.env` (minimum 32 characters)
- Token is sent in Authorization header: `Bearer <token>`
- Token hasn't expired (60 minutes for access tokens)

#### 7. Python Cache Issues

**Solution:** Clear Python cache files:

```bash
# Windows
rd /s /q __pycache__
rd /s /q app\__pycache__
rd /s /q app\api\__pycache__
rd /s /q app\core\__pycache__
rd /s /q app\models\__pycache__
rd /s /q app\schemas\__pycache__
rd /s /q app\services\__pycache__

# Linux/macOS
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

#### 8. Port Already in Use

**Error:** `Address already in use: 0.0.0.0:8000`

**Solution:** Kill the process using port 8000:

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

---

## API Rate Limiting

Default: 60 requests per minute per user (configurable in `settings.py`)

---

## Support

### Getting Help

- Check documentation: This file
- API documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Reporting Issues

Create an issue on GitHub with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

---

## License

MIT License - See LICENSE file for details

---

## Changelog

### Version 1.0.0 (Current)

**Features:**
- ✅ JWT authentication with access and refresh tokens
- ✅ Role-based access control (Student, TA, Instructor, Admin)
- ✅ User profile management
- ✅ AI chatbot integration with LangChain and Google Gemini
- ✅ Real-time streaming chatbot responses with Server-Sent Events
- ✅ Conversation memory and history management
- ✅ Multiple chat modes (Academic, Doubt Clarification, Study Help, General)
- ✅ Complete API documentation (Swagger UI + ReDoc)
- ✅ Frontend-backend integration with Axios
- ✅ Secure password hashing with Argon2
- ✅ Async/await support for improved performance
- ✅ CORS middleware for cross-origin requests

**Bug Fixes:**
- 🐛 Fixed `NameError: name 'ConversationBufferMemory' is not defined` using TYPE_CHECKING pattern
- 🐛 Fixed module import errors with proper package structure
- 🐛 Removed all Python cache files and added to .gitignore
- 🐛 Consolidated documentation into single comprehensive file

**Technical Improvements:**
- 🔧 Improved error handling in chatbot service with graceful fallbacks
- 🔧 Added comprehensive .gitignore for Python, Node.js, and project-specific files
- 🔧 Cleaned up project structure (removed backup files, test databases)
- 🔧 Created automated test scripts for Windows and Linux/macOS
- 🔧 Enhanced type hints while maintaining compatibility

**Documentation:**
- 📚 Complete setup and configuration guide
- 📚 API endpoint reference with examples
- 📚 Chatbot integration guide
- 📚 Contributing guidelines with Git workflow
- 📚 Deployment guide (Production, Docker, Nginx)
- 📚 Troubleshooting section with common issues and solutions

---

## Project Files

### Root Directory
```
soft-engg-project-sep-2025-se-SEP-12/
├── README.md                        # Quick start guide
├── .gitignore                       # Ignore patterns
├── test_chatbot.sh                  # Linux/macOS test script
├── test_chatbot.bat                 # Windows test script
├── backend/                         # Backend API
└── frontend/                        # Frontend UI
```

### Backend Structure
```
backend/
├── app/
│   ├── api/                         # API endpoints
│   │   ├── auth.py                  # Authentication (signup, login, refresh)
│   │   ├── chatbot.py               # Chatbot (chat, stream, history)
│   │   └── dependencies.py          # FastAPI dependencies
│   ├── core/                        # Core functionality
│   │   ├── config.py                # Settings and environment config
│   │   ├── db.py                    # Database connection
│   │   └── security.py              # JWT and password utilities
│   ├── models/                      # SQLAlchemy models
│   │   ├── user.py                  # User model with roles
│   │   ├── query.py                 # Query/doubt model
│   │   ├── resource.py              # Resource model
│   │   ├── announcement.py          # Announcement model
│   │   └── profile.py               # User profile model
│   ├── schemas/                     # Pydantic schemas
│   │   ├── user_schema.py           # User validation schemas
│   │   └── chatbot_schema.py        # Chatbot request/response schemas
│   └── services/                    # Business logic
│       └── chatbot_service.py       # Chatbot service with LangChain
├── .env                             # Environment variables (create this)
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies
├── app.db                           # SQLite database (auto-created)
└── COMPLETE_DOCUMENTATION.md        # This file
```

### Frontend Structure
```
frontend/
├── src/
│   ├── api/                         # API client
│   │   ├── axios.js                 # HTTP client with interceptors
│   │   └── auth.js                  # Auth API calls
│   ├── components/                  # Vue components
│   │   ├── Admin/                   # Admin dashboard components
│   │   ├── student/                 # Student components
│   │   ├── instructor/              # Instructor components
│   │   └── TA/                      # TA components
│   ├── router/                      # Vue Router
│   │   ├── index.js                 # Main router
│   │   ├── adminRoutes.js           # Admin routes
│   │   └── studentRoutes.js         # Student routes
│   ├── stores/                      # Pinia stores
│   │   └── user.js                  # User state management
│   └── views/                       # Page components
├── package.json                     # Node dependencies
└── README.md                        # Frontend-specific guide
```

---

## Quick Reference

### Backend Commands
```bash
# Setup
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Run server
python main.py
# OR
uvicorn main:app --reload

# Access docs
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

### Frontend Commands
```bash
# Setup
cd frontend
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Run tests
npm run test
```

### Test Chatbot
```bash
# Windows
test_chatbot.bat

# Linux/macOS
bash test_chatbot.sh
```

### Environment Variables (.env)
```bash
# Required
SECRET_KEY=your-secret-key-minimum-32-characters
GOOGLE_API_KEY=your-gemini-api-key

# Optional (defaults shown)
APP_NAME=AURA
DEBUG=true
DATABASE_URL=sqlite:///./app.db
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1024
```

---

**Last Updated:** November 6, 2025
**Version:** 1.0.0
**Maintained by:** AURA Development Team

**Contributors:**
- Aryan Kumar
- Aziz Ahmed
- Imran Ashraf
- Laxmi Kumari
- Mohit Raj Rathor
- Nooha Rahman C.P
- Taniya Chouhan
- Vikas Rathore
