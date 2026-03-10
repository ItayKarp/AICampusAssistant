from dataclasses import dataclass


@dataclass
class ResetPassword:
    token:str
    newPassword:str

    def __post_init__(self):
        self.newPassword = self.newPassword.strip()
        if not self.newPassword:
            raise ValueError("New password cannot be empty")
        if len(self.newPassword) < 8:
            raise ValueError("New password must be at least 8 characters long")