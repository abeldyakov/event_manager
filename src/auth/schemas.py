from pydantic import BaseModel, UUID4, Field, EmailStr, field_validator
import uuid
import re


class BaseUser(BaseModel):
    email: EmailStr
    username: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not bool(re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', value)):
            raise ValueError("Email is invalid")
        return value


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    uuid: UUID4 = Field(default_factory=uuid.uuid4)

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
