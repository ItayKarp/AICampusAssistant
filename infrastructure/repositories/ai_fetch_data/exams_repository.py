from datetime import datetime

from infrastructure.db.models import Course, Exam, Student, StudentClass
from infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository
from infrastructure.repositories.ai_fetch_data.helpers import (
    RepositoryClassificationHelper as ClassificationHelper,
    RepositoryResponseBuilder as ResponseBuilder,
)


class SqlAlchemyExamsRepo(BaseAIRepository):
    def get_results(self, classification: dict, user_question: str | None = None, user_id: int | None = None) -> dict:
        relevant_columns = ClassificationHelper.get_relevant_columns(classification)
        filters = ClassificationHelper.get_filters(classification)
        scope = ClassificationHelper.get_scope(classification)

        with self.context_manager() as session:
            query = session.query(Exam).join(Course, Exam.course_id == Course.id)

            if scope == "self":
                if user_id is None:
                    return ResponseBuilder.error("User context is required for self-scoped exam queries.")

                query = (
                    query.join(StudentClass, StudentClass.course_id == Course.id)
                    .join(Student, Student.id == StudentClass.student_id)
                    .filter(Student.user_id == user_id)
                )

            query = self._apply_filters(query, filters)
            query = query.order_by(Exam.exam_date.asc(), Exam.exam_time.asc())

            exams = query.all()

            if not exams:
                return ResponseBuilder.empty("No exams found.")

            data = [self._serialize_exam(exam, relevant_columns) for exam in exams]

            return ResponseBuilder.success(
                category="exams",
                table="exams",
                results=data,
                applied_filters={
                    "scope": scope,
                },
                message="Exam results fetched successfully.",
            )

    def _apply_filters(self, query, filters: dict):
        class_name = self._normalize_string(filters.get("class_name"))
        class_code = self._normalize_string(filters.get("class_code"))
        lecturer = self._normalize_string(filters.get("lecturer"))
        semester = self._normalize_string(filters.get("semester"))
        exam_type = self._normalize_string(filters.get("type"))
        room = self._normalize_string(filters.get("room"))
        date_from = self._parse_date(filters.get("date_from"))
        date_to = self._parse_date(filters.get("date_to"))

        if class_name:
            query = query.filter(Course.class_name.ilike(f"%{class_name}%"))

        if class_code:
            query = query.filter(Course.class_code.ilike(f"%{class_code}%"))

        if lecturer:
            query = query.filter(Course.lecturer.ilike(f"%{lecturer}%"))

        if semester:
            query = query.filter(Course.semester.ilike(f"%{semester}%"))

        if exam_type:
            query = query.filter(Exam.type.ilike(f"%{exam_type}%"))

        if room:
            query = query.filter(Exam.room.ilike(f"%{room}%"))

        if date_from:
            query = query.filter(Exam.exam_date >= date_from)

        if date_to:
            query = query.filter(Exam.exam_date <= date_to)

        return query

    def _serialize_exam(self, exam: Exam, relevant_columns: list[str]) -> dict:
        course = exam.course

        column_map = {
            "id": exam.id,
            "class_name": course.class_name if course else None,
            "class_code": course.class_code if course else None,
            "lecturer": course.lecturer if course else None,
            "semester": course.semester if course else None,
            "exam_date": exam.exam_date.isoformat() if exam.exam_date else None,
            "exam_time": exam.exam_time.isoformat() if exam.exam_time else None,
            "room": exam.room,
            "type": exam.type,
        }

        allowed_columns = set(column_map.keys())
        selected_columns = [column for column in relevant_columns if column in allowed_columns]

        if not selected_columns:
            selected_columns = ["class_name", "class_code", "exam_date", "exam_time", "room", "type"]

        return {column: column_map[column] for column in selected_columns}

    @staticmethod
    def _normalize_string(value):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()
        return value or None

    @staticmethod
    def _parse_date(value):
        if value is None:
            return None

        if hasattr(value, "year") and hasattr(value, "month") and hasattr(value, "day"):
            return value

        if not isinstance(value, str):
            return None

        value = value.strip()
        if not value:
            return None

        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue

        return None