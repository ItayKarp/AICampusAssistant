from contextlib import contextmanager
from datetime import datetime

from infrastructure.db.database import Session
from infrastructure.db.models import FaqItem, User

class FaqItemsRepository:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    @contextmanager
    def context_manager(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_faq_items(self):
        with self.context_manager() as session:
            faq_items = session.query(FaqItem).all()
            return [
                {
                    "id": item.id,
                    "title": item.title,
                    "question": item.question,
                    "answer": item.answer,
                    "category": item.category,
                    "is_active": item.is_active,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                }
                for item in faq_items
            ]

    def create_faq_item(self, faq_item, email):
        with self.context_manager() as session:
            user = session.query(User).filter(User.email == email).first()
            if user.role != "admin":
                raise ValueError("Unauthorized access")
            faq_item = FaqItem(**faq_item)
            session.add(faq_item)


    def update_faq_item(self, updated_faq_item, faq_item_id, email):
        with self.context_manager() as session:
            user = session.query(User).filter(User.email == email).first()
            if user.role != "admin":
                raise ValueError("Unauthorized access")
            faq_item = session.get(FaqItem, faq_item_id)
            if not faq_item:
                raise ValueError(f"FaqItem with id {faq_item_id} not found")
            faq_item.title = updated_faq_item.title
            faq_item.question = updated_faq_item.question
            faq_item.answer = updated_faq_item.answer
            faq_item.category = updated_faq_item.category
            faq_item.updated_at = datetime.now


    def delete_faq_item(self, faq_item_id, email):
        with self.context_manager() as session:
            user = session.query(User).filter(User.email == email).first()
            if user.role != "admin":
                raise ValueError("Unauthorized access")
            faq_item = session.get(FaqItem, faq_item_id)
            if not faq_item:
                raise ValueError(f"FaqItem with id {faq_item_id} not found")
            session.delete(faq_item)
