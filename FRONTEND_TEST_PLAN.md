# AURA Frontend Testing Plan

## Critical Issues Found

### 🔴 BLOCKING ISSUE: Pinia Not Installed
**Problem:** The frontend uses Pinia store (`src/stores/user.js`) but Pinia is NOT in `package.json`.
**Impact:** State management will not work, authentication will fail.
**Fix Required:**
```bash
cd frontend
npm install pinia axios
```

Then update `src/main.js` to include Pinia:
```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')
```

---

## Testing Checklist

### Phase 1: Setup and Installation ✓

- [ ] **Install missing dependencies**
  ```bash
  cd frontend
  npm install pinia axios
  ```

- [ ] **Update main.js** to initialize Pinia

- [ ] **Verify backend is running**
  ```bash
  cd backend
  .venv\Scripts\activate
  uvicorn main:app --reload
  ```

- [ ] **Start frontend dev server**
  ```bash
  cd frontend
  npm run dev
  ```

- [ ] **Verify no console errors** on startup

---

### Phase 2: Authentication Testing

#### 2.1 Registration Flow
- [ ] Navigate to `/register`
- [ ] Test form validation:
  - [ ] Empty fields show error
  - [ ] Invalid email format shows error
  - [ ] Short password (< 8 chars) shows error
- [ ] Test role selection (Student, TA, Instructor)
- [ ] Submit valid registration
- [ ] Verify success message/redirect
- [ ] Check token stored in localStorage
- [ ] Verify user store is populated

#### 2.2 Login Flow
- [ ] Navigate to `/login`
- [ ] Test form validation:
  - [ ] Empty fields show error
  - [ ] Invalid credentials show error message
- [ ] Submit valid login
- [ ] Verify JWT token received
- [ ] Check localStorage has:
  - [ ] `token`
  - [ ] `refreshToken`
  - [ ] `user`
  - [ ] `role`
- [ ] Verify redirect to appropriate dashboard based on role

#### 2.3 Token Management
- [ ] Verify access token sent in Authorization header
- [ ] Test token refresh on 401 error
- [ ] Test logout clears all tokens
- [ ] Test page reload maintains authentication

---

### Phase 3: Student Features Testing

#### 3.1 Student Dashboard (`/student/dashboard`)
- [ ] Stats display correctly:
  - [ ] Lectures watched count
  - [ ] Assignments done count
  - [ ] Quizzes completed count
  - [ ] Study hours
- [ ] Upcoming deadlines list
- [ ] Recent announcements
- [ ] Course progress bars
- [ ] Navigation to other student pages works

#### 3.2 AI Assistant (`/student/AI-assistant`)
- [ ] Chat interface loads
- [ ] Can send messages
- [ ] Messages appear in chat history
- [ ] AI responses are received
- [ ] Scroll works properly
- [ ] Input field clears after send

#### 3.3 Query Management (`/student/queries`)
- [ ] Query list displays
- [ ] Filter tabs work (All, Open, Resolved)
- [ ] Can create new query
- [ ] Can view query details
- [ ] Can add responses
- [ ] Can mark as resolved
- [ ] Search functionality works
- [ ] Pagination works

#### 3.4 New Query (`/student/new-query`)
- [ ] Form displays correctly
- [ ] Can enter title and description
- [ ] Can select category/subject
- [ ] Can attach files
- [ ] Submit creates query
- [ ] Validation works
- [ ] Redirects after creation

#### 3.5 Resources (`/student/resources`)
- [ ] Course cards display
- [ ] Filter tabs work (All, Enrolled, Archived)
- [ ] Can view resource details
- [ ] Can add new resources
- [ ] Modal opens/closes properly
- [ ] File upload works
- [ ] Search/filter works

#### 3.6 Study Break (`/student/study-break`)
- [ ] Timer preset buttons (5, 10, 15, 30 min)
- [ ] Custom time input works
- [ ] Timer starts correctly
- [ ] Full-screen overlay displays
- [ ] Countdown is accurate
- [ ] Can pause/resume
- [ ] Notification when complete
- [ ] Can exit early

#### 3.7 Profile (`/student/profile`)
- [ ] Profile data displays
- [ ] Can edit profile fields
- [ ] Can update password
- [ ] Changes save correctly
- [ ] Validation works
- [ ] Avatar/photo upload

---

### Phase 4: TA Features Testing

#### 4.1 TA Dashboard (`/ta/dashboard`)
- [ ] Metrics cards display:
  - [ ] Doubts resolved
  - [ ] Students helped
  - [ ] Avg response time
  - [ ] Satisfaction rate
- [ ] Assigned courses list
- [ ] Recent doubts list
- [ ] Escalated queries
- [ ] Quick actions sidebar

#### 4.2 Query Tracker (`/ta/query-tracker`)
- [ ] Query table displays
- [ ] Advanced filters work:
  - [ ] Search
  - [ ] Priority filter
  - [ ] Topic filter
  - [ ] Status filter
  - [ ] Escalation filter
- [ ] Sorting works on all columns
- [ ] Priority indicators (High/Medium/Low)
- [ ] Status badges display correctly
- [ ] Can respond to queries
- [ ] Can escalate queries
- [ ] Can mark as resolved
- [ ] Pagination works
- [ ] Export functionality

#### 4.3 Tools
- [ ] **Doubt Summarizer** (`/ta/doubt-summarizer`)
  - [ ] Input form works
  - [ ] AI generates summary
  - [ ] Can copy/save summary

- [ ] **Assessment Generator** (`/ta/assessment-generator`)
  - [ ] Form inputs work
  - [ ] Generates questions
  - [ ] Can edit generated content
  - [ ] Can export

- [ ] **Slide Deck Creator** (`/ta/slide-deck-creator`)
  - [ ] Topic input
  - [ ] Generates slides
  - [ ] Preview works
  - [ ] Can download

- [ ] **Onboarding Mentor** (`/ta/onboarding-mentor`)
  - [ ] Guide displays
  - [ ] Step-by-step works
  - [ ] Can complete steps

- [ ] **Resource Hub** (`/ta/resource`)
  - [ ] Resources display
  - [ ] Can filter/search
  - [ ] Can add resources

#### 4.4 TA Profile (`/ta/profile`)
- [ ] Profile displays
- [ ] Can edit information
- [ ] Changes save

---

### Phase 5: Instructor Features Testing

#### 5.1 Instructor Dashboard (`/instructor/dashboard`)
- [ ] Engagement line chart displays
- [ ] Assignment heatmap renders
- [ ] Deadline tracker works
- [ ] Quiz distribution chart
- [ ] Top students list
- [ ] Quick actions work:
  - [ ] Generate reports
  - [ ] Export data
  - [ ] Create assignments

#### 5.2 Tools
- [ ] **Assessment Generator** (`/instructor/assessment-generator`)
  - [ ] Configuration form
  - [ ] Generates assessment
  - [ ] Can edit/preview
  - [ ] Can export

- [ ] **Slide Generator** (`/instructor/slide-generator`)
  - [ ] Topic and settings input
  - [ ] Generates slides
  - [ ] Preview functionality
  - [ ] Download option

- [ ] **Discussion Summaries** (`/instructor/discussion-summaries`)
  - [ ] Discussion list
  - [ ] Can generate summary
  - [ ] Summary displays correctly

#### 5.3 Instructor Profile (`/instructor/profile`)
- [ ] Profile information
- [ ] Edit functionality
- [ ] Save changes

---

### Phase 6: Admin Features Testing

#### 6.1 Admin Dashboard (`/admin/dashboard`)
- [ ] Top metrics cards:
  - [ ] Active users
  - [ ] Open queries
  - [ ] Flagged issues
  - [ ] System health
- [ ] FAQ analytics chart
- [ ] Unresolved queries chart
- [ ] Institutional queries table:
  - [ ] Data displays
  - [ ] Export works
- [ ] User management table:
  - [ ] User list displays
  - [ ] Can approve users
  - [ ] Can block users
  - [ ] Can flag users
  - [ ] Filters work
  - [ ] Search works
- [ ] Quick actions:
  - [ ] Send announcements
  - [ ] Export reports
  - [ ] Manage roles
- [ ] System announcements section

---

### Phase 7: Navigation and Routing

#### 7.1 Public Routes
- [ ] `/` - Landing page displays
- [ ] `/login` - Login page accessible
- [ ] `/register` - Register page accessible
- [ ] Unauthenticated users redirected to login

#### 7.2 Role-Based Routing
- [ ] Student can only access `/student/*` routes
- [ ] TA can only access `/ta/*` routes
- [ ] Instructor can only access `/instructor/*` routes
- [ ] Admin can only access `/admin/*` routes
- [ ] Unauthorized access redirects to login

#### 7.3 Navigation Components
- [ ] **Student Sidebar** - All links work
- [ ] **TA Sidebar** - All links work
- [ ] **Instructor Sidebar** - All links work
- [ ] **Header bars** - Search, profile dropdown
- [ ] **Bottom bar** (Student) - Mobile navigation
- [ ] Active route highlighting
- [ ] Breadcrumbs (if implemented)

---

### Phase 8: API Integration Testing

#### 8.1 Authentication APIs
- [ ] POST `/api/auth/signup` - Register
- [ ] POST `/api/auth/login` - Login
- [ ] POST `/api/auth/refresh` - Refresh token
- [ ] GET `/api/auth/me` - Get current user
- [ ] PUT `/api/auth/me` - Update profile

#### 8.2 Error Handling
- [ ] 400 - Bad request shows error message
- [ ] 401 - Unauthorized triggers token refresh
- [ ] 403 - Forbidden shows access denied
- [ ] 404 - Not found shows error
- [ ] 500 - Server error shows message
- [ ] Network error shows connection issue
- [ ] Timeout shows timeout message

#### 8.3 Loading States
- [ ] Buttons show loading spinner
- [ ] Forms disable during submission
- [ ] Lists show skeleton loaders
- [ ] Charts show loading state

---

### Phase 9: UI/UX Testing

#### 9.1 Responsive Design
- [ ] **Desktop (1920x1080)** - Layout correct
- [ ] **Laptop (1366x768)** - Layout correct
- [ ] **Tablet (768x1024)** - Layout adapts
- [ ] **Mobile (375x667)** - Mobile-friendly
- [ ] Sidebar collapses on mobile
- [ ] Touch targets adequate (min 44x44px)
- [ ] Text readable on all sizes

#### 9.2 Browser Compatibility
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers

#### 9.3 Accessibility
- [ ] Keyboard navigation works
- [ ] Tab order is logical
- [ ] Focus indicators visible
- [ ] ARIA labels present
- [ ] Alt text on images
- [ ] Color contrast sufficient
- [ ] Screen reader compatible

#### 9.4 Visual Elements
- [ ] Colors consistent with theme
- [ ] Icons load correctly
- [ ] Charts render properly
- [ ] Animations smooth
- [ ] No layout shifts
- [ ] Loading spinners visible

---

### Phase 10: Performance Testing

- [ ] **Initial page load** < 3 seconds
- [ ] **Time to Interactive** < 5 seconds
- [ ] No memory leaks on navigation
- [ ] Images optimized
- [ ] Lazy loading implemented
- [ ] Bundle size reasonable
- [ ] No console warnings/errors

---

### Phase 11: Edge Cases and Error Scenarios

#### 11.1 Authentication Edge Cases
- [ ] Expired token handling
- [ ] Multiple tabs syncing
- [ ] Logout from one tab affects others
- [ ] Invalid token format
- [ ] Backend down scenario

#### 11.2 Form Validation Edge Cases
- [ ] Special characters in input
- [ ] Very long input strings
- [ ] SQL injection attempts (should be sanitized)
- [ ] XSS attempts (should be escaped)
- [ ] Empty strings vs null vs undefined

#### 11.3 Data Edge Cases
- [ ] Empty lists display "No data"
- [ ] Very long text truncates properly
- [ ] Large file uploads
- [ ] Pagination with 0 items
- [ ] Pagination with 1000+ items

---

## Test Execution Commands

### Manual Testing
```bash
# Terminal 1 - Backend
cd backend
.venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install pinia axios  # First time only
npm run dev

# Open browser
# http://localhost:5173
```

### Automated Testing (Future)
```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

---

## Bug Report Template

```markdown
## Bug Report

**Title:** [Short description]

**Severity:** Critical | High | Medium | Low

**Component:** [Which page/component]

**Steps to Reproduce:**
1.
2.
3.

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Screenshots:**
[If applicable]

**Console Errors:**
```
[Error messages]
```

**Environment:**
- OS: [Windows/macOS/Linux]
- Browser: [Chrome/Firefox/Safari/Edge]
- Version: [Version number]

**Additional Context:**
[Any other relevant information]
```

---

## Test Results Summary

### Test Execution Date: _____________

#### Overall Results
- **Total Tests:** ___
- **Passed:** ___
- **Failed:** ___
- **Blocked:** ___
- **Skipped:** ___

#### Critical Issues Found
1.
2.
3.

#### High Priority Issues
1.
2.
3.

#### Medium/Low Issues
1.
2.
3.

#### Notes
[Additional observations]

---

## Next Steps

1. **Fix Critical Issues**
   - Install Pinia and Axios
   - Update main.js
   - Test authentication flow

2. **Implement Missing Features**
   - Route guards for authentication
   - Global error handling
   - Loading states
   - Toast notifications

3. **Optimize Performance**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Bundle analysis

4. **Enhance Testing**
   - Add unit tests
   - Add E2E tests
   - CI/CD pipeline
   - Automated testing

---

**Tester:** _____________
**Date:** _____________
**Sign-off:** _____________
