from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'


settings = Settings()
