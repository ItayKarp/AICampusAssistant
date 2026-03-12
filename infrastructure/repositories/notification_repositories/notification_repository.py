from datetime import datetime
from pathlib import Path
import os

from openai import OpenAI
from dotenv import load_dotenv

from infrastructure.db.models import User,Notification
from infrastructure.repositories.notification_repositories.base_notification_repository import BaseNotificationRepository

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = OpenAI(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTIONS_PATH = Path(__file__).resolve().parent / "ai_notification_system_instructions.txt"
SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")


class CreateNotificationRepository(BaseNotificationRepository):
    def create_notification(self, payload):
        with self.context_manager() as session:
            details = self.get_notification_details(payload)
            targeted_users = session.query(User).filter(
                User.role == details['target_role']
            ).all()
            for user in targeted_users:
                notification = Notification(user_id=user.id, title=details['title'], message=details['content'], is_read=False, created_at= datetime.now())
                session.add(notification)
                session.flush()


    def update_notification(self, payload, announcement_id):
        with self.context_manager() as session:
            details = self.get_notification_details(payload)
            notification = session.query(Notification).filter(
                Notification.id == announcement_id
            ).first()
            if not notification:
                raise ValueError(f"Notification with id {announcement_id} not found")
            notification.title = details['title']
            notification.message = details['content']
            notification.created_at = datetime.now()

    def get_notifications(self, user_id):
        with self.context_manager() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User with id {user_id} not found")
            notifications = session.query(Notification).filter(
                Notification.user_id == user_id
            ).all()
            return [
                {
                    "title": notification.title,
                    "content": notification.message,
                    "user_id": notification.user_id,
                }
                for notification in notifications
            ]

