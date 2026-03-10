from dataclasses import dataclass


@dataclass
class Register:
    name:str
    email:str
    password:str

    def __post_init__(self):
        self.name = self.name.strip()
        self.email = self.email.strip()
        self.password = self.password.strip()
        if not self.name:
            raise ValueError("Name cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not self.email.endswith("@gmail.com"):
            raise ValueError("Email must be a gmail account")