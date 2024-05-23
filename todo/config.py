from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    client_id: str
    secret: SecretStr
    auth: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
