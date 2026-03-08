from fastapi import APIRouter

from ...services.assistant_service import AssistantService
from ...infrastracture.repositories import SqlAlchemyOfficeRepo,SqlAlchemyExamRepo,SqlAlchemyCoursesRepo
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
    user_id: int | None = None
users_router = APIRouter()

@users_router.post("/ai-prompt")
async def ask(body: AskRequest):
    uc = AssistantService(
        exam_repo=SqlAlchemyExamRepo(),
        office_repo=SqlAlchemyOfficeRepo(),
        courses_repo=SqlAlchemyCoursesRepo()
    )
    return uc.handle_question(body.question, body.user_id)
