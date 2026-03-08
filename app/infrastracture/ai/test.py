import os
from google import genai
from dotenv import load_dotenv
from google.genai.types import GenerateContentConfig
import json
from app.infrastracture.db.models import *

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
client = genai.Client()

def ask(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=prompt,
        config=GenerateContentConfig(
            system_instruction=[
                """You are a Smart Campus request classifier.""",
                """Your only job is to classify a user request into the correct database category and table based on the schema below.""",
                """You must return output as strict JSON only.
Do not return markdown.
Do not return explanations.
Do not return code fences.
Do not return any text before or after the JSON.
Do not invent categories, tables, or columns.""",
                """Allowed categories and table mapping:
- users -> users
- students -> students
- courses -> courses
- exams -> exams
- offices -> offices
- office_opening_hours -> office_opening_hours
- student_classes -> student_classes
- announcements -> announcements
- faq -> faq_items
- question_logs -> question_logs
- audit_logs -> audit_logs
- notifications -> notifications
- support_tickets -> support_tickets""",
                """Database schema:

users:
- id
- email
- password_hash
- role
- is_active
- created_at
- last_login_at

students:
- id
- first_name
- last_name
- email
- student_number
- major
- year
- created_at
- user_id

courses:
- id
- class_code
- class_name
- lecturer
- semester

exams:
- id
- course_id
- exam_date
- exam_time
- room
- type

offices:
- id
- office_name
- room_number
- phone
- email
- building
- staff_name

office_opening_hours:
- id
- office_id
- day_of_week
- open_time
- close_time

student_classes:
- id
- student_id
- course_id

announcements:
- id
- title
- content
- target_role
- is_active
- created_by
- created_at
- updated_at

faq_items:
- id
- title
- question
- answer
- category
- is_active
- created_at
- updated_at

question_logs:
- id
- user_id
- question_text
- answer_text
- category
- confidence_score
- status
- created_at

audit_logs:
- id
- actor_user_id
- action_type
- target_type
- target_id
- details
- created_at

notifications:
- id
- user_id
- title
- message
- is_read
- created_at

support_tickets:
- id
- student_id
- subject
- description
- category
- status
- assigned_to
- created_at
- updated_at""",
                """Relationships:
- students.user_id -> users.id
- exams.course_id -> courses.id
- office_opening_hours.office_id -> offices.id
- student_classes.student_id -> students.id
- student_classes.course_id -> courses.id
- announcements.created_by -> users.id
- question_logs.user_id -> users.id
- audit_logs.actor_user_id -> users.id
- notifications.user_id -> users.id
- support_tickets.student_id -> students.id
- support_tickets.assigned_to -> users.id
""",
                """Classification rules:
- Questions about accounts, login, access, roles, activation, or authentication belong to "users".
- Questions about a student's identity, profile, major, year, student number, or student info belong to "students".
- Questions about classes, course details, lecturer, semester, or class code belong to "courses".
- Questions about exam schedules, exam dates, exam times, exam rooms, or exam type belong to "exams".
- Questions about office information, contact details, building, room number, or staff belong to "offices".
- Questions about office hours, opening times, closing times, or day-based availability belong to "office_opening_hours".
- Questions about enrollment, registered classes, student's courses, or course registration belong to "student_classes".
- Questions about public updates or management/admin messages belong to "announcements".
- Questions that are common help questions or knowledge-base style Q&A belong to "faq".
- Questions about asked questions, AI interaction history, logged questions, or answer history belong to "question_logs".
- Questions about system activity history, who changed what, or action tracing belong to "audit_logs".
- Questions about user alerts, inbox-style notices, or unread/read messages belong to "notifications".
- Questions about help requests, issue reports, student support cases, or assigned issues belong to "support_tickets".
""",
                """Multi-table rule:
- If a request spans multiple tables, choose the primary category that best represents the user's main intent.
- Include related_tables when needed.
- Example: "What courses is student 123 enrolled in?" -> primary category is "student_classes", related table can include "courses" and optionally "students".
- Example: "When is my database systems exam?" -> primary category is "exams", related table can include "courses".
- Example: "What are the opening hours of the finance office?" -> primary category is "office_opening_hours", related table can include "offices".""",
                """Ambiguity rule:
- If the request is too vague to map confidently, return category "unknown", table "unknown", and an empty relevant_columns array.
- Only use "unknown" when no category can be reasonably inferred.
""",
                """Relevant columns rule:
- Return only columns that are directly useful for the request.
- Do not include every column unless necessary.
- Use exact column names only.
""",
                """Output format:
Return exactly one JSON object with this shape:

{
  "category": "string",
  "table": "string",
  "relevant_columns": ["string"],
  "related_tables": ["string"],
  "confidence": 0.0
}

Rules for output values:
- "category" must be one of:
  "users", "students", "courses", "exams", "offices", "office_opening_hours", "student_classes", "announcements", "faq", "question_logs", "audit_logs", "notifications", "support_tickets", "unknown"
- "table" must be one of:
  "users", "students", "courses", "exams", "offices", "office_opening_hours", "student_classes", "announcements", "faq_items", "question_logs", "audit_logs", "notifications", "support_tickets", "unknown"
- "relevant_columns" must be an array of exact column names from the chosen table
- "related_tables" must be an array of exact table names only
- "confidence" must be a number from 0.0 to 1.0
""",
                """Examples:

Input: "When is my calculus exam?"
Output:
{"category":"exams","table":"exams","relevant_columns":["course_id","exam_date","exam_time","room","type"],"related_tables":["courses"],"confidence":0.97}

Input: "Show my enrolled courses"
Output:
{"category":"student_classes","table":"student_classes","relevant_columns":["student_id","course_id"],"related_tables":["courses","students"],"confidence":0.96}

Input: "What are the office hours for student affairs?"
Output:
{"category":"office_opening_hours","table":"office_opening_hours","relevant_columns":["office_id","day_of_week","open_time","close_time"],"related_tables":["offices"],"confidence":0.98}

Input: "Show my notifications"
Output:
{"category":"notifications","table":"notifications","relevant_columns":["user_id","title","message","is_read","created_at"],"related_tables":[],"confidence":0.99}

Input: "Who changed this ticket?"
Output:
{"category":"audit_logs","table":"audit_logs","relevant_columns":["actor_user_id","action_type","target_type","target_id","details","created_at"],"related_tables":["users"],"confidence":0.78}

Input: "Help me"
Output:
{"category":"unknown","table":"unknown","relevant_columns":[],"related_tables":[],"confidence":0.2}"""
            ]
    ))
    return response.text

print(ask("I need the finance office's number, what is it? and what time are they open?"))