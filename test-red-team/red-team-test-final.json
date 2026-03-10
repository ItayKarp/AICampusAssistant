{
  "passed": 13,
  "failed": 0,
  "results": [
    {
      "id": "T01",
      "name": "Course lookup by class_name",
      "status": true,
      "passed": true,
      "expected": "Exactly 1 matching course",
      "risk": "Low",
      "direct_input": {
        "relevant_columns": [
          "class_name",
          "class_code"
        ],
        "filters": {
          "class_name": "Database Systems"
        }
      },
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "count": 1,
        "results": [
          {
            "class_name": "Database Systems",
            "class_code": "20451"
          }
        ],
        "message": null
      },
      "notes": "—"
    },
    {
      "id": "T02",
      "name": "Course lookup by class_code filter from classifier contract",
      "status": true,
      "passed": true,
      "expected": "Exactly 1 matching course",
      "risk": "High",
      "direct_input": {
        "relevant_columns": [
          "class_name",
          "class_code"
        ],
        "filters": {
          "class_code": 20451
        }
      },
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "count": 1,
        "results": [
          {
            "class_name": "Database Systems",
            "class_code": "20451"
          }
        ],
        "message": null
      },
      "notes": "—"
    },
    {
      "id": "T03",
      "name": "Exam lookup by room",
      "status": true,
      "passed": true,
      "expected": "Exactly 1 matching exam",
      "risk": "Low",
      "direct_input": {
        "relevant_columns": [
          "exam_date",
          "room"
        ],
        "filters": {
          "room": "B201"
        }
      },
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "count": 1,
        "results": [
          {
            "exam_date": "2026-06-01",
            "room": "B201"
          }
        ],
        "message": null
      },
      "notes": "—"
    },
    {
      "id": "T04",
      "name": "Exam lookup by class_name from classifier contract",
      "status": true,
      "passed": true,
      "expected": "Exactly 1 matching exam",
      "risk": "Critical",
      "direct_input": {
        "relevant_columns": [
          "exam_date",
          "room"
        ],
        "filters": {
          "class_name": "Database Systems"
        }
      },
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "count": 1,
        "results": [
          {
            "exam_date": "2026-06-01",
            "room": "B201"
          }
        ],
        "message": null
      },
      "notes": "—"
    },
    {
      "id": "T05",
      "name": "Office hours lookup by day_of_week from classifier contract",
      "status": true,
      "passed": true,
      "expected": "Exactly 1 matching office-hours row",
      "risk": "High",
      "direct_input": {
        "relevant_columns": [
          "day_of_week",
          "open_time",
          "close_time",
          "office_name"
        ],
        "filters": {
          "office_name": "Finance Office",
          "day_of_week": "Sunday"
        }
      },
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "count": 1,
        "results": [
          {
            "day_of_week": "Sunday",
            "open_time": "08:00:00",
            "close_time": "12:00:00",
            "office_name": "Finance Office"
          }
        ],
        "message": null
      },
      "notes": "—"
    },
    {
      "id": "T06",
      "name": "Office hours lookup by day_of_week alias",
      "status": true,
      "passed": true,
      "expected": "Exactly 1 matching office-hours row",
      "risk": "Low",
      "direct_input": {
        "relevant_columns": [
          "day_of_week",
          "open_time",
          "close_time",
          "office_name"
        ],
        "filters": {
          "office_name": "Finance Office",
          "day_of_week": "sun"
        }
      },
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "count": 1,
        "results": [
          {
            "day_of_week": "Sunday",
            "open_time": "08:00:00",
            "close_time": "12:00:00",
            "office_name": "Finance Office"
          }
        ],
        "message": null
      },
      "notes": "—"
    },
    {
      "id": "T07",
      "name": "Invalid day_of_week rejected",
      "status": true,
      "passed": true,
      "expected": "Validation error message",
      "risk": "Low",
      "direct_input": {
        "relevant_columns": [
          "day_of_week"
        ],
        "filters": {
          "office_name": "Finance Office",
          "day_of_week": "notaday"
        }
      },
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "count": 0,
        "results": [],
        "message": "Invalid day filter."
      },
      "notes": "—"
    },
    {
      "id": "T08",
      "name": "Unsupported category returned by classifier",
      "status": true,
      "passed": true,
      "expected": "Explicit unsupported-category response",
      "risk": "High",
      "direct_input": {
        "question": "How do I reset my password?"
      },
      "classifier_input": "How do I reset my password?",
      "classifier_output": "{\"category\": \"faq\", \"table\": \"faq_items\", \"relevant_columns\": [\"question\", \"answer\"], \"related_tables\": [], \"filters\": {}, \"confidence\": 0.9}",
      "responder_input": {
        "user_question": "How do I reset my password?",
        "classification": {
          "category": "faq",
          "table": "faq_items",
          "relevant_columns": [
            "question",
            "answer"
          ],
          "related_tables": [],
          "filters": {},
          "confidence": 0.9
        },
        "data": {
          "success": false,
          "source": "unsupported",
          "category": "faq",
          "data": [],
          "message": "Work in progress. We do not have access to that data yet."
        }
      },
      "responder_output": "ok",
      "final_observed": {
        "classification": {
          "category": "faq",
          "table": "faq_items",
          "relevant_columns": [
            "question",
            "answer"
          ],
          "related_tables": [],
          "filters": {},
          "confidence": 0.9
        },
        "data": {
          "success": false,
          "source": "unsupported",
          "category": "faq",
          "data": [],
          "message": "Work in progress. We do not have access to that data yet."
        },
        "answer": "ok"
      },
      "notes": "—"
    },
    {
      "id": "T09",
      "name": "Malformed classifier JSON handled",
      "status": true,
      "passed": true,
      "expected": "Graceful classification failure",
      "risk": "Medium",
      "direct_input": {
        "question": "bad json please"
      },
      "classifier_input": "bad json please",
      "classifier_output": "not json at all",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "classification": null,
        "data": null,
        "answer": "I couldn’t understand the request classification."
      },
      "notes": "—"
    },
    {
      "id": "T10",
      "name": "Classifier exception sanitization",
      "status": true,
      "passed": true,
      "expected": "Sanitized public error message",
      "risk": "High",
      "direct_input": {
        "question": "trigger classifier exception"
      },
      "classifier_input": "trigger classifier exception",
      "classifier_output": "RAISED RuntimeError: quota detail should not leak",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "classification": null,
        "data": null,
        "answer": "An error occurred"
      },
      "notes": "—"
    },
    {
      "id": "T11",
      "name": "Responder exception HTTP behavior",
      "status": true,
      "passed": true,
      "expected": "Non-500 controlled error response",
      "risk": "Critical",
      "direct_input": {
        "method": "POST",
        "endpoint": "/ai-prompt",
        "json": {
          "question": "trigger responder crash"
        }
      },
      "classifier_input": "trigger responder crash",
      "classifier_output": "{\"category\": \"courses\", \"table\": \"courses\", \"relevant_columns\": [\"class_name\"], \"related_tables\": [], \"filters\": {}, \"confidence\": 0.9}",
      "responder_input": {
        "user_question": "trigger responder crash",
        "classification": {
          "category": "courses",
          "table": "courses",
          "relevant_columns": [
            "class_name"
          ],
          "related_tables": [],
          "filters": {},
          "confidence": 0.9
        },
        "data": {
          "count": 2,
          "results": [
            {
              "class_name": "Database Systems"
            },
            {
              "class_name": "Calculus I"
            }
          ],
          "message": null
        }
      },
      "responder_output": "RAISED RuntimeError: responder boom",
      "final_observed": {
        "status_code": 200,
        "body": {
          "classification": {
            "category": "courses",
            "table": "courses",
            "relevant_columns": [
              "class_name"
            ],
            "related_tables": [],
            "filters": {},
            "confidence": 0.9
          },
          "data": {
            "count": 2,
            "results": [
              {
                "class_name": "Database Systems"
              },
              {
                "class_name": "Calculus I"
              }
            ],
            "message": null
          },
          "answer": "An error occurred"
        }
      },
      "notes": "—"
    },
    {
      "id": "T12",
      "name": "Identity-aware \"my\" query isolation",
      "status": true,
      "passed": true,
      "expected": "User-scoped result, not all exams",
      "risk": "Critical",
      "direct_input": {
        "question": "When is my exam?",
        "user_id": 999
      },
      "classifier_input": "When is my exam?",
      "classifier_output": "{\"category\": \"exams\", \"table\": \"exams\", \"relevant_columns\": [\"exam_date\", \"room\"], \"related_tables\": [\"courses\"], \"filters\": {}, \"confidence\": 0.9, \"scope\": \"self\"}",
      "responder_input": {
        "user_question": "When is my exam?",
        "classification": {
          "category": "exams",
          "table": "exams",
          "relevant_columns": [
            "exam_date",
            "room"
          ],
          "related_tables": [
            "courses"
          ],
          "filters": {},
          "confidence": 0.9,
          "scope": "self"
        },
        "data": {
          "count": 1,
          "results": [
            {
              "exam_date": "2026-06-01",
              "room": "B201"
            }
          ],
          "message": null
        }
      },
      "responder_output": "ok",
      "final_observed": {
        "classification": {
          "category": "exams",
          "table": "exams",
          "relevant_columns": [
            "exam_date",
            "room"
          ],
          "related_tables": [
            "courses"
          ],
          "filters": {},
          "confidence": 0.9,
          "scope": "self"
        },
        "data": {
          "count": 1,
          "results": [
            {
              "exam_date": "2026-06-01",
              "room": "B201"
            }
          ],
          "message": null
        },
        "answer": "ok"
      },
      "notes": "—"
    },
    {
      "id": "T13",
      "name": "Classifier instruction file formatting",
      "status": true,
      "passed": true,
      "expected": "Clean plain-text instruction content only",
      "risk": "Medium",
      "direct_input": "/mnt/data/campus_new/CampusAssistantAI - Copy/app/infrastracture/ai/classifier_system_instructions.txt",
      "classifier_input": "—",
      "classifier_output": "—",
      "responder_input": "—",
      "responder_output": "—",
      "final_observed": {
        "clean_plain_text": true
      },
      "notes": "This is a static file-format check, so classifier/responder are not invoked."
    }
  ]
}