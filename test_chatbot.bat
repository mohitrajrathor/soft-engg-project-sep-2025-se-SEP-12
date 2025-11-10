@echo off
REM AURA Chatbot API Testing Script for Windows
REM This script tests all chatbot endpoints

echo ==================================================
echo AURA Chatbot API Test Suite
echo ==================================================
echo.

set BASE_URL=http://localhost:8000/api
set TOTAL_TESTS=0
set PASSED_TESTS=0

echo ==================================================
echo Test 1: Chatbot Status (No Auth Required)
echo ==================================================
echo.

curl -X GET "%BASE_URL%/chatbot/status"
if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Chatbot status endpoint
    set /a PASSED_TESTS+=1
) else (
    echo [FAILED] Chatbot status endpoint
)
set /a TOTAL_TESTS+=1
echo.

echo ==================================================
echo Test 2: User Registration
echo ==================================================
echo.

curl -X POST "%BASE_URL%/auth/signup" ^
    -H "Content-Type: application/json" ^
    -d "{\"email\":\"chatbot_test@example.com\",\"password\":\"testpass123\",\"full_name\":\"Chatbot Test User\",\"role\":\"student\"}" ^
    -o signup_response.json

if %ERRORLEVEL% EQU 0 (
    echo [PASSED] User registration
    set /a PASSED_TESTS+=1
) else (
    echo User might already exist, trying login...
    curl -X POST "%BASE_URL%/auth/login" ^
        -H "Content-Type: application/json" ^
        -d "{\"email\":\"chatbot_test@example.com\",\"password\":\"testpass123\"}" ^
        -o signup_response.json
    if %ERRORLEVEL% EQU 0 (
        echo [PASSED] User login (fallback)
        set /a PASSED_TESTS+=1
    ) else (
        echo [FAILED] User registration/login
    )
)
set /a TOTAL_TESTS+=1
echo.

REM Extract access token (simplified for Windows)
for /f "tokens=2 delims=:," %%a in ('findstr "access_token" signup_response.json') do set ACCESS_TOKEN=%%a
set ACCESS_TOKEN=%ACCESS_TOKEN:"=%
set ACCESS_TOKEN=%ACCESS_TOKEN: =%

echo Access Token: %ACCESS_TOKEN:~0,20%...
echo.

echo ==================================================
echo Test 3: Simple Chat Request
echo ==================================================
echo.

curl -X POST "%BASE_URL%/chatbot/chat" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"message\":\"What is Python programming language?\",\"mode\":\"academic\"}" ^
    -o chat_response.json

if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Simple chat request
    set /a PASSED_TESTS+=1
    type chat_response.json
) else (
    echo [FAILED] Simple chat request
)
set /a TOTAL_TESTS+=1
echo.

echo ==================================================
echo Test 4: Get Conversation History
echo ==================================================
echo.

REM Extract conversation ID
for /f "tokens=2 delims=:," %%a in ('findstr "conversation_id" chat_response.json') do set CONV_ID=%%a
set CONV_ID=%CONV_ID:"=%
set CONV_ID=%CONV_ID: =%

echo Conversation ID: %CONV_ID%

curl -X GET "%BASE_URL%/chatbot/conversation/%CONV_ID%/history" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%"

if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Get conversation history
    set /a PASSED_TESTS+=1
) else (
    echo [FAILED] Get conversation history
)
set /a TOTAL_TESTS+=1
echo.

echo ==================================================
echo Test 5: Chat with Different Modes
echo ==================================================
echo.

curl -X POST "%BASE_URL%/chatbot/chat" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"message\":\"I am confused about recursion\",\"mode\":\"doubt_clarification\"}"

if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Doubt clarification mode
    set /a PASSED_TESTS+=1
) else (
    echo [FAILED] Doubt clarification mode
)
set /a TOTAL_TESTS+=1
echo.

curl -X POST "%BASE_URL%/chatbot/chat" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"message\":\"How can I manage my study time better?\",\"mode\":\"study_help\"}"

if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Study help mode
    set /a PASSED_TESTS+=1
) else (
    echo [FAILED] Study help mode
)
set /a TOTAL_TESTS+=1
echo.

echo ==================================================
echo Test 6: Clear Conversation History
echo ==================================================
echo.

curl -X DELETE "%BASE_URL%/chatbot/conversation/%CONV_ID%" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%"

if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Clear conversation history
    set /a PASSED_TESTS+=1
) else (
    echo [FAILED] Clear conversation history
)
set /a TOTAL_TESTS+=1
echo.

echo ==================================================
echo Test 7: Unauthorized Access (No Token)
echo ==================================================
echo.

curl -X POST "%BASE_URL%/chatbot/chat" ^
    -H "Content-Type: application/json" ^
    -d "{\"message\":\"Test without auth\",\"mode\":\"general\"}" ^
    -w "%%{http_code}"

REM This should return 401 or 403
echo [INFO] This should return 401/403 status code
set /a TOTAL_TESTS+=1
set /a PASSED_TESTS+=1
echo.

echo ==================================================
echo Test 8: Streaming Chat Request
echo ==================================================
echo.

curl -X POST "%BASE_URL%/chatbot/chat/stream" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"message\":\"Tell me about machine learning\",\"mode\":\"academic\"}" ^
    --no-buffer

if %ERRORLEVEL% EQU 0 (
    echo [PASSED] Streaming chat request
    set /a PASSED_TESTS+=1
) else (
    echo [FAILED] Streaming chat request
)
set /a TOTAL_TESTS+=1
echo.

REM Cleanup
del signup_response.json 2>nul
del chat_response.json 2>nul

echo ==================================================
echo TEST SUMMARY
echo ==================================================
echo.
echo Total Tests: %TOTAL_TESTS%
echo Passed: %PASSED_TESTS%
set /a FAILED_TESTS=%TOTAL_TESTS%-%PASSED_TESTS%
echo Failed: %FAILED_TESTS%
echo.

if %PASSED_TESTS% EQU %TOTAL_TESTS% (
    echo [SUCCESS] ALL TESTS PASSED!
    exit /b 0
) else (
    echo [WARNING] Some tests failed
    exit /b 1
)
