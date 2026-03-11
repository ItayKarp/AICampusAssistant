from fastapi import HTTPException


class UserHandlerService:
    def __init__(self, load_personnel_repository = None, new_account_setup_repository = None, new_user_repository = None, temporary_user_id_repository = None):
        self.load_personnel_repository = load_personnel_repository
        self.new_account_setup_repository = new_account_setup_repository
        self.new_user_repository = new_user_repository
        self.temporary_user_id_repository = temporary_user_id_repository

    def handle_load_personnel(self, user_id):
        try:
            return self.load_personnel_repository.get_user_data(user_id)
        except ValueError:
            return HTTPException(status_code=404, detail="User not found.")

    def setup_new_user(self,user_id, body):
        return self.new_account_setup_repository.setup(user_id, body)

    def set_temporary_user_id(self,token):
        return self.temporary_user_id_repository.add_temporary_user_id(token.get("sub"), token.get("email"))
