from ..infrastructure.repositories.authentication_repositories import validate_neon_token
from ..infrastructure.repositories.authentication_repositories.temporary_user_id_repository import TemporaryUserIdRepository


class AuthenticationHandlerService:
    def __init__(self, login_repository = None, register_repository = None, reset_password_repository = None, request_reset_password_repository = None, new_account_setup_repository = None, temporary_user_id_repository = TemporaryUserIdRepository(), new_user_repository = None):
        self.login_repository = login_repository
        self.register_repository = register_repository
        self.reset_password_repository = reset_password_repository
        self.request_reset_password_repository = request_reset_password_repository
        self.new_account_setup_repository = new_account_setup_repository
        self.temporary_user_id_repository = temporary_user_id_repository
        self.new_user_repository = new_user_repository

    def handle_login(self,body, request):
        token = self.login_repository.login_user(body, request)
        self.temporary_user_id_repository.add_temporary_user_id(token.get("sub"), token.get("email"))
        return token

    def handle_register(self,body, request):
        token = self.register_repository.register(body, request)
        self.new_user_repository.create(body.get("email"), body.get("password"), body.get("name"))
        self.temporary_user_id_repository.add_temporary_user_id(token.get("sub"), token.get("email"))
        return token

    def handle_reset_password(self, token, body):
        return self.reset_password_repository.reset_password(token, body.get("password"))

    def handle_request_reset_password(self, user_email):
        return self.request_reset_password_repository.request_reset_password(user_email)

    @staticmethod
    def handle_verify_jwt(token):
        return validate_neon_token(token)

