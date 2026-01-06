# AURA API Test Suite

Comprehensive test suite for the AURA (Academic Unified Response Assistant) API.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)

## Overview

This test suite provides comprehensive coverage for:

- **Authentication API** - User registration, login, token management
- **Chatbot API** - Chat endpoints, streaming, conversation management
- **Health & Info APIs** - System status and documentation endpoints
- **Chatbot Service** - Unit tests for chatbot service logic

## Test Structure

```
test/
├── __init__.py                 # Package initialization
├── conftest.py                 # Shared fixtures and configuration
├── pytest.ini                  # Pytest configuration
├── requirements-test.txt       # Test dependencies
├── README.md                   # This file
├── test_auth_api.py           # Authentication endpoint tests
├── test_chatbot_api.py        # Chatbot endpoint tests
├── test_health_api.py         # Health check and info tests
└── test_chatbot_service.py    # Chatbot service unit tests
```

## Installation

### 1. Install Test Dependencies

```bash
# From backend directory
cd backend

# Install test requirements
pip install -r test/requirements-test.txt

# Or install all requirements including test dependencies
pip install -r requirements.txt
```

### 2. Set Up Test Environment

Create a `.env` file in the backend directory if you don't have one:

```bash
# backend/.env
DATABASE_URL=sqlite:///./test_aura.db
SECRET_KEY=test-secret-key-for-testing-only
GOOGLE_API_KEY=your-google-api-key  # Optional, for chatbot tests
```

## Running Tests

### Run All Tests

```bash
# From backend directory
pytest test/

# Or with verbose output
pytest test/ -v

# Or with detailed output
pytest test/ -vv
```

### Run Specific Test Files

```bash
# Run only authentication tests
pytest test/test_auth_api.py

# Run only chatbot tests
pytest test/test_chatbot_api.py

# Run only service unit tests
pytest test/test_chatbot_service.py
```

### Run Specific Test Classes or Methods

```bash
# Run specific test class
pytest test/test_auth_api.py::TestSignup

# Run specific test method
pytest test/test_auth_api.py::TestSignup::test_signup_success
```

### Run Tests by Markers

```bash
# Run only API tests
pytest test/ -m api

# Run only unit tests
pytest test/ -m unit

# Run only chatbot tests
pytest test/ -m chatbot

# Run only authentication tests
pytest test/ -m auth

# Run integration tests
pytest test/ -m integration
```

### Run Tests in Parallel

```bash
# Run tests using 4 CPU cores
pytest test/ -n 4

# Run tests using all available CPU cores
pytest test/ -n auto
```

### Run Tests with Coverage

```bash
# Run tests with coverage report
pytest test/ --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser

# Run with terminal coverage report
pytest test/ --cov=app --cov-report=term-missing
```

## Test Coverage

### Current Test Coverage

#### Authentication API (`test_auth_api.py`)
- ✅ User registration (signup)
  - Successful registration
  - Duplicate email handling
  - Invalid email format
  - Weak password validation
  - Different user roles
  - Missing required fields

- ✅ User login
  - Successful login
  - Invalid credentials
  - Inactive account handling
  - Missing credentials

- ✅ Token refresh
  - Successful token refresh
  - Invalid token handling
  - Missing token

- ✅ Get current user profile
  - Authenticated access
  - Unauthorized access
  - Invalid token

- ✅ Update user profile
  - Update full name
  - Update email
  - Email conflict handling
  - Password change
  - Wrong current password
  - Multiple field updates

- ✅ Role-based access control
  - Student access
  - TA access
  - Instructor access
  - Admin access

#### Chatbot API (`test_chatbot_api.py`)
- ✅ Chatbot status
  - Get status endpoint
  - Feature display
  - Available modes

- ✅ Chat functionality
  - Authentication requirement
  - Successful chat
  - Different chat modes
  - Conversation continuity
  - Invalid mode handling
  - Empty message validation
  - Long message handling

- ✅ Streaming chat
  - Authentication requirement
  - Successful streaming
  - Conversation ID handling

- ✅ Conversation management
  - Clear conversation
  - Get conversation history
  - History structure
  - Nonexistent conversation handling

- ✅ Conversation state
  - Get session state
  - Nonexistent conversation

- ✅ Metrics and observability
  - Get metrics
  - Metrics structure

- ✅ Integration tests
  - Full conversation flow
  - Multiple concurrent conversations
  - User isolation

#### Health & Info API (`test_health_api.py`)
- ✅ Root endpoint
  - Redirect to documentation

- ✅ Health check
  - Successful health check
  - Response structure
  - No authentication required

- ✅ API information
  - API info endpoint
  - Documentation URLs
  - Endpoint listing

- ✅ Documentation endpoints
  - Swagger UI
  - ReDoc
  - OpenAPI JSON

- ✅ CORS
  - CORS headers
  - Preflight requests

- ✅ Error handling
  - 404 responses
  - 405 responses
  - Error format

#### Chatbot Service (`test_chatbot_service.py`)
- ✅ Service initialization
  - Default implementation
  - Native SDK implementation
  - LangChain implementation
  - ADK features

- ✅ Implementation switching
  - Switch to LangChain
  - Switch to Native SDK
  - Conversation preservation

- ✅ Chat functionality
  - Conversation ID generation
  - Provided conversation ID
  - Different chat modes

- ✅ Streaming chat
  - Async iterator
  - Chunk yielding

- ✅ Conversation management
  - Clear conversation
  - Get history
  - Empty conversations

- ✅ Session state
  - Get session state
  - Without session service

- ✅ Metrics and observability
  - Get metrics
  - Without observability

- ✅ Error handling
  - Exception handling
  - Empty messages

- ✅ Chat modes
  - Academic mode
  - Doubt clarification mode
  - Study help mode
  - General mode

- ✅ Integration tests
  - Multiple conversations
  - Conversation isolation

## Writing Tests

### Test File Structure

```python
"""
Brief description of what this test file covers.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.api  # Mark with appropriate marker
@pytest.mark.auth
class TestFeatureName:
    """Tests for specific feature."""

    def test_specific_behavior(self, client: TestClient):
        """Test description."""
        # Arrange
        # ... setup

        # Act
        response = client.get("/endpoint")

        # Assert
        assert response.status_code == 200
```

### Using Fixtures

```python
def test_with_authenticated_user(client: TestClient, auth_headers):
    """Test that uses authenticated user fixture."""
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
```

### Available Fixtures

See `conftest.py` for all available fixtures:

- `client` - Test client
- `db_session` - Database session
- `create_test_user` - Factory to create users
- `authenticated_user` - Pre-created student user
- `authenticated_ta` - Pre-created TA user
- `authenticated_instructor` - Pre-created instructor user
- `authenticated_admin` - Pre-created admin user
- `auth_headers` - Auth headers for student
- `ta_auth_headers` - Auth headers for TA
- `instructor_auth_headers` - Auth headers for instructor
- `admin_auth_headers` - Auth headers for admin
- `sample_chat_request` - Sample chatbot request
- `invalid_token` - Invalid JWT token
- `expired_token` - Expired JWT token

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit        # Unit tests
@pytest.mark.integration # Integration tests
@pytest.mark.api         # API endpoint tests
@pytest.mark.auth        # Authentication tests
@pytest.mark.chatbot     # Chatbot tests
@pytest.mark.slow        # Slow running tests
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install -r test/requirements-test.txt

    - name: Run tests
      run: |
        cd backend
        pytest test/ --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on other tests
2. **Use Fixtures**: Leverage pytest fixtures for setup and teardown
3. **Clear Names**: Test names should clearly describe what they test
4. **AAA Pattern**: Arrange, Act, Assert - structure tests clearly
5. **Mock External Services**: Use mocks for external API calls
6. **Test Edge Cases**: Include tests for error conditions and edge cases
7. **Keep Tests Fast**: Unit tests should run quickly; mark slow tests appropriately
8. **Document Complex Tests**: Add comments for complex test logic
9. **Test Coverage**: Aim for >80% code coverage
10. **Regular Maintenance**: Keep tests updated with code changes

## Troubleshooting

### Database Errors

If you get database errors:
```bash
# Delete test database and let it recreate
rm backend/test.db
pytest test/
```

### Import Errors

If you get import errors:
```bash
# Make sure you're in the backend directory
cd backend
pytest test/
```

### Environment Variables

If tests fail due to missing environment variables:
```bash
# Create or update .env file
echo "GOOGLE_API_KEY=your-key-here" >> .env
```

## Running Specific Test Suites

### Quick Test (Fast Unit Tests Only)

```bash
pytest test/ -m "unit and not slow"
```

### Full Test Suite (All Tests)

```bash
pytest test/ --cov=app --cov-report=html
```

### Authentication Tests Only

```bash
pytest test/test_auth_api.py -v
```

### Chatbot Tests Only

```bash
pytest test/test_chatbot_api.py test/test_chatbot_service.py -v
```

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Check code coverage
4. Update this README if needed

## Support

For issues or questions about tests:
- Check test logs for specific error messages
- Review fixtures in `conftest.py`
- Check pytest configuration in `pytest.ini`
- Consult pytest documentation: https://docs.pytest.org/
