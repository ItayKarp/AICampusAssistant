from sqlalchemy import or_

from ....infrastructure.db.models import FaqItem
from ....infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository as BaseRepo


class SqlAlchemyFaqRepo(BaseRepo):
    def get_results(
        self,
        classification: dict,
        user_question: str | None = None,
        user_id: int | None = None,
    ) -> dict:
        filters = classification.get("filters", {})
        relevant_columns = classification.get("relevant_columns", [])

        if not relevant_columns:
            return {
                "success": False,
                "message": "No relevant columns were provided.",
                "results": [],
            }

        with self.context_manager() as session:
            query = session.query(FaqItem)

            category = filters.get("category")
            if category:
                query = query.filter(FaqItem.category.ilike(f"%{category.strip()}%"))

            search_value = (
                filters.get("question")
                or filters.get("search_text")
                or user_question
            )

            if search_value:
                terms = [term.strip() for term in search_value.split() if term.strip()]

                if terms:
                    conditions = []
                    for term in terms:
                        pattern = f"%{term}%"
                        conditions.extend([
                            FaqItem.title.ilike(pattern),
                            FaqItem.question.ilike(pattern),
                            FaqItem.answer.ilike(pattern),
                        ])

                    query = query.filter(or_(*conditions))

            results = query.all()

            return {
                "success": True,
                "message": "FAQ results fetched successfully.",
                "results": [
                    {
                        "id": row.id,
                        "title": row.title,
                        "question": row.question,
                        "answer": row.answer,
                        "category": row.category,
                    }
                    for row in results
                ],
            }