import json
from typing import Callable, Dict

from app.infrastracture.ai.classifier import classify_prompt
from app.infrastracture.ai.responder import respond


class AssistantService:
    def __init__(self, exam_repo, office_repo, courses_repo):
        self.exam_repo = exam_repo
        self.office_repo = office_repo
        self.courses_repo = courses_repo

    def handle_question(self, user_question: str, user_id: int | None = None):
        try:
            classification = self._classify_question(user_question)
        except json.JSONDecodeError:
            return {
                "classification": None,
                "data": None,
                "answer": "I couldn’t understand the request classification."
            }
        except Exception as e:
            return {
                "classification": None,
                "data": None,
                "answer": f"An error occurred: {str(e)}"
            }

        data = self._fetch_data(classification, user_question, user_id)
        answer = self._generate_answer(user_question, classification, data)

        return {
            "classification": classification,
            "data": data,
            "answer": answer
        }

    @staticmethod
    def _classify_question(user_question: str) -> dict:
        return json.loads(classify_prompt(user_question))


    def _fetch_data(self, classification: dict, user_question: str, user_id: int| None):
        category = classification.get("category")
        if not category:
            return {}
        categories: Dict[str, Callable[[str, int| None], dict]] = {
            "exams": self.exam_repo.get_results,
            "office_opening_hours": self.office_repo.get_results,
            "courses": self.courses_repo.get_results
        }
        if category not in categories:
            return {}
        response = categories.get(category)(classification,user_question, user_id)
        if not response:
            return {}
        return response


    @staticmethod
    def _generate_answer(user_question: str, classification: dict, data):
        return respond(user_question, classification, data)