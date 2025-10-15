from pydantic_settings import BaseSettings  # ✅ 새 방식


class Settings(BaseSettings):
    EMAIL_PROVIDER: str = "gmail"
    EMAIL_USER: str
    EMAIL_PASS: str
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587

    class Config:
        env_file = ".env"

settings = Settings()
