#!/bin/bash

# AURA Chatbot API Testing Script
# This script tests all chatbot endpoints

echo "=================================================="
echo "AURA Chatbot API Test Suite"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000/api"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0

# Function to print test result
print_result() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $2"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAILED${NC}: $2"
    fi
    echo ""
}

echo "=================================================="
echo "Test 1: Chatbot Status (No Auth Required)"
echo "=================================================="
echo ""

STATUS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/chatbot/status")
STATUS_CODE=$(echo "$STATUS_RESPONSE" | tail -n 1)
STATUS_BODY=$(echo "$STATUS_RESPONSE" | sed '$d')

echo "Response: $STATUS_BODY"
echo "Status Code: $STATUS_CODE"

if [ "$STATUS_CODE" = "200" ]; then
    print_result 0 "Chatbot status endpoint"
else
    print_result 1 "Chatbot status endpoint"
fi

echo "=================================================="
echo "Test 2: User Registration"
echo "=================================================="
echo ""

SIGNUP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/signup" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "chatbot_test@example.com",
        "password": "testpass123",
        "full_name": "Chatbot Test User",
        "role": "student"
    }')

SIGNUP_CODE=$(echo "$SIGNUP_RESPONSE" | tail -n 1)
SIGNUP_BODY=$(echo "$SIGNUP_RESPONSE" | sed '$d')

echo "Status Code: $SIGNUP_CODE"

if [ "$SIGNUP_CODE" = "201" ] || [ "$SIGNUP_CODE" = "200" ]; then
    print_result 0 "User registration"
    ACCESS_TOKEN=$(echo "$SIGNUP_BODY" | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')
else
    # If user already exists, try to login
    echo "User might already exist, trying login..."

    LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d '{
            "email": "chatbot_test@example.com",
            "password": "testpass123"
        }')

    LOGIN_CODE=$(echo "$LOGIN_RESPONSE" | tail -n 1)
    LOGIN_BODY=$(echo "$LOGIN_RESPONSE" | sed '$d')

    if [ "$LOGIN_CODE" = "200" ]; then
        print_result 0 "User login (fallback)"
        ACCESS_TOKEN=$(echo "$LOGIN_BODY" | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')
    else
        print_result 1 "User registration/login"
        echo "Cannot proceed without authentication token"
        exit 1
    fi
fi

echo "Access Token: ${ACCESS_TOKEN:0:20}..."
echo ""

echo "=================================================="
echo "Test 3: Simple Chat Request"
echo "=================================================="
echo ""

CHAT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/chatbot/chat" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "What is Python programming language?",
        "mode": "academic"
    }')

CHAT_CODE=$(echo "$CHAT_RESPONSE" | tail -n 1)
CHAT_BODY=$(echo "$CHAT_RESPONSE" | sed '$d')

echo "Status Code: $CHAT_CODE"
echo "Response (first 200 chars): ${CHAT_BODY:0:200}..."

if [ "$CHAT_CODE" = "200" ]; then
    print_result 0 "Simple chat request"
    # Extract conversation ID for next tests
    CONV_ID=$(echo "$CHAT_BODY" | grep -o '"conversation_id":"[^"]*' | sed 's/"conversation_id":"//')
    echo "Conversation ID: $CONV_ID"
else
    print_result 1 "Simple chat request"
    CONV_ID="test-conv-123"  # Fallback
fi
echo ""

echo "=================================================="
echo "Test 4: Chat with Conversation ID (Context)"
echo "=================================================="
echo ""

CHAT2_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/chatbot/chat" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"message\": \"Can you give me a simple example?\",
        \"mode\": \"academic\",
        \"conversation_id\": \"$CONV_ID\"
    }")

CHAT2_CODE=$(echo "$CHAT2_RESPONSE" | tail -n 1)
CHAT2_BODY=$(echo "$CHAT2_RESPONSE" | sed '$d')

echo "Status Code: $CHAT2_CODE"
echo "Response (first 200 chars): ${CHAT2_BODY:0:200}..."

if [ "$CHAT2_CODE" = "200" ]; then
    print_result 0 "Chat with conversation context"
else
    print_result 1 "Chat with conversation context"
fi

echo "=================================================="
echo "Test 5: Get Conversation History"
echo "=================================================="
echo ""

HISTORY_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/chatbot/conversation/$CONV_ID/history" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

HISTORY_CODE=$(echo "$HISTORY_RESPONSE" | tail -n 1)
HISTORY_BODY=$(echo "$HISTORY_RESPONSE" | sed '$d')

echo "Status Code: $HISTORY_CODE"
echo "Response (first 300 chars): ${HISTORY_BODY:0:300}..."

if [ "$HISTORY_CODE" = "200" ]; then
    print_result 0 "Get conversation history"
else
    print_result 1 "Get conversation history"
fi

echo "=================================================="
echo "Test 6: Chat with Different Modes"
echo "=================================================="
echo ""

# Test doubt_clarification mode
DOUBT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/chatbot/chat" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "I am confused about recursion",
        "mode": "doubt_clarification"
    }')

DOUBT_CODE=$(echo "$DOUBT_RESPONSE" | tail -n 1)
echo "Doubt Clarification Mode - Status Code: $DOUBT_CODE"

# Test study_help mode
STUDY_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/chatbot/chat" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "How can I manage my study time better?",
        "mode": "study_help"
    }')

STUDY_CODE=$(echo "$STUDY_RESPONSE" | tail -n 1)
echo "Study Help Mode - Status Code: $STUDY_CODE"

if [ "$DOUBT_CODE" = "200" ] && [ "$STUDY_CODE" = "200" ]; then
    print_result 0 "Different chat modes"
else
    print_result 1 "Different chat modes"
fi

echo "=================================================="
echo "Test 7: Clear Conversation History"
echo "=================================================="
echo ""

CLEAR_RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/chatbot/conversation/$CONV_ID" \
    -H "Authorization: Bearer $ACCESS_TOKEN")

CLEAR_CODE=$(echo "$CLEAR_RESPONSE" | tail -n 1)
CLEAR_BODY=$(echo "$CLEAR_RESPONSE" | sed '$d')

echo "Status Code: $CLEAR_CODE"
echo "Response: $CLEAR_BODY"

if [ "$CLEAR_CODE" = "200" ]; then
    print_result 0 "Clear conversation history"
else
    print_result 1 "Clear conversation history"
fi

echo "=================================================="
echo "Test 8: Unauthorized Access (No Token)"
echo "=================================================="
echo ""

UNAUTH_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/chatbot/chat" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "Test without auth",
        "mode": "general"
    }')

UNAUTH_CODE=$(echo "$UNAUTH_RESPONSE" | tail -n 1)
echo "Status Code: $UNAUTH_CODE"

if [ "$UNAUTH_CODE" = "401" ] || [ "$UNAUTH_CODE" = "403" ]; then
    print_result 0 "Unauthorized access protection"
else
    print_result 1 "Unauthorized access protection"
fi

echo "=================================================="
echo "Test 9: Invalid Chat Mode"
echo "=================================================="
echo ""

INVALID_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/chatbot/chat" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "Test message",
        "mode": "invalid_mode"
    }')

INVALID_CODE=$(echo "$INVALID_RESPONSE" | tail -n 1)
echo "Status Code: $INVALID_CODE"

if [ "$INVALID_CODE" = "422" ]; then
    print_result 0 "Invalid chat mode validation"
else
    print_result 1 "Invalid chat mode validation"
fi

echo "=================================================="
echo "Test 10: Empty Message Validation"
echo "=================================================="
echo ""

EMPTY_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/chatbot/chat" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "",
        "mode": "general"
    }')

EMPTY_CODE=$(echo "$EMPTY_RESPONSE" | tail -n 1)
echo "Status Code: $EMPTY_CODE"

if [ "$EMPTY_CODE" = "422" ]; then
    print_result 0 "Empty message validation"
else
    print_result 1 "Empty message validation"
fi

echo "=================================================="
echo "TEST SUMMARY"
echo "=================================================="
echo ""
echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $((TOTAL_TESTS - PASSED_TESTS))${NC}"
echo ""

if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some tests failed${NC}"
    exit 1
fi
