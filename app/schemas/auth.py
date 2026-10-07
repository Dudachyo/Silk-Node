from pydantic import BaseModel


class LoginAuthSchema(BaseModel):
    email: str
    password: str

class RegistrationAuthSchema(BaseModel):
    email: str
    password: str


