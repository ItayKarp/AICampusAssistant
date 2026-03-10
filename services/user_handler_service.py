from fastapi import HTTPException


class UserHandlerService:
    def __init__(self, load_personnel_repository = None, new_account_setup_repository = None):
        self.load_personnel_repository = load_personnel_repository
        self.new_account_setup_repository = new_account_setup_repository

    def handle_load_personnel(self, email):
        try:
            return self.load_personnel_repository.get_user_data(email)
        except ValueError:
            return HTTPException(status_code=404, detail="User not found.")

    def setup_new_user(self,email, body):
        return self.new_account_setup_repository.setup(email, body)