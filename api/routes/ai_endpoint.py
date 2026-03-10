from fastapi import APIRouter, Header
from pydantic import BaseModel

from ...domain.ai.ai_response_service import AIResponseService
from ...domain.ai.classifier_service import AIClassifierService
from ...domain.ai.classification_validator import ClassificationValidator
from ...domain.ai.enums import CategoryEnum
from ...infrastructure.repositories.ai_fetch_data.courses_repository import SqlAlchemyCoursesRepo
from ...infrastructure.repositories.ai_fetch_data.office_repository import SqlAlchemyOfficeHoursRepo
from ...infrastructure.repositories.ai_fetch_data.repository_selector import AIRepositorySelector
from ...domain.ai.ai_query_service import AIQueryService
from ...infrastructure.repositories.ai_fetch_data import SqlAlchemyExamsRepo,SqlAlchemyFaqRepo
from ...api.dependencies import get_user_id_and_email

users_router = APIRouter(tags=["ai"])

class AIPromptRequest(BaseModel):
    question: str

@users_router.post("/ai-prompt")
async def ask(body: AIPromptRequest, authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    repository_selector = AIRepositorySelector(
        repositories_map={
            CategoryEnum.EXAMS: SqlAlchemyExamsRepo(),
            CategoryEnum.FAQ: SqlAlchemyFaqRepo(),
            CategoryEnum.COURSES: SqlAlchemyCoursesRepo(),
            CategoryEnum.OFFICE_OPENING_HOURS: SqlAlchemyOfficeHoursRepo()
        }
    )
    use_case = AIQueryService(
        classifier=AIClassifierService(),
        repository_selector=repository_selector,
        validator=ClassificationValidator(),
        response_service=AIResponseService()
    )
    return use_case.handle_question(body.question, user_id=user_id)
