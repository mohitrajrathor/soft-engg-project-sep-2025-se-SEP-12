# Query Response Message Flow - Complete Trace

## Overview
When a user types a message in the BottomBar and sends it, here's the complete journey from frontend to backend and back.

---

## 1️⃣ FRONTEND: BottomBar Component
**File:** `frontend/src/components/layout/StudentLayout/BottomBar.vue`

### User Action
- User types message in textarea: `Message AURA...`
- User presses Enter or clicks Send button
- BottomBar validates: `if (!message.value.trim()) return`

### BottomBar Code (Lines 80-90)
```javascript
const sendMessage = () => {
  if (!message.value.trim()) return;  // ← Check if message is empty
  emit("send", { message: message.value, file: attachedFile.value })
  // Emits event with payload object
  message.value = ""  // ← Clear textarea
  attachedFile.value = null  // ← Clear file
  nextTick(() => autoResize())
}
```

### Event Emission
- **Event Name:** `"send"`
- **Payload:** 
  ```javascript
  {
    message: "User's typed text here",
    file: FileObject || null  // Optional file attachment
  }
  ```

---

## 2️⃣ FRONTEND: studentQueries.vue Component
**File:** `frontend/src/components/student/studentQueries.vue`

### BottomBar Listener (Line 503)
```vue
<BottomBar @send="handleBottomBarSend" />
```

### Handler Function (Lines 208-238)
```javascript
const handleBottomBarSend = async (payload) => {
  // Step 1: Check if query is selected
  if (!selectedQuery.value) {
    error.value = 'Please select a query first'
    setTimeout(() => { error.value = null }, 3000)
    return
  }

  // Step 2: Extract message and trim whitespace
  const messageContent = payload.message?.trim() || ''

  // Step 3: Validate message length (backend requires minimum 5 characters)
  if (messageContent.length < 5) {
    error.value = 'Message must be at least 5 characters long'
    setTimeout(() => { error.value = null }, 3000)
    return
  }

  // Step 4: Call API to add response
  try {
    await queriesAPI.addResponse(selectedQuery.value.id, {
      content: messageContent,
      is_solution: false
    })

    // Step 5: Reload query to show new response
    await selectQuery(selectedQuery.value.id)
    
    // Step 6: Refresh query list
    await loadQueries()

    error.value = null
  } catch (err) {
    console.error('Failed to send response:', err)
    error.value = err.response?.data?.detail || 'Failed to send response. Please try again.'
  }
}
```

### What Happens Here
1. ✅ Validates query is selected
2. ✅ Extracts and trims message text
3. ✅ Validates minimum 5 character requirement
4. ✅ Calls API with query ID and response data
5. ✅ Reloads the query to display new response immediately
6. ✅ Refreshes the query list to update response counts

---

## 3️⃣ FRONTEND: API Client Call
**File:** `frontend/src/api/queries.js` (Lines 60-70)

```javascript
async addResponse(queryId, data) {
  // Makes HTTP POST request to backend
  const response = await api.post(`/queries/${queryId}/response`, data)
  return response.data
}
```

### HTTP Request Details
- **Method:** `POST`
- **Endpoint:** `/api/queries/{query_id}/response`
- **Headers:** Automatically includes:
  - `Content-Type: application/json`
  - `Authorization: Bearer {jwt_token}` (from axios interceptor)
- **Request Body:**
  ```json
  {
    "content": "User's message (at least 5 chars)",
    "is_solution": false
  }
  ```

---

## 4️⃣ BACKEND: FastAPI Endpoint
**File:** `backend/app/api/queries.py` (Lines 290-350)

### Route Definition
```python
@router.post(
    "/{query_id}/response",
    summary="Add response to query",
    description="Add a response to a query. TAs/Instructors can mark responses as solutions.",
    status_code=http_status.HTTP_201_CREATED  # Returns 201 Created
)
async def add_query_response(
    query_id: int,
    response_data: QueryResponseCreate,
    current_user: User = Depends(get_current_user),  # ← JWT auth
    db: Session = Depends(get_db)  # ← Database session
)
```

### Request Validation
- **Pydantic Schema:** `QueryResponseCreate` (from `queries.py` lines 43-46)
  ```python
  class QueryResponseCreate(BaseModel):
      content: str = Field(..., min_length=5)  # ← Validates minimum 5 chars
      is_solution: Optional[bool] = False
  ```
- If validation fails → **422 Unprocessable Entity** error

### Step-by-Step Backend Processing

#### 1. Authentication
```python
current_user: User = Depends(get_current_user)
# ← Extracts JWT token from header and identifies user
```

#### 2. Query Lookup
```python
query = db.query(Query).filter(Query.id == query_id).first()
if not query:
    raise HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail=f"Query {query_id} not found"
    )
```

#### 3. Create QueryResponse Object
```python
new_response = QueryResponse(
    query_id=query_id,                    # ← Link to query
    user_id=current_user.id,              # ← Who sent response
    content=response_data.content,        # ← Message text
    is_solution=response_data.is_solution and current_user.role.value in ["ta", "instructor", "admin"]
    # ↑ Only TAs/Instructors/Admins can mark as solution
)
```

#### 4. Update Query Status
```python
# If first response, change status from OPEN → IN_PROGRESS
if query.status == QueryStatus.OPEN and not query.responses:
    query.status = QueryStatus.IN_PROGRESS

# If marked as solution, resolve the query
if new_response.is_solution:
    query.status = QueryStatus.RESOLVED
    query.resolved_at = datetime.utcnow()
```

#### 5. Save to Database
```python
db.add(new_response)      # ← Add response to session
db.commit()               # ← Persist to database
db.refresh(new_response)  # ← Get auto-generated ID and timestamps
```

#### 6. Database Operations
```
INSERT INTO query_responses (query_id, user_id, content, is_solution, created_at)
VALUES (1, 42, 'User message here', false, NOW())

UPDATE queries 
SET status = 'IN_PROGRESS', updated_at = NOW()
WHERE id = 1
```

#### 7. Return Success Response
```python
return {
    "message": "Response added successfully",
    "response": {
        "id": new_response.id,                          # ← Auto-generated ID
        "content": new_response.content,                # ← Echo back message
        "is_solution": new_response.is_solution,        # ← Solution status
        "created_at": new_response.created_at.isoformat()  # ← Timestamp
    }
}
```

### HTTP Response
- **Status Code:** `201 Created` ✅
- **Response Body:**
  ```json
  {
    "message": "Response added successfully",
    "response": {
      "id": 123,
      "content": "User's message here",
      "is_solution": false,
      "created_at": "2025-12-05T10:30:45.123456"
    }
  }
  ```

---

## 5️⃣ BACKEND: Database Operations
**Database:** SQLite (app.db)

### Tables Involved
1. **query_responses** - New row inserted
   ```sql
   INSERT INTO query_responses 
   (query_id, user_id, content, is_solution, created_at, updated_at)
   VALUES (1, 42, 'Response text', 0, NOW(), NOW())
   ```

2. **queries** - Updated status
   ```sql
   UPDATE queries 
   SET status = 'IN_PROGRESS', updated_at = NOW()
   WHERE id = 1
   ```

### Related Tables (via relationships)
- **users** - Linked via `user_id` to get responder details
- **query_responses** - Ordered by `created_at` for chronological display

---

## 6️⃣ FRONTEND: Response Reception
**File:** `frontend/src/components/student/studentQueries.vue`

### What Happens After API Call Succeeds

```javascript
// Step 1: API call succeeds with 201 response
await queriesAPI.addResponse(selectedQuery.value.id, {
  content: messageContent,
  is_solution: false
})

// Step 2: Reload the selected query with responses
await selectQuery(selectedQuery.value.id)
// ↑ Makes GET /api/queries/{id} request to fetch updated data

// Step 3: Refresh the query list
await loadQueries()
// ↑ Makes GET /api/queries/ request to update response counts

error.value = null  // ← Clear any error messages
```

### Reload Query Request
**File:** `frontend/src/api/queries.js` (Line 30)
```javascript
async getQuery(queryId) {
  const response = await api.get(`/queries/${queryId}`)
  return response.data
}
```

Backend now returns (with eager-loaded responses):
```json
{
  "id": 1,
  "title": "Query Title",
  "description": "Query description",
  "status": "IN_PROGRESS",  // ← Updated!
  "response_count": 1,
  "responses": [
    {
      "id": 123,
      "content": "User's message here",
      "is_solution": false,
      "user_id": 42,
      "user_name": "Student Name",
      "user_role": "student",
      "created_at": "2025-12-05T10:30:45.123456"
    }
  ]
  // ... other fields
}
```

---

## 7️⃣ FRONTEND: UI Update
**File:** `frontend/src/components/student/studentQueries.vue`

### Vue Reactivity Updates
```vue
<!-- The ChatBubble component re-renders with new response -->
<ChatBubble
  v-for="response in selectedQuery.responses || []"
  :key="response.id"
  :message="{ 
    content: response.content,                    // ← Your message
    timestamp: new Date(response.created_at),      // ← Sent time
    user_role: response.user_role                  // ← Your role
  }"
  :isUser="response.user_role === 'student'"  // ← Show on right side
  :isDark="themeStore.currentTheme === 'dark'"
/>
```

### Visual Result
- ✅ Message appears as a chat bubble in the conversation
- ✅ Query status changes from "OPEN" to "IN_PROGRESS"
- ✅ Response count in sidebar updates
- ✅ BottomBar textarea clears
- ✅ No error message displayed

---

## 📊 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│ USER ACTION: Types message in BottomBar & presses Enter             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ BottomBar.vue: sendMessage()                                        │
│ - Validates message not empty                                       │
│ - Emits "send" event with { message, file }                         │
│ - Clears textarea                                                   │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ studentQueries.vue: handleBottomBarSend(payload)                    │
│ - Checks query selected ✓                                           │
│ - Validates message length (≥5 chars) ✓                             │
│ - Calls queriesAPI.addResponse()                                    │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Axios HTTP Request                                                  │
│ POST /api/queries/1/response                                        │
│ Headers: Authorization: Bearer {jwt}                                │
│ Body: { content: "message", is_solution: false }                    │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Backend: add_query_response() endpoint                              │
│ - Authenticate user (JWT) ✓                                         │
│ - Validate request data (Pydantic) ✓                                │
│ - Lookup Query by ID ✓                                              │
│ - Create QueryResponse object                                       │
│ - Update Query status: OPEN → IN_PROGRESS                           │
│ - db.add() & db.commit() to database                                │
│ - Return 201 Created with response data                             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Database: SQLite Operations                                         │
│ - INSERT into query_responses table                                 │
│ - UPDATE queries table (status, updated_at)                         │
│ - Commit transaction                                                │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ HTTP Response: 201 Created                                          │
│ { message: "...", response: { id, content, ... } }                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Frontend: Catch success response                                    │
│ - Call selectQuery(id) to reload with responses                     │
│ - Call loadQueries() to refresh list                                │
│ - Clear error state                                                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Backend: GET /api/queries/1 (with eager-loaded responses)           │
│ - Query found ✓                                                     │
│ - Load related QueryResponse objects                                │
│ - Serialize to JSON with responses array                            │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Frontend: selectedQuery.responses now has new message               │
│ - Vue reactivity triggers                                           │
│ - ChatBubble re-renders with new response                           │
│ - Message appears in conversation thread                            │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ USER SEES: Message appears in chat as blue bubble                   │
│ - Query status updated to "IN_PROGRESS"                             │
│ - Response count incremented                                        │
│ - BottomBar cleared and ready for next message                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Points

### Frontend Validation
- ✅ Message must not be empty
- ✅ Query must be selected
- ✅ Message must be ≥ 5 characters

### Backend Validation
- ✅ JWT token must be valid
- ✅ User must be authenticated
- ✅ Query must exist
- ✅ Request body must match `QueryResponseCreate` schema
- ✅ `content` must be min 5 characters (Pydantic validation)
- ✅ Only TAs/Instructors/Admins can mark as solution

### Database Changes
1. **query_responses table** - New row created
2. **queries table** - Status updated
3. **Cascading updates** - response_count field updated in serialization

### Error Handling
- ❌ Empty message → Frontend validation fails
- ❌ No query selected → Frontend shows "Please select a query first"
- ❌ Message < 5 chars → Frontend validation fails (422 from backend)
- ❌ Query doesn't exist → Backend returns 404
- ❌ User not authenticated → Backend returns 401
- ❌ Database error → Backend returns 500 + rollback

---

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Message sent but doesn't appear | Response not eagerly loaded | Ensure `joinedload(Query.responses)` in GET endpoint |
| 422 error when sending | Message < 5 chars OR field name mismatch | Check `content` field (not `message`) |
| 401 Unauthorized | JWT token expired or invalid | Check Authorization header in axios |
| Query status not updating | Transaction not committed | Verify `db.commit()` called in backend |
| Empty responses array | Relationship not configured | Check `Query.responses` relationship in model |

