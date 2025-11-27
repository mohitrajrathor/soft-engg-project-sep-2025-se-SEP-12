📘 TA Doubt Summarizer – API Contract
This document defines the API shape, request/response formats, and schema expectations for the TA Doubt Summarizer feature.

Used by:

Person 2 (Schemas)

Person 3 (Services)

Person 4 (Routers)

Frontend Integration

---------------------------------------
✅ 1. POST /api/v1/ta/doubts/upload
---------------------------------------
Uploads a batch of student doubts (forum posts / chat logs / emails).

Request Body
{
  "course_code": "CS1010",
  "source": "moodle_forum",
  "messages": [
    { "author_role": "student", "text": "I don't understand DP transitions." },
    { "author_role": "student", "text": "How does DP recurrence work?" }
  ]
}
Description
course_code — Which course the uploaded doubts belong to.

source — Where the doubts were collected from (email, whatsapp, moodle…)

messages — List of student/TA messages extracted.

Success Response
{
  "status": "success",
  "upload_id": 12
}
Error Response Example
{
  "status": "error",
  "message": "course_code missing"
}
---------------------------------------
✅ 2. GET /api/v1/ta/doubts/summary
---------------------------------------
Generates a summary of all doubts for a given course.

Query Parameters
?course_code=CS1010
Response
{
  "course_code": "CS1010",
  "overall_summary": "Students are confused about DP transitions and recursion.",
  "topics": [
    {
      "label": "DP Recurrence",
      "example_questions": [
        "How does the recurrence work?",
        "Why do we use min() here?"
      ]
    },
    {
      "label": "Base Case Confusion",
      "example_questions": [
        "How to choose base cases?",
        "Why initialize dp[0] = 1?"
      ]
    }
  ]
}
Description
overall_summary — LLM-generated general summary of confusion areas.

topics — Clusters of related questions.

---------------------------------------
✅ 3. GET /api/v1/ta/doubts/topics
---------------------------------------
Returns only the topic clusters.

Query Parameters
?course_code=CS1010
Response
[
  {
    "label": "DP Recurrence",
    "example_questions": [
      "How does recurrence work?",
      "What is the transition formula?"
    ]
  },
  {
    "label": "Memoization vs Tabulation",
    "example_questions": [
      "Which is faster?",
      "When to use which?"
    ]
  }
]
Description
Useful for:

TAs preparing for session

Showing clusters to instructors

---------------------------------------
✅ 4. GET /api/v1/ta/doubts/insights
---------------------------------------
Provides LLM-generated suggestions to instructors/TAs on how to improve teaching.

Query Parameters
?course_code=CS1010
Response
{
  "course_code": "CS1010",
  "insights": [
    "Students struggle with recurrence transitions. Add a live example.",
    "Explain base cases with diagrams.",
    "Provide 2-3 solved DP examples in the next lecture."
  ]
}
Description
Insights are generated based on:

Questions patterns

Confusion clusters

Frequent themes

---------------------------------------
📦 Schemas Used (From Person 2)
---------------------------------------
Request Schemas
DoubtMessageCreate
{
  "author_role": "student",
  "text": "I don't understand DP"
}
DoubtUploadCreate
{
  "course_code": "CS1010",
  "source": "moodle_forum",
  "messages": [ ... ]
}
Response Schemas
DoubtTopic
{
  "label": "DP Recurrence",
  "example_questions": [ ... ]
}
DoubtSummaryResponse
{
  "course_code": "CS1010",
  "overall_summary": "...",
  "topics": [ ... ]
}
DoubtInsightsResponse
{
  "course_code": "CS1010",
  "insights": [ ... ]
}
