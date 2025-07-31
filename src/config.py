from pydantic_settings import BaseSettings, SettingsConfigDict
#postgresql+asyncpg://postgres:postgres@db:5432/postgres

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_ADMIN_ID: str

    model_config = SettingsConfigDict(
        env_file='.docker-env'
    )

    def get_db_url(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

    def get_db_url_migrations(self):
        return (f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

settings = Settings()
