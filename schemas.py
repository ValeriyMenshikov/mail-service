from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    subject: str
    message: str
    user_email: str
