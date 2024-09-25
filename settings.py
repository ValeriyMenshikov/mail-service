from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAIL_FROM: str = "no-reply@pomodoro.com"
    SMTP_HOST: str = "0.0.0.0"
    SMTP_PORT: int = 1025
    SMTP_PASSWORD: str = ""
    RABBIT_URL: str = 'amqp://guest:guest@localhost:5672//'
