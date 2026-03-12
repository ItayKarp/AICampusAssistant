class NotificationHandlerService:
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def get_notifications(self, user_id):
        return self.notification_repository.get_notifications(user_id)