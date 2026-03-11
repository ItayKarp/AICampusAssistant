from typing import Any


class AIQueryService:
    def __init__(self, validator, repository_selector, classifier, response_service):
        self.classifier = classifier
        self.validator = validator
        self.repository_selector = repository_selector
        self.response_service = response_service

    def handle_question(self, question: str, user_id: int | None = None) -> dict[str, Any]:
        raw = self.classifier.classify(question=question)
        validated = self.validator.validate(classification=raw)

        if not validated.is_valid:
            return {
                "success": False,
                "stage": "validation",
                "data": None,
                "answer": "Invalid table classification.",
            }

        repo = self.repository_selector.get_repository(validated.table)
        data = repo.get_results(
            user_id=user_id
        )

        answer = self.response_service.generate_answer(
            question=question,
            table=validated.table,
            rows=data.get("rows", []),
        )

        return {
            "answer": answer,
        }