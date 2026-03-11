from fastapi import APIRouter, Header

from infrastructure.repositories.faq_items_repositories import FaqItemsRepository
from api.dependencies import get_user_id_and_email
from services.faq_items_handler_service import FaqItemsHandleService
from schemas.endpoint_validation.faq_items_validation import FaqItem

faq_router = APIRouter(tags=["faq-items"])


@faq_router.get("/faq-items")
async def get_faq_items(authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = FaqItemsHandleService(FaqItemsRepository())
    use_case.handle_get_faq_items()

@faq_router.post("/faq-item")
async def create_faq_item(body: FaqItem,authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = FaqItemsHandleService(FaqItemsRepository())
    use_case.handle_create_faq_item(body, email)

@faq_router.delete("/{faq_item_id}")
async def delete_faq_item(faq_item_id: int,authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = FaqItemsHandleService(FaqItemsRepository())
    use_case.handle_delete_faq_item(faq_item_id, email)

@faq_router.put("/{faq_item_id}")
async def update_faq_item(faq_item_id: int,payload: FaqItem,authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = FaqItemsHandleService(FaqItemsRepository())
    use_case.handle_update_faq_item(faq_item_id, payload, email)