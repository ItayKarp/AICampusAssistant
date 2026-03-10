from typing import Any

from domain.ai.schemas import ClassificationOutput, ValidatedClassification


class AIQueryService:
    def __init__(self, validator, repository_selector, classifier, response_service):
        self.classifier = classifier
        self.validator = validator
        self.repository_selector = repository_selector
        self.response_service = response_service

    def handle_question(self, question: str, user_id: int | None = None) -> dict[str, Any]:
        try:
            raw_classification: ClassificationOutput = self.classifier.classify(question=question)
        except RuntimeError:
            return {"status": "failed",
                    "message":"Please try again later"}
        validated: ValidatedClassification = self.validator.validate(classification=raw_classification)

        if not validated.is_valid:
            return {
                "success": False,
                "stage": "validation",
                "errors": validated.validation_errors,
                "classification": raw_classification.model_dump(),
                "validated_classification": validated.model_dump(),
                "answer": "I could not understand the request well enough to answer it safely.",
            }

        classification_dict = validated.model_dump()
        repository = self.repository_selector.get_repository(validated.category)

        result = repository.get_results(
            classification=classification_dict,
            user_question=question,
            user_id=user_id,
        )
        try:
            humanized_answer = self.response_service.generate_answer(
                question=question,
                classification=validated,
                repository_result=result,
            )
        except RuntimeError:
            return {"status": "failed",
                    "message":"Please try again later"}

        return {
            "success": result.get("success", True),
            "stage": "completed",
            "classification": raw_classification.model_dump(),
            "validated_classification": validated.model_dump(),
            "data": result,
            "answer": humanized_answer,
        }