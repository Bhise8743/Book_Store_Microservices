from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginSchema(BaseModel):
    user_name: str = Field("")
    password: str


class UserSchema(LoginSchema):
    first_name: str = Field("")
    last_name: str = Field("")
    email: EmailStr
    phone: int
    city: str
    state: str
    super_key: Optional[str] = None
    is_verified : Optional[bool] = Field(default=False)