

class FaqItemsHandleService:
    def __init__(self, faq_items_repository):
        self.faq_items_repository = faq_items_repository

    def handle_get_faq_items(self):
        return self.faq_items_repository.get_faq_items()

    def handle_create_faq_item(self, payload, user_email: str):
        return self.faq_items_repository.create_faq_item(payload, user_email)

    def handle_update_faq_item(self, faq_item_id, payload, user_email: str):
        return self.faq_items_repository.update_faq_item(faq_item_id, payload, user_email)

    def handle_delete_faq_item(self, faq_item_id, user_email: str):
        return self.faq_items_repository.delete_faq_item(faq_item_id, user_email)
