from dataclasses import dataclass


@dataclass
class Login:
    email:str
    password:str

    def __post_init__(self):
        self.email = self.email.strip()
        self.password = self.password.strip()
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")
        if "@" not in self.email:
            raise ValueError("Email must have a valid format")