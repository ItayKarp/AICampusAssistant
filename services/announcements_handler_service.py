class AnnouncementsHandlerService:
    def __init__(self, announcements_repository = None, notification_repository = None):
        self.announcements_repository = announcements_repository
        self.notification_repository = notification_repository

    def handle_create_announcements(self, payload, user_id):
        create_announcement =  self.announcements_repository.create(payload, user_id)
        self.notification_repository.create_notification(payload)
        return create_announcement


    def handle_get_announcements(self, user_id):
        return self.announcements_repository.get_announcements(user_id)

    def handle_management_announcements(self, user_id):
        return self.announcements_repository.get_management_announcements(user_id)

    def handle_update_announcements(self,announcement_id, payload,details, user_id):
        update_announcement = self.announcements_repository.update(announcement_id, payload,details, user_id)
        self.notification_repository.update_notification(payload,announcement_id)
        return update_announcement


    def handle_delete_announcements(self,announcement_id,details, user_id):
        return self.announcements_repository.delete(announcement_id,details, user_id)