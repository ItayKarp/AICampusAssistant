from fastapi import HTTPException


class LoadPersonnelHandlerService:
    def __init__(self, load_personnel_repository = None):
        self.load_personnel_repository = load_personnel_repository

    def handle_load_personnel(self, email):
        try:
            return self.load_personnel_repository.get_user_data(email)
        except ValueError:
            return HTTPException(status_code=404, detail="User not found.")
