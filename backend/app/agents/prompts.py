# prompts module

# imports



def build_quiz_prompt(user_query: str) -> str:
    """
    Build a prompt for an LLM to generate a quiz in a strict JSON format.
    """
    template = """
You are an AI quiz generator. Based on the following user query, create a quiz following these rules:

User Query:
<<<USER_QUERY>>>

Rules:
- Extract from the query: topic, difficulty level, number of questions, and question type.
- Default number of questions to 10 if not specified.
- If requested questions < 5 or > 25, adjust to 5 or 25 respectively, and explain this adjustment briefly in the "ai_response" field.
- Difficulty must be one of: "easy", "medium", or "hard". If not specified, infer it based on topic or assume "medium".
- Questions must be factual, clear, and diverse.
- Each question must include:
  - id
  - type (one of: mcq, msq, boolean)
  - question_text (Markdown supported)
  - options (list of strings)
  - answers (list of correct option strings, exactly matching options)
- Include a "difficulty" field in the quiz content.
- Return **only valid JSON** — no markdown code fences, no extra text, no commentary.

Expected JSON format:
{
  "ai_response": "<Brief explanation of quiz creation and adjustments>",
  "quiz": {
    "topic": "<quiz topic>",
    "difficulty": "<easy | medium | hard>",
    "questions_count": <int>,
    "tags": ["<tag1>", "<tag2>"],
    "questions": [
      {
        "id": <int>,
        "type": "mcq | msq | boolean",
        "question_text": "<question text in Markdown>",
        "options": [
          "<option 1>", "<option 2>", "<option 3>", "<option 4>"
        ],
        "answers": ["<correct option text>", "<correct option text>"]
      }
    ]
  }
}


example:
{
    "ai_response": "Here is your quiz on Python basics.",
    "quiz": {
        "topic": "Python Basics",
        "difficulty": "easy",
        "questions_count": 5,
        "tags": ["python", "programming"],
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "question_text": "What is the output of print(2 + 3)?",
                "options": ["5", "8", "error", "9"],
                "answers": ["5"]
            },
            {
                "id": 2,
                "type": "boolean",
                "question_text": "Is Python dynamically typed?",
                "options": ["True", "False"],
                "answers": ["True"]
            }
        ]
    }
}

Notes:
- If the user requests fewer than 5 or more than 25 questions, limit to 5 or 25 and explain in "ai_response".
- Output must be valid JSON only — no markdown, no commentary.
- Only the "question_text" may include Markdown.
"""
    return template.replace("<<<USER_QUERY>>>", user_query.strip())


def build_update_quiz_prompt(quiz, feedback: str) -> str:
    """
    Build a prompt for an LLM to update or improve an existing quiz
    based on user feedback while preserving the JSON schema above.
    """
    template = """
You are an AI quiz editor. You will receive a quiz (in JSON) and user feedback.
Your task is to update or improve the quiz based on the feedback while keeping it valid and consistent.

Input Quiz JSON:
<<<QUIZ_JSON>>>

User Feedback:
<<<USER_FEEDBACK>>>

Instructions:
- Analyze the feedback and make minimal, necessary changes.
- Preserve the same JSON structure and field names.
- You may modify:
  - Question wording (clarity, correctness, or phrasing)
  - Options and answers (accuracy)
  - Tags, difficulty, or question count (only if feedback suggests)
- Add or remove questions **only** if explicitly requested.
- Maintain unique and consistent IDs.
- Ensure answers correspond exactly to updated options.
- Keep schema integrity (no missing or extra fields).
- Output **only valid JSON** — no markdown, no extra commentary.
- Only "question_text" may contain Markdown.

Expected JSON format:
{
  "ai_response": "<Brief summary of changes made>",
  "quiz": {
    "topic": "<topic>",
    "difficulty": "<easy | medium | hard>",
    "questions_count": <int>,
    "tags": ["<tag1>", "<tag2>"],
    "questions": [
      {
        "id": <int>,
        "type": "mcq | msq | boolean",
        "question_text": "<question text in Markdown>",
        "options": [
          "<option 1>", "<option 2>", "<option 3>", "<option 4>"
        ],
        "answers": ["<correct option text>", "<correct option text>"]
      }
    ]
  }
}


example: 
{
    "ai_response": "Here is your quiz on Python basics.",
    "quiz": {
        "topic": "Python Basics",
        "difficulty": "easy",
        "questions_count": 5,
        "tags": ["python", "programming"],
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "question_text": "What is the output of print(2 + 3)?",
                "options": ["5", "8", "error", "9"],
                "answers": ["5"]
            },
            {
                "id": 2,
                "type": "boolean",
                "question_text": "Is Python dynamically typed?",
                "options": ["True", "False"],
                "answers": ["True"]
            }
        ]
    }
}

Important:
- Output must be strictly valid JSON (parse-able).
- The "ai_response" field should briefly describe what was updated.
"""
    quiz_json = quiz.model_dump_json()
    prompt = template.replace("<<<QUIZ_JSON>>>", quiz_json)
    prompt = prompt.replace("<<<USER_FEEDBACK>>>", feedback.strip())
    return prompt